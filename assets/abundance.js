(() => {
  const story = document.querySelector('.facilitator-story');
  if (!story) return;
  const summary = story.querySelector('summary');
  story.querySelector('.story-close-button').addEventListener('click', () => {
    story.open = false;
    summary.focus({preventScroll: true});
    summary.scrollIntoView({block: 'nearest', behavior: 'instant'});
  });
})();
