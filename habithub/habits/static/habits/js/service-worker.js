var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
    '/offline',
    '/static/habits/css/styles.css',
    '/static/habits/documents/lst_habits.csv',
    '/static/habits/fonts/Cormorant_Garamond/CormorantGaramond-LightItalic.ttf',
    '/static/habits/fonts/Cormorant_Garamond/CormorantGaramond-LightItalic.woff',
    '/static/habits/fonts/Cormorant_Garamond/CormorantGaramond-LightItalic.woff2',
    '/static/habits/fonts/Cormorant_Garamond/CormorantGaramond-Regular.ttf',
    '/static/habits/fonts/Cormorant_Garamond/CormorantGaramond-Regular.woff',
    '/static/habits/fonts/Cormorant_Garamond/CormorantGaramond-Regular.woff2',
    '/static/habits/images/archive-icon.png',
    '/static/habits/images/delete-key.png',
    '/static/habits/images/favicon.ico',
    '/static/habits/images/icons-check-mark.png',
    '/static/habits/images/logo_192px.png',
    '/static/habits/images/logo_512px.png',
    '/static/habits/images/logo_160px.png',
    '/static/habits/images/splash-640x1136.png',
    '/static/habits/images/logo.png',
    '/static/habits/js/index.js',
    '/static/habits/js/scripts.js'
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
            .catch(() => {
                return caches.match('offline');
            })
    )
});