'use strict';
(() => {
  const search = document.getElementById('search');
  if (!search) return;
  const industry = document.getElementById('industry');
  const status = document.getElementById('status');
  const cards = [...document.querySelectorAll('.card')];
  function filter() {
    let count = 0;
    const query = search.value.trim().toLowerCase();
    for (const card of cards) {
      const visible = card.dataset.search.includes(query) && (!industry.value || card.dataset.industry.split('|').includes(industry.value)) && (!status.value || status.value === card.dataset.status);
      card.hidden = !visible;
      if (visible) count++;
    }
    document.getElementById('result-count').textContent = `${count} record${count === 1 ? '' : 's'} shown`;
    document.getElementById('no-results').hidden = count !== 0;
  }
  for (const control of [search, industry, status]) control.addEventListener('input', filter);
  filter();
})();
