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

// Copy buttons (contact page): copy the value and confirm for two seconds.
document.addEventListener('click', (event) => {
  const button = event.target.closest('.copy-btn');
  if (!button) return;
  const label = button.querySelector('span');
  const original = label ? label.textContent : '';
  const done = () => {
    if (!label) return;
    label.textContent = button.dataset.done || original;
    setTimeout(() => { label.textContent = original; }, 2000);
  };
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(button.dataset.copy).then(done, () => {});
  } else {
    const field = document.createElement('textarea');
    field.value = button.dataset.copy;
    document.body.appendChild(field);
    field.select();
    try { document.execCommand('copy'); done(); } catch (e) {}
    field.remove();
  }
});
