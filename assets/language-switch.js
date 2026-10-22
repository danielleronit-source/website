// Keep the visitor at the equivalent section when changing page language.
document.querySelectorAll('a.site-language:not([aria-current="page"])').forEach(link => {
  link.addEventListener('click', () => {
    const target = new URL(link.href, window.location.href);
    if (window.location.hash) target.hash = window.location.hash;
    link.href = target.href;
  });
});
