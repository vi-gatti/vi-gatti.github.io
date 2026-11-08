// Light and dark theme. Light is the default; the choice is remembered on
// this device when the browser allows it.
(() => {
  const root = document.documentElement;
  const button = document.querySelector('.theme-toggle');
  if (!button) return;
  const sync = () => button.setAttribute('aria-pressed', String(root.dataset.theme === 'dark'));
  sync();
  button.addEventListener('click', () => {
    const dark = root.dataset.theme !== 'dark';
    if (dark) root.dataset.theme = 'dark';
    else delete root.dataset.theme;
    try { localStorage.setItem('theme', dark ? 'dark' : 'light'); } catch (e) {}
    sync();
  });
})();
