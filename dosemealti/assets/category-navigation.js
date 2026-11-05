'use strict';
(() => {
  // Native <details> disclosure: pointer, keyboard, outside-click and Escape.
  const menu = document.querySelector('.mobile-worlds-menu');
  if (!menu) return;
  document.addEventListener('pointerdown', event => {
    if (menu.open && !menu.contains(event.target)) menu.open = false;
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.open) {
      menu.open = false;
      menu.querySelector('summary')?.focus();
    }
  });
  menu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => { menu.open = false; });
  });
  window.matchMedia('(min-width: 1061px)').addEventListener?.('change', event => {
    if (event.matches) menu.open = false;
  });
})();
