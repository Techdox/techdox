(() => {
  const panel = document.querySelector('[data-search-index]');
  if (!panel) return;
  const input = document.getElementById('search-input');
  const status = document.getElementById('search-status');
  const results = document.getElementById('search-results');
  let indexPromise;
  let generation = 0;
  async function search() {
    const current = ++generation;
    const words = input.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
    results.replaceChildren();
    if (!words.length) { status.textContent = 'Enter a topic or keyword.'; return; }
    status.textContent = 'Searching…';
    try {
      if (!indexPromise) indexPromise = fetch(panel.dataset.searchIndex).then(response => {
        if (!response.ok) throw new Error('Search index unavailable');
        return response.json();
      }).catch(error => { indexPromise = undefined; throw error; });
      const entries = await indexPromise;
      if (current !== generation) return;
      if (!Array.isArray(entries)) throw new Error('Invalid search index');
      const matches = entries.filter(entry => {
        if (typeof entry.url !== 'string' || !entry.url.startsWith('/') || entry.url.startsWith('//')) return false;
        const url = new URL(entry.url, location.origin);
        if (url.origin !== location.origin) return false;
        const haystack = [entry.title, entry.description, entry.text, ...(entry.tags || [])].join(' ').toLocaleLowerCase();
        return words.every(word => haystack.includes(word));
      });
      for (const entry of matches) {
        const link = document.createElement('a');
        link.className = 'card'; link.href = entry.url;
        const title = document.createElement('h2'); title.textContent = entry.title;
        const description = document.createElement('p'); description.textContent = entry.description;
        const date = document.createElement('span'); date.className = 'meta'; date.textContent = entry.date;
        link.append(title, description, date); results.append(link);
      }
      status.textContent = matches.length ? `${matches.length} ${matches.length === 1 ? 'result' : 'results'}.` : 'No posts found. Try a broader topic.';
    } catch {
      if (current === generation) status.textContent = 'Search is unavailable. Try again, or browse Posts and Topics above.';
    }
  }
  input.addEventListener('input', search);
})();
