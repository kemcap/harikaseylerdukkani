'use strict';
(() => {
  const toggle = document.querySelector('[data-category-menu-toggle]');
  const panel = document.getElementById('category-menu');
  if (!toggle || !panel) return;
  const setOpen = open => {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Menüyü kapat' : 'Kategoriler menüsünü aç');
    panel.hidden = !open;
  };
  toggle.addEventListener('click', () => setOpen(panel.hidden));
  document.addEventListener('pointerdown', event => {
    if (!panel.hidden && !event.target.closest('.category-menu-wrap')) setOpen(false);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !panel.hidden) {
      setOpen(false);
      toggle.focus();
    }
  });
  panel.addEventListener('click', event => {
    if (event.target.closest('a')) setOpen(false);
  });
  window.addEventListener('scroll', () => {
    if (!panel.hidden) setOpen(false);
  }, {passive:true});
  window.addEventListener('pageshow', () => setOpen(false));
})();
