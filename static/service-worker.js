const CACHE = "film-saloon-v2";

const SHELL = [
    "/",
    "/genres/",
    "/clips/",
    "/actors/",
    "/static/css/site.css",
    "/static/js/app.js",
    "/static/js/pwa.js",
    "/static/js/notifications.js"
];


self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE)
            .then(cache => cache.addAll(SHELL))
            .then(() => self.skipWaiting())
    );
});


self.addEventListener("activate", event => {
    event.waitUntil(
        caches.keys()
            .then(keys =>
                Promise.all(
                    keys
                        .filter(key => key !== CACHE)
                        .map(key => caches.delete(key))
                )
            )
            .then(() => self.clients.claim())
    );
});


self.addEventListener("fetch", event => {
    if (event.request.method !== "GET") {
        return;
    }

    const url = new URL(event.request.url);

    if (
        url.pathname.startsWith("/admin/") ||
        url.pathname.startsWith("/notifications/")
    ) {
        return;
    }

    event.respondWith(
        fetch(event.request)
            .then(response => {
                const copy = response.clone();

                caches.open(CACHE).then(cache => {
                    cache.put(event.request, copy);
                });

                return response;
            })
            .catch(() =>
                caches.match(event.request)
                    .then(response =>
                        response || caches.match("/")
                    )
            )
    );
});


/* ============================================================
   FILM SALOON PUSH NOTIFICATION
   ============================================================ */

self.addEventListener("push", event => {
    let data = {};

    try {
        if (event.data) {
            data = event.data.json();
        }
    } catch (error) {
        console.error(
            "FILM SALOON push data error:",
            error
        );

        data = {
            title: "FILM SALOON",
            body: "A new movie is available.",
            url: "/"
        };
    }

    const title =
        data.title || "FILM SALOON";

    const options = {
        body:
            data.body ||
            "A new movie has been added.",

        icon:
            data.icon ||
            "/static/icons/icon-192.png",

        badge:
            data.badge ||
            "/static/icons/icon-192.png",

        tag:
            data.tag ||
            "film-saloon-notification",

        renotify: true,

        requireInteraction: false,

        data: {
            url: data.url || "/"
        }
    };

    event.waitUntil(
        self.registration.showNotification(
            title,
            options
        )
    );
});


/* ============================================================
   NOTIFICATION CLICK
   ============================================================ */

self.addEventListener(
    "notificationclick",
    event => {
        event.notification.close();

        let targetUrl = "/";

        if (
            event.notification.data &&
            event.notification.data.url
        ) {
            targetUrl =
                event.notification.data.url;
        }

        let target;

        try {
            target = new URL(
                targetUrl,
                self.location.origin
            );

            if (
                target.origin !==
                self.location.origin
            ) {
                target = new URL(
                    "/",
                    self.location.origin
                );
            }
        } catch (error) {
            target = new URL(
                "/",
                self.location.origin
            );
        }

        event.waitUntil(
            clients.matchAll({
                type: "window",
                includeUncontrolled: true
            }).then(windowClients => {

                for (const client of windowClients) {
                    try {
                        const clientUrl =
                            new URL(client.url);

                        if (
                            clientUrl.origin ===
                                self.location.origin &&
                            "focus" in client
                        ) {
                            if ("navigate" in client) {
                                client.navigate(
                                    target.href
                                );
                            }

                            return client.focus();
                        }
                    } catch (error) {
                        console.error(
                            "FILM SALOON notification navigation error:",
                            error
                        );
                    }
                }

                if (clients.openWindow) {
                    return clients.openWindow(
                        target.href
                    );
                }

                return null;
            })
        );
    }
);
