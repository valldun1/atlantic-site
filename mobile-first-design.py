#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mobile-first design: Complete transformation of Wix site for mobile devices
"""

import os
import re
from pathlib import Path

# Comprehensive mobile-first CSS
MOBILE_FIRST_CSS = """<style>
/* ===== MOBILE-FIRST DESIGN TRANSFORMATION ===== */
/* Complete redesign for touch devices and small screens */

/* ===== GLOBAL MOBILE STYLES ===== */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* Ensure proper text rendering on mobile */
body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

/* ===== CONTAINER STACKING ===== */
/* Stack all multi-column layouts vertically on mobile */
[class*="grid"], [class*="Grid"],
[class*="row"], [class*="Row"],
[class*="flex"], [class*="Flex"],
[id*="Container"], [class*="container"],
section, article, .section {
  display: flex !important;
  flex-direction: column !important;
  width: 100% !important;
  max-width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
}

/* ===== TYPOGRAPHY FOR MOBILE ===== */
/* Readable font sizes for small screens */
body {
  font-size: 16px;
  line-height: 1.5;
  color: #333;
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
/* Minimum 44x44px touch targets for accessibility */
a, button, [role="button"], input[type="button"], input[type="submit"] {
  min-height: 44px !important;
  min-width: 44px !important;
  padding: 12px 16px !important;
  font-size: 16px !important;
  line-height: 1.5 !important;
  display: inline-block !important;
  margin: 8px 8px 8px 0 !important;
}

/* ===== IMAGES & MEDIA ===== */
img, video, iframe, picture {
  width: 100% !important;
  max-width: 100% !important;
  height: auto !important;
  display: block !important;
  margin: 0 !important;
}

/* Prevent image overflow */
img {
  object-fit: contain !important;
}

/* ===== FORMS ===== */
input, textarea, select {
  width: 100% !important;
  max-width: 100% !important;
  min-height: 44px !important;
  padding: 12px 16px !important;
  font-size: 16px !important;
  border: 1px solid #ddd !important;
  border-radius: 4px !important;
  margin: 8px 0 !important;
  box-sizing: border-box !important;
}

textarea {
  min-height: 120px !important;
  resize: vertical !important;
}

/* ===== TABLES ===== */
table {
  width: 100% !important;
  border-collapse: collapse !important;
  margin: 16px 0 !important;
  overflow-x: auto !important;
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
  border-radius: 4px !important;
  padding: 12px !important;
}

td, th {
  padding: 8px 12px !important;
  text-align: left !important;
  word-break: break-word !important;
}

td::before {
  content: attr(data-label) !important;
  font-weight: bold !important;
  display: block !important;
  margin-bottom: 4px !important;
}

/* ===== LISTS ===== */
ul, ol {
  margin: 16px 0 !important;
  padding: 0 16px !important;
}

li {
  margin: 8px 0 !important;
  padding: 0 !important;
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

/* ===== SPACING & PADDING ===== */
/* Consistent spacing for mobile */
section, article, .section, [class*="Container"] {
  padding: 16px !important;
  margin: 0 !important;
}

/* ===== HIDE UNNECESSARY ELEMENTS ===== */
/* Hide decorative elements that waste space on mobile */
[class*="decoration"], [class*="Decoration"],
[class*="spacer"], [class*="Spacer"],
[class*="divider"], [class*="Divider"],
.wix-ads, .wix-banner {
  display: none !important;
}

/* ===== CARD LAYOUT FOR MOBILE ===== */
/* Transform content into cards */
[class*="card"], [class*="Card"],
[class*="item"], [class*="Item"],
[class*="product"], [class*="Product"] {
  width: 100% !important;
  max-width: 100% !important;
  margin: 12px 0 !important;
  padding: 16px !important;
  border: 1px solid #eee !important;
  border-radius: 8px !important;
  background: #fff !important;
}

/* ===== RESPONSIVE IMAGES ===== */
/* Optimize images for mobile */
.wix-image, [class*="image"], [class*="Image"] {
  width: 100% !important;
  height: auto !important;
  max-width: 100% !important;
}

/* ===== FOOTER ===== */
footer, [role="contentinfo"] {
  width: 100% !important;
  padding: 16px !important;
  margin-top: 24px !important;
}

/* ===== ENSURE NO HORIZONTAL SCROLL ===== */
* {
  box-sizing: border-box !important;
  max-width: 100% !important;
}

html, body {
  width: 100vw !important;
  overflow-x: hidden !important;
}

/* ===== TABLET OPTIMIZATION (768px+) ===== */
@media (min-width: 768px) {
  /* Return to original layout on tablets */
  [class*="grid"], [class*="Grid"],
  [class*="row"], [class*="Row"],
  [class*="flex"], [class*="Flex"] {
    display: grid !important;
    flex-direction: row !important;
  }
  
  /* Increase font sizes for better readability */
  body {
    font-size: 17px;
  }
  
  h1 { font-size: 28px !important; }
  h2 { font-size: 24px !important; }
  h3 { font-size: 20px !important; }
  
  /* Restore table display */
  table, thead, tbody, tr, td, th {
    display: table !important;
  }
  
  thead {
    display: table-header-group !important;
  }
  
  td::before {
    display: none !important;
  }
}

/* ===== DESKTOP OPTIMIZATION (1024px+) ===== */
@media (min-width: 1024px) {
  /* Full desktop experience */
  body {
    font-size: 16px;
  }
  
  h1 { font-size: 32px !important; }
  h2 { font-size: 28px !important; }
  h3 { font-size: 24px !important; }
  
  p, span, div, li {
    font-size: 16px !important;
    padding: 0 !important;
  }
}
</style>"""

def remove_old_css(html_content):
    """Remove old CSS versions"""
    patterns = [
        r'<style>\s*\/\* ===== RESPONSIVE FIXES FOR MOBILE ===== \*\/.*?<\/style>',
        r'<style>\s*\/\* ===== SOFT RESPONSIVE FIXES ===== \*\/.*?<\/style>',
        r'<style>\s*\/\* ===== FINAL RESPONSIVE FIX ===== \*\/.*?<\/style>',
        r'<style>\s*\/\* ===== MOBILE-FIRST DESIGN TRANSFORMATION ===== \*\/.*?<\/style>'
    ]
    
    for pattern in patterns:
        html_content = re.sub(pattern, '', html_content, flags=re.DOTALL | re.IGNORECASE)
    
    return html_content

def inject_mobile_css(html_content):
    """Inject mobile-first CSS into head section"""
    # Remove old versions
    html_content = remove_old_css(html_content)
    
    # Inject new CSS before closing </head>
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', MOBILE_FIRST_CSS + '\n</head>')
    elif '<body' in html_content:
        html_content = re.sub(
            r'(<body[^>]*>)',
            r'\1\n' + MOBILE_FIRST_CSS,
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
        if html_file.name in ['mobile-first-design.py', 'final-responsive-fix.py', 'soft-responsive.py', 
                              'make-responsive.py', 'mobile-menu-ultra.html', 'mobile-responsive-menu.html', 
                              'dropdown-menu-fixed.html', 'dropdown-menu.html']:
            continue
        
        try:
            with open(html_file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Apply transformation
            content = inject_mobile_css(content)
            
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
