(function () {
  'use strict';
  var form = document.getElementById('dl-form');
  if (!form) return;
  var T = JSON.parse(document.getElementById('dl-i18n').textContent);
  var api = form.getAttribute('data-api'), version = form.getAttribute('data-version'), lang = form.getAttribute('data-lang');
  var fileBox = document.getElementById('dl-file'), ready = document.getElementById('dl-ready'), unavailable = document.getElementById('dl-unavailable');
  var submit = document.getElementById('dl-submit'), generalErr = document.getElementById('dl-error');
  var token = '', EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  function human(n) {
    if (!n) return '';
    var u = ['B', 'KB', 'MB', 'GB'], i = 0;
    while (n >= 1024 && i < u.length - 1) { n /= 1024; i++; }
    return (i ? n.toFixed(n < 10 ? 1 : 0) : n) + ' ' + u[i];
  }
  function fileInfo(f) {
    fileBox.textContent = '';
    [[T.file, f.name], [T.size, human(f.size)], [T.sha256, f.sha256]].forEach(function (r) {
      if (!r[1]) return;
      var d = document.createElement('div'), b = document.createElement('strong'), c = document.createElement('code');
      b.textContent = r[0] + ': '; c.textContent = r[1]; d.appendChild(b); d.appendChild(c); fileBox.appendChild(d);
    });
    fileBox.hidden = false;
  }
  function setErr(name, code) {
    var el = form.querySelector('[data-err="' + name + '"]');
    if (el) el.textContent = code ? (T['err_' + code] || T.err_invalid) : '';
  }
  function clearErrs() {
    form.querySelectorAll('[data-err]').forEach(function (e) { e.textContent = ''; });
    generalErr.textContent = '';
  }

  fetch(api + '/init?version=' + encodeURIComponent(version)).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
    .then(function (x) {
      if (!x.ok || !x.j.ok) { unavailable.hidden = false; return; }
      token = x.j.t; fileInfo(x.j.release.files[0]); form.hidden = false;
    })
    .catch(function () { generalErr.textContent = T.err_network; unavailable.hidden = false; });

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    clearErrs();
    var v = function (n) { return (form.elements[n].value || '').replace(/\s+/g, ' ').trim(); };
    var bad = false;
    ['first_name', 'last_name', 'company', 'email'].forEach(function (n) { if (!v(n)) { setErr(n, 'required'); bad = true; } });
    if (v('email') && !EMAIL.test(v('email'))) { setErr('email', 'invalid'); bad = true; }
    if (!form.elements.privacy.checked) { setErr('privacy', 'privacy'); bad = true; }
    if (bad) return;
    submit.disabled = true; var label = submit.textContent; submit.textContent = T.sending;
    fetch(api + '/request', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ version: version, first_name: v('first_name'), last_name: v('last_name'), company: v('company'), email: v('email'), phone: v('phone'),
        contact_ok: form.elements.contact_ok.checked, privacy: form.elements.privacy.checked, lang: lang, website: form.elements.website.value, t: token })
    }).then(function (r) { return r.json().then(function (j) { return { status: r.status, j: j }; }); })
      .then(function (x) {
        if (x.j.ok) {
          document.getElementById('dl-link').href = x.j.url;
          form.hidden = true; ready.hidden = false;
          if (x.j.file) fileInfo(x.j.file);
          setTimeout(function () { window.location.href = x.j.url; }, 600);
          return;
        }
        if (x.status === 422 && x.j.fields) { Object.keys(x.j.fields).forEach(function (n) { setErr(n, n === 'privacy' ? 'privacy' : x.j.fields[n]); }); }
        else generalErr.textContent = T['err_' + x.j.error] || T.err_generic;
      })
      .catch(function () { generalErr.textContent = T.err_network; })
      .then(function () { submit.disabled = false; submit.textContent = label; });
  });
})();
