<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Orbitron&weight=900&size=48&duration=3000&pause=1000&color=00FFFF&center=true&vCenter=true&width=700&height=80&lines=SANDI+RIDWAN" alt="Sandi Ridwan" />

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=16&duration=2500&pause=800&color=00FFFF&center=true&vCenter=true&multiline=true&width=860&height=50&lines=Akamai+Bot+Manager+%2B+NuData+Bypass+%E2%86%92+Adobe.com+%E2%86%92+90%25+Success" alt="Tagline" />

<br/>

![Python](https://img.shields.io/badge/Python-3.12-00FFFF?style=for-the-badge&logo=python&logoColor=black)
![curl_cffi](https://img.shields.io/badge/curl__cffi-Chrome124_TLS-00FFFF?style=for-the-badge&logo=curl&logoColor=black)
![Playwright](https://img.shields.io/badge/Playwright-Stealth-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)
![Akamai](https://img.shields.io/badge/Akamai_Bot_Manager-Bypassed-FF4500?style=for-the-badge&logo=akamai&logoColor=white)
![NuData](https://img.shields.io/badge/NuData_Security-Bypassed-6A0DAD?style=for-the-badge&logo=datadog&logoColor=white)
![Proxy](https://img.shields.io/badge/Proxy-Multi--Provider-00FFFF?style=for-the-badge&logo=cloudflare&logoColor=black)
![Success](https://img.shields.io/badge/Success_Rate-90%25-00FF00?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-0D1117?style=for-the-badge)

</div>

---

```
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║      █████╗ ██╗  ██╗ █████╗ ███╗   ███╗ █████╗ ██╗                     ║
║     ██╔══██╗██║ ██╔╝██╔══██╗████╗ ████║██╔══██╗██║                     ║
║     ███████║█████╔╝ ███████║██╔████╔██║███████║██║                     ║
║     ██╔══██║██╔═██╗ ██╔══██║██║╚██╔╝██║██╔══██║██║                     ║
║     ██║  ██║██║  ██╗██║  ██║██║ ╚═╝ ██║██║  ██║██║                     ║
║     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝                     ║
║                                                                          ║
║      +  N U D A T A   B Y P A S S   S U I T E  ·  Adobe.com  ·  90%    ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## 🎬 Demo

<div align="center">
  <a href="#">
    <img src="thumbnail.png" width="860" alt="Watch full demo" />
  </a>
  <br/>
  <sub><i>Click to watch — TLS bypass live, stealth browser signup flow, 90% success run</i></sub>
</div>

<br/>

<div align="center">
  <video src="PASTE_YOUR_VIDEO_LINK_HERE"
         width="860"
         controls>
  </video>
  <br/>
  <sub><i>Full walkthrough — Akamai + NuData bypass, Adobe.com production target</i></sub>
</div>

---

## 🧠 Overview

**Adobe Akamai & NuData Bypass Suite** is a portfolio-grade anti-bot research project that defeats two of the most sophisticated bot-detection stacks in production use — **Akamai Bot Manager v3** (TLS/HTTP2 fingerprinting) and **NuData Security** (behavioral biometrics) — validated live against **Adobe.com**, not a sandbox.

<div align="center">

| Metric | Value |
|-------:|:------|
| 🎯 Target | Adobe.com — protected by Akamai Bot Manager v3 + NuData Security |
| 🔐 Layer 1 Bypassed | Akamai — TLS/HTTP2 fingerprint (JA3/JA4) via `curl_cffi` |
| 🎭 Layer 2 Bypassed | NuData — behavioral biometrics via Playwright Stealth |
| 📊 Scrape Success | **9 / 10 pages — 90%** (datacenter proxy) |
| 🚀 Registration Success | Requires residential proxy (BrightData/Oxylabs) — documented limitation |
| 🔑 Session Trick | Dynamic `x-debug-id` per session via `uuid4()` — static ID = instant Access Denied |
| 🌐 Proxy Layer | Multi-provider fallback: WebShare → Decodo → BrightData/Oxylabs |
| 🧵 Concurrency | ThreadPoolExecutor + retry logic + browser profile rotation (chrome124/123/120, edge101) |
| 📁 Output | `production_results.json` (9/10) · `adobe_homepage.html` · `adobe_stealth_test.png` · `adobe_stealth_demo.png` · `registration_url.txt` + `registration_params.json` |

</div>

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                         run.py (ORCHESTRATOR)                        │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
          ┌────────────────────┴─────────────────────┐
          ▼                                           ▼
┌─────────────────────────┐               ┌───────────────────────────┐
│  production_scraper.py  │               │  adobe_actions.py         │
│  curl_cffi impersonate   │               │  Login & Signup           │
│  chrome124 · 10 URLs     │               │  Playwright Stealth       │
│  ThreadPoolExecutor      │               │  human-mimicry behavior   │
└────────────┬─────────────┘               └─────────────┬─────────────┘
             │                                            │
             ▼                                            ▼
┌──────────────────────────────────────────────────────────────────────┐
│                       proxy_manager.py                                │
│   WebShare (datacenter, implemented) → Decodo (residential trial)     │
│   Fallback chain · round-robin rotation · domain memory per target    │
│   ⚠️ Production recommendation: BrightData / Oxylabs (residential)    │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
                  ✅ 90% scrape success · session capture
```

---

## ⚡ Technical Challenges Solved

### Challenge 1 — Akamai TLS/HTTP2 Fingerprint (JA3/JA4)

**Problem:** Standard `requests` gets dropped at the SSL handshake itself — `ConnectionResetError(10054)` before any HTTP request is even sent. Akamai fingerprints the TLS ClientHello, not the headers.

**Solution:** `curl_cffi` with Chrome impersonation replicates the exact TLS handshake — cipher suites, extensions, TLS version negotiation — byte-for-byte like real Chrome. Profile rotation (`chrome124`, `chrome123`, `chrome120`, `edge101`) plus a **domain memory** layer — remembering which profile worked best for a given target — keeps fingerprint tracking from converging on one signature.

```python
# ❌ requests — blocked at SSL layer, before HTTP exists
import requests
response = requests.get('https://www.adobe.com/')
# ConnectionResetError(10054) — JA3 fingerprint detected

# ✅ curl_cffi — exact Chrome TLS handshake
from curl_cffi import requests
session = requests.Session(impersonate="chrome124")
response = session.get('https://www.adobe.com/')
# Status: 200 — TLS handshake passed

# Domain memory — reuse the profile that already worked for this domain
best_profile = domain_memory.get("adobe.com", default="chrome124")
if best_profile_failed:
    domain_memory.rotate("adobe.com", next_profile="chrome123")
```

---

### Challenge 2 — NuData Behavioral Detection (Not Just Headers)

**Problem:** Even with a perfect TLS fingerprint, NuData still flagged automation through behavior — uniform typing speed, straight-line mouse movement, zero scroll activity. NuData scores *how* you interact, not just *what* you send.

**Solution:** Playwright Stealth patches `navigator.webdriver` and friends, then human-behavior simulation handles the rest: randomized typing delay, zig-zag mouse movement, smooth scroll with random stops.

```python
# Stealth patches
page.add_init_script("""
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    window.chrome = { runtime: {} };
    Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
""")

# Realistic viewport — matches real device profile
page.set_viewport_size({"width": 1920, "height": 1080})

# Human-like typing — 60-200ms per character, not uniform
for char in email:
    page.keyboard.type(char, delay=random.randint(60, 200))

# Zig-zag mouse movement, not a straight line to target
page.mouse.move(x + offset_x, y + offset_y, steps=random.randint(5, 10))

# Smooth scroll with random stops — not an instant jump
page.evaluate("window.scrollTo({top: Math.random() * 200, behavior: 'smooth'})")
```

---

### Challenge 3 — Dynamic `x-debug-id` + Session Fingerprint (Adobe-Specific)

**Problem:** A hardcoded `x-debug-id` copied straight from DevTools triggers an immediate Access Denied. Adobe tracks this header as a session identifier — reusing it across sessions is itself a signal of automation.

**Solution:** Generate a fresh UUID per session and inject it into every fetch/XHR request via Playwright's `page.add_init_script()`. Pair it with the correct static client header — `x-ims-clientid: SunbreakWebUI1` for Adobe's web app.

```python
# ❌ Hardcoded — same ID across sessions = Access Denied
x-debug-id: 3426dc24-b348-43c5-8b20-339212120538

# ✅ Dynamic per session
import uuid
DEBUG_ID = str(uuid.uuid4())
# Injected into all fetch/XHR via page.add_init_script()

# Static client header — always this value for Adobe web app
x-ims-clientid: SunbreakWebUI1
```

**Analytics sequence:** Adobe fires a strict 5-event sequence to `/signin/v1/audit` during signup — skipping or reordering any of them is a secondary detection signal:

```
1. Account:IMS:GetStarted:OnLoad          (page load)
2. Account:IMS:GetStarted:CreateAccountClick   (click "Create account")
3. Account:IMS:CreateAccount:OnLoad       (registration page)
4. Account:IMS:CreateAccount:SignUpSplit  (method selection)
5. Account:IMS:SignUpFlow:Start           (registration flow begins)
```

Each event payload requires specific fields — `fv.version`, `clientId`, and a structured `message` object — matched to what a real browser sends.

**Registration URL capture:** Opening `account.adobe.com` → clicking "Create an account" redirects to `auth.services.adobe.com/signup` carrying a full parameter set captured via Playwright intercept:

```python
# Captured via Playwright network intercept, parsed from redirect URL
{
    "state": "...",        # JSON blob containing jslibver + nonce
    "nonce": "...",        # unique per session — must be parsed, not reused
    "client_id": "...",
    "scope": "...",
    "redirect_uri": "..."
}
# Saved to registration_url.txt + registration_params.json
```

---

### Challenge 4 — Datacenter Proxy Blocked on High-Risk Actions

**Problem:** WebShare datacenter IPs pass fine for read-only scraping (90% success) but get blocked outright the moment a high-risk action — account registration — is attempted. Even a perfectly-formed request fails if the IP reputation is wrong.

**Solution:** Multi-provider proxy manager — datacenter proxy for scraping, residential proxy reserved for registration/signup flows. Documented as a hard requirement, not a workaround.

```python
# proxy_manager.py — fallback chain by risk tier
PROXY_TIERS = {
    "scrape": ["webshare"],                       # datacenter OK — 90% success
    "signup": ["decodo", "brightdata", "oxylabs"]  # residential required
}

def get_proxy(action_type: str):
    for provider in PROXY_TIERS[action_type]:
        if proxy := try_provider(provider):
            return proxy
    raise ProxyExhaustedError(action_type)
```

---

## 📁 File Structure

```
akamai-bypass-adobe/
├── run.py                    # ⭐ Main Orchestrator
├── production_scraper.py     # Production scraper — curl_cffi + ThreadPoolExecutor
├── adobe_actions.py          # Login & Signup — Playwright Stealth
├── proxy_manager.py          # Multi-provider proxy manager + fallback chain
├── stealth_browser.py        # Playwright stealth patches + human behavior sim
├── http_client.py            # curl_cffi session wrapper
├── config.py                 # Load .env
├── test_proxy.py             # Proxy connection test
├── test_adobe.py             # Adobe bypass test
├── .env                       # 🔐 Configuration
├── requirements.txt
├── registration_url.txt      # Captured registration URL
├── registration_params.json  # state / nonce / client_id extracted
├── production_results.json   # 9/10 success — full run output
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/sandiridwan/akamai-bypass-adobe.git
cd akamai-bypass-adobe
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure Environment

```env
PROXY_HOST=p.webshare.io:80
PROXY_USER=your_username
PROXY_PASS=your_password
TARGET_URL=https://www.adobe.com
BROWSER_PROFILE=chrome124
```

### 3. Run

```bash
python run.py
```

---

## 📊 Live Run Results

```
Pipeline run — Adobe.com scrape (10 URLs)

✅ https://www.adobe.com                              Success
✅ https://www.adobe.com/products/photoshop.html       Success
✅ https://www.adobe.com/products/illustrator.html     Success
✅ https://www.adobe.com/creativecloud.html            Success
✅ https://www.adobe.com/products/premiere.html        Success
✅ https://www.adobe.com/products/aftereffects.html    Success
✅ https://www.adobe.com/products/indesign.html        Success
✅ https://www.adobe.com/products/acrobat.html         Success
✅ https://www.adobe.com/products/dreamweaver.html     Success
❌ https://www.adobe.com/products/xd.html              Failed (datacenter proxy detected)
──────────────────────────────────────────────────────────────
   Success rate: 9/10 — 90%  ·  Potential 99%+ with residential proxy
```

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|-------|------------|
| **Language** | Python 3.12 |
| **HTTP Client** | curl_cffi — TLS fingerprint spoofing, `impersonate="chrome124"` |
| **Browser Automation** | Playwright + playwright-stealth |
| **Proxy** | WebShare (datacenter) · Decodo / BrightData / Oxylabs (residential) |
| **Concurrency** | ThreadPoolExecutor |
| **Parsing** | BeautifulSoup4 · lxml |
| **Config** | python-dotenv |

</div>

---

## 🏆 Why This Matters

<div align="center">

| Security System | Companies Using It | Freelancer Market Value |
|---|---|---|
| Akamai Bot Manager | Adobe, Salesforce, eBay, PayPal, Airbnb | $50–100/hr |
| NuData Security | Adobe, Mastercard, Discover, Experian | $75–150/hr |
| Combined (both layers) | Adobe, Mastercard, major banks | $100–200/hr |

</div>

This project proves capability that typically requires enterprise-grade tooling and dedicated security engineering — bypassed with an open-source stack and documented, reproducible technique.

---

## 📝 Lessons Learned

1. **Akamai ≠ Cloudflare** — Akamai operates at the SSL layer (JA3/JA4); Cloudflare operates at the HTTP layer (403, CAPTCHA). Different bypass approach required for each.
2. **Datacenter proxies fail on high-risk actions** — Perfect headers don't matter if the IP reputation is wrong. Residential proxy is mandatory for signup/registration.
3. **`x-debug-id` must be dynamic** — Adobe tracks session IDs; reusing one is itself a tell.
4. **NuData is behavioral, not header-based** — Simulating human behavior matters as much as spoofing headers.
5. **Screenshots are the best debugging tool** — When Playwright silently fails, a screenshot reveals the real page state instantly.

---

## 👤 Author

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Orbitron&weight=700&size=20&duration=3000&pause=1000&color=00FFFF&center=true&vCenter=true&width=400&lines=Sandi+Ridwan" />

**Data Automation Engineer · Web Scraping Specialist · AI Automation Builder**

📍 Palu, Central Sulawesi, Indonesia

[![Upwork](https://img.shields.io/badge/Upwork-Hire_Me-00FFFF?style=for-the-badge&logo=upwork&logoColor=black)](https://www.upwork.com/freelancers/sandiridwan)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/sandi-ridwan)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/SandiRidwan)

</div>

---

<div align="center">
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=12&duration=4000&pause=1000&color=00FFFF&center=true&vCenter=true&width=700&lines=Akamai+Bypassed+%E2%9C%85+%7C+NuData+Bypassed+%E2%9C%85+%7C+90%25+Success+%7C+Adobe.com+%7C+Building+things+that+shouldn%27t+be+possible" />
</div>

---

## 📄 License

MIT License — Educational and testing purposes only.
