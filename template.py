#!/usr/bin/env python3
"""
Atlantic Sail — Template Builder
Extracts content from Wix HTML and wraps in new design
"""
from bs4 import BeautifulSoup
import os, re

TG_BOT = "https://t.me/captainatlanticbot"
SITE = "https://atlanticsail.net"
WA = "https://wa.me/+34605675361"
PHONE1 = "+34 605-675-361"
PHONE2 = "+7(903)55-00-654"
EMAIL = "info@atlanticsail.net"
YT = "https://youtube.com/@capitankosta"
IG = "https://www.instagram.com/capitankosta/"

NAV_HTML = """
<ul class="as-nav">
  <li><a href="index.html">Главная</a></li>
  <li>
    <span>Наш флот <span class="as-caret">▾</span></span>
    <div class="as-dropdown">
      <a href="yacht-charter.html">Весь флот</a>
      <a href="lipari41.html">Катамаран Липари 41</a>
      <a href="oceanis-473.html">Океанис 473 Клипер</a>
      <a href="dufour44.html">Катамаран Бали 4.6</a>
      <a href="dufour405.html">Дюфур 405</a>
      <a href="lucia40.html">Люсия 40</a>
    </div>
  </li>
  <li>
    <span>Маршруты <span class="as-caret">▾</span></span>
    <div class="as-dropdown">
      <a href="plan-2026.html">Переходы 2026</a>
      <a href="plan-2025.html">Переходы 2025</a>
      <a href="plan-2024.html">Переходы 2024</a>
      <a href="kanarskie-ostrova.html">Канарские острова</a>
      <a href="caribs.html">Карибские острова</a>
      <a href="malaga-mallorca.html">Малага — Майорка</a>
      <a href="montenegro.html">Черногория</a>
      <a href="sailing.html">Парусный спорт</a>
      <a href="yachtingtravel.html">Яхтинг путешествия</a>
      <a href="otchet-o-perehodah.html">Отчёт о переходах</a>
    </div>
  </li>
  <li>
    <span>Базирование <span class="as-caret">▾</span></span>
    <div class="as-dropdown">
      <a href="rekomenduemye-mariny.html">Канарские острова</a>
      <a href="mariny-v-chernogorii.html">Черногория</a>
      <a href="marina-karibes.html">Карибы</a>
      <a href="marina.html">Все марины</a>
    </div>
  </li>
  <li><a href="prajs.html">Прайс</a></li>
  <li><a href="contact.html">Контакты</a></li>
</ul>
"""

MOB_NAV_HTML = """
<div class="as-mob-item">
  <a href="index.html">Главная</a>
</div>
<div class="as-mob-item">
  <span onclick="toggleMobSub(this)">Наш флот ▾</span>
  <div class="as-mob-sub">
    <a href="yacht-charter.html">Весь флот</a>
    <a href="lipari41.html">Катамаран Липари 41</a>
    <a href="oceanis-473.html">Океанис 473 Клипер</a>
    <a href="dufour44.html">Катамаран Бали 4.6</a>
    <a href="dufour405.html">Дюфур 405</a>
    <a href="lucia40.html">Люсия 40</a>
  </div>
</div>
<div class="as-mob-item">
  <span onclick="toggleMobSub(this)">Маршруты ▾</span>
  <div class="as-mob-sub">
    <a href="plan-2026.html">Переходы 2026</a>
    <a href="plan-2025.html">Переходы 2025</a>
    <a href="plan-2024.html">Переходы 2024</a>
    <a href="kanarskie-ostrova.html">Канарские острова</a>
    <a href="caribs.html">Карибские острова</a>
    <a href="malaga-mallorca.html">Малага — Майорка</a>
    <a href="montenegro.html">Черногория</a>
    <a href="sailing.html">Парусный спорт</a>
    <a href="otchet-o-perehodah.html">Отчёт о переходах</a>
  </div>
</div>
<div class="as-mob-item">
  <span onclick="toggleMobSub(this)">Базирование ▾</span>
  <div class="as-mob-sub">
    <a href="rekomenduemye-mariny.html">Канарские острова</a>
    <a href="mariny-v-chernogorii.html">Черногория</a>
    <a href="marina-karibes.html">Карибы</a>
  </div>
</div>
<div class="as-mob-item"><a href="prajs.html">Прайс</a></div>
<div class="as-mob-item"><a href="contact.html">Контакты</a></div>
<div class="as-mob-actions">
  <a href="{TG_BOT}" target="_blank" class="as-btn as-btn-telegram">
    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12s5.37 12 12 12 12-5.37 12-12S18.63 0 12 0zm5.56 8.25-2.01 9.46c-.15.66-.54.82-1.08.51l-3-2.21-1.45 1.39c-.16.16-.3.3-.61.3l.21-3.05 5.56-5.02c.24-.21-.05-.33-.37-.12L7.16 14.24l-2.95-.92c-.64-.2-.65-.64.14-.95l11.52-4.44c.53-.19 1 .13.69.32z"/></svg>
    Написать капитану
  </a>
</div>
""".replace("{TG_BOT}", TG_BOT)

