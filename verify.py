#!/usr/bin/env python3
import glob, re, os, html.parser

VOID={'meta','link','img','br','hr','input','source','area','base','col','embed','param','track','wbr'}
IGNORE={'title','svg','path','noscript','em','style','script','select','option','button'}

class Checker(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[]; self.h1=0; self.canonical=0; self.title=0; self.desc=0
        self.a_hrefs=[]; self.errors=[]
    def _link(self,tag,attrs):
        d=dict(attrs)
        if tag=='link' and d.get('rel')=='canonical': self.canonical+=1
        if tag=='meta' and d.get('name')=='description': self.desc+=1
        if tag=='title': self.title+=1
    def handle_starttag(self,tag,attrs):
        if tag in VOID or tag in IGNORE: 
            if tag in ('link','meta','title'): self._link(tag,attrs)
            return
        self.stack.append(tag)
        if tag=='h1': self.h1+=1
        if tag=='a' and dict(attrs).get('href'): self.a_hrefs.append(dict(attrs)['href'])
    def handle_startendtag(self,tag,attrs):
        if tag in ('link','meta','title'): self._link(tag,attrs)
    def handle_endtag(self,tag):
        if tag in VOID or tag in IGNORE: return
        if self.stack and self.stack[-1]==tag: self.stack.pop()
        else: self.errors.append(f"</{tag}> vs {self.stack[-3:]}")

html_files = sorted(glob.glob('/tmp/atlantic-cron/*.html') + glob.glob('/tmp/atlantic-cron/routes/*.html') + glob.glob('/tmp/atlantic-cron/blog/*.html') + glob.glob('/tmp/atlantic-cron/posts/*.html'))
res={}
for f in html_files:
    c=Checker(); c.feed(open(f,encoding='utf-8',errors='replace').read()); c.close()
    res[os.path.basename(f)]=(c,f)

issues=[]
for name,(c,f) in res.items():
    if 'google7d' in name: continue
    if c.errors: issues.append(f"{name}: DOM {c.errors[:3]}")
    if c.h1!=1: issues.append(f"{name}: H1={c.h1}")
    if c.canonical!=1: issues.append(f"{name}: canonical={c.canonical}")
    if c.title!=1: issues.append(f"{name}: title={c.title}")
    if c.desc!=1: issues.append(f"{name}: desc={c.desc}")
    txt=open(f,encoding='utf-8',errors='replace').read()
    if 'click_contact' not in txt: issues.append(f"{name}: no click_contact")

for name,(c,f) in res.items():
    txt=open(f,encoding='utf-8',errors='replace').read()
    if '/routes/' in f:
        if 'view_route' not in txt: issues.append(f"{name}: no view_route")
    m=re.search(r'<nav[^>]*class="[^"]*as-menu[^"]*"[^>]*>(.*?)</nav>', txt, re.S)
    if m:
        seg=m.group(1)
        for item in ['Ближайшие переходы','Яхты','Капитаны','Как это устроено','Контакты']:
            if item not in seg: issues.append(f"{name}: menu missing {item}")
        em=re.findall(r'[\U0001F300-\U0001FAFF\u2600-\u27BF]', seg)
        if em: issues.append(f"{name}: emoji in menu {em}")

for name,(c,f) in res.items():
    for h in c.a_hrefs:
        if h.startswith(('http','mailto:','tel:','#','data:')): continue
        p=h.split('#')[0].split('?')[0]
        if not p: continue
        t1=os.path.normpath(os.path.join(os.path.dirname(f),p))
        t2=os.path.normpath('/tmp/atlantic-cron/'+p.lstrip('/'))
        if not os.path.exists(t1) and not os.path.exists(t2): issues.append(f"{name}: broken {h}")

print("FILES:", len(html_files))
print("ISSUES:" if issues else "ALL OK")
[print(" -",i) for i in issues]
sm=open('/tmp/atlantic-cron/sitemap.xml',encoding='utf-8').read()
print("sitemap routes:", len(re.findall(r'<loc>[^<]*routes[^<]*</loc>', sm)))
# tivat-rome dates
t=open('/tmp/atlantic-cron/routes/tivat-rome.html',encoding='utf-8').read()
m=re.findall(r'(\d{1,2}\s*[–-]\s*\d{1,2}\s*[а-я]+|\d{1,2}\s+[а-я]+\w*\s*[–-]\s*\d{1,2}\s+[а-я]+\w*)', t)
print("tivat dates:", m[:3])