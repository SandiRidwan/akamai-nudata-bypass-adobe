"""
run.py - Orchestrator Utama
Menjalankan semua fitur: Scraping, Login, Registrasi
"""

import sys
import json
from datetime import datetime
from production_scraper import ProductionScraper
from adobe_actions import AdobeActions
from proxy_manager import get_proxy_manager

def show_menu():
    print("=" * 70)
    print("🎯 ADOBE SUPER SCRAPER - Orchestrator")
    print("=" * 70)
    print("1. Jalankan Scraping Production (10 URL)")
    print("2. Simulasi Login (butuh email & password)")
    print("3. Simulasi Registrasi Akun Baru (otomatis generate email)")
    print("4. Jalankan SEMUA (Scrape -> Login -> Register)")
    print("5. Lihat Hasil Scraping Terakhir")
    print("0. Keluar")
    print("=" * 70)

def run_scraping():
    print("\n🚀 Memulai Production Scraping...")
    scraper = ProductionScraper(max_workers=2, retries=3)
    scraper.run()
    print("\n✅ Scraping selesai. Cek production_results.json")

def run_login():
    print("\n🔐 Simulasi Login Adobe")
    email = input("Masukkan Email: ")
    password = input("Masukkan Password: ")
    
    actions = AdobeActions(headless=False)
    try:
        success, page = actions.login(email, password)
        if success:
            print("✅ Login berhasil!")
            # Screenshot
            page.screenshot(path="login_success.png")
            print("📸 Screenshot disimpan: login_success.png")
        else:
            print("❌ Login gagal.")
    finally:
        actions.close()

def run_register():
    import random
    import string
    
    print("\n📝 Simulasi Registrasi Adobe")
    # Generate email random
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    email = f"test_{random_str}@mailinator.com"
    password = "P@ssw0rd123!" + ''.join(random.choices(string.digits, k=4))
    
    print(f"📧 Email: {email}")
    print(f"🔑 Password: {password}")
    print("📝 Nama: Test User")
    
    confirm = input("Lanjutkan registrasi? (y/n): ")
    if confirm.lower() != 'y':
        return
    
    actions = AdobeActions(headless=False)
    try:
        success, page = actions.signup(email, password, "Test", "User")
        if success:
            print("✅ Registrasi berhasil!")
            page.screenshot(path="signup_success.png")
            print("📸 Screenshot disimpan: signup_success.png")
            
            # Simpan credential ke file
            with open("new_account.txt", "w") as f:
                f.write(f"Email: {email}\nPassword: {password}\n")
            print("💾 Credential disimpan di new_account.txt")
        else:
            print("❌ Registrasi gagal.")
    finally:
        actions.close()

def run_all():
    print("\n🔥 Menjalankan SEMUA fitur...")
    print("=" * 70)
    
    # 1. Scraping
    run_scraping()
    
    # 2. Login Demo (skip, karena butuh input manual)
    print("\n⏭️  Skip Login Demo (butuh input manual)")
    
    # 3. Registrasi Demo (otomatis)
    run_register()
    
    print("\n🎉 Semua selesai!")

def show_results():
    try:
        with open('production_results.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("\n📊 Hasil Scraping Terakhir:")
        print(f"   Waktu: {data['timestamp']}")
        print(f"   Total URL: {data['total_urls']}")
        print(f"   ✅ Berhasil: {data['success_count']}")
        print(f"   ❌ Gagal: {data['failed_count']}")
        print(f"   📈 Success Rate: {data['success_rate']:.1f}%")
        print("\n   URL Berhasil:")
        for r in data['results']:
            if r['status'] == 'success':
                print(f"      - {r['url']} ({r['title'][:40]}...)")
        if data['failed_urls']:
            print("\n   ❌ URL Gagal:")
            for f in data['failed_urls']:
                print(f"      - {f}")
    except FileNotFoundError:
        print("❌ Belum ada hasil scraping. Jalankan scraping dulu (Menu 1).")
    except Exception as e:
        print(f"❌ Error membaca file: {e}")

def main():
    while True:
        show_menu()
        choice = input("Pilih menu (0-5): ")
        
        if choice == '0':
            print("👋 Sampai jumpa!")
            break
        elif choice == '1':
            run_scraping()
        elif choice == '2':
            run_login()
        elif choice == '3':
            run_register()
        elif choice == '4':
            run_all()
        elif choice == '5':
            show_results()
        else:
            print("❌ Pilihan tidak valid.")
        
        input("\nTekan Enter untuk kembali ke menu...")

if __name__ == '__main__':
    main()