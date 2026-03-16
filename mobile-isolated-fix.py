#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mobile-isolated fix: Strictly isolate mobile CSS within media queries
Preserves desktop layout completely
"""

import os
import re
from pathlib import Path

# Strictly isolated mobile CSS - only applies to mobile devices
ISOLATED_MOBILE_CSS = """<style>
/* ===== MOBILE-ONLY DESIGN (Strictly Isolated) ===== */
/* This CSS ONLY applies to screens smaller than 768px */
/* Desktop layout is completely preserved */

/* ===== DESKTOP DEFAULTS (No changes) ===== */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
}

* {
  box-sizing: border-box;
}

/* ===== MOBILE-ONLY STYLES (max-width: 768px) ===== */
@media (max-width: 768px) {
  /* ===== GLOBAL MOBILE STYLES ===== */
  html, body {
    width: 100%;
    max-width: 100%;
    overflow-x: hidden;
  }

  /* ===== CONTAINER STACKING FOR MOBILE ===== */
  /* Only stack on mobile, preserve desktop layout */
  [class*="grid"], [class*="Grid"],
  [class*="row"], [class*="Row"],
  [class*="flex"], [class*="Flex"],
  [id*="Container"], [class*="container"],
  section, article, .section {
    display: flex !important;
    flex-direction: column !important;
    width: 100% !important;
    max-width: 100% !important;
  }

  /* ===== TYPOGRAPHY FOR MOBILE ===== */
  body {
    font-size: 16px !important;
    line-height: 1.5 !important;
  }

  h1, [class*="heading1"], [class*="Heading1"] {
    font-size: 24px !important;
    line-height: 1.2 !important;
    margin: 16px 0 !important;
    padding: 0 16px !important;
  }

  h2, [class*="heading2"], [class*="Heading2"] {
    font-size: 20px !important;
    line-height: 1.3 !important;
    margin: 12px 0 !important;
    padding: 0 16px !important;
  }

  h3, [class*="heading3"], [class*="Heading3"] {
    font-size: 18px !important;
    line-height: 1.3 !important;
    margin: 10px 0 !important;
    padding: 0 16px !important;
  }

  p, span, div, li {
    font-size: 16px !important;
    line-height: 1.5 !important;
    padding: 0 16px !important;
  }

  /* ===== TOUCH-FRIENDLY ELEMENTS ===== */
  a, button, [role="button"], input[type="button"], input[type="submit"] {
    min-height: 44px !important;
    min-width: 44px !important;
    padding: 12px 16px !important;
    font-size: 16px !important;
  }

  /* ===== IMAGES & MEDIA ===== */
  img, video, iframe, picture {
    width: 100% !important;
    max-width: 100% !important;
    height: auto !important;
    display: block !important;
  }

  /* ===== FORMS ===== */
  input, textarea, select {
    width: 100% !important;
    max-width: 100% !important;
    min-height: 44px !important;
    padding: 12px 16px !important;
    font-size: 16px !important;
  }

  /* ===== TABLES ===== */
  table {
    width: 100% !important;
    margin: 16px 0 !important;
  }

  table, thead, tbody, tr, td, th {
    display: block !important;
    width: 100% !important;
  }

  thead {
    display: none !important;
  }

  tr {
    margin-bottom: 16px !important;
    border: 1px solid #ddd !important;
    padding: 12px !important;
  }

  td, th {
    padding: 8px 12px !important;
    text-align: left !important;
    word-break: break-word !important;
  }

  /* ===== LISTS ===== */
  ul, ol {
    margin: 16px 0 !important;
    padding: 0 16px !important;
  }

  li {
    margin: 8px 0 !important;
  }

  /* ===== NAVIGATION MENU ===== */
  .atlantic-menu-container {
    width: 100vw !important;
    left: 0 !important;
    right: 0 !important;
    position: fixed !important;
    top: 0 !important;
    z-index: 2147483647 !important;
  }

  /* ===== SPACING ===== */
  section, article, .section, [class*="Container"] {
    padding: 16px !important;
    margin: 0 !important;
  }

  /* ===== HIDE UNNECESSARY ELEMENTS ===== */
  [class*="decoration"], [class*="Decoration"],
  [class*="spacer"], [class*="Spacer"],
  [class*="divider"], [class*="Divider"] {
    display: none !important;
  }
}

