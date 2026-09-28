// 📱 Einkaufsliste – Offline-Speicher für die App-Seite (nur das Programm, keine Daten)
const CACHE = "einkaufsliste-app-__EL_VERSION__";
const FILES = ["./", "manifest.json", "icon-192.png", "icon-512.png"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k.startsWith("einkaufsliste-app-") && k !== CACHE).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});

// Erst das Netz fragen (dann ist die App immer aktuell), ohne Netz die gespeicherte Seite nehmen
self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || !url.pathname.startsWith("/einkaufsliste/app/") || url.pathname.endsWith("sw.js")) return;
  e.respondWith(
    fetch(e.request).then((resp) => {
      if (resp.ok) { const copy = resp.clone(); caches.open(CACHE).then((c) => c.put(url.pathname === "/einkaufsliste/app/index.html" ? "./" : e.request, copy)); }
      return resp;
    }).catch(() => caches.match(e.request, { ignoreSearch: true }).then((r) => r || caches.match("./")))
  );
});
