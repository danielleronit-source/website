(() => {
  const story = document.querySelector('.facilitator-story');
  if (!story) return;
  const summary = story.querySelector('summary');
  const openStoryFromHash = () => {
    if (window.location.hash === '#danielle-story') story.open = true;
  };
  window.addEventListener('hashchange', openStoryFromHash);
  openStoryFromHash();
  story.querySelector('.story-close-button').addEventListener('click', () => {
    story.open = false;
    summary.focus({preventScroll: true});
    summary.scrollIntoView({block: 'nearest', behavior: 'instant'});
  });
})();

(() => {
  const dismiss = document.querySelector('.contact-dismiss');
  if (!dismiss) return;
  dismiss.addEventListener('click', () => {
    document.querySelector('.contact-greeting').hidden = true;
    document.querySelector('.contact-widget').classList.add('contact-compact');
    document.querySelector('.contact-launcher').focus({preventScroll: true});
  });
})();
