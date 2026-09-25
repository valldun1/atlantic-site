#!/usr/bin/env python3
import os, re, glob
from html.parser import HTMLParser

ROOT = "/tmp/atlantic-cron"
VOID = {"meta","link","img","br","hr","input","source","wbr","base","area","col","embed","track","param"}
IGNORE = {"script","style","svg"}

class DomCheck(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack=[]; self.errors=[]
    def handle_starttag(self,tag,attrs):
        if tag in VOID or tag in IGNORE: return
        self.stack.append(tag)
    def handle_startendtag(self,tag,attrs): pass
    def handle_endtag(self,tag):
        if tag in VOID or tag in IGNORE: return
        if self.stack and self.stack[-1]==tag: self.stack.pop()
        else:
            if tag in self.stack:
                while self.stack and self.stack[-1]!=tag: self.errors.append("unclosed:"+self.stack.pop())
                self.stack.pop()
            else: self.errors.append("stray:</"+tag+">")

def get(path,key):
    s=open(path,encoding="utf-8",errors="replace").read()
    m=re.search(key+r'\s*=\s*"([^"]*)"',s)
    return m.group(1) if m else None

pages=glob.glob(ROOT+"/*.html")+glob.glob(ROOT+"/routes/*.html")+glob.glob(ROOT+"/blog/*.html")+glob.glob(ROOT+"/posts/*.html")
pages=[p for p in pages if "google7d" not in p]
issues=[]
for p in sorted(pages):
    rel=os.path.relpath(p,ROOT)
    s=open(p,encoding="utf-8",errors="replace").read()
    # DOM
    d=DomCheck(); d.feed(s)
    if d.errors: issues.append(f"{rel}: DOM {d.errors[:3]}")
    # menu emoji
    for m in re.finditer(r'class="as-menu[^"]*"[^>]*>(.*?)</nav>',s,re.S):
        if re.search(r'[\U0001F300-\U0001FAFF\u2600-\u27BF]',m.group(1)): issues.append(f"{rel}: emoji in menu")
    # canonical
    if not re.search(r'<link[^>]*rel=["\']canonical["\']',s): issues.append(f"{rel}: no canonical")
    # one H1
    if len(re.findall(r'<h1\b',s,re.I))!=1: issues.append(f"{rel}: H1={len(re.findall(r'<h1\b',s,re.I))}")
    # title/description
    if not re.search(r'<title>',s): issues.append(f"{rel}: no title")
    if not get(p,'name="description"') and not get(p,"name='description'"): issues.append(f"{rel}: no description")
    # click_contact
    if "click_contact" not in s: issues.append(f"{rel}: no click_contact")
    # broken hrefs
    base=os.path.dirname(p)
    for h in re.findall(r'href="([^"#]+?\.html[^"]*)"',s):
        h2=h.split("#")[0]
        if h2.startswith("http") or h2.startswith("//"): continue
        tgt=os.path.normpath(os.path.join(base,h2))
        if not os.path.exists(tgt): issues.append(f"{rel}: broken {h}")
# routes view_route
for r in glob.glob(ROOT+"/routes/*.html"):
    s=open(r,encoding="utf-8").read()
    if "view_route" not in s: issues.append(os.path.relpath(r,ROOT)+": no view_route")
# sitemap routes
sm=open(ROOT+"/sitemap.xml",encoding="utf-8").read()
for r in glob.glob(ROOT+"/routes/*.html"):
    name=os.path.basename(r)
    if name not in sm: issues.append(f"sitemap missing {name}")
# tivat-rome 13 days
for p in glob.glob(ROOT+"/routes/*.html")+[ROOT+"/plan-2026.html"]:
    s=open(p,encoding="utf-8").read()
    if "Тиват" in s and "Рим" in s:
        if "13" not in s: issues.append(os.path.basename(p)+": tivat-rome no 13")
# plan-2026 prices
s=open(ROOT+"/plan-2026.html",encoding="utf-8").read()
for price in ["800","650","650","700"]:
    if price not in s: issues.append(f"plan-2026 missing {price}")
# captions
for p in glob.glob(ROOT+"/routes/*.html")+[ROOT+"/index.html"]:
    s=open(p,encoding="utf-8").read()
    if "иллюстративн" not in s: issues.append(os.path.relpath(p,ROOT)+": no caption")
print("FILES:",len(pages))
print("ISSUES:",len(issues))
for i in issues: print(" -",i)