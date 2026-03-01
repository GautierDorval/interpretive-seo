(() => {
  const button = document.querySelector('.menu-toggle');
  const nav = document.querySelector('[data-nav]');

  if (!button || !nav) {
    return;
  }

  const mobileQuery = window.matchMedia('(max-width: 760px)');

  const setOpen = (open) => {
    button.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  };

  const syncMenu = () => {
    if (!mobileQuery.matches) {
      setOpen(false);
      return;
    }

    const isOpen = button.getAttribute('aria-expanded') === 'true';
    nav.classList.toggle('is-open', isOpen);
  };

  button.addEventListener('click', () => {
    const isOpen = button.getAttribute('aria-expanded') === 'true';
    setOpen(!isOpen);
  });

  nav.addEventListener('click', (event) => {
    if (!mobileQuery.matches) {
      return;
    }

    const link = event.target.closest('a');
    if (link) {
      setOpen(false);
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && mobileQuery.matches && button.getAttribute('aria-expanded') === 'true') {
      setOpen(false);
      button.focus();
    }
  });

  if (typeof mobileQuery.addEventListener === 'function') {
    mobileQuery.addEventListener('change', syncMenu);
  } else if (typeof mobileQuery.addListener === 'function') {
    mobileQuery.addListener(syncMenu);
  }

  syncMenu();
})();