def tg_icon():
    return '<svg viewBox="0 0 24 24" fill="currentColor" width="13" height="13"><path d="M12 0C5.37 0 0 5.37 0 12s5.37 12 12 12 12-5.37 12-12S18.63 0 12 0zm5.56 8.25-2.01 9.46c-.15.66-.54.82-1.08.51l-3-2.21-1.45 1.39c-.16.16-.3.3-.61.3l.21-3.05 5.56-5.02c.24-.21-.05-.33-.37-.12L7.16 14.24l-2.95-.92c-.64-.2-.65-.64.14-.95l11.52-4.44c.53-.19 1 .13.69.32z"/></svg>'

def header_html(title, active=""):
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>{title} | Atlantic Sail</title>
  <meta name="description" content="Аренда яхт с капитаном. Атлантика, Канары, Средиземноморье, Карибы."/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@300;400;500&display=swap" rel="stylesheet"/>
  <link rel="stylesheet" href="style.css"/>
  <script type="text/javascript">
    function googleTranslateElementInit() {{
      new google.translate.TranslateElement({{pageLanguage:'ru',includedLanguages:'en,de,fr,es,it',layout:google.translate.TranslateElement.InlineLayout.SIMPLE}},'google_translate_element');
    }}
  </script>
</head>
<body>

<header class="as-header">
  <a href="index.html" class="as-logo">
    <span class="as-logo-icon">⚓</span>
    Atlantic <span>Sail</span>
  </a>
  {NAV_HTML}
  <div class="as-header-right">
    <div class="as-translate-wrap">
      <button class="as-btn-translate" onclick="document.getElementById('google_translate_element').style.display=document.getElementById('google_translate_element').style.display==='none'?'block':'none'">🌐 EN</button>
      <div id="google_translate_element"></div>
    </div>
    <a href="{TG_BOT}" target="_blank" class="as-btn-tg">{tg_icon()} Написать</a>
    <button class="as-hamburger" id="hbg" onclick="toggleMenu()"><span></span><span></span><span></span></button>
  </div>
</header>

<div class="as-mobile-menu" id="mobMenu">
  {MOB_NAV_HTML}
</div>
"""

FOOTER_HTML = f"""
<div class="as-bot-bar">
  <p>Задайте вопрос капитану прямо в Telegram — ответим быстро!</p>
  <a href="{TG_BOT}" target="_blank" class="as-btn as-btn-telegram">
    <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M12 0C5.37 0 0 5.37 0 12s5.37 12 12 12 12-5.37 12-12S18.63 0 12 0zm5.56 8.25-2.01 9.46c-.15.66-.54.82-1.08.51l-3-2.21-1.45 1.39c-.16.16-.3.3-.61.3l.21-3.05 5.56-5.02c.24-.21-.05-.33-.37-.12L7.16 14.24l-2.95-.92c-.64-.2-.65-.64.14-.95l11.52-4.44c.53-.19 1 .13.69.32z"/></svg>
    @CaptainAtlanticBot
  </a>
