import time
import random
import os
from DrissionPage import ChromiumPage, ChromiumOptions

# --- AYARLAR ---
DOMAIN = "barashhelvadzhaoglu.com"
GSC_RESOURCE = f"sc-domain:{DOMAIN}"
BASE_PATH = "/Users/user/Documents/myblog/urlinspection/"
DEBUG_FILE = os.path.join(BASE_PATH, "gsc_capture.html")

# TÜM LİSTE (Taranmış ve N/A olanların tamamı)
ALL_URLS = [
    # N/A Olanlar
    "https://barashhelvadzhaoglu.com/de/about/",
    "https://barashhelvadzhaoglu.com/de/posts/",
    "https://barashhelvadzhaoglu.com/de/tags/active-directory/",
    "https://barashhelvadzhaoglu.com/de/tags/automatisierung/",
    "https://barashhelvadzhaoglu.com/de/tags/betrieb/",
    "https://barashhelvadzhaoglu.com/de/tags/it-infrastruktur/",
    "https://barashhelvadzhaoglu.com/de/tags/netzwerkingenieurwesen/",
    "https://barashhelvadzhaoglu.com/de/tags/operative-architektur/",
    "https://barashhelvadzhaoglu.com/de/tags/pki/",
    "https://barashhelvadzhaoglu.com/de/tags/rechenzentrum/",
    "https://barashhelvadzhaoglu.com/de/tags/systemdenken/",
    "https://barashhelvadzhaoglu.com/de/tags/zabbix/",
    "https://barashhelvadzhaoglu.com/en/architecture/core-network-is-not-a-product-list/",
    "https://barashhelvadzhaoglu.com/en/posts/",
    "https://barashhelvadzhaoglu.com/en/projects/",
    "https://barashhelvadzhaoglu.com/en/tags/network-strategy/",
    "https://barashhelvadzhaoglu.com/en/tags/switching/",
    "https://barashhelvadzhaoglu.com/tr/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/",
    "https://barashhelvadzhaoglu.com/tr/posts/",
    "https://barashhelvadzhaoglu.com/tr/projeler/",
    "https://barashhelvadzhaoglu.com/tr/tags/ürün-seçimi/",
    "https://barashhelvadzhaoglu.com/tr/tags/802.1x/",
    "https://barashhelvadzhaoglu.com/tr/tags/active-directory/",
    "https://barashhelvadzhaoglu.com/tr/tags/kurumsal-ağ/",
    "https://barashhelvadzhaoglu.com/tr/tags/kurumsal-tasarım/",
    "https://barashhelvadzhaoglu.com/tr/tags/network-mimarisi/",
    "https://barashhelvadzhaoglu.com/tr/tags/network-tasarımı/",
    "https://barashhelvadzhaoglu.com/tr/tags/operasyonel-mimari/",
    "https://barashhelvadzhaoglu.com/tr/tags/otomasyon/",
    "https://barashhelvadzhaoglu.com/tr/tags/pki/",
    "https://barashhelvadzhaoglu.com/tr/tags/proaktif-it/",
    "https://barashhelvadzhaoglu.com/tr/tags/siber-güvenlik/",
    "https://barashhelvadzhaoglu.com/tr/tags/sistem-düşüncesi/",
    # Daha Önce Taranmış Olanlar (Kontrol amaçlı)
    "https://barashhelvadzhaoglu.com/en/architecture/it-infrastructure-not-a-collection-of-products/",
    "https://barashhelvadzhaoglu.com/de/architecture/network-product-selection-strategy/",
    "https://barashhelvadzhaoglu.com/en/technology/identity-based-microsegmentation-8021x/",
    "https://barashhelvadzhaoglu.com/tr/architecture/zero-trust-architecture-behaviors/",
    "https://barashhelvadzhaoglu.com/de/technology/identity-based-microsegmentation-8021x/",
    "https://barashhelvadzhaoglu.com/tr/technology/identity-based-microsegmentation-8021x/",
    "https://barashhelvadzhaoglu.com/en/architecture/monitoring-not-just-seeing/",
    "https://barashhelvadzhaoglu.com/tr/architecture/zero-trust-bir-urun-degil/"
]

def kota_kontrol(page):
    """HTML içinde kota aşımı mesajlarını arar."""
    error_msgs = ["exceeded your daily quota", "quota exceeded", "try again tomorrow", "couldn't process"]
    page_content = page.html.lower()
    for msg in error_msgs:
        if msg in page_content:
            return True
    return False

def debug_kaydet(page):
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)
    with open(DEBUG_FILE, "w", encoding="utf-8") as f:
        f.write(page.html)

def google_index_otomasyon():
    print(f"--- {DOMAIN} Full Otomasyon Başlatıldı ---")
    random.shuffle(ALL_URLS)
    
    co = ChromiumOptions()
    page = ChromiumPage(co)
    page.get(f'https://search.google.com/search-console?resource_id={GSC_RESOURCE}')
    
    print("GSC Yükleniyor (10 sn)...")
    time.sleep(10)

    for url in ALL_URLS:
        try:
            # İşlem öncesi kota kontrolü
            if kota_kontrol(page):
                print("!!! KOTA HATASI: İşlem durduruldu.")
                break

            print(f"\n[SIRADAKİ]: {url}")
            search_input = page.ele('tag:input@@placeholder^Inspect any URL')
            if not search_input: search_input = page.ele('@type=text')
            search_input.clear()
            search_input.input(url + '\n')
            
            # Database check
            print("Google veritabanı kontrolü (10 sn)...")
            time.sleep(10)
            
            if "URL is on Google" in page.html:
                print(">>> ATLANIYOR: Zaten dizinde.")
                continue
            
            if kota_kontrol(page):
                print("!!! KOTA HATASI: Arama sonrası tespit edildi.")
                break

            # Live Test (20 sn)
            print("Canlı Test (20 sn)...")
            time.sleep(20)
            
            if kota_kontrol(page):
                print("!!! KOTA HATASI: Test sonrası tespit edildi.")
                break

            # Request Indexing
            click_js = """
            (function() {
                const buttons = Array.from(document.querySelectorAll('div[role="button"]'));
                const target = buttons.find(b => b.innerText.includes('REQUEST INDEXING'));
                if (target && !target.disabled) { target.click(); return "CLICKED"; }
                return "NOT_FOUND";
            })()
            """
            
            if page.run_js(click_js) == "CLICKED":
                print(">>> TALEP GÖNDERİLDİ: Onay bekleniyor (20 sn)...")
                time.sleep(20)
                
                if kota_kontrol(page):
                    print("!!! KOTA HATASI: Gönderim sırasında oluştu.")
                    break

                # Got it
                page.run_js("const btn = Array.from(document.querySelectorAll('span, div')).find(s => s.innerText.includes('Got it') || s.innerText.includes('GOT IT')); if(btn) btn.click();")
                print(">>> ONAY ALINDI.")
                
            # Güvenli mola
            mola = random.randint(15, 30)
            print(f"Mola veriliyor: {mola} sn...")
            time.sleep(mola)

        except Exception as e:
            print(f"Hata oluştu: {e}")
            debug_kaydet(page)
            continue

if __name__ == "__main__":
    google_index_otomasyon()