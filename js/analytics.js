(() => {
  const GA_ID = "G-FE9X30EBMG";
  window.dataLayer = window.dataLayer || [];
  window.gtag =
    window.gtag ||
    function gtag() {
      window.dataLayer.push(arguments);
    };

  let loaded = false;

  const loadGtag = () => {
    if (loaded) return;
    loaded = true;

    window.gtag("js", new Date());
    window.gtag("config", GA_ID, { send_page_view: true });

    const script = document.createElement("script");
    script.id = "ga-gtag";
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
    document.head.appendChild(script);
  };

  const arm = () => {
    const onInteract = () => loadGtag();
    const events = ["scroll", "pointerdown", "keydown", "touchstart"];
    events.forEach((type) =>
      window.addEventListener(type, onInteract, { once: true, passive: true })
    );

    // Fallback so bounce visits still count without blocking mobile LCP.
    if ("requestIdleCallback" in window) {
      window.requestIdleCallback(loadGtag, { timeout: 5000 });
    } else {
      window.setTimeout(loadGtag, 5000);
    }
  };

  if (document.readyState === "complete") {
    arm();
  } else {
    window.addEventListener("load", arm, { once: true });
  }
})();
