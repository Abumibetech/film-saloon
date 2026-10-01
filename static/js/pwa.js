(()=> {
  "use strict";

  let deferredPrompt = null;

  const installButtons = [
    document.getElementById("installBtn"),
    document.getElementById("mobileInstallBtn")
  ].filter(Boolean);

  const installedKey = "film_saloon_app_installed";

  const isStandalone = () => {
    return (
      window.matchMedia("(display-mode: standalone)").matches ||
      window.matchMedia("(display-mode: fullscreen)").matches ||
      window.navigator.standalone === true
    );
  };

  const wasInstalled = () => {
    return localStorage.getItem(installedKey) === "true";
  };

  const hideInstallButtons = () => {
    installButtons.forEach((button) => {
      button.hidden = true;
      button.style.display = "none";
    });
  };

  const showInstallButtons = () => {
    if (isStandalone() || wasInstalled()) {
      hideInstallButtons();
      return;
    }

    if (deferredPrompt) {
      installButtons.forEach((button) => {
        button.hidden = false;
        button.style.display = "";
      });
    }
  };

  const markInstalled = () => {
    localStorage.setItem(installedKey, "true");
    deferredPrompt = null;
    hideInstallButtons();
  };

  async function installApp() {

    if (isStandalone() || wasInstalled()) {
      hideInstallButtons();
      return;
    }

    if (deferredPrompt) {
      deferredPrompt.prompt();

      try {
        const choice = await deferredPrompt.userChoice;

        if (choice && choice.outcome === "accepted") {
          markInstalled();
        }
      } catch (error) {
        console.warn("Install prompt error:", error);
      }

      deferredPrompt = null;
      return;
    }

    const isIOS =
      /iphone|ipad|ipod/i.test(navigator.userAgent) &&
      !window.MSStream;

    if (isIOS) {
      alert(
        'To install FILM SALOON on iPhone or iPad, tap Share in Safari and choose "Add to Home Screen".'
      );
    } else {
      alert(
        'Your browser has not supplied the automatic install prompt yet. Open the browser menu and choose "Install app" or "Add to Home screen".'
      );
    }
  }

  installButtons.forEach((button) => {
    button.addEventListener("click", installApp);
  });

  window.addEventListener("beforeinstallprompt", (event) => {
    event.preventDefault();
    deferredPrompt = event;
    showInstallButtons();
  });

  window.addEventListener("appinstalled", () => {
    markInstalled();
  });

  // If the app is already installed or opened as a PWA,
  // never show the installation controls.
  if (isStandalone() || wasInstalled()) {
    hideInstallButtons();
  } else {
    hideInstallButtons();
  }

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker
        .register("/service-worker.js", { scope: "/" })
        .then((registration) => {
          console.log("PWA ready", registration.scope);
        })
        .catch((error) => {
          console.error("Service worker registration failed:", error);
        });
    });
  }
})();
