#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final responsive fix: Full-width containers and proper viewport scaling
"""

import os
import re
from pathlib import Path

# Final responsive CSS - fixes the "half-screen" issue
FINAL_RESPONSIVE_CSS = """<style>
/* ===== FINAL RESPONSIVE FIX ===== */
/* This CSS ensures full-width display on mobile devices */

/* Force full-width display on all devices */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
}

/* Fix Wix main container to be responsive */
#SITE_CONTAINER,
#site-root,
[id*="SITE_CONTAINER"],
[id*="site-root"] {
  width: 100% !important;
  max-width: 100% !important;
  min-width: 0 !important;
  overflow-x: hidden !important;
}

/* Fix all containers to not have fixed widths */
[id*="Container"],
[class*="container"],
[class*="Container"],
.wix-container {
  width: 100% !important;
  max-width: 100% !important;
  min-width: 0 !important;
}

/* Ensure no element causes horizontal overflow */
* {
  box-sizing: border-box;
  max-width: 100%;
}

/* Allow images and media to scale */
img, video, iframe {
  max-width: 100%;
  height: auto;
  display: block;
}

/* Fix sections and rows */
section, [role="region"], .section {
  width: 100% !important;
  max-width: 100% !important;
}

/* Mobile-specific improvements */
@media (max-width: 768px) {
  html, body {
    width: 100vw;
    overflow-x: hidden;
  }
  
  body {
    font-size: 15px;
  }
  
  h1 { font-size: 22px !important; line-height: 1.3; }
  h2 { font-size: 19px !important; line-height: 1.3; }
  h3 { font-size: 17px !important; line-height: 1.3; }
  
  /* Ensure menu doesn't break layout */
  .atlantic-menu-container {
    width: 100vw !important;
    left: 0 !important;
    right: 0 !important;
  }
  
  /* Make buttons and links easier to tap */
  button, a[role="button"], [role="button"] {
    min-height: 44px;
    min-width: 44px;
  }
  
  input, textarea, select {
    font-size: 16px;
    min-height: 44px;
  }
}

/* Very small phones */
@media (max-width: 480px) {
  body {
    font-size: 14px;
  }
  
  h1 { font-size: 20px !important; }
  h2 { font-size: 18px !important; }
  h3 { font-size: 16px !important; }
}

/* Prevent Wix fixed-width styles from breaking layout */
[style*="width: 9999px"],
[style*="width:9999px"],
[style*="max-width: 9999px"],
[style*="max-width:9999px"] {
  width: 100% !important;
  max-width: 100% !important;
}
</style>"""

def update_viewport_meta(html_content):
    """Update viewport meta tag for better mobile scaling"""
    # Replace existing viewport or add new one
    if 'name="viewport"' in html_content or "name='viewport'" in html_content:
        html_content = re.sub(
            r'<meta\s+name=["\']?viewport["\']?[^>]*>',
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
            html_content,
            flags=re.IGNORECASE
        )
    else:
        if '<meta charset' in html_content:
            html_content = re.sub(
                r'(<meta\s+charset[^>]*>)',
                r'\1\n  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
                html_content,
                flags=re.IGNORECASE
            )
        elif '<head>' in html_content:
            html_content = re.sub(
                r'(<head[^>]*>)',
                r'\1\n  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
                html_content,
                flags=re.IGNORECASE
            )
    
    return html_content

def remove_old_responsive_css(html_content):
    """Remove old responsive CSS versions"""
    # Remove RESPONSIVE FIXES
    html_content = re.sub(
        r'<style>\s*\/\* ===== RESPONSIVE FIXES FOR MOBILE ===== \*\/.*?<\/style>',
        '',
        html_content,
        flags=re.DOTALL | re.IGNORECASE
    )
    # Remove SOFT RESPONSIVE FIXES
    html_content = re.sub(
        r'<style>\s*\/\* ===== SOFT RESPONSIVE FIXES ===== \*\/.*?<\/style>',
        '',
        html_content,
        flags=re.DOTALL | re.IGNORECASE
    )
    # Remove FINAL RESPONSIVE FIX (if already exists)
    html_content = re.sub(
        r'<style>\s*\/\* ===== FINAL RESPONSIVE FIX ===== \*\/.*?<\/style>',
        '',
        html_content,
        flags=re.DOTALL | re.IGNORECASE
    )
    return html_content

def inject_final_responsive_css(html_content):
    """Inject final responsive CSS into head section"""
    # First remove old versions
    html_content = remove_old_responsive_css(html_content)
    
    # Find where to inject CSS (before closing </head>)
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', FINAL_RESPONSIVE_CSS + '\n</head>')
    elif '<body' in html_content:
        html_content = re.sub(
            r'(<body[^>]*>)',
            r'\1\n' + FINAL_RESPONSIVE_CSS,
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
        if html_file.name in ['final-responsive-fix.py', 'soft-responsive.py', 'make-responsive.py', 
                              'mobile-menu-ultra.html', 'mobile-responsive-menu.html', 
                              'dropdown-menu-fixed.html', 'dropdown-menu.html']:
            continue
        
        try:
            with open(html_file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Apply transformations
            content = update_viewport_meta(content)
            content = inject_final_responsive_css(content)
            
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