/* ===== TABLET OPTIMIZATION (768px - 1024px) ===== */
@media (min-width: 768px) and (max-width: 1024px) {
  /* Slightly larger fonts for tablets */
  body {
    font-size: 17px;
  }
  
  h1 { font-size: 28px !important; }
  h2 { font-size: 24px !important; }
  h3 { font-size: 20px !important; }
}

/* ===== DESKTOP OPTIMIZATION (1024px+) ===== */
@media (min-width: 1024px) {
  /* Restore full desktop experience - NO changes to layout */
  body {
    font-size: 16px;
  }
  
  h1 { font-size: 32px !important; }
  h2 { font-size: 28px !important; }
  h3 { font-size: 24px !important; }
  
  /* Ensure desktop layout is NOT affected by mobile rules */
  [class*="grid"], [class*="Grid"],
  [class*="row"], [class*="Row"],
  [class*="flex"], [class*="Flex"] {
    display: initial !important;
    flex-direction: initial !important;
  }
}
</style>"""

def remove_all_old_css(html_content):
    """Remove all previous CSS versions"""
    patterns = [
        r'<style>\s*\/\* ===== RESPONSIVE FIXES FOR MOBILE ===== \*\/.*?<\/style>',
        r'<style>\s*\/\* ===== SOFT RESPONSIVE FIXES ===== \*\/.*?<\/style>',
        r'<style>\s*\/\* ===== FINAL RESPONSIVE FIX ===== \*\/.*?<\/style>',
        r'<style>\s*\/\* ===== MOBILE-FIRST DESIGN TRANSFORMATION ===== \*\/.*?<\/style>',
        r'<style>\s*\/\* ===== MOBILE-ONLY DESIGN \(Strictly Isolated\) ===== \*\/.*?<\/style>'
    ]
    
    for pattern in patterns:
        html_content = re.sub(pattern, '', html_content, flags=re.DOTALL | re.IGNORECASE)
    
    return html_content

def inject_isolated_mobile_css(html_content):
    """Inject strictly isolated mobile CSS into head section"""
    # Remove all old versions
    html_content = remove_all_old_css(html_content)
    
    # Inject new CSS before closing </head>
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', ISOLATED_MOBILE_CSS + '\n</head>')
    elif '<body' in html_content:
        html_content = re.sub(
            r'(<body[^>]*>)',
            r'\1\n' + ISOLATED_MOBILE_CSS,
            html_content,
            flags=re.IGNORECASE
        )
    
    return html_content

def process_html_files(directory):
    """Process all HTML files in directory"""
    html_files = list(Path(directory).glob('*.html'))
    
    success_count = 0
    error_count = 0
    
    for html_file in sorted(html_files):
        # Skip template files
        if html_file.name in ['mobile-isolated-fix.py', 'mobile-first-design.py', 'final-responsive-fix.py', 
                              'soft-responsive.py', 'make-responsive.py', 'mobile-menu-ultra.html', 
                              'mobile-responsive-menu.html', 'dropdown-menu-fixed.html', 'dropdown-menu.html']:
            continue
        
        try:
            with open(html_file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Apply transformation
            content = inject_isolated_mobile_css(content)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ {html_file.name}")
            success_count += 1
            
        except Exception as e:
            print(f"✗ {html_file.name}: {str(e)}")
            error_count += 1
    
    print(f"\n✓ Обработано: {success_count} файлов")
    if error_count > 0:
        print(f"✗ Ошибок: {error_count}")

if __name__ == '__main__':
    import sys
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    process_html_files(directory)
