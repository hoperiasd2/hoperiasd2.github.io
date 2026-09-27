// Shared utility: scroll-reveal for elements with class "reveal"
document.addEventListener('DOMContentLoaded', () => {
  const items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window) || items.length === 0) {
    items.forEach(el => el.classList.add('is-visible'));
    return;
  }
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.01, rootMargin: '0px 0px 120px 0px' });
  items.forEach(el => io.observe(el));

  // Safety net: if anything is still hidden after a few seconds
  // (e.g. fast programmatic scroll, unusual viewport), reveal it anyway.
  setTimeout(() => {
    document.querySelectorAll('.reveal:not(.is-visible)').forEach(el => el.classList.add('is-visible'));
  }, 2500);
});
