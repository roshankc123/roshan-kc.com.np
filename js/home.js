document.addEventListener("DOMContentLoaded", () => {

const year = String(new Date().getFullYear());
document.querySelectorAll("[data-copyright-year]").forEach((el) => {
    el.textContent = year;
});

const menuButton = document.getElementById("mobile-menu-button");
const closeButton = document.getElementById("mobile-menu-close-button");
const menu = document.getElementById("mobile-menu");
const overlay = document.getElementById("mobile-menu-overlay");
const mobileNavLinks = document.querySelectorAll("#mobile-nav-links a");
const focusableSelector = 'a[href], button:not([disabled])';
let lastFocused = null;

const setExpanded = (open) => {
    menuButton.setAttribute("aria-expanded", open ? "true" : "false");
    menuButton.setAttribute("aria-label", open ? "Close navigation menu" : "Open navigation menu");
    menu.dataset.open = open ? "true" : "false";
                menu.classList.toggle("is-open", open);
                menu.classList.toggle("translate-x-full", !open);
    overlay.setAttribute("aria-hidden", open ? "false" : "true");
};

const trapFocus = (e) => {
    if (!menu.dataset.open || menu.dataset.open !== "true") return;
    if (e.key !== "Tab") return;
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
    overlay.classList.remove("hidden");
    document.body.style.overflow = "hidden";
    setExpanded(true);
    closeButton.focus();
    document.addEventListener("keydown", onKeydown);
};

const closeMenu = () => {
    overlay.classList.add("hidden");
    document.body.style.overflow = "";
    setExpanded(false);
    document.removeEventListener("keydown", onKeydown);
    if (lastFocused && typeof lastFocused.focus === "function") lastFocused.focus();
};

const onKeydown = (e) => {
    if (e.key === "Escape") closeMenu();
    trapFocus(e);
};

menuButton.addEventListener("click", () => {
    const isOpen = menuButton.getAttribute("aria-expanded") === "true";
    if (isOpen) closeMenu();
    else openMenu();
});
closeButton.addEventListener("click", closeMenu);
overlay.addEventListener("click", closeMenu);
mobileNavLinks.forEach((link) => link.addEventListener("click", closeMenu));

const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (!prefersReducedMotion) {
    document.querySelectorAll(".stagger-reveal-container").forEach((container) => {
        const text = container.textContent.trim();
        container.textContent = "";
        [...text].forEach((char, index) => {
            const span = document.createElement("span");
            span.className = "char";
            span.textContent = char === " " ? "\u00A0" : char;
            span.style.setProperty("--delay", `${index * 40}ms`);
            container.appendChild(span);
        });
    });

    const sections = document.querySelectorAll(".fade-in-section, .stagger-reveal-container");
    const sectionObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("is-visible");
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12 });
    sections.forEach((section) => sectionObserver.observe(section));
} else {
    document.querySelectorAll(".fade-in-section, .stagger-reveal-container").forEach((el) => {
        el.classList.add("is-visible");
    });
}

const navSections = document.querySelectorAll("main section[id]");
const navLinks = document.querySelectorAll("#desktop-nav-links a");
const navObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            const id = entry.target.getAttribute("id");
            navLinks.forEach((link) => {
                link.removeAttribute("aria-current");
                if (link.getAttribute("href") === `#${id}`) {
                    link.setAttribute("aria-current", "page");
                }
            });
        }
    });
}, { rootMargin: "-40% 0px -55% 0px" });
navSections.forEach((section) => {
    if (["home", "about", "focus", "writing", "contact"].includes(section.id)) {
        navObserver.observe(section);
    }
});

const STORAGE_KEY = "rk-sidebar-collapsed";
const toggleBtns = document.querySelectorAll("[data-sidebar-toggle]");
const setCollapsed = (collapsed, { persist = true } = {}) => {
    document.documentElement.setAttribute("data-sidebar", collapsed ? "collapsed" : "expanded");
    toggleBtns.forEach((btn) => {
        btn.setAttribute("aria-pressed", collapsed ? "true" : "false");
        btn.setAttribute("aria-label", collapsed ? "Exit full width" : "Full width reading");
    });
    if (persist) {
        try { localStorage.setItem(STORAGE_KEY, collapsed ? "1" : "0"); } catch (_) {}
    }
};
let initialCollapsed = false;
try { initialCollapsed = localStorage.getItem(STORAGE_KEY) === "1"; } catch (_) {}
setCollapsed(initialCollapsed, { persist: false });
toggleBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
        const next = document.documentElement.getAttribute("data-sidebar") !== "collapsed";
        setCollapsed(next);
    });
});

