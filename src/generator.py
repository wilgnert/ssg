import re
from src.converter import markdown_to_html

def extract_title(markdown):
    
    title = re.search(r'^# (.+)', markdown, re.MULTILINE)
    if not title:
        raise ValueError("No title found in the markdown.")
    
    return title.group(1).strip()
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    md = None
    with open(from_path, 'r', encoding='utf-8') as f:
        md = f.read()
    title = extract_title(md)
    template = None
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    html = template.replace("{{ Content }}", markdown_to_html(md))
    html = html.replace("{{ Title }}", title)
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(html)