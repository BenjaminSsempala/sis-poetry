/* Keeps the SIS Poetry lessons working when the internet drops.
   add_lesson.py changes VERSION whenever a lesson is added, so every computer picks up the new list. */
const VERSION = "2026-10-29-111608";
const CACHE = "sis-poetry-" + VERSION;
const CORE = ["./", "index.html", "lessons.json", "manifest.webmanifest",
  "assets/logo.png", "assets/icon-192.png", "assets/icon-512.png", "assets/jakarta.woff2"];

self.addEventListener("install", (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    await cache.addAll(CORE);
    try {
      const list = await (await fetch("lessons.json", { cache: "no-store" })).json();
      await cache.addAll(list.flatMap((lesson) => (lesson.guide ? [lesson.path, lesson.guide] : [lesson.path])));
    } catch (err) { /* lessons are cached the first time they are opened instead */ }
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    for (const key of await caches.keys()) if (key !== CACHE) await caches.delete(key);
    await self.clients.claim();
  })());
});

/* Lessons are big, so they come from the saved copy first and refresh in the background.
   The home page and the lesson list try the internet first, so new lessons show up. */
self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET" || new URL(req.url).origin !== location.origin) return;
  const isLesson = new URL(req.url).pathname.includes("/lessons/");
  event.respondWith((async () => {
    const cache = await caches.open(CACHE);
    const saved = await cache.match(req, { ignoreSearch: true });
    const fresh = fetch(req).then((res) => {
      if (res.ok) cache.put(req.url.split("?")[0], res.clone());
      return res;
    });
    if (isLesson && saved) { event.waitUntil(fresh.catch(() => {})); return saved; }
    try { return await fresh; }
    catch (err) {
      if (saved) return saved;
      if (req.mode === "navigate") return (await cache.match("index.html")) || Response.error();
      return Response.error();
    }
  })());
});