const deckSlides = [
    { id: "home", label: "Presence" },
    { id: "about", label: "The Story" },
    { id: "focus", label: "Focus" },
    { id: "writing", label: "Writing" },
    { id: "faq", label: "FAQ" },
    { id: "contact", label: "Connect" }
];
const deckPrev = document.querySelector("[data-deck-prev]");
const deckNext = document.querySelector("[data-deck-next]");
const deckLabel = document.querySelector("[data-deck-label]");
const deckIndexEl = document.querySelector("[data-deck-index]");
const deckTotalEl = document.querySelector("[data-deck-total]");
let deckIndex = 0;
let deckAnimating = false;
const deckCount = deckSlides.length + 1; /* + blog exit */

if (deckTotalEl) deckTotalEl.textContent = String(deckCount);

const updateDeckChrome = (index) => {
    const slide = deckSlides[index];
    if (deckLabel) deckLabel.textContent = slide.label;
    if (deckIndexEl) deckIndexEl.textContent = String(index + 1);
    if (deckPrev) deckPrev.disabled = index === 0;
    if (deckNext) {
        deckNext.disabled = false;
        deckNext.setAttribute(
            "aria-label",
            index === deckSlides.length - 1 ? "Continue to blog" : "Next section"
        );
    }
};

const goToDeck = (index, { updateHash = true } = {}) => {
    if (index < 0) return;
    if (index >= deckSlides.length) {
        window.location.href = "/blog";
        return;
    }
    const slide = deckSlides[index];
    const el = document.getElementById(slide.id);
    if (!el) return;
    deckAnimating = true;
    deckIndex = index;
    updateDeckChrome(index);
    el.scrollIntoView({ behavior: prefersReducedMotion ? "auto" : "smooth", block: "start" });
    if (updateHash) {
        history.replaceState(null, "", `#${slide.id}`);
    }
    window.setTimeout(() => { deckAnimating = false; }, prefersReducedMotion ? 50 : 700);
};

const syncDeckFromScroll = () => {
    if (deckAnimating) return;
    const marker = window.innerHeight * 0.35;
    let best = 0;
    let bestDist = Infinity;
    deckSlides.forEach((slide, i) => {
        const el = document.getElementById(slide.id);
        if (!el) return;
        const top = el.getBoundingClientRect().top;
        const dist = Math.abs(top - marker);
        if (top <= marker + 80 && dist < bestDist) {
            bestDist = dist;
            best = i;
        }
    });
    if (best !== deckIndex) {
        deckIndex = best;
        updateDeckChrome(best);
    }
};

deckPrev?.addEventListener("click", () => goToDeck(deckIndex - 1));
deckNext?.addEventListener("click", () => goToDeck(deckIndex + 1));

document.addEventListener("keydown", (e) => {
    if (e.target && /INPUT|TEXTAREA|SELECT/.test(e.target.tagName)) return;
    if (menu?.dataset.open === "true") return;
    if (e.key === "ArrowRight" || e.key === "PageDown") {
        e.preventDefault();
        goToDeck(deckIndex + 1);
    } else if (e.key === "ArrowLeft" || e.key === "PageUp") {
        e.preventDefault();
        goToDeck(deckIndex - 1);
    } else if (e.key === "Home" && !e.metaKey && !e.ctrlKey) {
        e.preventDefault();
        goToDeck(0);
    } else if (e.key === "End" && !e.metaKey && !e.ctrlKey) {
        e.preventDefault();
        goToDeck(deckSlides.length - 1);
    }
});

let deckScrollTick = 0;
window.addEventListener("scroll", () => {
    window.cancelAnimationFrame(deckScrollTick);
    deckScrollTick = window.requestAnimationFrame(syncDeckFromScroll);
}, { passive: true });

const hashId = location.hash.replace(/^#/, "");
const hashIndex = deckSlides.findIndex((s) => s.id === hashId);
if (hashIndex >= 0) {
    goToDeck(hashIndex, { updateHash: false });
} else {
    updateDeckChrome(0);
    syncDeckFromScroll();
}
});
