document.querySelectorAll('.testimonial-video').forEach(container => {
  const button = container.querySelector('.testimonial-video-play');
  button.addEventListener('click', () => {
    const frame = document.createElement('iframe');
    const url = new URL(container.dataset.videoSrc);
    url.searchParams.set('autoplay', '1');
    url.searchParams.set('playsinline', '1');
    // Match the current preview or live host for the embedded player.
    url.searchParams.set('origin', window.location.origin);
    frame.src = url.href;
    frame.title = container.dataset.videoTitle;
    frame.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    frame.allowFullscreen = true;
    frame.referrerPolicy = 'strict-origin-when-cross-origin';
    container.replaceChildren(frame);
    frame.focus();
  }, {once: true});
});
