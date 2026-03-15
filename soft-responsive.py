#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Soft responsive CSS that preserves Wix structure while improving mobile readability
"""

import os
import re
from pathlib import Path

# Soft responsive CSS - doesn't break the layout
SOFT_RESPONSIVE_CSS = """<style>
/* ===== SOFT RESPONSIVE FIXES ===== */
/* This CSS improves mobile readability WITHOUT breaking the Wix layout */

/* Ensure proper viewport scaling */
html, body {
  margin: 0;
  padding: 0;
}

/* Allow images to scale responsively */
img {
  max-width: 100%;
  height: auto;
}

/* Prevent horizontal overflow */
html, body {
  overflow-x: hidden;
}

/* Make text readable on mobile without breaking layout */
@media (max-width: 768px) {
  /* Slightly increase base font size for readability */
  body {
    font-size: 15px;
  }
  
  /* Make headings readable */
  h1 { font-size: 22px !important; line-height: 1.3; }
  h2 { font-size: 19px !important; line-height: 1.3; }
  h3 { font-size: 17px !important; line-height: 1.3; }
  
  /* Make buttons and links easier to tap */
  button, a[role="button"], [role="button"] {
    min-height: 44px;
    min-width: 44px;
  }
  
  /* Improve form input sizes */
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

/* Ensure menu doesn't break */
.atlantic-menu-container {
  overflow: hidden;
}

/* Fix any element that might cause horizontal scroll */
* {
  box-sizing: border-box;
}
</style>"""

def remove_old_responsive_css(html_content):
    """Remove the old aggressive responsive CSS"""
    # Remove the old RESPONSIVE FIXES section
    html_content = re.sub(
        r'<style>\s*\/\* ===== RESPONSIVE FIXES FOR MOBILE ===== \*\/.*?<\/style>',
        '',
        html_content,
        flags=re.DOTALL | re.IGNORECASE
    )
    return html_content

def ensure_viewport_meta(html_content):
    """Ensure proper viewport meta tag is present"""
    # Check if viewport meta already exists
    if 'name="viewport"' in html_content or "name='viewport'" in html_content:
        # Replace with simpler, less aggressive version
        html_content = re.sub(
            r'<meta\s+name=["\']?viewport["\']?[^>]*>',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            html_content,
            flags=re.IGNORECASE
        )
    else:
        # Add viewport meta tag after charset
        if '<meta charset' in html_content:
            html_content = re.sub(
                r'(<meta\s+charset[^>]*>)',
                r'\1\n  <meta name="viewport" content="width=device-width, initial-scale=1">',
                html_content,
                flags=re.IGNORECASE
            )
        elif '<head>' in html_content:
            html_content = re.sub(
                r'(<head[^>]*>)',
                r'\1\n  <meta name="viewport" content="width=device-width, initial-scale=1">',
                html_content,
                flags=re.IGNORECASE
            )
    
    return html_content

def inject_soft_responsive_css(html_content):
    """Inject soft responsive CSS into head section"""
    # First remove old version
    html_content = remove_old_responsive_css(html_content)
    
    # Check if soft responsive CSS already exists
    if 'SOFT RESPONSIVE FIXES' in html_content:
        return html_content
    
    # Find where to inject CSS (before closing </head>)
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', SOFT_RESPONSIVE_CSS + '\n</head>')
    elif '<body' in html_content:
        # If no </head>, inject after <body>
        html_content = re.sub(
            r'(<body[^>]*>)',
            r'\1\n' + SOFT_RESPONSIVE_CSS,
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
        if html_file.name in ['soft-responsive.py', 'make-responsive.py', 'mobile-menu-ultra.html', 'mobile-responsive-menu.html', 'dropdown-menu-fixed.html', 'dropdown-menu.html']:
            continue
        
        try:
            with open(html_file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Apply transformations
            content = ensure_viewport_meta(content)
            content = inject_soft_responsive_css(content)
            
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
