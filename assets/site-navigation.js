document.querySelectorAll('.site-programs').forEach(menu => {
  const summary = menu.querySelector('summary');
  let openedOnHover = false;
  let closeTimer;

  function cancelClose() {
    clearTimeout(closeTimer);
  }

  function close() {
    cancelClose();
    openedOnHover = false;
    menu.open = false;
  }

  function closeAfterPointerLeaves() {
    cancelClose();
    closeTimer = setTimeout(() => {
      if (!menu.matches(':hover') && !menu.contains(document.activeElement)) close();
    }, 220);
  }

  menu.addEventListener('pointerenter', event => {
    cancelClose();
    if (event.pointerType !== 'mouse' || menu.open) return;
    menu.open = true;
    openedOnHover = true;
  });

  menu.addEventListener('pointerleave', () => {
    if (openedOnHover) closeAfterPointerLeaves();
  });

  // Keep the disclosure open from pressing a link through its native click.
  menu.addEventListener('pointerdown', event => {
    cancelClose();
    if (event.target.closest('a[href]')) openedOnHover = false;
  });

  summary.addEventListener('click', event => {
    cancelClose();
    if (event.detail && openedOnHover && menu.open) event.preventDefault();
    openedOnHover = false;
  });

  menu.addEventListener('keydown', event => {
    if (event.key !== 'Escape' || !menu.open) return;
    event.preventDefault();
    close();
    summary.focus();
  });

  menu.addEventListener('focusin', cancelClose);
  menu.addEventListener('focusout', () => {
    cancelClose();
    closeTimer = setTimeout(() => {
      if (!menu.contains(document.activeElement) && !menu.matches(':hover')) close();
    }, 220);
  });

  document.addEventListener('pointerdown', event => {
    if (!menu.contains(event.target)) close();
  });
});
