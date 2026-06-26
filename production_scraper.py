"""
production_scraper.py - Production-ready scraper with rotation, concurrency, and logging
- Rotates user-agent and browser profile
- Uses ThreadPoolExecutor for concurrent requests
- Retries on failure
- Saves results to JSON
"""

import sys
import os
import time
import json
import random
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from http_client import get_client
from config import config

# ============================================================
# SETUP LOGGING DENGAN UTF-8 (MENCEGAH UNICODE ERROR)
# ============================================================
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ============================================================
# KONFIGURASI
# ============================================================

# Daftar User-Agent untuk rotasi
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
]

# Profile yang didukung oleh curl_cffi (tanpa safari)
SUPPORTED_PROFILES = ['chrome124', 'chrome123', 'chrome120', 'edge101', 'chrome118']


class ProductionScraper:
    def __init__(self, max_workers=2, retries=3):
        self.max_workers = max_workers
        self.retries = retries
        self.client = get_client(use_tls_chameleon=False)  # pakai curl_cffi
        self.results = []
        self.failed_urls = []
        self.start_time = None
        self.end_time = None

    def _get_random_headers(self):
        """Dapatkan headers acak dengan User-Agent berbeda"""
        return {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': random.choice(['en-US,en;q=0.9', 'id-ID,id;q=0.9,en;q=0.8', 'en-GB,en;q=0.9']),
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
        }

    def _scrape_single_url(self, url):
        """Scrape satu URL dengan retry dan rotasi profile"""
        for attempt in range(self.retries):
            try:
                # Delay acak sebelum request
                delay = random.uniform(0.5, 2)
                logger.info(f"Scraping: {url} (attempt {attempt+1}/{self.retries})")
                time.sleep(delay)

                headers = self._get_random_headers()

                # Coba dengan profile random jika attempt > 0
                if attempt > 0:
                    new_profile = random.choice(SUPPORTED_PROFILES)
                    logger.info(f"Rotating to profile: {new_profile}")
                    self.client = get_client(use_tls_chameleon=False)
                    self.client.browser_profile = new_profile
                    self.client._init_session()

                response = self.client.get(url, headers=headers)

                if response is None:
                    logger.warning(f"No response from {url}, attempt {attempt+1}")
                    continue

                if response.status_code == 200:
                    # Cek apakah halaman mengandung captcha/block
                    text_lower = response.text.lower()
                    if 'captcha' in text_lower or 'blocked' in text_lower or 'access denied' in text_lower:
                        logger.warning(f"CAPTCHA/BLOCK detected on {url}, attempt {attempt+1}")
                        continue

                    # Sukses!
                    title = 'No title'
                    try:
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(response.text, 'html.parser')
                        if soup.title:
                            title = soup.title.string
                    except:
                        pass

                    logger.info(f"SUCCESS: {url} -> {title[:50]}...")
                    return {
                        'url': url,
                        'status': 'success',
                        'status_code': response.status_code,
                        'title': title,
                        'content_length': len(response.text),
                        'timestamp': datetime.now().isoformat()
                    }

                else:
                    logger.warning(f"Status {response.status_code} on {url}, attempt {attempt+1}")

            except Exception as e:
                logger.error(f"Error scraping {url}: {e}, attempt {attempt+1}")
                time.sleep(random.uniform(2, 4))

        # Gagal setelah semua retry
        logger.warning(f"FAILED: {url} after {self.retries} attempts")
        return {
            'url': url,
            'status': 'failed',
            'timestamp': datetime.now().isoformat()
        }

    def scrape_batch(self, urls):
        """Scrape banyak URL secara concurrent"""
        self.start_time = datetime.now()
        logger.info(f"Starting batch scrape: {len(urls)} URLs, {self.max_workers} workers")

        results = []
        failed_urls = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {executor.submit(self._scrape_single_url, url): url for url in urls}
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    if result['status'] == 'success':
                        results.append(result)
                    else:
                        failed_urls.append(url)
                        results.append(result)
                    logger.info(f"Completed: {url}")
                except Exception as e:
                    logger.error(f"Unexpected error for {url}: {e}")
                    failed_urls.append(url)
                    results.append({'url': url, 'status': 'error', 'error': str(e)})

        self.end_time = datetime.now()
        self.results = results
        self.failed_urls = failed_urls
        return results

    def run(self):
        """Jalankan scraper dengan daftar URL Adobe"""
        urls = [
            'https://www.adobe.com',
            'https://www.adobe.com/products/photoshop.html',
            'https://www.adobe.com/products/illustrator.html',
            'https://www.adobe.com/creativecloud.html',
            'https://www.adobe.com/products/premiere.html',
            'https://www.adobe.com/products/aftereffects.html',
            'https://www.adobe.com/products/indesign.html',
            'https://www.adobe.com/products/xd.html',
            'https://www.adobe.com/products/acrobat.html',
            'https://www.adobe.com/products/dreamweaver.html',
        ]

        print("=" * 70)
        print("PRODUCTION SCRAPER - Adobe.com")
        print(f"   Total URLs: {len(urls)}")
        print(f"   Max Workers: {self.max_workers}")
        print(f"   Retries: {self.retries}")
        print(f"   Proxy: {config.PROXY_HOST}")
        print("=" * 70)

        results = self.scrape_batch(urls)

        # Hitung statistik
        success = [r for r in results if r.get('status') == 'success']
        failed = [r for r in results if r.get('status') != 'success']
        duration = (self.end_time - self.start_time).total_seconds()

        print("\n" + "=" * 70)
        print("SCRAPING STATISTICS")
        print("=" * 70)
        print(f"Duration: {duration:.2f}s")
        print(f"Total URLs: {len(results)}")
        print(f"Success: {len(success)}")
        print(f"Failed: {len(failed)}")
        print(f"Success Rate: {len(success)/len(results)*100:.1f}%")

        if failed:
            print("\nFailed URLs:")
            for f in failed:
                print(f"   - {f.get('url', 'Unknown')}")

        # Simpan ke JSON
        output = {
            'timestamp': datetime.now().isoformat(),
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'duration_seconds': duration,
            'total_urls': len(results),
            'success_count': len(success),
            'failed_count': len(failed),
            'success_rate': len(success)/len(results)*100,
            'failed_urls': [r.get('url', '') for r in results if r.get('status') != 'success'],
            'results': results
        }

        with open('production_results.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print("\nResults saved to production_results.json")
        print("=" * 70)


if __name__ == '__main__':
    scraper = ProductionScraper(max_workers=2, retries=3)
    scraper.run()