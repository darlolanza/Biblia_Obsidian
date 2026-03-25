import os
import re

vault_path = r'f:\Antigravity\Dario\Biblia_Obsidian'
index_file = os.path.join(vault_path, 'Índice de Libros.md')

with open(index_file, 'r', encoding='utf-8') as f:
    content = f.read()

links = re.findall(r'\[\[(.*?)#(.*?)(?:\|.*?)?\]\]', content)

for filename, anchor in links:
    # Try to find the file
    target_file = None
    for root, dirs, files in os.walk(vault_path):
        for f in files:
            if f.lower() == (filename + '.md').lower():
                target_file = os.path.join(root, f)
                break
        if target_file:
            break
    
    if not target_file:
        print(f"MISSING FILE: {filename}")
        continue
    
    with open(target_file, 'r', encoding='utf-8') as f:
        file_content = f.read()
    
    # Check if anchor exists (simplified check)
    # Obsidian anchors are based on header text, ignoring # prefixes and tags like {#id}
    # But often they are exact matches of the text.
    pattern = re.compile(rf'^[# ]+{re.escape(anchor)}(?:\s*\{{.*\}})?(?:\s*\(.*\))?$', re.MULTILINE)
    if not pattern.search(file_content):
        # Try a more fuzzy search
        # Find all headers to see what's there
        headers = re.findall(r'^#{2,}\s+(.*)', file_content, re.MULTILINE)
        print(f"MISSING ANCHOR in {filename}: '{anchor}' not found. Found headers: {headers[:5]}...")
