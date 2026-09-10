(() => {
  const STORAGE_KEY = "rk-sidebar-collapsed";

  const year = String(new Date().getFullYear());
  document.querySelectorAll("[data-copyright-year]").forEach((el) => {
    el.textContent = year;
  });

  const menuButton = document.getElementById("mobile-menu-button");
  const closeButton = document.getElementById("mobile-menu-close-button");
  const menu = document.getElementById("mobile-menu");
  const overlay = document.getElementById("mobile-menu-overlay");
  const mobileNavLinks = document.querySelectorAll("#mobile-nav-links a");
  const focusableSelector = "a[href], button:not([disabled])";
  let lastFocused = null;

  const setMobileOpen = (open) => {
    if (!menuButton || !menu || !overlay) return;
    menuButton.setAttribute("aria-expanded", open ? "true" : "false");
    menuButton.setAttribute("aria-label", open ? "Close navigation menu" : "Open navigation menu");
    menu.classList.toggle("is-open", open);
    overlay.classList.toggle("is-open", open);
    overlay.setAttribute("aria-hidden", open ? "false" : "true");
    document.body.style.overflow = open ? "hidden" : "";
  };

  const trapFocus = (e) => {
    if (!menu || !menu.classList.contains("is-open") || e.key !== "Tab") return;
    const focusables = [...menu.querySelectorAll(focusableSelector)];
    if (!focusables.length) return;
    const first = focusables[0];
    const last = focusables[focusables.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  };

  const openMenu = () => {
    lastFocused = document.activeElement;
    setMobileOpen(true);
    closeButton?.focus();
    document.addEventListener("keydown", onKeydown);
  };

  const closeMenu = () => {
    setMobileOpen(false);
    document.removeEventListener("keydown", onKeydown);
    if (lastFocused && typeof lastFocused.focus === "function") lastFocused.focus();
  };

  const onKeydown = (e) => {
    if (e.key === "Escape") closeMenu();
    trapFocus(e);
  };

  if (menuButton && menu && overlay) {
    menuButton.addEventListener("click", () => {
      const isOpen = menuButton.getAttribute("aria-expanded") === "true";
      if (isOpen) closeMenu();
      else openMenu();
    });
    closeButton?.addEventListener("click", closeMenu);
    overlay.addEventListener("click", closeMenu);
    mobileNavLinks.forEach((link) => link.addEventListener("click", closeMenu));
  }

  const toggleBtns = document.querySelectorAll("[data-sidebar-toggle]");

  const setCollapsed = (collapsed, { persist = true } = {}) => {
    document.documentElement.setAttribute("data-sidebar", collapsed ? "collapsed" : "expanded");
    toggleBtns.forEach((btn) => {
      btn.setAttribute("aria-pressed", collapsed ? "true" : "false");
      btn.setAttribute("aria-label", collapsed ? "Exit full width" : "Full width reading");
    });
    if (persist) {
      try {
        localStorage.setItem(STORAGE_KEY, collapsed ? "1" : "0");
      } catch (_) {
        /* ignore */
      }
    }
  };

  let initial = false;
  try {
    initial = localStorage.getItem(STORAGE_KEY) === "1";
  } catch (_) {
    initial = false;
  }
  setCollapsed(initial, { persist: false });

  toggleBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const next = document.documentElement.getAttribute("data-sidebar") !== "collapsed";
      setCollapsed(next);
    });
  });

  const BLOG_POSTS = [
    "/blog/security-basics-startups-before-fundraising",
    "/blog/engineering-principles-what-not-to-build",
    "/blog/hiring-engineers-as-first-time-cto",
    "/blog/how-ai-coding-tools-changed-engineering-velocity",
    "/blog/hidden-cost-premature-microservices-monolith",
    "/blog/build-vs-buy-framework-what-to-build-in-house",
    "/blog/laravel-octane-swoole-concurrent-load",
    "/blog/what-typephp-means-for-php-performance",
    "/blog/business-logic-first-not-perfect-tech-stack",
    "/blog/why-we-chose-laravel-over-nodejs",
    "/blog/how-to-run-startup-tech-stack-free-until-funded",
    "/blog/ship-fast-without-losing-client-trust",
    "/blog/building-a-software-team-in-kathmandu",
    "/blog/what-a-first-time-cto-actually-does",
    "/blog/why-i-left-teaching-to-build-a-company"
  ];

  const deckRoot = document.querySelector("[data-deck]");
  if (deckRoot) {
    const mode = deckRoot.getAttribute("data-deck");
    const prevBtn = deckRoot.querySelector("[data-deck-prev]");
    const nextBtn = deckRoot.querySelector("[data-deck-next]");
    const labelEl = deckRoot.querySelector("[data-deck-label]");
    const indexEl = deckRoot.querySelector("[data-deck-index]");
    const totalEl = deckRoot.querySelector("[data-deck-total]");

    if (mode === "blog-index") {
      if (labelEl) labelEl.textContent = "Blog";
      if (indexEl) indexEl.textContent = "1";
      if (totalEl) totalEl.textContent = String(1 + BLOG_POSTS.length);
      if (prevBtn) {
        prevBtn.addEventListener("click", () => {
          location.href = "/#contact";
        });
      }
      if (nextBtn) {
        nextBtn.disabled = !BLOG_POSTS.length;
        nextBtn.addEventListener("click", () => {
          if (BLOG_POSTS[0]) location.href = BLOG_POSTS[0];
        });
      }
    }

    if (mode === "blog-post") {
      const file = location.pathname.split("/").pop() || "";
      const i = Math.max(0, BLOG_POSTS.findIndex((href) => href.endsWith("/" + file) || href.endsWith(file)));
      if (labelEl) labelEl.textContent = "Article";
      if (indexEl) indexEl.textContent = String(i + 1);
      if (totalEl) totalEl.textContent = String(BLOG_POSTS.length);
      if (prevBtn) {
        prevBtn.setAttribute("aria-label", i <= 0 ? "Back to blog listing" : "Previous article");
        prevBtn.addEventListener("click", () => {
          location.href = i <= 0 ? "/blog" : BLOG_POSTS[i - 1];
        });
      }
      if (nextBtn) {
        nextBtn.disabled = i >= BLOG_POSTS.length - 1;
        nextBtn.setAttribute("aria-label", "Next article");
        nextBtn.addEventListener("click", () => {
          if (i < BLOG_POSTS.length - 1) location.href = BLOG_POSTS[i + 1];
        });
      }
      document.addEventListener("keydown", (e) => {
        if (e.target && /INPUT|TEXTAREA|SELECT/.test(e.target.tagName)) return;
        if (menu?.classList.contains("is-open")) return;
        if (e.key === "ArrowRight" || e.key === "PageDown") {
          e.preventDefault();
          if (i < BLOG_POSTS.length - 1) location.href = BLOG_POSTS[i + 1];
        } else if (e.key === "ArrowLeft" || e.key === "PageUp") {
          e.preventDefault();
          location.href = i <= 0 ? "/blog" : BLOG_POSTS[i - 1];
        }
      });
    }
  }
})();
