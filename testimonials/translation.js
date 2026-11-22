(() => {
  const toggle = document.querySelector('.translation-toggle');
  if (!toggle) return;
  const hebrew = document.getElementById('dana-hebrew');
  const english = document.getElementById('dana-english');
  toggle.addEventListener('click', () => {
    const showEnglish = english.hidden;
    english.hidden = !showEnglish;
    hebrew.hidden = showEnglish;
    toggle.setAttribute('aria-pressed', String(showEnglish));
    toggle.textContent = showEnglish ? 'Show original Hebrew' : 'Translate to English';
  });
})();
