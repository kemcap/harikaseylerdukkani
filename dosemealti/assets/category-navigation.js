'use strict';
(() => {
  // Desktop/tablet: keep the homepage navigation, with "Dört dünya" as a category submenu.
  const worlds = document.querySelector('.nav-worlds');
  if (worlds) {
    document.addEventListener('pointerdown', event => {
      if (worlds.open && !worlds.contains(event.target)) worlds.open = false;
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && worlds.open) {
        worlds.open = false;
        worlds.querySelector('summary')?.focus();
      }
    });
    worlds.querySelectorAll('.nav-worlds-panel a').forEach(link => {
      link.addEventListener('click', () => { worlds.open = false; });
    });
  }

  // Mobile: a subtle story-style dock appears after the visitor begins scrolling.
  // It is hidden on the untouched hero, so the 100svh composition stays uncluttered.
  const dock = document.getElementById('mobile-world-dock');
  if (!dock) return;
  const mobile = window.matchMedia('(max-width: 760px)');
  let pending = false;
  const update = () => {
    pending = false;
    const show = mobile.matches && window.scrollY >= Math.min(240, window.innerHeight * 0.28);
    dock.classList.toggle('is-visible', show);
    dock.setAttribute('aria-hidden', String(!show));
    if ('inert' in dock) dock.inert = !show;
  };
  const requestUpdate = () => {
    if (pending) return;
    pending = true;
    requestAnimationFrame(update);
  };
  window.addEventListener('scroll', requestUpdate, {passive:true});
  window.addEventListener('resize', requestUpdate, {passive:true});
  window.addEventListener('pageshow', requestUpdate);
  mobile.addEventListener?.('change', requestUpdate);
  update();
})();
