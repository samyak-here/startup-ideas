'use strict';
(() => {
  const search = document.getElementById('search');
  if (!search) return;
  const controls = {kind: document.getElementById('kind'), industry: document.getElementById('industry'), status: document.getElementById('status')};
  const cards = [...document.querySelectorAll('.card')];
  let index = null; // id -> full lowercase record text, fetched on first query; falls back to card text.
  const base = new Map(cards.map(c => [c.dataset.id, c.textContent.toLowerCase()]));
  function load() {
    if (index !== null) return;
    index = new Map();
    fetch('search-index.json').then(r => r.ok ? r.json() : []).then(rows => {
      for (const row of rows) index.set(row.id, row.text);
      filter();
    }).catch(() => {});
  }
  function filter() {
    let count = 0;
    const query = search.value.trim().toLowerCase();
    for (const card of cards) {
      const text = (index && index.get(card.dataset.id)) || base.get(card.dataset.id);
      const visible = text.includes(query)
        && (!controls.kind.value || controls.kind.value === card.dataset.kind)
        && (!controls.industry.value || card.dataset.industry.split('|').includes(controls.industry.value))
        && (!controls.status.value || controls.status.value === card.dataset.status);
      card.hidden = !visible;
      if (visible) count++;
    }
    document.getElementById('result-count').textContent = `${count} record${count === 1 ? '' : 's'} shown`;
    document.getElementById('no-results').hidden = count !== 0;
  }
  search.addEventListener('input', () => { if (search.value) load(); filter(); });
  for (const control of Object.values(controls)) control.addEventListener('change', filter);
  filter();
})();
