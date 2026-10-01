(function () {
    "use strict";

    const desktopButton =
        document.getElementById(
            "notificationBtn"
        );

    const mobileButton =
        document.getElementById(
            "mobileNotificationBtn"
        );

    const csrfInput =
        document.querySelector(
            "#notificationCsrfForm input[name='csrfmiddlewaretoken']"
        );


    if (
        !desktopButton &&
        !mobileButton
    ) {
        return;
    }


    function buttons() {
        return [
            desktopButton,
            mobileButton
        ].filter(Boolean);
    }


    function setButtonsVisible(
        visible
    ) {
        buttons().forEach(button => {
            button.hidden = !visible;
        });
    }


    function setButtonText(
        text
    ) {
        buttons().forEach(button => {
            button.textContent = text;
        });
    }


    function getCsrfToken() {
        if (csrfInput) {
            return csrfInput.value;
        }

        const match =
            document.cookie.match(
                /(?:^|;\s*)csrftoken=([^;]+)/
            );

        return match
            ? decodeURIComponent(match[1])
            : "";
    }


    function urlBase64ToUint8Array(
        base64String
    ) {
        const padding =
            "=".repeat(
                (4 -
                    (base64String.length % 4)) %
                    4
            );

        const base64 =
            base64String
                .replace(/-/g, "+")
                .replace(/_/g, "/") +
            padding;

        const rawData =
            window.atob(base64);

        return Uint8Array.from(
            [...rawData].map(
                character =>
                    character.charCodeAt(0)
            )
        );
    }


    async function getRegistration() {
        if (
            !("serviceWorker" in navigator)
        ) {
            throw new Error(
                "Service workers are not supported."
            );
        }

        return navigator.serviceWorker.ready;
    }


    async function getPublicKey() {
        const response =
            await fetch(
                "/notifications/public-key/",
                {
                    method: "GET",
                    cache: "no-store",
                    credentials: "same-origin"
                }
            );

        if (!response.ok) {
            throw new Error(
                "Could not load notification configuration."
            );
        }

        const data =
            await response.json();

        if (!data.publicKey) {
            throw new Error(
                "FILM SALOON notifications are not configured yet."
            );
        }

        return data.publicKey;
    }


    async function saveSubscription(
        subscription
    ) {
        const response =
            await fetch(
                "/notifications/subscribe/",
                {
                    method: "POST",
                    credentials: "same-origin",
                    headers: {
                        "Content-Type":
                            "application/json",
                        "X-CSRFToken":
                            getCsrfToken()
                    },
                    body: JSON.stringify({
                        subscription:
                            subscription.toJSON()
                    })
                }
            );

        if (!response.ok) {
            throw new Error(
                "Could not save notification subscription."
            );
        }

        return response.json();
    }


    async function subscribe() {
        if (
            !("Notification" in window) ||
            !("PushManager" in window)
        ) {
            setButtonsVisible(false);
            return;
        }

        const permission =
            await Notification.requestPermission();

        if (permission !== "granted") {
            setButtonsVisible(false);
            return;
        }

        const registration =
            await getRegistration();

        const publicKey =
            await getPublicKey();

        let subscription =
            await registration.pushManager
                .getSubscription();

        if (!subscription) {
            subscription =
                await registration.pushManager
                    .subscribe({
                        userVisibleOnly: true,
                        applicationServerKey:
                            urlBase64ToUint8Array(
                                publicKey
                            )
                    });
        }

        await saveSubscription(
            subscription
        );

        localStorage.setItem(
            "film_saloon_notifications_enabled",
            "1"
        );

        setButtonsVisible(false);

        console.log(
            "FILM SALOON notifications enabled."
        );
    }


    async function initialise() {
        if (
            !("Notification" in window) ||
            !("PushManager" in window) ||
            !("serviceWorker" in navigator)
        ) {
            setButtonsVisible(false);
            return;
        }

        if (
            Notification.permission ===
            "denied"
        ) {
            setButtonsVisible(false);
            return;
        }

        try {
            const registration =
                await getRegistration();

            const subscription =
                await registration.pushManager
                    .getSubscription();

            if (subscription) {
                await saveSubscription(
                    subscription
                );

                localStorage.setItem(
                    "film_saloon_notifications_enabled",
                    "1"
                );

                setButtonsVisible(false);
            } else {
                setButtonsVisible(true);
            }
        } catch (error) {
            console.error(
                "FILM SALOON notification setup error:",
                error
            );

            setButtonsVisible(true);
        }
    }


    buttons().forEach(button => {
        button.addEventListener(
            "click",
            async () => {
                try {
                    button.disabled = true;

                    setButtonText(
                        "Enabling..."
                    );

                    await subscribe();
                } catch (error) {
                    console.error(
                        "FILM SALOON notification error:",
                        error
                    );

                    setButtonText(
                        "Enable Notifications"
                    );

                    setButtonsVisible(
                        true
                    );
                } finally {
                    button.disabled =
                        false;
                }
            }
        );
    });


    if (
        document.readyState ===
        "loading"
    ) {
        document.addEventListener(
            "DOMContentLoaded",
            initialise,
            { once: true }
        );
    } else {
        initialise();
    }
})();
