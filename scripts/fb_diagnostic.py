"""
Diagnostic: What does Facebook actually return when we fetch?
Tests:
1. HTTP response code & headers
2. OG meta tags (text + image URLs)
3. twitter:image tag
4. Can we actually download the image?
"""
import httpx
from bs4 import BeautifulSoup
import html as html_module

URL = "https://www.facebook.com/share/p/1KDguwVmKP/"

print("=" * 60)
print(f"DIAGNOSTIC: {URL}")
print("=" * 60)

# --- Step 1: Fetch with Googlebot UA ---
print("\n[1] Fetching page (Googlebot UA)...")
try:
    with httpx.Client(timeout=20, follow_redirects=True, headers={
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    }) as client:
        resp = client.get(URL)
    
    print(f"  Status: {resp.status_code}")
    print(f"  Final URL: {resp.url}")
    print(f"  Content-Type: {resp.headers.get('content-type', 'N/A')}")
    print(f"  HTML size: {len(resp.text)} chars")
    
    # Check for login redirect
    if "login" in str(resp.url).lower():
        print("  ⚠️ REDIRECTED TO LOGIN!")
    
except Exception as e:
    print(f"  ❌ FETCH FAILED: {e}")
    exit()

# --- Step 2: Parse meta tags ---
print("\n[2] Parsing meta tags...")
soup = BeautifulSoup(resp.text, "html.parser")

og_desc = soup.find("meta", property="og:description")
og_title = soup.find("meta", property="og:title") 
og_image = soup.find("meta", property="og:image")
tw_image = soup.find("meta", attrs={"name": "twitter:image"})

print(f"  og:title   = {og_title.get('content', '')[:80] if og_title else 'NOT FOUND'}")

desc_text = og_desc.get("content", "") if og_desc else ""
if desc_text:
    desc_text = html_module.unescape(desc_text)
print(f"  og:description = {desc_text[:150] if desc_text else 'NOT FOUND'}...")
print(f"  og:description length = {len(desc_text)} chars")

og_img_url = html_module.unescape(og_image.get("content", "")) if og_image else None
tw_img_url = html_module.unescape(tw_image.get("content", "")) if tw_image else None

print(f"  og:image   = {og_img_url[:100] if og_img_url else 'NOT FOUND'}...")
print(f"  twitter:image = {tw_img_url[:100] if tw_img_url else 'NOT FOUND'}...")

if og_img_url and tw_img_url:
    print(f"  Same URL?  = {og_img_url == tw_img_url}")

# --- Step 3: Try downloading the image ---
image_url = tw_img_url or og_img_url
if image_url:
    print(f"\n[3] Downloading image...")
    print(f"  URL: {image_url[:120]}...")
    try:
        with httpx.Client(timeout=15, follow_redirects=True, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }) as client:
            img_resp = client.get(image_url)
        
        print(f"  Status: {img_resp.status_code}")
        print(f"  Content-Type: {img_resp.headers.get('content-type', 'N/A')}")
        print(f"  Size: {len(img_resp.content)} bytes ({len(img_resp.content)/1024:.1f} KB)")
        
        if img_resp.status_code == 200 and len(img_resp.content) > 1000:
            print("  ✅ IMAGE DOWNLOADED OK!")
        elif img_resp.status_code == 200 and len(img_resp.content) < 1000:
            print("  ⚠️ Image very small — might be a placeholder/error page")
            print(f"  First 200 bytes: {img_resp.content[:200]}")
        else:
            print(f"  ❌ IMAGE DOWNLOAD FAILED (status {img_resp.status_code})")
            
    except Exception as e:
        print(f"  ❌ IMAGE DOWNLOAD ERROR: {e}")
else:
    print("\n[3] No image URL found, skipping download test")

# --- Step 4: Check for login wall indicators ---
print("\n[4] Login wall check...")
html_text = resp.text.lower()
indicators = {
    "login_form": "login_form" in html_text,
    "not_logged_in": "not_logged_in" in html_text,
    "login popup": "logindialog" in html_text or "login_dialog" in html_text,
    "must log in": "must log in" in html_text or "you must log in" in html_text,
    "content_not_available": "content isn't available" in html_text or "this content isn" in html_text,
}
for k, v in indicators.items():
    print(f"  {k}: {'⚠️ YES' if v else '✅ No'}")

print("\n" + "=" * 60)
print("DONE")
