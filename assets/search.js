'use strict';
(() => {
  const search = document.getElementById('search');
  if (!search) return;
  const industry = document.getElementById('industry');
  const status = document.getElementById('status');
  const type = document.getElementById('type');
  const cards = [...document.querySelectorAll('.card')];
  function filter() {
    let count = 0;
    const query = search.value.trim().toLowerCase();
    for (const card of cards) {
      const visible = card.dataset.search.includes(query) && (!industry || !industry.value || card.dataset.industry.split('|').includes(industry.value)) && (!status || !status.value || status.value === card.dataset.status) && (!type || !type.value || type.value === card.dataset.type);
      card.hidden = !visible;
      if (visible) count++;
    }
    document.getElementById('result-count').textContent = `${count} record${count === 1 ? '' : 's'} shown`;
    document.getElementById('no-results').hidden = count !== 0;
  }
  for (const control of [search, industry, status, type]) if (control) control.addEventListener('input', filter);
  filter();
})();
