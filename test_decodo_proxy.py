"""
test_decodo_proxy.py - Kirim request ke Adobe dengan proxy Decodo (residential)
Menggunakan curl_cffi untuk memalsukan TLS fingerprint
"""

from curl_cffi import requests
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

# Proxy Decodo — isi via .env, jangan hardcode kredensial asli
PROXY_HOST = os.getenv("DECODO_PROXY_HOST", "gate.decodo.com:10001")
PROXY_USER = os.getenv("DECODO_PROXY_USER", "")
PROXY_PASS = os.getenv("DECODO_PROXY_PASS", "")

# URL-encode password (karakter '+' harus diencode)
ENCODED_PASS = urllib.parse.quote(PROXY_PASS, safe='')
PROXY_URL = f"http://{PROXY_USER}:{ENCODED_PASS}@{PROXY_HOST}"

print(f"🔐 Proxy: {PROXY_HOST}")
print(f"👤 User: {PROXY_USER}")
print(f"🔑 Pass: {PROXY_PASS[:5]}***")
print(f"🌐 Proxy URL: http://{PROXY_USER}:{ENCODED_PASS}@...")
print("-" * 70)

# Headers persis seperti dari Developer Tools
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": '"Not/A)Brand";v="99", "Chromium";v="148"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

# Cookies (dari browser)
cookies = {
    "s_nr": "1782443392952-New",
    "gpv": "account.adobe.com",
    "relay": "920edf5d-a29e-4d1c-b0ac-e863ad4721a6"
}

print("🌐 Mengirim request ke https://auth.services.adobe.com/ ...")
print("   (dengan impersonate chrome124)")

try:
    response = requests.get(
        "https://auth.services.adobe.com/",
        headers=headers,
        cookies=cookies,
        impersonate="chrome124",
        proxies={"http": PROXY_URL, "https": PROXY_URL},
        timeout=30,
        verify=False  # Bypass SSL verify untuk testing
    )
    
    print(f"\n✅ Status Code: {response.status_code}")
    print(f"📏 Content Length: {len(response.text)}")
    print("\n📋 Response Headers (penting):")
    for key in ["Content-Type", "Set-Cookie", "Server", "X-"]:
        for h, v in response.headers.items():
            if key.lower() in h.lower():
                print(f"   {h}: {v[:100]}...")
    
    # Cek apakah ada Access Denied
    content_lower = response.text.lower()
    if "accessdenied" in content_lower or "access denied" in content_lower:
        print("\n❌ ACCESS DENIED DETECTED!")
        print("   Preview response:")
        print(response.text[:500])
        print("\n💡 Ini berarti proxy Decodo trial sudah diblokir oleh Akamai.")
    elif "adobe" in content_lower or "sign in" in content_lower:
        print("\n✅ SUCCESS! Halaman login Adobe muncul.")
        print("   Preview:")
        print(response.text[:300])
    else:
        print("\n⚠️ Response tidak jelas:")
        print(response.text[:300])
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()