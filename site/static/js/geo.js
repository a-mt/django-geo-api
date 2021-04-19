/* global API_URL, EDIT_URL */
const URL       = window.location.origin;
const container = document.getElementById('results');

if(window.location.search) {
  let urlParams = new URLSearchParams(window.location.href);
  search(
    urlParams.get('q') || '',
    urlParams.get('page') || 1);
}

function search(value, page=1) {
  let q = encodeURIComponent(value);

  fetch(API_URL + '?format=json&q=' + q + '&page=' + page)
    .then(response => response.json())
    .then(data => {
      container.innerHTML = render(data, q);
    });
}

function render(data, q) {
  if(data.detail) {
    return `<div class="alert alert--error">${data.detail}</div>`;
  }
  if(data.count == 0) {
    return '<h2 class="header2">0 résultat</h2>';
  }
  let pagination = (data.num_pages > 1 ? getPagination(data, q) : '');

  return `<h2 class="header2">${data.count.toLocaleString()} résultat${data.count == 1 ? '' : 's'}</h2>
    ${pagination}
    <div class="mt-8 mb-8">
      ${data.results.map(item => {
        let extraClass = (item.population > 100000 ? 'green' : '');

        let info = '';
        if(item.departement) {
          info += `<tr><td class="card-info">Département:</td><td>${item.departement.nom} (${item.departement.code})</td></tr>`;
        }
        if(item.codesPostaux.length) {
          info += `<tr><td class="card-info">Code Postaux:</td><td>${item.codesPostaux.join(', ')}</td></tr>`;
        }
        if(item.population) {
          info += `<tr><td class="card-info">Population:</td><td>${item.population.toLocaleString()}</td></tr>`;
        }

        return `<div class="card ${extraClass}">
          <a class="card-title ${extraClass}" href="${EDIT_URL.replace('CODE', item.code)}">${item.code} ${item.nom}</a>
          ${info ? `<div class="card-description ${extraClass}"><table>${info}</table></div>` : ''}
        </div>`;

      }).join("\n")}
    </div>
    ${pagination}
    `;
}

function getPagination({page, num_pages, previous, next}, q) {
  let url = `${URL}?q=${q}&page=`

  let pages = '';
  for(let i=Math.max(1, page-1); i<=Math.min(page+1, num_pages); i++) {
    pages += (i==page
            ? `<span class="pag-num pag-num--current">${i}</span>`
            : `<a class="pag-num" href="${url}${i}">${i}</a>`);
  }

  return `<nav class="paging">
      <div class="paging-left">
        ${previous ? `<a href="${url}${page-1}" class="pag-num pag-num--prev">Précédent</a>` : ''}
      </div>
      <div class="paging-center">
        ${page > 2  ? `<a class="pag-num" href="${url}1">1</a>` : ''}
        ${page > 3  ? '<span class="pag-num pag-num--dots">…</span>' : ''}
        ${pages}
        ${page+2 < num_pages ? '<span class="pag-num pag-num--dots">…</span>' : ''}
        ${page+1 < num_pages ? `<a class="pag-num" href="${url}${num_pages}">${num_pages}</a>` : ''}
      </div>
      <div class="paging-right">
        ${next ? `<a href="${url}${page+1}" class="pag-num pag-num--next">Suivant</a>` : ''}
      </div>
    </nav>`;
}