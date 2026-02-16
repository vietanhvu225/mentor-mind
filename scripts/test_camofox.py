"""Extract the Figma/Claude article and check for comments."""
import sys
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv()

from services.camofox_client import CamofoxClient

# The correct post
FB_URL = "https://www.facebook.com/share/v/1JCaM8krV7/"

client = CamofoxClient()
if not client.is_available():
    print("Camofox not running!")
    exit(1)

print(f"Extracting: {FB_URL}")
print("Wait 8s for full render...")
result = client.extract_page(FB_URL, wait_seconds=8)

if result:
    text = result["text"]
    links = result.get("links", [])
    
    print(f"\nText: {len(text)} chars")
    print(f"Links: {len(links)}")
    
    # Search for prompt/figma keywords
    print("\n=== Lines with 'prompt', 'figma', 'claude', 'comment' ===")
    for i, line in enumerate(text.split("\n")):
        if any(kw in line.lower() for kw in ["prompt", "figma", "claude", "comment", "opus", "insane"]):
            print(f"  Line {i}: {line[:150]}")

    print(f"\n=== FULL TEXT ===")
    print(text[:5000])
    
    if len(text) > 5000:
        print(f"\n... (truncated, total {len(text)} chars)")
    
    # Show non-facebook links (potential GitHub/external)
    print(f"\n=== External links (non-Facebook) ===")
    for link in links:
        url_str = str(link) if isinstance(link, str) else str(link.get("href", link.get("url", "")))
        if "facebook.com" not in url_str and url_str.startswith("http"):
            print(f"  {url_str[:120]}")
else:
    print("Extraction returned None")
