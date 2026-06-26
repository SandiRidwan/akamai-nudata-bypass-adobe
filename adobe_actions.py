"""
adobe_actions.py - Aksi Berisiko Tinggi di Adobe
(Login & Registrasi) dengan simulasi perilaku manusia
"""

import time
import random
from stealth_browser import StealthBrowser
from config import config

class AdobeActions:
    def __init__(self, headless=False):
        self.headless = headless
        self.browser = None
    
    def _start_browser(self):
        """Mulai stealth browser jika belum"""
        if self.browser is None:
            self.browser = StealthBrowser(headless=self.headless)
            self.browser.start()
        return self.browser
    
    def _find_and_fill(self, page, selectors, value, field_name="field"):
        """Coba berbagai selector untuk mengisi form"""
        for selector in selectors:
            try:
                # Tunggu selector
                page.wait_for_selector(selector, timeout=3000)
                # Scroll ke element
                page.evaluate(f'document.querySelector("{selector}")?.scrollIntoView({{behavior: "smooth", block: "center"}})')
                time.sleep(0.5)
                # Klik dan isi
                page.click(selector)
                time.sleep(random.uniform(0.2, 0.5))
                page.keyboard.press('Control+A')
                page.keyboard.press('Backspace')
                # Typing dengan delay
                for char in value:
                    page.keyboard.type(char, delay=random.randint(60, 150))
                print(f"   ✅ Filled {field_name}")
                return True
            except:
                continue
        print(f"   ⚠️ Could not find {field_name} with any selector")
        return False
    
    def login(self, email, password, max_retries=2):
        """
        Simulasi login ke Adobe.com
        Returns: (success, page)
        """
        for attempt in range(max_retries):
            try:
                print(f"\n🔐 Attempting login to Adobe (attempt {attempt+1})...")
                browser = self._start_browser()
                page = browser.page
                
                # 1. Buka halaman login yang benar
                page.goto('https://auth.services.adobe.com/', wait_until='load', timeout=60000)
                time.sleep(random.uniform(2, 4))
                
                # 2. Scroll ke form
                page.evaluate("window.scrollTo({top: 200, behavior: 'smooth'})")
                time.sleep(random.uniform(1, 2))
                
                # 3. Isi email - selector sudah terverifikasi dari screenshot
                email_selectors = [
                    'input[type="email"]',
                    'input[name="email"]',
                    '#email',
                    'input[placeholder*="email" i]',
                    'input[placeholder*="Email" i]'
                ]
                self._find_and_fill(page, email_selectors, email, "Email")
                time.sleep(random.uniform(0.5, 1.5))
                
                # 4. Klik tombol Continue
                continue_selectors = [
                    'button:has-text("Continue")',
                    'button[type="submit"]',
                    'button:has-text("Next")',
                    '[data-testid="submit-button"]'
                ]
                found = False
                for sel in continue_selectors:
                    try:
                        if page.locator(sel).count() > 0:
                            page.click(sel)
                            found = True
                            print(f"   ✅ Clicked Continue")
                            break
                    except:
                        continue
                if not found:
                    print("   ⚠️ Trying Enter key...")
                    page.keyboard.press('Enter')
                time.sleep(random.uniform(2, 4))
                
                # 5. Tunggu password field muncul
                try:
                    page.wait_for_selector('input[type="password"]', timeout=10000)
                except:
                    pass
                
                # 6. Isi password
                pass_selectors = [
                    'input[type="password"]',
                    'input[name="password"]',
                    '#password',
                    'input[placeholder*="password" i]'
                ]
                self._find_and_fill(page, pass_selectors, password, "Password")
                time.sleep(random.uniform(0.5, 1.5))
                
                # 7. Klik Sign In
                signin_selectors = [
                    'button:has-text("Sign In")',
                    'button:has-text("Login")',
                    'button[type="submit"]',
                    '[data-testid="login-button"]'
                ]
                found = False
                for sel in signin_selectors:
                    try:
                        if page.locator(sel).count() > 0:
                            page.click(sel)
                            found = True
                            print(f"   ✅ Clicked Sign In")
                            break
                    except:
                        continue
                if not found:
                    page.keyboard.press('Enter')
                
                # 8. Tunggu hasil
                time.sleep(random.uniform(4, 7))
                
                current_url = page.url
                page_content = page.content().lower()
                
                # Cek apakah login berhasil
                if 'dashboard' in current_url or 'account' in current_url or 'home' in current_url:
                    print("✅ LOGIN BERHASIL!")
                    return True, page
                elif 'invalid' in page_content or 'wrong' in page_content or 'error' in page_content:
                    print("❌ Login gagal: Email atau password salah.")
                    return False, page
                else:
                    print(f"⚠️  Status tidak jelas. URL: {current_url}")
                    return False, page
                
            except Exception as e:
                print(f"❌ Login error pada attempt {attempt+1}: {e}")
                if attempt < max_retries - 1:
                    print("   🔄 Mereset browser dan mencoba lagi...")
                    self.browser.close()
                    self.browser = None
                    time.sleep(3)
                else:
                    return False, None
        
        return False, None
    
    def signup(self, email, password, first_name=None, last_name=None, max_retries=2):
        """
        Simulasi registrasi akun baru di Adobe
        Returns: (success, page)
        """
        for attempt in range(max_retries):
            try:
                print(f"\n📝 Attempting signup to Adobe (attempt {attempt+1})...")
                browser = self._start_browser()
                page = browser.page
                
                # ====== STRATEGI 1: Buka halaman login dan klik "Create an account" ======
                print("   🌐 Opening auth.services.adobe.com...")
                page.goto('https://auth.services.adobe.com/', wait_until='load', timeout=30000)
                time.sleep(random.uniform(2, 4))
                
                # Cari dan klik link "Create an account"
                create_account_selectors = [
                    'a:has-text("Create an account")',
                    'a:has-text("Create account")',
                    'a:has-text("Sign Up")',
                    'a:has-text("New user")',
                    '[data-testid="create-account-link"]'
                ]
                
                clicked = False
                for sel in create_account_selectors:
                    try:
                        if page.locator(sel).count() > 0:
                            page.click(sel)
                            clicked = True
                            print(f"   ✅ Clicked: {sel}")
                            time.sleep(random.uniform(3, 5))
                            break
                    except:
                        continue
                
                if not clicked:
                    print("   ⚠️ Link 'Create an account' tidak ditemukan. Coba URL langsung...")
                    # Coba langsung ke URL signup
                    page.goto('https://auth.services.adobe.com/signup', wait_until='load', timeout=30000)
                    time.sleep(random.uniform(2, 4))
                
                # ====== STRATEGI 2: Isi form registrasi ======
                print("   📝 Filling registration form...")
                
                # Scroll ke form
                page.evaluate("window.scrollTo({top: 300, behavior: 'smooth'})")
                time.sleep(random.uniform(1, 2))
                
                # Isi Email (biasanya field pertama di form signup)
                email_selectors = [
                    'input[type="email"]',
                    'input[name="email"]',
                    '#email',
                    'input[placeholder*="email" i]',
                    'input[placeholder*="Email" i]'
                ]
                self._find_and_fill(page, email_selectors, email, "Email")
                time.sleep(random.uniform(0.5, 1.5))
                
                # Isi Password
                pass_selectors = [
                    'input[type="password"]',
                    'input[name="password"]',
                    '#password',
                    'input[placeholder*="password" i]',
                    'input[placeholder*="Password" i]'
                ]
                self._find_and_fill(page, pass_selectors, password, "Password")
                time.sleep(random.uniform(0.5, 1.5))
                
                # Isi First Name (jika ada)
                if first_name:
                    fn_selectors = [
                        'input[name="firstName"]',
                        'input[placeholder*="First"]',
                        'input[id*="first"]',
                        'input[aria-label*="First" i]'
                    ]
                    self._find_and_fill(page, fn_selectors, first_name, "First Name")
                    time.sleep(random.uniform(0.5, 1))
                
                # Isi Last Name (jika ada)
                if last_name:
                    ln_selectors = [
                        'input[name="lastName"]',
                        'input[placeholder*="Last"]',
                        'input[id*="last"]',
                        'input[aria-label*="Last" i]'
                    ]
                    self._find_and_fill(page, ln_selectors, last_name, "Last Name")
                    time.sleep(random.uniform(0.5, 1))
                
                # ====== STRATEGI 3: Submit form ======
                submit_selectors = [
                    'button:has-text("Create")',
                    'button:has-text("Sign Up")',
                    'button:has-text("Continue")',
                    'button[type="submit"]',
                    '[data-testid="submit"]'
                ]
                
                submitted = False
                for sel in submit_selectors:
                    try:
                        if page.locator(sel).count() > 0:
                            page.click(sel)
                            submitted = True
                            print(f"   ✅ Clicked submit: {sel}")
                            break
                    except:
                        continue
                
                if not submitted:
                    print("   ⚠️ Trying Enter key...")
                    page.keyboard.press('Enter')
                
                # ====== STRATEGI 4: Tunggu dan cek hasil ======
                time.sleep(random.uniform(4, 7))
                
                current_url = page.url
                page_content = page.content().lower()
                
                # Screenshot untuk debugging
                page.screenshot(path=f"signup_attempt_{attempt+1}.png")
                print(f"   📸 Screenshot: signup_attempt_{attempt+1}.png")
                
                # Cek hasil
                if 'verify' in current_url or 'verification' in current_url:
                    print("✅ REGISTRASI BERHASIL! Kirim ke email untuk verifikasi.")
                    return True, page
                elif 'welcome' in page_content or 'congrat' in page_content:
                    print("✅ REGISTRASI BERHASIL!")
                    return True, page
                elif 'used' in page_content or 'exists' in page_content or 'taken' in page_content:
                    print("❌ Registrasi gagal: Email sudah terdaftar.")
                    return False, page
                elif 'captcha' in page_content or 'verify' in page_content:
                    print("⚠️  CAPTCHA terdeteksi! Perlu solusi manual atau service.")
                    return False, page
                else:
                    print(f"⚠️  Status tidak jelas. URL: {current_url}")
                    # Coba cek apakah ada error message
                    try:
                        error_messages = page.locator('[class*="error"], [class*="alert"], [role="alert"]')
                        if error_messages.count() > 0:
                            error_text = error_messages.first.text_content()
                            print(f"   Error message: {error_text}")
                    except:
                        pass
                    return False, page
                
            except Exception as e:
                print(f"❌ Signup error pada attempt {attempt+1}: {e}")
                # Screenshot error
                try:
                    if self.browser and self.browser.page:
                        self.browser.screenshot(f"signup_error_{attempt+1}.png")
                except:
                    pass
                if attempt < max_retries - 1:
                    print("   🔄 Mereset browser...")
                    self.browser.close()
                    self.browser = None
                    time.sleep(3)
                else:
                    return False, None
        
        return False, None
    
    def close(self):
        """Tutup browser"""
        if self.browser:
            self.browser.close()
            self.browser = None


if __name__ == '__main__':
    # Test demo
    actions = AdobeActions(headless=False)
    try:
        import random
        import string
        random_email = f"test_{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}@mailinator.com"
        actions.signup(random_email, 'P@ssw0rd123!', 'Test', 'User')
    finally:
        actions.close()