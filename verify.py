#!/usr/bin/env python3
"""Fast TZ-audit verification for atlantic-site."""
import os, re, sys, glob
from html.parser import HTMLParser

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
SKIP = {'google7d00934345706795.html'}

class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors = [], []
    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)
    def handle_startendtag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        if tag in VOID: return
        if not self.stack:
            self.errors.append(f'extra </{tag}>'); return
        # pop until match (ignore mismatches as error)
        if self.stack[-1] == tag:
            self.stack.pop()
        else:
            if tag in self.stack:
                while self.stack and self.stack[-1] != tag:
                    self.errors.append(f'unclosed <{self.stack.pop()}>')
                self.stack.pop()
            else:
                self.errors.append(f'stray </{tag}>')

def check(fn):
    src = open(fn, encoding='utf-8', errors='replace').read()
    c = Checker(); c.feed(src)
    issues = list(c.errors)
    if c.stack: issues.append('unclosed at EOF: ' + ','.join(c.stack))
    return src, issues

files = sorted(glob.glob('*.html')) + sorted(glob.glob('routes/*.html')) + sorted(glob.glob('blog/*.html'))
files = [f for f in files if os.path.basename(f) not in SKIP]

bad = 0
for f in files:
    src, issues = check(f)
    if issues:
        bad += 1; print(f'DOM ERROR {f}: {issues}')

# broken links
broken = []
for f in files:
    src = open(f, encoding='utf-8', errors='replace').read()
    for m in re.finditer(r'href="([^"#]+?)(?:#[^"]*)?"', src):
        href = m.group(1)
        if href.startswith(('http','mailto:','tel:','/', 'data:')): continue
        if href.endswith('.html') or '/' in href:
            target = href.split('#')[0]
            if not os.path.exists(target): broken.append((f, href))

# menu emoji check
menu_bad = []
for f in files:
    src = open(f, encoding='utf-8', errors='replace').read()
    for m in re.finditer(r'<nav[^>]*>.*?</nav>', src, re.S):
        nav = m.group(0)
        if re.search(r'[\U0001F300-\U0001FAFF\u2600-\u27BF]', nav): menu_bad.append(f)

# per-file: canonical, h1 count, title, description, umami
miss = []
for f in files:
    src = open(f, encoding='utf-8', errors='replace').read()
    low = src.lower()
    if 'rel="canonical"' not in low: miss.append((f,'canonical'))
    if src.count('<h1') != 1: miss.append((f,f'h1x{src.count("<h1")}'))
    if '<title>' not in low: miss.append((f,'title'))
    if 'name="description"' not in low: miss.append((f,'description'))
    if 'click_contact' not in src: miss.append((f,'click_contact'))

vr = [f for f in glob.glob('routes/*.html') if os.path.basename(f) not in SKIP]
vr_miss = [f for f in vr if 'view_route' not in open(f, encoding='utf-8', errors='replace').read()]

# caption
cap_miss = [f for f in vr if 'Иллюстративное изображение' not in open(f, encoding='utf-8', errors='replace').read()]

# plan-2026 prices
p = open('plan-2026.html', encoding='utf-8').read()
prices = re.findall(r'(\d{3,4})\s*€', p)
price_ok = ('800' in re.findall(r'800', p)) and ('650' in p) and ('700' in p)

# tivat-rim dates
tr_ok = '2026-09-15' in open('routes/rim-2026.html', encoding='utf-8').read() if os.path.exists('routes/rim-2026.html') else None

print(f'files={len(files)} dom_bad={bad} broken={broken} menu_emoji={menu_bad}')
print(f'page_miss={miss} view_route_miss={vr_miss} cap_miss={cap_miss}')
print(f'plan2026_has_800_650_700={price_ok} tivat_rim_ok={tr_ok}')
sm = open('sitemap.xml', encoding='utf-8').read()
print(f'sitemap_routes={sum(1 for r in glob.glob("routes/*.html") if r.split("/")[-1] in sm)}')