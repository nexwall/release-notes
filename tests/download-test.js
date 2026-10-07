// Runs assets/download.js against a stub DOM and a fake API. Usage: node tests/download-test.js
const vm = require('vm'), fs = require('fs'), path = require('path');
const js = fs.readFileSync(path.join(__dirname, '..', 'assets', 'download.js'), 'utf8');
const T = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'content', 'ui.json'), 'utf8'))['pt-BR'].dl;
let fail = 0;
const ok = (c, m) => { if (!c) { console.log('FAIL', m); fail++; } else console.log('ok  ', m); };

function el(extra) { return Object.assign({ hidden: false, textContent: '', children: [], appendChild(c) { this.children.push(c); }, setAttribute() {}, getAttribute(n) { return (this.attrs || {})[n]; } }, extra || {}); }
function run(responses) {
  const err = {}, byId = {};
  const names = ['first_name', 'last_name', 'company', 'email', 'phone', 'privacy', 'contact_ok', 'website'];
  const elements = {};
  names.forEach(n => elements[n] = { value: '', checked: false });
  const form = el({ hidden: true, attrs: { 'data-api': 'https://api.test/api/downloads', 'data-version': '26.1.0', 'data-lang': 'pt-BR' }, elements, listeners: {},
    addEventListener(t, f) { this.listeners[t] = f; }, querySelector(sel) { const m = /data-err="([^"]+)"/.exec(sel); return (err[m[1]] = err[m[1]] || el()); },
    querySelectorAll() { return Object.values(err); } });
  ['dl-file', 'dl-ready', 'dl-unavailable', 'dl-submit', 'dl-error', 'dl-link'].forEach(i => byId[i] = el({ hidden: true }));
  byId['dl-submit'] = el({ textContent: 'Continuar', disabled: false });
  byId['dl-i18n'] = el({ textContent: JSON.stringify(T) });
  byId['dl-form'] = form;
  const calls = [];
  const location = { href: '' };
  const ctx = { document: { getElementById: id => byId[id], createElement: () => el() }, window: { location }, location,
    fetch: (url, opt) => { calls.push({ url, opt }); const r = responses.shift(); return Promise.resolve({ ok: r.status < 400, status: r.status, json: () => Promise.resolve(r.body) }); },
    setTimeout: (f) => { ctx.timer = f; return 1; }, console, JSON, encodeURIComponent };
  vm.createContext(ctx);
  vm.runInContext(js, ctx);
  return { ctx, form, err, byId, calls, elements, location };
}
const tick = () => new Promise(r => setImmediate(r));
const REL = { ok: true, t: 'tok', release: { version: '26.1.0', files: [{ name: 'a.img.gz', size: 2048, sha256: 'ab'.repeat(32) }] } };

(async () => {
  // init failure: the release is not available
  let s = run([{ status: 404, body: { ok: false, error: 'unknown_version' } }]); await tick(); await tick();
  ok(s.byId['dl-unavailable'].hidden === false && s.form.hidden === true, 'unknown version: the form stays hidden, the message shows');

  // init ok: the form and the file details show
  s = run([{ status: 200, body: REL }]); await tick(); await tick();
  ok(s.form.hidden === false && s.byId['dl-file'].hidden === false && s.byId['dl-file'].children.length === 2, 'the form and the file name, size and SHA-256 show');
  ok(s.calls[0].url === 'https://api.test/api/downloads/init?version=26.1.0', 'init asks for the version');

  // client side validation: nothing is sent
  const ev = { preventDefault() {} };
  s.form.listeners.submit(ev); await tick();
  ok(s.calls.length === 1 && s.err.first_name.textContent === T.err_required && s.err.privacy.textContent === T.err_privacy, 'empty form: required messages , no request');
  Object.assign(s.elements.first_name, { value: 'Ana' }); s.elements.last_name.value = 'Souza'; s.elements.company.value = 'Acme'; s.elements.email.value = 'not-mail'; s.elements.phone.value = '+55 11 99999-0000'; s.elements.privacy.checked = true;
  s.form.listeners.submit(ev); await tick();
  ok(s.calls.length === 1 && s.err.email.textContent === T.err_invalid, 'bad email: invalid message, no request');

  // success: the link and the redirect
  s.elements.email.value = 'ana@acme.com.br'; s.elements.phone.value = ''; s.elements.contact_ok.checked = true;
  s.calls.length = 0;
  const s2 = run([{ status: 200, body: REL }, { status: 200, body: { ok: true, url: 'https://files.test/get/xyz', file: REL.release.files[0] } }]); await tick(); await tick();
  Object.assign(s2.elements.first_name, { value: 'Ana' }); s2.elements.last_name.value = 'Souza'; s2.elements.company.value = 'Acme'; s2.elements.email.value = 'ana@acme.com.br'; s2.elements.phone.value = '+55 11 99999-0000';
  s2.elements.privacy.checked = true; 
  s2.form.listeners.submit(ev); await tick(); await tick();
  const sent = JSON.parse(s2.calls[1].opt.body);
  ok(sent.email === 'ana@acme.com.br' && sent.privacy === true && sent.t === 'tok' && sent.version === '26.1.0' && sent.lang === 'pt-BR', 'the request carries the fields, the consents, the timer and the language');
  ok(s2.byId['dl-ready'].hidden === false && s2.form.hidden === true && s2.byId['dl-link'].href === 'https://files.test/get/xyz', 'success: the ready panel with the link');
  s2.ctx.timer(); ok(s2.location.href === 'https://files.test/get/xyz', 'the download starts by itself');
  ok(s2.byId['dl-submit'].disabled === false, 'the button is enabled again');

  // server errors
  const s3 = run([{ status: 200, body: REL }, { status: 429, body: { ok: false, error: 'rate_limited' } }]); await tick(); await tick();
  Object.assign(s3.elements.first_name, { value: 'A' }); s3.elements.last_name.value = 'B'; s3.elements.company.value = 'C'; s3.elements.email.value = 'a@b.co'; s3.elements.phone.value = '11 3333-4444'; s3.elements.privacy.checked = true;
  s3.form.listeners.submit(ev); await tick(); await tick();
  ok(s3.byId['dl-error'].textContent === T.err_rate_limited && s3.byId['dl-ready'].hidden === true, 'rate limit: its message, no download');
  const s4 = run([{ status: 200, body: REL }, { status: 422, body: { ok: false, error: 'validation', fields: { email: 'invalid', privacy: 'required' } } }]); await tick(); await tick();
  Object.assign(s4.elements.first_name, { value: 'A' }); s4.elements.last_name.value = 'B'; s4.elements.company.value = 'C'; s4.elements.email.value = 'a@b.co'; s4.elements.phone.value = '11 3333-4444'; s4.elements.privacy.checked = true;
  s4.form.listeners.submit(ev); await tick(); await tick();
  ok(s4.err.email.textContent === T.err_invalid && s4.err.privacy.textContent === T.err_privacy, 'field errors of the server show next to the fields');

  // every message the script can ask for exists in the three languages
  const all = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'content', 'ui.json'), 'utf8'));
  for (const l of ['en', 'es', 'pt-BR']) for (const k of ['err_required', 'err_invalid', 'err_privacy', 'err_rate_limited', 'err_form_expired', 'err_too_fast', 'err_unknown_version', 'err_network', 'err_generic', 'sending', 'questions'])
    ok(all[l].dl[k], l + ': ' + k);
  console.log(fail ? '\n' + fail + ' FAILED' : '\nALL PASSED'); process.exit(fail ? 1 : 0);
})();
