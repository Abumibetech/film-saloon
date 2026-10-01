(()=> {
  const root = document.documentElement;

  const savedTheme = localStorage.getItem("film_saloon_theme");
  if (savedTheme) {
    root.dataset.theme = savedTheme;
  }

  const themeToggle = document.getElementById("themeToggle");

  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const nextTheme = root.dataset.theme === "light" ? "dark" : "light";
      root.dataset.theme = nextTheme;
      localStorage.setItem("film_saloon_theme", nextTheme);
    });
  }

  const menuButton = document.getElementById("menuButton");
  const mobileMenu = document.getElementById("mobileMenu");

  if (menuButton && mobileMenu) {

    const closeMenu = () => {
      mobileMenu.classList.remove("open");
      menuButton.setAttribute("aria-expanded", "false");
    };

    const openMenu = () => {
      mobileMenu.classList.add("open");
      menuButton.setAttribute("aria-expanded", "true");
    };

    menuButton.setAttribute("aria-expanded", "false");

    menuButton.addEventListener("click", (event) => {
      event.stopPropagation();

      if (mobileMenu.classList.contains("open")) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    // Close when clicking/tapping anywhere outside the menu.
    document.addEventListener("click", (event) => {
      if (
        mobileMenu.classList.contains("open") &&
        !mobileMenu.contains(event.target) &&
        !menuButton.contains(event.target)
      ) {
        closeMenu();
      }
    });

    // Close when a menu link is selected.
    mobileMenu.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", closeMenu);
    });

    // Close the menu with Escape.
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        closeMenu();
      }
    });
  }
})();
