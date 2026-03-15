#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to make all HTML pages responsive by:
1. Ensuring proper viewport meta tag
2. Adding responsive CSS rules
3. Fixing fixed widths and containers
"""

import os
import re
from pathlib import Path

# Responsive CSS that will be injected into all pages
RESPONSIVE_CSS = """<style>
/* ===== RESPONSIVE FIXES FOR MOBILE ===== */

/* Ensure viewport is properly set */
html, body {
  width: 100% !important;
  height: auto !important;
  margin: 0 !important;
  padding: 0 !important;
  box-sizing: border-box !important;
}

*, *::before, *::after {
  box-sizing: border-box !important;
}

/* Fix all containers to be responsive */
[id*="Container"], 
[class*="container"],
[class*="Container"],
#site-root,
#SITE_CONTAINER,
.wix-container,
[role="main"] {
  width: 100% !important;
  max-width: 100% !important;
  overflow-x: hidden !important;
}

/* Make all images responsive */
img {
  max-width: 100% !important;
  height: auto !important;
  display: block !important;
}

/* Fix sections and rows */
section, 
[role="region"],
.section,
[id*="Section"],
[class*="Section"] {
  width: 100% !important;
  max-width: 100% !important;
}

/* Fix text sizing for mobile */
@media (max-width: 768px) {
  body {
    font-size: 14px !important;
  }
  
  h1 {
    font-size: 24px !important;
  }
  
  h2 {
    font-size: 20px !important;
  }
  
  h3 {
    font-size: 18px !important;
  }
  
  h4, h5, h6 {
    font-size: 16px !important;
  }
  
  p {
    font-size: 14px !important;
    line-height: 1.5 !important;
  }
  
  /* Make buttons and links bigger for touch */
  button, a, [role="button"] {
    min-height: 44px !important;
    min-width: 44px !important;
    padding: 12px 16px !important;
    font-size: 16px !important;
  }
  
  /* Fix padding and margins for small screens */
  [id*="Container"],
  [class*="container"],
  section,
  [role="region"] {
    padding: 16px !important;
    margin: 0 !important;
  }
  
  /* Ensure no horizontal overflow */
  body, html, #SITE_CONTAINER, #site-root {
    overflow-x: hidden !important;
  }
  
  /* Make tables responsive */
  table {
    width: 100% !important;
    font-size: 12px !important;
  }
  
  /* Fix forms for mobile */
  input, textarea, select {
    width: 100% !important;
    max-width: 100% !important;
    padding: 12px !important;
    font-size: 16px !important;
    border: 1px solid #ccc !important;
    border-radius: 4px !important;
  }
}

/* Ensure menu doesn't break layout */
.atlantic-menu-container {
  width: 100% !important;
  max-width: 100% !important;
}

/* Prevent Wix elements from breaking layout */
[class*="wix"],
[data-testid*="wix"] {
  max-width: 100% !important;
  overflow-x: hidden !important;
}

/* Fix any element with fixed width */
[style*="width: 9999px"],
[style*="width:9999px"] {
  width: 100% !important;
  max-width: 100% !important;
}

/* Ensure proper scaling on all devices */
@media (max-width: 480px) {
  body {
    font-size: 13px !important;
  }
  
  h1 {
    font-size: 20px !important;
  }
  
  h2 {
    font-size: 18px !important;
  }
  
  button, a, [role="button"] {
    min-height: 48px !important;
    padding: 14px 12px !important;
    font-size: 14px !important;
  }
}

/* Tablet adjustments */
@media (min-width: 769px) and (max-width: 1024px) {
  body {
    font-size: 15px !important;
  }
  
  [id*="Container"],
  [class*="container"] {
    padding: 20px !important;
  }
}
</style>"""

def ensure_viewport_meta(html_content):
    """Ensure proper viewport meta tag is present"""
    # Check if viewport meta already exists
    if 'name="viewport"' in html_content or "name='viewport'" in html_content:
        # Replace existing viewport with proper one
        html_content = re.sub(
            r'<meta\s+name=["\']?viewport["\']?[^>]*>',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">',
            html_content,
            flags=re.IGNORECASE
        )
    else:
        # Add viewport meta tag after charset
        if '<meta charset' in html_content:
            html_content = re.sub(
                r'(<meta\s+charset[^>]*>)',
                r'\1\n  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">',
                html_content,
                flags=re.IGNORECASE
            )
        elif '<head>' in html_content:
            html_content = re.sub(
                r'(<head[^>]*>)',
                r'\1\n  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">',
                html_content,
                flags=re.IGNORECASE
            )
    
    return html_content

def inject_responsive_css(html_content):
    """Inject responsive CSS into head section"""
    # Check if responsive CSS already exists
    if 'RESPONSIVE FIXES FOR MOBILE' in html_content:
        return html_content
    
    # Find where to inject CSS (before closing </head>)
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', RESPONSIVE_CSS + '\n</head>')
    elif '<body' in html_content:
        # If no </head>, inject after <body>
        html_content = re.sub(
            r'(<body[^>]*>)',
            r'\1\n' + RESPONSIVE_CSS,
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
        if html_file.name in ['make-responsive.py', 'mobile-menu-ultra.html', 'mobile-responsive-menu.html', 'dropdown-menu-fixed.html', 'dropdown-menu.html']:
            continue
        
        try:
            with open(html_file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Apply transformations
            content = ensure_viewport_meta(content)
            content = inject_responsive_css(content)
            
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
