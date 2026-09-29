"""Rebuild the curated fork. Python standard library only."""
import argparse, html, json, re, unicodedata, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = 'https://pmsdatabase.github.io/pmsdatabase/pmsdatabase_score.json'
SOURCE_PAGE = 'https://pmsdifficulty.xxxxxxxx.jp/PMSdifficulty.html'
def norm(value):
    return ''.join(c for c in unicodedata.normalize('NFKC', html.unescape(value)).casefold().replace('℟', 'r') if c.isalnum())
def matches(row, song):
    title = html.unescape(row['title'])
    # Remove chart annotations only, not arbitrary song-name suffixes.
    base = re.split(r'\s+[\[(]', title)[0]
    names = [song['name']] + song['aliases']
    title_match = any(norm(title) == norm(n) or norm(base) == norm(n) for n in names)
    if song['name'] == 'Alice in Misanthrope':
        title_match = title.casefold().startswith('alice in misanthrope -')
    return title_match and bool(re.search(song['artist'], row['artist'], re.I))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--refresh', action='store_true')
    parser.add_argument('--base-url', default='')
    args = parser.parse_args()
    snapshot = ROOT / 'source-normal.json'
    if args.refresh:
        with urllib.request.urlopen(SOURCE, timeout=45) as response:
            snapshot.write_bytes(response.read())
    rows = json.loads(snapshot.read_text(encoding='utf-8-sig'))
    normal_count = len(rows)
    supplements = json.loads((ROOT / 'supplemental-charts.json').read_text(encoding='utf-8'))
    for entry in supplements:
        original = entry['record']
        level = entry['level']
        assert original['comment'].endswith('→' + level), 'Supplement rating must be documented upstream'
        assert not any(row['md5'] == original['md5'] for row in rows), 'Supplement now exists in normal source; reconcile it'
        rows.append(dict(original, level=level,
                         comment=entry['chart'] + ' — ' + original['comment'] + ' · Excluded upstream for BGA gore; rating retained from source comment.',
                         source_url=entry['source_url'], source_category=original['level']))
    catalog = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8-sig'))
    allowed = {str(i) for i in range(1, 46)} | {'45+'}
    included, catalog_report, mapping = [], [], {}
    for song in catalog:
        found = [row for row in rows if matches(row, song) and str(row['level']) in allowed]
        for row in found:
            assert row['md5'] not in mapping, 'Chart matched more than one song'
            mapping[row['md5']] = song['name']
        included.extend(found)
        catalog_report.append(dict(song, count=len(found), levels=sorted({str(r['level']) for r in found}, key=lambda x: 46 if x == '45+' else int(x))))
    included.sort(key=lambda r: (46 if r['level'] == '45+' else int(r['level']), norm(r['title']), r['md5']))
    assert len({r['md5'] for r in included}) == len(included)
    assert all(r in rows for r in included)
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    base = args.base_url.rstrip('/')
    url = lambda name: base + '/' + name if base else name
    header = {'name':'Pump × PMS — Normal (1–45+)', 'symbol':'PIU Lv', 'data_url':url('data.json'), 'level_order':list(range(1,46))+['45+']}
    for filename, data in [('data.json',included),('header.json',header),('catalog-report.json',catalog_report)]:
        (dist / filename).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
    payload = {'rows':included,'catalog':catalog_report,'mapping':mapping,'source':SOURCE_PAGE,'snapshot':'2026-09-28','updated':'2026-09-29'}
    (dist / 'data.js').write_text('window.PMS_DATA = '+json.dumps(payload,ensure_ascii=False).replace('<','\\u003c')+';\n',encoding='utf-8')
    page = (ROOT / 'page.html').read_text(encoding='utf-8')
    (dist / 'index.html').write_text(page.replace('@@HEADER_URL@@',html.escape(url('header.json'),quote=True)),encoding='utf-8')
    summary = {'source_charts':normal_count,'supplemental_charts':len(supplements),'included_charts':len(included),'matched_songs':sum(bool(s['count']) for s in catalog_report),'checked_songs':len(catalog),'missing':[s['name'] for s in catalog_report if not s['count']]}
    (ROOT / 'build-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False))

if __name__ == '__main__':
    main()
