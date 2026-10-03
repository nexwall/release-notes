#!/usr/bin/env python3
"""Builds the static release-notes site (site/) from content/. No dependencies.

    python3 build.py            # writes ./site
    SITE_URL=https://example.org/releases python3 build.py   # also writes sitemap.xml with absolute URLs

Content:
    content/ui.json                      interface strings per language
    content/releases.json                list of releases (newest first): version, date, status, downloads
    content/<version>/<lang>.json        the release notes of one version in one language
"""
import json
import os
import shutil
import sys
from html import escape as esc

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'site')
LANGS = [('en', 'English'), ('es', 'Español'), ('pt-BR', 'Português (Brasil)')]
TAGS = ['new', 'improved', 'changed', 'fixed']


def load(*parts):
    with open(os.path.join(ROOT, *parts), encoding='utf-8') as f:
        return json.load(f)


def write(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def up(depth):
    return '../' * depth if depth else './'


def paragraphs(text):
    return ''.join('<p>%s</p>' % esc(p) for p in text.split('\n\n') if p.strip())


def shell(lang, ui, title, body, depth, here, nav_extra=''):
    """here: path of this page below the language folder ('' for the language home, '26.0.0-rc1/' for a release)."""
    base = up(depth)
    langs = ''.join(
        '<a href="%s%s/%s" hreflang="%s"%s>%s</a>' % (base, code, here, code, ' aria-current="true"' if code == lang else '', esc(name))
        for code, name in LANGS)
    return '''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{base}assets/style.css">
<script>try{{var t=localStorage.getItem('nx-theme');if(t)document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
</head>
<body>
<a class="skip" href="#main">{skip}</a>
<header class="top">
  <div class="top-in">
    <a class="brand" href="{base}{lang}/"><span class="mark" aria-hidden="true"></span><span>Nexwall <b>{site}</b></span></a>
    <nav class="top-nav" aria-label="{site}">
      <a href="{base}{lang}/">{all}</a>
      {nav_extra}
    </nav>
    <div class="top-tools">
      <details class="lang"><summary>{language}</summary><div class="menu">{langs}</div></details>
      <button class="icon-btn" id="theme" type="button" aria-label="{theme}" title="{theme}">&#9680;</button>
    </div>
  </div>
</header>
{body}
<footer class="foot"><div class="foot-in"><span>{footer}</span><span>&copy; Nexwall</span></div></footer>
<script src="{base}assets/site.js"></script>
</body>
</html>
'''.format(lang=lang, title=esc(title), desc=esc(ui['meta_description']), base=base, skip=esc(ui['skip']), site=esc(ui['site']),
           all=esc(ui['all_releases']), nav_extra=nav_extra, language=esc(ui['language']), langs=langs, theme=esc(ui['theme']),
           body=body, footer=esc(ui['footer']))


def status_badge(ui, status):
    return '<span class="status status-%s">%s</span>' % (esc(status), esc(ui['status_' + status]))


def release_card(lang, ui, rel, note, depth):
    return '''<a class="card release" href="{base}{lang}/{ver}/">
  <div class="card-top"><span class="ver">{ver}</span>{badge}</div>
  <h3>{title}</h3>
  <p>{summary}</p>
  <div class="card-meta"><span>{date_label}: <time datetime="{date}">{date}</time></span></div>
</a>'''.format(base=up(depth), lang=lang, ver=esc(rel['version']), badge=status_badge(ui, rel['status']), title=esc(note['title']),
               summary=esc(note['summary']), date_label=esc(ui['release_date']), date=esc(rel['date']))


def build_home(lang, ui, releases, notes):
    latest = releases[0]
    cards = ''.join(release_card(lang, ui, r, notes[r['version']], 1) for r in releases)
    body = '''<main id="main">
<section class="hero"><div class="wrap">
  <p class="eyebrow">{eyebrow}</p>
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>
  <p><a class="btn" href="{latest}/">{latest_label}: {latest}</a></p>
</div></section>
<section class="wrap"><h2>{all}</h2><div class="grid">{cards}</div></section>
</main>'''.format(eyebrow=esc(ui['eyebrow']), h1=esc(ui['home_title']), lead=esc(ui['home_lead']), latest=esc(latest['version']),
                  latest_label=esc(ui['latest']), all=esc(ui['all_releases']), cards=cards)
    write('%s/index.html' % lang, shell(lang, ui, '%s | Nexwall' % ui['home_title'], body, 1, ''))


def render_item(ui, item):
    tag = item.get('tag', 'new')
    bullets = ''
    if item.get('bullets'):
        bullets = '<ul>%s</ul>' % ''.join('<li>%s</li>' % esc(b) for b in item['bullets'])
    note = ''
    if item.get('note'):
        note = '<p class="note">%s</p>' % esc(item['note'])
    return '''<article class="item" data-tag="{tag}">
  <header><span class="tag tag-{tag}">{tag_label}</span><h3>{title}</h3></header>
  {body}{bullets}{note}
</article>'''.format(tag=esc(tag), tag_label=esc(ui['tag_' + tag]), title=esc(item['title']), body=paragraphs(item['body']), bullets=bullets, note=note)


def render_downloads(ui, rel):
    rows = rel.get('downloads') or []
    if not rows:
        return '<p class="note">%s</p>' % esc(ui['downloads_pending'])
    out = ['<div class="table-wrap"><table><thead><tr><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>' % (esc(ui['file']), esc(ui['size']), esc(ui['checksum']))]
    for d in rows:
        out.append('<tr><td><code>%s</code></td><td>%s</td><td><code class="hash" id="h-%s">%s</code> <button type="button" class="copy" data-copy="h-%s" data-done="%s">%s</button></td></tr>'
                   % (esc(d['name']), esc(d['size']), esc(d['name']), esc(d['sha256']), esc(d['name']), esc(ui['copied']), esc(ui['copy'])))
    out.append('</tbody></table></div>')
    out.append('<p class="hint">%s</p>' % esc(ui['verify_hint']))
    return ''.join(out)


def build_release(lang, ui, rel, note, releases):
    ver = rel['version']
    toc, parts = [], []

    def section(sid, title, inner):
        toc.append((sid, title))
        parts.append('<section id="%s"><h2>%s</h2>%s</section>' % (sid, esc(title), inner))

    glance = ''.join('<div class="fact"><dt>%s</dt><dd>%s</dd></div>' % (esc(f['label']), esc(f['value'])) for f in note['at_a_glance'])
    section('overview', ui['overview'], paragraphs(note['overview']) + '<dl class="facts">%s</dl>' % glance)
    for sec in note['sections']:
        intro = paragraphs(sec['intro']) if sec.get('intro') else ''
        section(sec['id'], sec['title'], intro + ''.join(render_item(ui, i) for i in sec['items']))
    comp = note['components']
    rows = ''.join('<tr><td>%s</td><td><code>%s</code></td><td>%s</td></tr>' % (esc(c['name']), esc(c['version']), esc(c['note'])) for c in comp['rows'])
    section('components', ui['components'], paragraphs(comp['intro']) + '<div class="table-wrap"><table><thead><tr><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table></div>' % (
        esc(ui['col_component']), esc(ui['version']), esc(ui['col_notes']), rows))
    tl = note['timeline']
    entries = ''.join('<li><time>%s</time><div><h3>%s</h3><p>%s</p></div></li>' % (esc(e['date']), esc(e['title']), esc(e['text'])) for e in tl['entries'])
    section('release-track', ui['timeline'], paragraphs(tl['intro']) + '<ol class="timeline">%s</ol>' % entries)
    issues = ''.join('<article class="item" data-tag="known"><header><span class="tag tag-known">%s</span><h3>%s</h3></header>%s%s</article>' % (
        esc(ui['tag_known']), esc(k['title']), paragraphs(k['body']),
        ('<p class="note"><b>%s</b> %s</p>' % (esc(ui['workaround']), esc(k['workaround']))) if k.get('workaround') else '') for k in note['known_issues'])
    section('known-issues', ui['known_issues'], issues)
    req = '<ul>%s</ul>' % ''.join('<li>%s</li>' % esc(r) for r in note['requirements'])
    section('requirements', ui['requirements'], req)
    upg = '<ul>%s</ul>' % ''.join('<li>%s</li>' % esc(r) for r in note['upgrade'])
    section('upgrade', ui['upgrade'], upg)
    section('downloads', ui['downloads'], render_downloads(ui, rel))
    section('open-source', ui['open_source'], paragraphs(note['open_source']))

    toc_html = ''.join('<li><a href="#%s">%s</a></li>' % (sid, esc(t)) for sid, t in toc)
    filters = '<div class="filters" role="group" aria-label="%s"><button type="button" class="chip on" data-filter="all">%s</button>%s</div>' % (
        esc(ui['filter']), esc(ui['filter_all']), ''.join('<button type="button" class="chip" data-filter="%s">%s</button>' % (t, esc(ui['tag_' + t])) for t in TAGS + ['known']))
    others = ''.join('<option value="%s"%s>%s</option>' % (esc(r['version']), ' selected' if r['version'] == ver else '', esc(r['version'])) for r in releases)
    selector = '<label class="ver-select"><span>%s</span><select id="ver" data-base="../">%s</select></label>' % (esc(ui['version']), others)
    body = '''<div class="release-head"><div class="wrap">
  <p class="crumbs"><a href="../">{all}</a> / {ver}</p>
  <h1>{title}</h1>
  <p class="lead">{summary}</p>
  <p class="meta">{badge} <span>{date_label}: <time datetime="{date}">{date}</time></span> {selector}</p>
</div></div>
<div class="wrap layout">
  <aside class="toc" aria-label="{on_page}"><p class="toc-title">{on_page}</p><ol>{toc}</ol></aside>
  <main id="main" class="doc">
    {filters}
    {parts}
  </main>
</div>'''.format(all=esc(ui['all_releases']), ver=esc(ver), title=esc(note['title']), summary=esc(note['summary']), badge=status_badge(ui, rel['status']),
                 date_label=esc(ui['release_date']), date=esc(rel['date']), selector=selector, on_page=esc(ui['on_this_page']), toc=toc_html,
                 filters=filters, parts=''.join(parts))
    write('%s/%s/index.html' % (lang, ver), shell(lang, ui, '%s | Nexwall' % note['title'], body, 2, '%s/' % ver))


def main():
    uis = load('content', 'ui.json')
    releases = load('content', 'releases.json')
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, 'assets'), os.path.join(OUT, 'assets'))
    if os.path.isfile(os.path.join(ROOT, 'CNAME')):
        shutil.copy(os.path.join(ROOT, 'CNAME'), os.path.join(OUT, 'CNAME'))
    write('.nojekyll', '')
    urls = []
    for lang, _ in LANGS:
        ui = uis[lang]
        notes = {r['version']: load('content', r['version'], '%s.json' % lang) for r in releases}
        build_home(lang, ui, releases, notes)
        urls.append('%s/' % lang)
        for rel in releases:
            build_release(lang, ui, rel, notes[rel['version']], releases)
            urls.append('%s/%s/' % (lang, rel['version']))
    write('index.html', '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nexwall release notes</title>
<link rel="stylesheet" href="assets/style.css">
<script>
(function () {
  var map = {en: 'en/', es: 'es/', pt: 'pt-BR/'};
  var l = (navigator.language || 'en').slice(0, 2).toLowerCase();
  var saved = null;
  try { saved = localStorage.getItem('nx-lang'); } catch (e) {}
  location.replace(saved || map[l] || 'en/');
})();
</script></head>
<body><main class="wrap" style="padding:3rem 0"><h1>Nexwall release notes</h1>
<p><a href="en/">English</a> &middot; <a href="es/">Español</a> &middot; <a href="pt-BR/">Português (Brasil)</a></p></main></body></html>
''')
    write('404.html', shell('en', uis['en'], 'Page not found | Nexwall', '<main id="main" class="wrap" style="padding:3rem 0"><h1>404</h1><p><a href="/">Nexwall release notes</a></p></main>', 0, ''))
    site_url = os.environ.get('SITE_URL', '').rstrip('/')
    if site_url:
        write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n'
              % ''.join('<url><loc>%s/%s</loc></url>\n' % (site_url, u) for u in urls))
        write('robots.txt', 'User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n' % site_url)
    print('built %d pages into %s' % (len(urls) + 2, OUT))


if __name__ == '__main__':
    sys.exit(main())
