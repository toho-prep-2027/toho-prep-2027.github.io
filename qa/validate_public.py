#!/usr/bin/env python3
"""Fail-closed syntax, schema, and privacy gate for published assets.
Semantic review remains a separate required release check; heuristic filters are not a guarantee.
"""
import json, re, pathlib, sys, hashlib, urllib.parse
P=pathlib.Path(__file__).resolve().parents[1]
C=P/'content'/'public-data.json'
SITE=P/'index.html'
assert C.exists() and SITE.exists(),'required public files missing'
data=json.loads(C.read_text(encoding='utf8'))
assert set(data)=={'schema','asOf','school','examWindow','menu','days','evidence','priority','research','sources','years','domainMatrix','philosophy','predictions','redteam','privacy'},'unexpected public keys'
assert data['schema']=='toho-app-content-v1.1' and data['privacy']=='public-generic-only; no personal data'
assert len(data['menu'])==12 and len(data['days'])==25 and len(data['research'])==12
assert sorted(x['id'] for x in data['menu'])==sorted('M'+str(i) for i in range(1,13))
assert sorted([x[0] for x in data['research']])==list('ABCDEFGHIJKL')
required_menu={'id','name','priority','minutes','domain','relation','things','say','steps','watch','help','transfer','avoid','next','kind','provenance'}
for x in data['menu']:
 assert set(x)==required_menu,'menu schema mismatch'
 assert x['priority'] in ('P1','P2','P3')
 assert isinstance(x['minutes'],int) and 0<x['minutes']<=10
 assert len(x['steps'])>=2 and x['provenance'].startswith('E｜独自設計')
for x in data['days']:
 assert set(x)=={'date','phase','menu','minutes','title','goal','materials','watch','notes'}
 assert re.fullmatch(r'2026-(10|11)-\d\d',x['date'])
 assert x['menu'] is None or x['menu'] in {m['id'] for m in data['menu']}
assert data['years']==list(range(2017,2027))
for source in data['sources']:
 url=urllib.parse.urlparse(source['url'])
 assert url.scheme=='https' and url.hostname in {'shogakko.toho.ac.jp','educationendowmentfoundation.org.uk'}
raw=SITE.read_text(encoding='utf8')
# Scan content shipped to the public repository and the deploy artifact.
# Do not embed actual family names, identifiers, or private values in this public CI.
check_texts={p: (P/p).read_text(encoding='utf8') for p in [
 'index.html', 'content/public-data.json', 'README.md',
 'sw.js', 'offline.appcache', '.github/workflows/qa.yml']}

assert 'var BUILTIN_FAMILY=null' in raw and '__DATA__' not in raw and '__FAMILY__' not in raw
# Generic patterns identify risk without disclosing any known private values.
for p, value in check_texts.items():
 for ptn in [
   r'AKIA[0-9A-Z]{16}',
   r'(?i)-----BEGIN.{0,40}PRIVATE KEY',
   r'(?i)(?:password|api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*["\\\']',
   r'(?<!\d)\d{10,13}(?!\d)',
   r'(?i)[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}',
   r'受験番号\s*[:：]?\s*[0-9A-Za-z-]+',
   r'学籍番号\s*[:：]?\s*[0-9A-Za-z-]+',
   r'郵便追跡\s*[:：]?\s*\d+',
 ]:
  assert not re.search(ptn,value),f'sensitive-looking content in {p}'
assert 'function snapshotStatus(dt)' in raw and 'function recommend(day)' in raw
assert sorted(p.name for p in P.iterdir() if p.is_file() and p.name not in {'README.md'})==['.nojekyll','icon.png','index.html','offline.appcache','sw.js']
# Home-screen icon: PNG, 180x180, RGB without alpha (iOS 10 paints transparency black).
png=(P/'icon.png').read_bytes()
assert png[:8]==b'\x89PNG\r\n\x1a\n' and png[12:16]==b'IHDR','icon.png is not a PNG'
assert int.from_bytes(png[16:20],'big')==180 and int.from_bytes(png[20:24],'big')==180,'icon.png must be 180x180'
assert png[24]==8 and png[25]==2,'icon.png must be 8-bit RGB without alpha'
assert '<link rel="apple-touch-icon" sizes="180x180" href="icon.png">' in raw
# The embedded app data must be exactly the reviewed public data file.
m=re.search(r'^var PUBLIC_DATA=(\{.*\});$',raw,re.M)
assert m and json.loads(m.group(1))==data,'embedded PUBLIC_DATA differs from content/public-data.json'
print('PUBLIC_DATA_GATE_PASS',len(data['menu']),'menus',len(data['days']),'days',hashlib.sha256(SITE.read_bytes()).hexdigest())
