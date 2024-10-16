#!/usr/bin/python3
"""
A script to convert Markdown to HTML with advanced features.

Usage: ./markdown2html.py <input_file> <output_file>
"""

import sys
import os
import re
import hashlib

def md_to_html(content):
    """Convert Markdown content to HTML."""
    # Headings
    content = re.sub(r'^(#{1,6}) (.+)$', 
                     lambda m: f'<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>', 
                     content, flags=re.MULTILINE)
    
    # Unordered list
    content = re.sub(r'(^|\n)- (.+)(?=\n|$)', r'\1<ul>\n<li>\2</li>\n</ul>', content)
    content = re.sub(r'</ul>\n<ul>', '', content)
    
    # Ordered list
    content = re.sub(r'(^|\n)\* (.+)(?=\n|$)', r'\1<ol>\n<li>\2</li>\n</ol>', content)
    content = re.sub(r'</ol>\n<ol>', '', content)
    
    # Paragraphs
    content = re.sub(r'(?<!\n)\n(?!\n)', '<br/>\n', content)
    content = re.sub(r'(?<!\n)\n\n(?!\n)', '</p>\n\n<p>', content)
    content = f'<p>{content}</p>'
    
    # Bold and emphasis
    content = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', content)
    content = re.sub(r'__(.+?)__', r'<em>\1</em>', content)
    
    # MD5 conversion
    content = re.sub(r'\[\[(.+?)\]\]', 
                     lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), 
                     content)
    
    # Remove 'c' from content
    content = re.sub(r'\(\((.+?)\)\)', 
                     lambda m: m.group(1).replace('c', '').replace('C', ''), 
                     content)
    
    return content

def main():
    """Main function to handle file I/O and conversion."""
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)
    
    input_file, output_file = sys.argv[1], sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(input_file, 'r') as f:
            content = f.read()
        
        html_content = md_to_html(content)
        
        with open(output_file, 'w') as f:
            f.write(html_content)
        
    except IOError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
