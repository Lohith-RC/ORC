/**
 * Service Worker Registration utility
 */

export const registerServiceWorker = () => {
    if ('serviceWorker' in navigator && window.location.protocol === 'https:' || window.location.hostname === 'localhost') {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/sw.js')
                .then((registration) => {
                    console.log('PWA Service Worker registered with scope:', registration.scope);
                })
                .catch((error) => {
                    console.warn('PWA Service Worker registration note:', error);
                });
        });
    }
};

export const unregisterServiceWorker = () => {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.ready
            .then((registration) => {
                registration.unregister();
            })
            .catch((error) => {
                console.error(error.message);
            });
    }
};
