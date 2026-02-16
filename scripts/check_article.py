"""Check article 119: try fresh Camofox extract + check links."""
import sys, re
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv()

import sqlite3
from services.camofox_client import CamofoxClient

URL = "https://www.facebook.com/share/p/1Za8YVE4LP/"
client = CamofoxClient()

if not client.is_available():
    print("Camofox not running!"); exit()

result = client.extract_page(URL, wait_seconds=5)
if not result:
    print("Extract failed"); exit()

raw = result["text"]
links = result.get("links", [])

print(f"Raw snapshot: {len(raw)} chars")

# Check all links for GitHub
print(f"\nAll page links ({len(links)}):")
gh_links_from_page = []
for l in links:
    href = l.get("href", "")
    text = l.get("text", "")
    if "github" in href.lower():
        gh_links_from_page.append(href)
        print(f"  🟢 GITHUB: {href}")
        print(f"     text: {text}")
    # also check text
    elif "github" in text.lower():
        print(f"  🟡 GITHUB in text: {text}")
        print(f"     href: {href}")

if not gh_links_from_page:
    print("  No GitHub links found in page links!")
    # Show all links for debugging
    print(f"\n  All links:")
    for l in links[:30]:
        href = l.get("href", "")
        text = l.get("text", "")[:60]
        print(f"    {text} → {href[:80]}")

# Check in raw text with looser regex
print(f"\nGitHub patterns in raw text:")
loose_patterns = [
    r'github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+',
    r'github\.com/\S+',
]
for pat in loose_patterns:
    found = re.findall(pat, raw)
    if found:
        for f in set(found):
            print(f"  → {f}")
