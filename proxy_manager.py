"""
proxy_manager.py - Manajer Proxy Multi-Provider
Mendukung: WebShare (free), BrightData, Oxylabs
"""

import os
import random
from dotenv import load_dotenv

load_dotenv()

class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.current_index = 0
        self._load_proxies()
    
    def _load_proxies(self):
        """Muat semua proxy dari environment variable"""
        
        # 1. WebShare (Free)
        ws_host = os.getenv('PROXY_HOST')
        ws_user = os.getenv('PROXY_USER')
        ws_pass = os.getenv('PROXY_PASS')
        if ws_host and ws_user and ws_pass:
            self.proxies.append({
                'name': 'WebShare',
                'host': ws_host,
                'user': ws_user,
                'pass': ws_pass,
                'url': f"http://{ws_user}:{ws_pass}@{ws_host}"
            })
        
        # 2. BrightData (Residential - Premium)
        bd_host = os.getenv('BRIGHTDATA_HOST')
        bd_user = os.getenv('BRIGHTDATA_USER')
        bd_pass = os.getenv('BRIGHTDATA_PASS')
        if bd_host and bd_user and bd_pass:
            self.proxies.append({
                'name': 'BrightData',
                'host': bd_host,
                'user': bd_user,
                'pass': bd_pass,
                'url': f"http://{bd_user}:{bd_pass}@{bd_host}"
            })
        
        # 3. Oxylabs (Residential - Premium)
        ox_host = os.getenv('OXYLABS_HOST')
        ox_user = os.getenv('OXYLABS_USER')
        ox_pass = os.getenv('OXYLABS_PASS')
        if ox_host and ox_user and ox_pass:
            self.proxies.append({
                'name': 'Oxylabs',
                'host': ox_host,
                'user': ox_user,
                'pass': ox_pass,
                'url': f"http://{ox_user}:{ox_pass}@{ox_host}"
            })
        
        if not self.proxies:
            raise Exception("Tidak ada proxy yang dikonfigurasi. Cek file .env")
        
        print(f"✅ Loaded {len(self.proxies)} proxy providers: {[p['name'] for p in self.proxies]}")
    
    def get_proxy(self):
        """Dapatkan proxy saat ini (round-robin)"""
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy
    
    def get_all(self):
        """Dapatkan semua proxy"""
        return self.proxies

# Singleton
_proxy_manager = None

def get_proxy_manager():
    global _proxy_manager
    if _proxy_manager is None:
        _proxy_manager = ProxyManager()
    return _proxy_manager