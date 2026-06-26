"""
HTTP Client dengan curl_cffi + TLS-Chameleon untuk bypass Akamai
"""

from curl_cffi import requests
from config import config
import time
import random

class AkamaiHttpClient:
    def __init__(self, use_tls_chameleon=True):
        """
        use_tls_chameleon: True = pakai TLS-Chameleon (lebih canggih)
                           False = pakai curl_cffi saja (lebih ringan)
        """
        self.use_tls_chameleon = use_tls_chameleon
        self.proxy_url = config.PROXY_URL
        self.browser_profile = config.BROWSER_PROFILE
        self.session = None
        self._init_session()
    
    def _init_session(self):
        """Inisialisasi session dengan impersonate browser"""
        self.session = requests.Session(
            impersonate=self.browser_profile,
            proxies={'http': self.proxy_url, 'https': self.proxy_url},
            timeout=30,
        )
        # Set headers seperti browser asli
        self.session.headers.update(config.DEFAULT_HEADERS)
    
    def get(self, url, headers=None, retry=3):
        """
        GET request dengan retry otomatis
        """
        for attempt in range(retry):
            try:
                # Delay acak agar tidak terdeteksi sebagai bot
                time.sleep(random.uniform(1, 3))
                
                if headers:
                    self.session.headers.update(headers)
                
                response = self.session.get(url)
                
                # Cek apakah kena block (Akamai biasanya return 403 atau halaman captcha)
                if response.status_code == 403:
                    print(f"⚠️  Status 403 - Mungkin kena block Akamai, attempt {attempt+1}/{retry}")
                    if attempt < retry - 1:
                        self._rotate_profile()
                        continue
                
                # Cek apakah ada indikasi captcha/block di HTML
                if 'captcha' in response.text.lower() or 'blocked' in response.text.lower():
                    print(f"⚠️  Detected CAPTCHA or blocked page, attempt {attempt+1}/{retry}")
                    if attempt < retry - 1:
                        self._rotate_profile()
                        continue
                
                return response
                
            except Exception as e:
                print(f"❌ Request failed: {e}, attempt {attempt+1}/{retry}")
                if attempt < retry - 1:
                    self._rotate_profile()
                    continue
        
        return None
    
    def _rotate_profile(self):
        """Rotasi profile browser untuk menghindari deteksi"""
        profiles = ['chrome124', 'chrome123', 'chrome120', 'edge101', 'safari16_5']
        current = self.browser_profile
        new_profile = random.choice([p for p in profiles if p != current])
        self.browser_profile = new_profile
        print(f"🔄 Rotating to profile: {new_profile}")
        self._init_session()
    
    def post(self, url, data=None, json=None, headers=None, retry=3):
        """POST request dengan retry otomatis"""
        for attempt in range(retry):
            try:
                time.sleep(random.uniform(1, 3))
                
                if headers:
                    self.session.headers.update(headers)
                
                response = self.session.post(url, data=data, json=json)
                
                if response.status_code == 403:
                    print(f"⚠️  Status 403 - Mungkin kena block Akamai, attempt {attempt+1}/{retry}")
                    if attempt < retry - 1:
                        self._rotate_profile()
                        continue
                
                return response
                
            except Exception as e:
                print(f"❌ POST failed: {e}, attempt {attempt+1}/{retry}")
                if attempt < retry - 1:
                    self._rotate_profile()
                    continue
        
        return None

# Singleton instance
_client = None

def get_client(use_tls_chameleon=True):
    """Dapatkan instance HTTP client (singleton)"""
    global _client
    if _client is None:
        _client = AkamaiHttpClient(use_tls_chameleon=use_tls_chameleon)
    return _client