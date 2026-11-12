document.querySelectorAll('.site-programs').forEach(menu => {
  const summary = menu.querySelector('summary');
  let openedOnHover = false;

  menu.addEventListener('pointerenter', event => {
    if (event.pointerType !== 'mouse' || menu.open) return;
    menu.open = true;
    openedOnHover = true;
  });

  menu.addEventListener('pointerleave', () => {
    if (openedOnHover && !menu.contains(document.activeElement)) close();
  });

  summary.addEventListener('click', event => {
    if (event.detail && openedOnHover && menu.open) event.preventDefault();
    openedOnHover = false;
  });

  menu.addEventListener('keydown', event => {
    if (event.key !== 'Escape' || !menu.open) return;
    event.preventDefault();
    close();
    summary.focus();
  });

  menu.addEventListener('focusout', event => {
    if (!menu.contains(event.relatedTarget)) close();
  });

  document.addEventListener('pointerdown', event => {
    if (!menu.contains(event.target)) close();
  });

  function close() {
    openedOnHover = false;
    menu.open = false;
  }
});
