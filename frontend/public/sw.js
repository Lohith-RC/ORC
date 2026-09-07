/**
 * ORC AI CLINICAL SERVICE WORKER
 * Offline caching and Progressive Web App shell support
 */

const CACHE_NAME = 'orc-clinical-cache-v1';
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/manifest.json',
    '/static/js/main.chunk.js',
    '/static/js/bundle.js',
    '/static/css/main.chunk.css'
];

// Install Lifecycle: Cache static shell assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(STATIC_ASSETS).catch((err) => {
                console.warn("Service worker cache prefetch note:", err);
            });
        })
    );
    self.skipWaiting();
});

// Activate Lifecycle: Cleanup legacy cache versions
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
            );
        })
    );
    self.clients.claim();
});

// Fetch Lifecycle: Network-first for API, Cache-first for static assets
self.addEventListener('fetch', (event) => {
    const { request } = event;

    // Bypass caching for non-GET or cross-origin Cloudflare/Render endpoints
    if (request.method !== 'GET') {
        return;
    }

    event.respondWith(
        fetch(request)
            .then((response) => {
                // Clone response to cache if successful
                if (response && response.status === 200 && response.type === 'basic') {
                    const responseToCache = response.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(request, responseToCache);
                    });
                }
                return response;
            })
            .catch(() => {
                // Offline fallback from local cache
                return caches.match(request).then((cachedResponse) => {
                    if (cachedResponse) {
                        return cachedResponse;
                    }
                    // Offline fallback for navigation
                    if (request.mode === 'navigate') {
                        return caches.match('/index.html');
                    }
                    return new Response(JSON.stringify({ offline: true, message: "Offline clinical mode active." }), {
                        headers: { "Content-Type": "application/json" }
                    });
                });
            })
    );
});
