/* ============================================
   CXY.BLOG — 全局脚本
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ---------- 1. Theme Toggle ----------
  const themeBtn = document.getElementById('themeToggle');
  if (themeBtn) {
    const saved = localStorage.getItem('theme');
    if (saved === 'dark') document.documentElement.setAttribute('data-theme', 'dark');

    themeBtn.addEventListener('click', () => {
      const html = document.documentElement;
      const isDark = html.getAttribute('data-theme') === 'dark';
      html.setAttribute('data-theme', isDark ? '' : 'dark');
      localStorage.setItem('theme', isDark ? '' : 'dark');
      themeBtn.textContent = isDark ? '☀️' : '🌙';
    });

    // sync button text
    if (document.documentElement.getAttribute('data-theme') === 'dark') {
      themeBtn.textContent = '🌙';
    }
  }

  // ---------- 2. Auto-hide Nav on Scroll ----------
  const nav = document.querySelector('.nav');
  if (nav) {
    let lastScroll = window.scrollY;
    window.addEventListener('scroll', () => {
      const cur = window.scrollY;
      if (cur > lastScroll && cur > 120) nav.classList.add('hidden');
      else nav.classList.remove('hidden');
      lastScroll = cur;
    });
  }

  // ---------- 3. Scroll Reveal (Intersection Observer) ----------
  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
    );
    revealEls.forEach(el => observer.observe(el));
  }

  // ---------- 4. Active Nav Link ----------
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(a => {
    const href = a.getAttribute('href');
    if (href === '/' && currentPath === '/') a.classList.add('active');
    else if (href !== '/' && currentPath.startsWith(href)) a.classList.add('active');
  });
});