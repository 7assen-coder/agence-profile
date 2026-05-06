/* ── Modal helpers ─────────────────────────────────────────────────────── */

function showModal(title, status, data) {
  document.getElementById('modal-title').textContent = title;

  const badge = document.getElementById('modal-status-badge');
  if (status === null) {
    badge.innerHTML = '<span class="status-badge s0">En cours…</span>';
  } else {
    const cls = status >= 200 && status < 300 ? 's2xx'
              : status >= 400 && status < 500 ? 's4xx'
              : status === 0 ? 's0' : 's5xx';
    badge.innerHTML = `<span class="status-badge ${cls}">HTTP ${status || 'ERR'}</span>`;
  }

  const pre = document.getElementById('modal-json');
  if (data) {
    pre.innerHTML = syntaxHL(data);
  } else {
    pre.textContent = '';
  }

  document.getElementById('modal').classList.add('open');
}

function closeModal() {
  document.getElementById('modal').classList.remove('open');
}

/* ── JSON syntax highlighter ───────────────────────────────────────────── */

function syntaxHL(obj) {
  return JSON.stringify(obj, null, 2)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"([^"]+)":/g, '<span class="jk">"$1"</span>:')
    .replace(/: "([^"]*)"/g, ': <span class="js">"$1"</span>')
    .replace(/: (\d+\.?\d*)/g, ': <span class="jn">$1</span>')
    .replace(/: (true|false)/g, ': <span class="jb">$1</span>')
    .replace(/: null/g, ': <span class="jnull">null</span>');
}

/* ── Close modal on Escape ─────────────────────────────────────────────── */

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeModal();
});
