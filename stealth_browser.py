"""
Playwright + Stealth untuk simulasi browser yang tidak terdeteksi
Khusus untuk handling NuData (perilaku pengguna)
"""

from playwright.sync_api import sync_playwright
from config import config
import time
import random
import os

class StealthBrowser:
    def __init__(self, headless=False):
        """
        headless: False = tampilkan browser (lebih natural)
                  True = tanpa UI (lebih cepat, tapi lebih mudah terdeteksi)
        """
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.proxy_url = config.PROXY_URL
    
    def start(self):
        """Mulai browser dengan konfigurasi stealth"""
        self.playwright = sync_playwright().start()
        
        # Proxy settings untuk Playwright
        proxy_settings = {
            'server': f'http://{config.PROXY_HOST}',
            'username': config.PROXY_USER,
            'password': config.PROXY_PASS,
        }
        
        print(f"🔧 Using proxy: {config.PROXY_HOST}")
        
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-features=IsolateOrigins,site-per-process',
                '--no-sandbox',
                '--disable-web-security',
                '--disable-features=BlockInsecurePrivateNetworkRequests',
                '--disable-gpu',
                '--disable-dev-shm-usage',
            ]
        )
        
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York',
            color_scheme='light',
            java_script_enabled=True,
            proxy=proxy_settings,
            bypass_csp=True,  # Bypass Content Security Policy
        )
        
        self.page = self.context.new_page()
        
        # Terapkan stealth patches manual
        self._apply_stealth_patches()
        
        print("✅ Stealth browser started")
        return self.page
    
    def _apply_stealth_patches(self):
        """Stealth patches untuk menghindari deteksi"""
        self.page.add_init_script("""
            // Hapus webdriver
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // Tambahkan chrome runtime
            window.chrome = {
                runtime: {
                    onMessage: { addListener: () => {} },
                    sendMessage: () => {}
                },
                loadTimes: () => ({
                    commitLoadTime: Date.now() / 1000,
                    connectionInfo: "h2",
                    finishDocumentLoadTime: Date.now() / 1000 + 0.1,
                    finishLoadTime: Date.now() / 1000 + 0.2,
                    firstPaintAfterLoadTime: 0,
                    firstPaintTime: Date.now() / 1000 + 0.05,
                    navigationType: "Other",
                    npnNegotiatedProtocol: "h2",
                    requestTime: Date.now() / 1000 - 0.5,
                })
            };
            
            // Tambahkan plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            // Tambahkan languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            
            // Fix permisions
            Object.defineProperty(navigator, 'permissions', {
                get: () => ({
                    query: () => Promise.resolve({state: 'granted'})
                })
            });
        """)
    
    def goto(self, url, wait_until='load', timeout=60000):
        """
        Navigasi ke URL
        - wait_until: 'load' lebih cepat dari 'networkidle'
        - timeout: 60 detik untuk mengakomodasi proxy lambat
        """
        print(f"🌐 Navigating to: {url} (wait_until={wait_until}, timeout={timeout}ms)")
        
        try:
            self.page.goto(url, wait_until=wait_until, timeout=timeout)
            
            # Human-like behavior: scroll sedikit
            self._human_scroll()
            
            # Human-like behavior: delay acak
            time.sleep(random.uniform(1, 3))
            
            # Cek apakah halaman adalah captcha/block
            current_url = self.page.url
            page_title = self.page.title()
            page_text = self.page.content().lower()
            
            if 'captcha' in page_text or 'blocked' in page_text or 'access denied' in page_text:
                print("⚠️  Detected CAPTCHA or BLOCK page!")
                print(f"   Title: {page_title}")
                print(f"   URL: {current_url}")
                return self.page
            
            print(f"✅ Page loaded: {page_title}")
            return self.page
            
        except Exception as e:
            print(f"❌ Failed to load page: {e}")
            raise
    
    def _human_scroll(self):
        """Simulasi scroll seperti manusia"""
        self.page.evaluate("""
            window.scrollTo({
                top: Math.random() * 200,
                behavior: 'smooth'
            });
        """)
        time.sleep(random.uniform(0.5, 1.5))
    
    def fill_form(self, selector, value):
        """Isi form dengan human-like typing"""
        self.page.click(selector)
        time.sleep(random.uniform(0.2, 0.5))
        self.page.type(selector, value, delay=random.randint(50, 150))
    
    def click(self, selector):
        """Klik dengan human-like movement"""
        self.page.click(selector)
        time.sleep(random.uniform(0.5, 1))
    
    def screenshot(self, filename='screenshot.png'):
        """Screenshot untuk debugging"""
        self.page.screenshot(path=filename, full_page=False)
        print(f"📸 Screenshot saved: {filename}")
    
    def close(self):
        """Tutup browser"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("🔒 Browser closed")


def test_stealth_browser():
    """Fungsi test untuk stealth browser"""
    browser = StealthBrowser(headless=False)  # True untuk mode tanpa UI
    try:
        page = browser.start()
        page = browser.goto('https://www.adobe.com')
        
        # Tampilkan informasi halaman
        print(f"📄 Page Title: {page.title()}")
        print(f"📍 Current URL: {page.url}")
        
        # Screenshot untuk dokumentasi
        browser.screenshot('adobe_stealth_test.png')
        
        print("✅ Test selesai. Browser akan ditutup dalam 5 detik...")
        time.sleep(5)  # Biarkan user melihat halaman
        
    except Exception as e:
        print(f"❌ Test gagal: {e}")
    finally:
        browser.close()

if __name__ == '__main__':
    test_stealth_browser()