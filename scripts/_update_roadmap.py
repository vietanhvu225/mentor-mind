"""Quick script to update ROADMAP.md with Camofox mention."""
with open("openspec/ROADMAP.md", "r", encoding="utf-8") as f:
    content = f.read()

old = 'bookmark URL \u2260 article URL)'
new = '**Camofox browser** (optional anti-detection cho Facebook/LinkedIn)'

content = content.replace(old, new)

with open("openspec/ROADMAP.md", "w", encoding="utf-8") as f:
    f.write(content)

print("ROADMAP updated!")
