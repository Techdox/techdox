(() => {
  document.querySelectorAll('.prose pre').forEach((pre, index) => {
    const code = pre.querySelector('code') || pre;
    const controls = document.createElement('div');
    controls.className = 'code-tools';
    const button = document.createElement('button');
    button.type = 'button'; button.className = 'copy-code'; button.textContent = 'Copy code';
    const status = document.createElement('span');
    status.className = 'copy-status'; status.id = `copy-status-${index}`;
    status.setAttribute('role', 'status'); status.setAttribute('aria-live', 'polite');
    button.setAttribute('aria-describedby', status.id);
    button.addEventListener('click', async () => {
      button.disabled = true;
      try {
        if (!navigator.clipboard) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(code.textContent);
        status.textContent = 'Copied.';
      } catch {
        status.textContent = 'Select the code and copy manually.';
      } finally { button.disabled = false; }
    });
    controls.append(button, status); pre.before(controls);
  });
})();
