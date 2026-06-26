"""
test_proxy.py - Testing koneksi proxy WebShare.io
Menggunakan curl_cffi untuk memalsukan TLS fingerprint Chrome
"""

from curl_cffi import requests
from config import config
import sys

def test_proxy():
    """Test koneksi proxy dengan httpbin.org"""
    
    print("=" * 60)
    print("🔍 TESTING PROXY CONNECTION")
    print("=" * 60)
    
    # Tampilkan konfigurasi yang digunakan
    print(f"📡 Proxy Host    : {config.PROXY_HOST}")
    print(f"👤 Proxy User    : {config.PROXY_USER}")
    print(f"🔑 Proxy Pass    : {'*' * len(config.PROXY_PASS)}")
    print(f"🌐 Target Profile: {config.BROWSER_PROFILE}")
    print("-" * 60)
    
    # Format proxy URL untuk curl_cffi
    proxy_url = config.PROXY_URL
    print(f"🔗 Proxy URL     : {proxy_url.replace(config.PROXY_PASS, '****')}")
    print("-" * 60)
    
    try:
        print("⏳ Menghubungkan ke httpbin.org/ip ...")
        
        # Kirim request via proxy dengan impersonate Chrome
        response = requests.get(
            'https://httpbin.org/ip',
            impersonate=config.BROWSER_PROFILE,  # Ini yang membuat Akamai tidak curiga
            proxies={'http': proxy_url, 'https': proxy_url},
            timeout=30,
            verify=True  # Verifikasi SSL
        )
        
        # Cek status code
        if response.status_code == 200:
            data = response.json()
            ip_address = data.get('origin', 'Tidak diketahui')
            
            print("=" * 60)
            print("✅ PROXY BERHASIL!")
            print(f"   📍 IP Address yang terdeteksi: {ip_address}")
            print(f"   🔒 Status Code: {response.status_code}")
            print("=" * 60)
            print("💡 Catatan: IP ini adalah IP DATACENTER dari WebShare.")
            print("   Untuk produksi di Adobe, sebaiknya pakai RESIDENTIAL proxy.")
            print("   Tapi untuk testing awal, ini sudah cukup.")
            return True
        else:
            print(f"❌ Proxy gagal! Status Code: {response.status_code}")
            return False
            
    except requests.exceptions.ProxyError as e:
        print(f"❌ ERROR PROXY: {e}")
        print("   Kemungkinan penyebab:")
        print("   1. Username atau password salah")
        print("   2. Proxy belum aktif (tunggu 5 menit setelah daftar)")
        print("   3. Koneksi internet terputus")
        print("   4. Firewall/antivirus memblokir port 80")
        return False
        
    except requests.exceptions.Timeout:
        print("❌ ERROR: Timeout! Koneksi terlalu lambat.")
        print("   Coba periksa koneksi internet Anda.")
        return False
        
    except Exception as e:
        print(f"❌ ERROR TAK TERDUGA: {e}")
        return False


def test_with_browser_info():
    """
    Test lanjutan: cek informasi browser yang dipalsukan
    (Opsional, untuk memastikan fingerprint berfungsi)
    """
    print("\n" + "=" * 60)
    print("🔍 TEST FINGERPRINT BROWSER")
    print("=" * 60)
    
    proxy_url = config.PROXY_URL
    
    try:
        response = requests.get(
            'https://httpbin.org/anything',
            impersonate=config.BROWSER_PROFILE,
            proxies={'http': proxy_url, 'https': proxy_url},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            headers = data.get('headers', {})
            
            print("📋 Headers yang dikirim:")
            print(f"   User-Agent: {headers.get('User-Agent', 'Tidak ada')}")
            print(f"   Accept-Encoding: {headers.get('Accept-Encoding', 'Tidak ada')}")
            print("-" * 60)
            print("✅ Fingerprint browser berhasil dipalsukan!")
            return True
        else:
            print(f"❌ Gagal: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == '__main__':
    print("🚀 MEMULAI TEST PROXY...\n")
    
    # Test 1: Basic proxy connection
    success = test_proxy()
    
    if success:
        # Test 2: Advanced fingerprint check (opsional)
        print("\n🔍 Melanjutkan ke test fingerprint browser...")
        test_with_browser_info()
        
        print("\n" + "=" * 60)
        print("🎉 SEMUA TEST BERHASIL! Proxy siap digunakan.")
        print("=" * 60)
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("❌ TEST GAGAL! Perbaiki masalah di atas, lalu coba lagi.")
        print("=" * 60)
        sys.exit(1)