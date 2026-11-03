
'use strict';
(() => {
  const header = document.querySelector('.header');
  const toggle = document.querySelector('.menu-toggle');
  const menu = document.getElementById('mobile-menu');
  const heroStar = document.querySelector('.hero-asterisk');
  const heroBadge = document.querySelector('.hero .float-label');
  const heroSection = document.querySelector('.hero');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const smallStars = [
    ...document.querySelectorAll('.twinkle, .note-star, .chapter-line span:last-child, .visit-photo-stamp span')
  ];
  const clamp = n => Math.max(0, Math.min(1, n));
  // Each small star rotates only while its own section passes through the viewport.
  // The angle is a function of scroll position, so upward scrolling reverses it.
  function updateSmallStars() {
    const vh = Math.max(1, window.innerHeight);
    smallStars.forEach(star => {
      const rect = star.getBoundingClientRect();
      if (rect.top > vh + 100 || rect.bottom < -100) return;
      const progress = clamp((vh - rect.top) / (vh + Math.max(1, rect.height)));
      const motion = reducedMotion.matches ? 0 : progress;
      const property = star.matches('.note-star') ? '--note-star-rotation'
        : star.matches('.twinkle') ? '--twinkle-rotation'
        : star.matches('.visit-photo-stamp span') ? '--stamp-star-rotation'
        : '--chapter-star-rotation';
      // Make the smaller decorative stars visibly rotate during their passage.
      const extent = property === '--note-star-rotation' ? -160
        : property === '--stamp-star-rotation' ? 135
        : property === '--twinkle-rotation' ? 110 : 150;
      star.style.setProperty(property, (motion * extent).toFixed(2) + 'deg');
    });
  }
  let headerAnchor = window.scrollY;
  let headerDirection = 0;
  let lastY = window.scrollY;
  let raf = 0;
  function onScroll() {
    raf = 0;
    const y = window.scrollY;
    // Make the info badge visibly tilt left as the hero is scrolled.
    // It turns back on upward scroll and respects reduced-motion settings.
    if (heroBadge && heroSection) {
      const fraction = Math.min(1, Math.max(0, y / Math.max(1, heroSection.offsetHeight)));
      const degrees = reducedMotion.matches ? 0 : -15 * fraction;
      heroBadge.style.setProperty('--hero-label-angle', `${degrees.toFixed(2)}deg`);
    }
    // Scroll position controls the angle: down turns clockwise, up reverses.
    // Respect reduced-motion settings and do not animate independently.
    if (heroStar) heroStar.style.setProperty('--hero-star-rotation', reducedMotion.matches ? '0deg' : `${(Math.max(0, y) * 0.105).toFixed(2)}deg`);
    updateSmallStars();
    updateVisualChapter();
    if (header) header.classList.toggle('scrolled', y > 24);
    const delta = y - headerAnchor;
    const direction = Math.sign(delta);
    if (y < 25) {
      document.documentElement.classList.remove('header-compact');
      headerAnchor = y; headerDirection = 0;
    } else if (direction !== headerDirection) {
      headerDirection = direction; headerAnchor = y;
    } else if (Math.abs(delta) > 12) {
      document.documentElement.classList.toggle('header-compact', direction > 0 && y > 80);
      headerAnchor = y;
    }
    lastY = y;
  }
  window.addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(onScroll); }, { passive: true });
  reducedMotion.addEventListener?.('change', onScroll);
  window.addEventListener('resize', () => { if (!raf) raf = requestAnimationFrame(onScroll); }, { passive: true });
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
  let activeChapter = -1;
  function updateVisualChapter() {
    if (!chapters.length || !images.length || !counter) return;
    const viewHeight = Math.max(1, window.innerHeight);
    const focusLine = viewHeight * 0.5;
    const tolerance = Math.min(72, Math.max(28, viewHeight * 0.06));
    const firstPass = activeChapter < 0;
    let index = firstPass ? 0 : activeChapter;

    if (firstPass) {
      // First view: determine which chapter contains the viewport focal point.
      for (let i = 1; i < chapters.length; i++) {
        if (chapters[i].getBoundingClientRect().top <= focusLine) index = i;
      }
    } else {
      // Forward scroll: change only after the next chapter passes the focus
      // line by a margin. Backward scroll uses the symmetrical threshold.
      while (index < chapters.length - 1 &&
             chapters[index + 1].getBoundingClientRect().top < focusLine - tolerance) {
        index++;
      }
      while (index > 0 &&
             chapters[index].getBoundingClientRect().top > focusLine + tolerance) {
        index--;
      }
    }
    // Avoid repainting the images and counter when the section hasn't changed.
    if (index === activeChapter) return;
    activeChapter = index;
    images.forEach(image => {
      image.classList.toggle('active', Number(image.dataset.visual) === index);
    });
    const value = String(index + 1).padStart(2, '0');
    counter.firstChild.textContent = value + ' ';
  }
  const year = document.getElementById('year');
  if (year) year.textContent = String(new Date().getFullYear());
  window.addEventListener('pageshow', onScroll);
  onScroll();
})();

