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