</div>

<footer class="as-footer">
  <div class="as-footer-inner">
    <div class="as-logo">⚓ Atlantic <span style="color:var(--gold)">Sail</span></div>
    <p class="as-footer-copy">© 2025 Atlantic Sail · Las Palmas de Gran Canaria</p>
    <div class="as-footer-links">
      <a href="{TG_BOT}" target="_blank">Telegram</a>
      <a href="{YT}" target="_blank">YouTube</a>
      <a href="{IG}" target="_blank">Instagram</a>
      <a href="contact.html">Контакты</a>
      <a href="prajs.html">Прайс</a>
    </div>
  </div>
</footer>

<script>
const hbg = document.getElementById('hbg');
const mob = document.getElementById('mobMenu');
function toggleMenu() {{
  hbg.classList.toggle('open');
  mob.classList.toggle('open');
  document.body.style.overflow = mob.classList.contains('open') ? 'hidden' : '';
}}
function toggleMobSub(el) {{
  const sub = el.nextElementSibling;
  sub.classList.toggle('open');
}}
const obs = new IntersectionObserver(e => e.forEach(x => {{ if(x.isIntersecting) x.target.classList.add('vis'); }}), {{threshold:0.1}});
document.querySelectorAll('.reveal').forEach(el => obs.observe(el));
</script>
<script src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
</body>
</html>
"""

def extract_wix_content(html_text):
    """Extract meaningful content from Wix HTML"""
    soup = BeautifulSoup(html_text, 'html.parser')
    
    # Remove script, style, nav tags
    for tag in soup.find_all(['script','style','noscript','header','footer']):
        tag.decompose()
    
    # Try to find main content area
    content_text = soup.get_text(separator='\n', strip=True)
    lines = [l.strip() for l in content_text.split('\n') if l.strip()]
    
    # Skip navigation lines (first ~50 lines are usually Wix nav)
    filtered = []
    skip_keywords = ['Главная','Наш флот','Места базирования','Маршруты','Контакты','Прайс',
                     'top of page','Atlantic Sail','Аренда парусных яхт','морской круиз',
                     'Use tab to navigate','Дюфур 405','Катамаран Бали','Катамаран Липари',
                     'Океанис 473','Марины на Канарских','Марины в Черногории','Марины на Карибах',
                     'Переходы 2024','Канарские острова S','Канарские острова N','Черногория',
                     'Карибские острова','путешествие на яхте','график маршрутов','Малага',
                     'Майорка - Рим','Рим - Катания','Клубный отдых','Отчет о переходах',
                     'Заказать','press to zoom','☰','▼','▾']
    
    nav_done = False
    for line in lines:
        if not nav_done:
            if any(kw in line for kw in ['Звоните нам', 'Лучше арендовать', 'Аренда яхт с капитаном',
                                          'Маршруты яхт', 'Трансатлантический', 'Черногория 06',
                                          'Наше участие', 'Условия оплаты']):
                nav_done = True
        if nav_done:
            if line not in skip_keywords and len(line) > 2:
                filtered.append(line)
    
    return filtered

def lines_to_html(lines):
    """Convert text lines to HTML content"""
    html = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Detect headers (short lines, no period)
        if len(line) < 80 and not line.endswith('.') and not line.startswith('+') and not line.startswith('http') and not ',' in line[:20] and i < len(lines)-1:
            if lines[i+1] if i+1 < len(lines) else '':
                html.append(f'<h3>{line}</h3>')
                i += 1
                continue
        # Bullet points
        if line.startswith('*') or line.startswith('-') or line.startswith('•'):
            html.append(f'<li>{line.lstrip("*-•").strip()}</li>')
        else:
            html.append(f'<p>{line}</p>')
        i += 1
    
    # Wrap consecutive li in ul
    result = '\n'.join(html)
    result = re.sub(r'(<li>.*?</li>\n?)+', lambda m: '<ul>\n' + m.group(0) + '</ul>\n', result, flags=re.DOTALL)
    return result

print("Template module loaded ✅")
