// 📱 Einkaufsliste – Offline-Speicher für die App (nur Programm + Symbole, die Daten merkt sich die Seite selbst)
const CACHE = "einkaufsliste-app-__EL_VERSION__";
const FILES = [
  "./", "manifest.json", "icon-192.png", "icon-512.png", "icons.json", "zxing.min.js?v=__EL_VERSION__",
  "/einkaufsliste_files/einkaufsliste-card.js?v=__EL_VERSION__",
  "/einkaufsliste_files/einkaufsliste-en.json?v=__EL_VERSION__",
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k.startsWith("einkaufsliste-app-") && k !== CACHE).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});

// Erst das Netz fragen (dann ist alles aktuell), ohne Netz das Gespeicherte nehmen
self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  const ours = url.pathname.startsWith("/einkaufsliste/app/") || url.pathname.startsWith("/einkaufsliste_files/");
  if (e.request.method !== "GET" || url.origin !== location.origin || !ours || url.pathname.endsWith("sw.js") || url.pathname.includes("/__ws/")) return;
  e.respondWith(
    fetch(e.request).then((resp) => {
      if (resp.ok) {
        const copy = resp.clone();
        caches.open(CACHE).then((c) => c.put(url.pathname === "/einkaufsliste/app/" || url.pathname === "/einkaufsliste/app/index.html" ? "./" : e.request, copy));
      }
      return resp;
    }).catch(() => caches.match(e.request).then((r) => r || caches.match(e.request, { ignoreSearch: true }))
      .then((r) => r || (url.pathname.startsWith("/einkaufsliste/app/") ? caches.match("./") : undefined))
      .then((r) => r || new Response("offline", { status: 503 })))
  );
});

// ---------------------------------------------------------------- 🔄 Im Hintergrund nachschicken (Android/Chrome)
// Ist die App zu und kommt das Netz zurück, weckt Chrome diesen Helfer kurz auf („sync“).
// Er schickt die gemerkten Änderungen an Home Assistant – genau so, wie es die Seite selbst tun würde.
// iPhones kennen das leider nicht; dort wird beim nächsten Öffnen nachgeschickt.
let dbp = null;
function db() {
  return dbp || (dbp = new Promise((ok, fail) => {
    const r = indexedDB.open("einkaufsliste-app", 1);
    r.onupgradeneeded = () => r.result.createObjectStore("kv");
    r.onsuccess = () => ok(r.result);
    r.onerror = () => { dbp = null; fail(r.error); };
  }));
}
async function kv(mode, fn) {
  const d = await db();
  return new Promise((ok, fail) => {
    const tx = d.transaction("kv", mode);
    let out;
    fn(tx.objectStore("kv"), (v) => { out = v; });
    tx.oncomplete = () => ok(out);
    tx.onerror = () => fail(tx.error);
  });
}
const kvGet = (k) => kv("readonly", (st, set) => { const r = st.get(k); r.onsuccess = () => set(r.result); });
const kvSet = (k, v) => kv("readwrite", (st) => { st.put(v, k); });
const lockTake = () => kv("readwrite", (st, set) => {
  const r = st.get("lock");
  r.onsuccess = () => {
    const l = r.result;
    if (l && l.owner !== "sw" && l.until > Date.now()) { set(false); return; }
    st.put({ owner: "sw", until: Date.now() + 60000 }, "lock");
    set(true);
  };
});
const lockFree = () => kv("readwrite", (st) => {
  const r = st.get("lock");
  r.onsuccess = () => { if (r.result?.owner === "sw") st.delete("lock"); };
});

async function accessToken(auth) {
  if (auth.access && auth.expires > Date.now()) return auth.access;
  const r = await fetch("/auth/token", {
    method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ grant_type: "refresh_token", refresh_token: auth.refresh, client_id: auth.client_id }),
  });
  if (!r.ok) throw new Error("token " + r.status);
  const j = await r.json();
  const next = { ...auth, access: j.access_token, expires: Date.now() + (j.expires_in || 1800) * 1000 - 60000 };
  await kvSet("auth", next);
  return next.access;
}

function openSocket(token) {
  return new Promise((ok, fail) => {
    const ws = new WebSocket(self.location.origin.replace(/^http/, "ws") + "/api/websocket");
    const pending = new Map();
    let id = 1;
    const timer = setTimeout(() => { try { ws.close(); } catch (_) { /* egal */ } fail(new Error("timeout")); }, 15000);
    ws.onmessage = (ev) => {
      const m = JSON.parse(ev.data);
      if (m.type === "auth_required") ws.send(JSON.stringify({ type: "auth", access_token: token }));
      else if (m.type === "auth_invalid") { clearTimeout(timer); fail(new Error("auth")); }
      else if (m.type === "auth_ok") {
        clearTimeout(timer);
        ok({
          call: (msg) => new Promise((res, rej) => { const n = id++; pending.set(n, { res, rej }); ws.send(JSON.stringify({ id: n, ...msg })); }),
          close: () => { try { ws.close(); } catch (_) { /* egal */ } },
        });
      } else if (m.type === "result") {
        const p = pending.get(m.id);
        if (p) { pending.delete(m.id); m.success ? p.res(m.result) : p.rej(Object.assign(new Error("ha"), { ha: m.error })); }
      }
    };
    ws.onclose = () => { clearTimeout(timer); for (const p of pending.values()) p.rej(Object.assign(new Error("lost"), { lost: true })); pending.clear(); fail(new Error("closed")); };
    ws.onerror = () => { try { ws.close(); } catch (_) { /* egal */ } };
  });
}

async function flushQueue(force) {
  if (!force) { // ist die App gerade offen und sichtbar? Dann macht sie das selbst
    const wins = await self.clients.matchAll({ type: "window", includeUncontrolled: true });
    if (wins.some((c) => c.visibilityState === "visible")) return;
  }
  let q = await kvGet("queue");
  if (!Array.isArray(q) || !q.length) return;
  const auth = await kvGet("auth");
  if (!auth?.refresh) return;
  if (!(await lockTake())) return; // die Seite schickt gerade selbst
  let sock = null, sent = 0;
  try {
    sock = await openSocket(await accessToken(auth));
    const ids = {};
    while (q.length) {
      const m = { ...q[0] };
      const tmp = m._tmp;
      delete m._tmp;
      for (const k of ["item_id", "recipe_id"]) if (m[k] && ids[m[k]]) m[k] = ids[m[k]];
      if (!String(m.item_id || m.recipe_id || "").startsWith("tmp_")) {
        try {
          const res = await sock.call(m);
          if (tmp && res?.id) ids[tmp] = res.id;
        } catch (err) {
          if (err.lost) throw err; // Netz wieder weg – der Rest bleibt gemerkt
          // echter Fehler (z. B. Artikel inzwischen gelöscht): diesen einen überspringen
        }
        sent += 1;
      }
      q = q.slice(1);
      await kvSet("queue", q);
    }
  } finally {
    sock?.close();
    if (sent) {
      const old = await kvGet("flushed").catch(() => null);
      await kvSet("flushed", { n: (old?.n || 0) + sent, at: Date.now() }).catch(() => {});
    }
    await lockFree().catch(() => {});
  }
}

self.addEventListener("sync", (e) => {
  if (e.tag === "el-queue") e.waitUntil(flushQueue(false));
});
// Zum Testen: die Seite kann den Helfer auch direkt bitten
self.addEventListener("message", (e) => {
  if (e.data?.type === "el-flush") e.waitUntil(flushQueue(!!e.data.force).catch(() => {}));
});
