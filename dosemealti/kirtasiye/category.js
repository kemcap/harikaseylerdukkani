
'use strict';
(() => {
  const header = document.querySelector('.header');
  const toggle = document.querySelector('.menu-toggle');
  const menu = document.getElementById('mobile-menu');
  const heroStar = document.querySelector('.hero-asterisk');
  const heroBadge = document.querySelector('.hero .float-label');
  const heroSection = document.querySelector('.hero');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let lastY = window.scrollY;
  let raf = 0;
  function onScroll() {
    raf = 0;
    const y = window.scrollY;
    // Subtle badge tilt between 4° and 10° as the hero scrolls past.
    // Scrolling up reverses the movement, reduced-motion keeps it still.
    if (heroBadge && heroSection) {
      const fraction = Math.min(1, Math.max(0, y / Math.max(1, heroSection.offsetHeight)));
      const degrees = reducedMotion.matches ? 4 : 4 + fraction * 6;
      heroBadge.style.setProperty('--hero-label-angle', `${degrees.toFixed(2)}deg`);
    }
    // Scroll position controls the angle: down turns clockwise, up reverses.
    // Respect reduced-motion settings and do not animate independently.
    if (heroStar) heroStar.style.setProperty('--hero-star-rotation', reducedMotion.matches ? '0deg' : `${(Math.max(0, y) * 0.42).toFixed(2)}deg`);
    if (y > 180 && y > lastY + 7) header.classList.add('is-hidden');
    else if (y < lastY - 7 || y < 80) header.classList.remove('is-hidden');
    lastY = y;
  }
  window.addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(onScroll); }, { passive: true });
  reducedMotion.addEventListener?.('change', onScroll);
  onScroll();
  if (toggle && menu) {
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      toggle.setAttribute('aria-label', open ? 'Menüyü aç' : 'Menüyü kapat');
      menu.hidden = open;
    });
    menu.addEventListener('click', event => {
      if (event.target.closest('a')) { menu.hidden = true; toggle.setAttribute('aria-expanded', 'false'); toggle.setAttribute('aria-label', 'Menüyü aç'); }
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && !menu.hidden) { menu.hidden = true; toggle.setAttribute('aria-expanded', 'false'); toggle.focus(); }
    });
  }
  const chapters = Array.from(document.querySelectorAll('[data-chapter]'));
  const images = Array.from(document.querySelectorAll('[data-visual]'));
  const counter = document.getElementById('visual-counter');
  if ('IntersectionObserver' in window && chapters.length && images.length) {
    const observer = new IntersectionObserver(entries => {
      const candidates = entries.filter(entry => entry.isIntersecting).sort((a,b) => b.intersectionRatio - a.intersectionRatio);
      if (!candidates.length) return;
      const index = Number(candidates[0].target.dataset.chapter);
      images.forEach(image => image.classList.toggle('active', Number(image.dataset.visual) === index));
      counter.innerHTML = String(index+1).padStart(2,'0') + ' <span>/ 03</span>';
    }, { rootMargin: '-24% 0px -24% 0px', threshold: [0,.1,.3,.5,.7] });
    chapters.forEach(chapter => observer.observe(chapter));
  }
  const year = document.getElementById('year');
  if (year) year.textContent = String(new Date().getFullYear());
})();

