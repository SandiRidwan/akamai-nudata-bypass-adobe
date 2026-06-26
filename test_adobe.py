"""
Test bypass ke Adobe.com
"""

from http_client import get_client
from config import config

def test_adobe():
    print("🚀 Testing bypass ke Adobe.com...")
    print(f"   Target: {config.TARGET_URL}")
    print(f"   Profile: {config.BROWSER_PROFILE}")
    print(f"   Proxy: {config.PROXY_HOST}")
    print("-" * 50)
    
    client = get_client(use_tls_chameleon=False)  # Pakai curl_cffi dulu
    
    response = client.get(config.TARGET_URL)
    
    if response is None:
        print("❌ Gagal mendapatkan response")
        return
    
    print(f"✅ Status Code: {response.status_code}")
    print(f"   Content Length: {len(response.text)} characters")
    
    # Cek apakah berhasil atau kena block
    if 'adobe' in response.text.lower() and 'captcha' not in response.text.lower():
        print("✅ SUKSES! Berhasil mengakses Adobe.com!")
        print("   (Tidak ada captcha/block)")
    elif 'captcha' in response.text.lower():
        print("⚠️  Kena CAPTCHA - Proxy datacenter terdeteksi")
        print("   Solusi: Ganti ke proxy residential (BrightData/Oxylabs)")
    elif response.status_code == 403:
        print("❌ Kena BLOCK (403) - Akamai mendeteksi bot")
    else:
        print(f"⚠️  Status tidak jelas: {response.status_code}")
        print(f"   Preview: {response.text[:200]}")

if __name__ == '__main__':
    test_adobe()