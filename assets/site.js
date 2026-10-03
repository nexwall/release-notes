(function () {
  'use strict';
  var root = document.documentElement;

  function store(key, value) { try { localStorage.setItem(key, value); } catch (e) { /* storage may be blocked */ } }

  // theme toggle: light, dark, or follow the system
  var themeBtn = document.getElementById('theme');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var current = root.getAttribute('data-theme');
      var dark = current ? current === 'dark' : window.matchMedia('(prefers-color-scheme: dark)').matches;
      var next = dark ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      store('nx-theme', next);
    });
  }

  // remember the chosen language
  document.querySelectorAll('.lang .menu a').forEach(function (a) {
    a.addEventListener('click', function () { store('nx-lang', a.getAttribute('hreflang') + '/'); });
  });

  // version selector
  var ver = document.getElementById('ver');
  if (ver) {
    ver.addEventListener('change', function () { location.href = ver.getAttribute('data-base') + ver.value + '/'; });
  }

  // filter the items by type
  var chips = document.querySelectorAll('.chip');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      var f = chip.getAttribute('data-filter');
      chips.forEach(function (c) { c.classList.toggle('on', c === chip); });
      document.querySelectorAll('.item').forEach(function (item) {
        item.hidden = f !== 'all' && item.getAttribute('data-tag') !== f;
      });
    });
  });

  // copy a checksum
  document.querySelectorAll('.copy').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var el = document.getElementById(btn.getAttribute('data-copy'));
      if (!el || !navigator.clipboard) { return; }
      var label = btn.textContent;
      navigator.clipboard.writeText(el.textContent.trim()).then(function () {
        btn.textContent = btn.getAttribute('data-done');
        setTimeout(function () { btn.textContent = label; }, 1500);
      });
    });
  });

  // highlight the section being read in the table of contents
  var links = document.querySelectorAll('.toc a');
  if (links.length && 'IntersectionObserver' in window) {
    var byId = {};
    links.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          links.forEach(function (a) { a.classList.remove('on'); });
          if (byId[e.target.id]) { byId[e.target.id].classList.add('on'); }
        }
      });
    }, { rootMargin: '-80px 0px -70% 0px' });
    document.querySelectorAll('.doc section[id]').forEach(function (s) { observer.observe(s); });
  }
})();
