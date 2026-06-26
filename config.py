"""
config.py - Konfigurasi utama untuk project Akamai Bypass
Membaca credential dari file .env
"""

import os
from dotenv import load_dotenv

# Muat file .env
load_dotenv()

class Config:
    """Class konfigurasi utama"""
    
    # ============ PROXY ============
    # Ambil dari environment variable — TIDAK ADA default credential asli.
    # Isi nilai kamu sendiri di file .env (lihat .env.example)
    PROXY_HOST = os.getenv('PROXY_HOST', 'p.webshare.io:80')
    PROXY_USER = os.getenv('PROXY_USER', '')
    PROXY_PASS = os.getenv('PROXY_PASS', '')
    
    # ============ TARGET ============
    TARGET_URL = os.getenv('TARGET_URL', 'https://www.adobe.com')
    BROWSER_PROFILE = os.getenv('BROWSER_PROFILE', 'chrome124')
    
    @property
    def PROXY_URL(self):
        """
        Format URL proxy untuk curl_cffi dan requests:
        http://USER:PASS@HOST
        """
        return f"http://{self.PROXY_USER}:{self.PROXY_PASS}@{self.PROXY_HOST}"
    
    # ============ HEADERS DEFAULT ============
    # Header ini HARUS persis seperti browser asli agar tidak terdeteksi
    DEFAULT_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
    }
    
    def __repr__(self):
        """Tampilkan konfigurasi (tanpa expose password full)"""
        return f"""
Config:
  PROXY_HOST: {self.PROXY_HOST}
  PROXY_USER: {self.PROXY_USER}
  PROXY_PASS: {'*' * len(self.PROXY_PASS)}
  TARGET_URL: {self.TARGET_URL}
  BROWSER_PROFILE: {self.BROWSER_PROFILE}
  PROXY_URL: {self.PROXY_URL.replace(self.PROXY_PASS, '****')}
"""

# Buat instance global agar mudah di-import
config = Config()

# Jika dijalankan langsung, tampilkan konfigurasi
if __name__ == '__main__':
    print("📋 Konfigurasi saat ini:")
    print(config)