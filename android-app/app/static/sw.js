// Service Worker для PWA
const CACHE_NAME = 'daily-rise-v1';
const ASSETS = [
  '/',
  '/static/index.html',
  '/static/manifest.json'
];

// Установка service worker
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

// Активация и очистка старого кэша
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))
      );
    })
  );
});

// Перехват запросов
self.addEventListener('fetch', (e) => {
  // API запросы всегда идут в сеть
  if (e.request.url.includes('/api/')) {
    e.respondWith(fetch(e.request));
    return;
  }
  
  // Статика из кэша, с обновлением в фоне
  e.respondWith(
    caches.match(e.request).then((res) => {
      return res || fetch(e.request);
    })
  );
});
