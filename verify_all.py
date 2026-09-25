#!/usr/bin/env python3
"""Comprehensive ТЗ verification for Atlantic Sail site."""
import os, re, glob, sys
from html.parser import HTMLParser

ROOT = '/tmp/atlantic-cron'
VOID = {'meta','link','img','br','hr','input','source','area','base','col','embed','track','wbr'}
IGNORED_UNBALANCED = {'meta','link','img','br','hr','input','source','area','base','col','embed','track','wbr'}

class DomCheck(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)
    def handle_startendtag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.errors.append(f'unclosed <{self.stack.pop()}>')
            if self.stack:
                self.stack.pop()
        else:
            self.errors.append(f'stray </{tag}>')

pages = sorted([f for f in glob.glob(ROOT + '/*.html')])
routes = sorted(glob.glob(ROOT + '/routes/*.html'))
all_pages = pages + routes
print(f'HTML files: {len(all_pages)} (root {len(pages)}, routes {len(routes)})')

menu_emojis = []
h1_count = []
no_canonical = []
no_title = []
no_desc = []
no_click = []
no_viewroute = []
broken = []
dom_errors = 0

for p in all_pages:
    name = os.path.basename(p)
    if name.startswith('google'):
        continue
    html = open(p, encoding='utf-8').read()
    # DOM balance
    d = DomCheck()
    d.feed(html)
    dom_errors += len(d.errors)
    # menu: find nav containing 5 items
    navs = re.findall(r'<nav[^>]*>(.*?)</nav>', html, re.S)
    for nav in navs:
        for m in re.findall(r'[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF]', nav):
            menu_emojis.append((name, m))
    # H1
    h1s = re.findall(r'<h1[^>]*>', html)
    if len(h1s) != 1:
        h1_count.append((name, len(h1s)))
    # canonical
    if not re.search(r'<link[^>]*rel=["\']canonical["\']', html):
        no_canonical.append(name)
    # title / description
    if not re.search(r'<title[^>]*>.*?</title>', html, re.S):
        no_title.append(name)
    if not re.search(r'<meta[^>]*name=["\']description["\']', html):
        no_desc.append(name)
    # umami click_contact
    if 'click_contact' not in html:
        no_click.append(name)
    # umami view_route on routes
    if p in routes and 'view_route' not in html:
        no_viewroute.append(name)
    # broken links: relative hrefs ending .html / .zip / .webp / .png / .jpg
    for m in re.finditer(r'href=["\']([^"\']+)["\']', html):
        href = m.group(1)
        if href.startswith(('http://','https://','mailto:','tel:','#','javascript:','data:')):
            continue
        if '://' in href:
            continue
        target = os.path.normpath(os.path.join(os.path.dirname(p), href.split('#')[0].split('?')[0]))
        if not os.path.exists(target):
            broken.append((name, href))

print('---')
print('DOM errors:', dom_errors)
print('menu emoji violations:', menu_emojis if menu_emojis else '0')
print('pages with !=1 H1:', h1_count if h1_count else '0')
print('no canonical:', no_canonical if no_canonical else '0')
print('no title:', no_title if no_title else '0')
print('no description:', no_desc if no_desc else '0')
print('no click_contact:', no_click if no_click else '0')
print('routes missing view_route:', no_viewroute if no_viewroute else '0')
print('broken links:', broken if broken else '0')

# captions
cap = []
for p in routes + [ROOT + '/index.html']:
    html = open(p, encoding='utf-8').read()
    if 'Иллюстративное изображение' not in html:
        # check alt too
        if 'иллюстративное' not in html.lower():
            cap.append(os.path.basename(p))
print('routes/index missing caption:', cap if cap else '0')

# Тиват→Рим 13 days
tivat = []
for p in all_pages:
    html = open(p, encoding='utf-8').read()
    if 'Тиват' in html and 'Рим' in html:
        ok = ('13 дней' in html)
        tivat.append((os.path.basename(p), 'OK' if ok else 'CHECK'))
print('Тиват→Рим pages:', tivat)

# plan-2026 prices
plan = open(ROOT + '/plan-2026.html', encoding='utf-8').read()
for price in ['800', '650', '650', '700']:
    pass
prices = re.findall(r'(\d{3,4})\s*€', plan)
print('plan-2026 mentions €:', prices[:20], '...')

# sitemap routes
sm = open(ROOT + '/sitemap.xml', encoding='utf-8').read()
sm_missing = [r for r in routes if os.path.basename(r) not in sm]
print('sitemap missing routes:', sm_missing if sm_missing else '0')

# form honest text
for p in all_pages:
    html = open(p, encoding='utf-8').read()
    if 'sendRequest' in html or ('WhatsApp' in html and 'Отрoется' in html) or 'Откроется WhatsApp' in html:
        pass
form_ok = 0
for p in all_pages:
    html = open(p, encoding='utf-8').read()
    if 'Откроется WhatsApp' in html or 'Продолжить в WhatsApp' in html:
        form_ok += 1
print('pages with honest WhatsApp text:', form_ok)