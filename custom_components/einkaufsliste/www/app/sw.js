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
