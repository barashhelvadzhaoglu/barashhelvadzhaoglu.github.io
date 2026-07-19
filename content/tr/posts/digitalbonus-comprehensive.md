---
title: "Bavyera'daki Küçük İşletmeler İçin BT Güvenlik Yükümlülükleri — ve Digitalbonus Bayern'in Maliyetlerin %50'sine Kadarını Nasıl Karşıladığı"
seoTitle: "DSGVO BT Güvenliği KOBİ Bavyera | Digitalbonus 2026 — Firewall, VLAN, Yedekleme, E-posta"
description: "Bavyera'da yasal olarak hangi BT güvenlik önlemleri zorunludur? Firewall, ağ ayırma, e-posta koruması, yedekleme — yasal dayanaklar ve 7.500 €'ya kadar teşvikle."
date: 2026-04-17
draft: false
showToc: true
TocOpen: false
tags:
  - Digitalbonus Bayern
  - DSGVO
  - BSI IT-Grundschutz
  - Ağ Güvenliği
  - BT Güvenliği
  - KOBİ Münih
keywords:
  - Digitalbonus Bayern 2026
  - DSGVO BT Güvenliği Yükümlülüğü
  - BSI IT-Grundschutz KOBİ
  - Firewall yükümlülüğü küçük işletmeler
  - VLAN ayırma DSGVO
  - Ağ segmentasyonu Bavyera
  - E-posta güvenliği DSGVO
  - Yedekleme yükümlülüğü şirketler
  - BT teşvikleri Bavyera 2026
---

# Küçük İşletmeler İçin BT Güvenlik Yükümlülükleri — ve Digitalbonus Bayern %50'ye Kadarını Nasıl Üstleniyor

Bavyera'daki birçok küçük işletme, BT güvenliğinin büyük şirketleri ilgilendiren bir konu olduğuna inanıyor. Gerçek ise farklıdır: DSGVO (Genel Veri Koruma Yönetmeliği), kişisel veri işleyen **herkes** için geçerlidir — perakendeciden doktor muayenehanesine, otelden kafeye kadar. Ve gereksinimler somut, bağlayıcı ve para cezalarıyla desteklenmiştir.

İyi haber: **Digitalbonus Bayern**, firewall, ağ ayırma, e-posta güvenliği, yedekleme ve daha fazlası için **yatırım maliyetlerinin %50'sine kadarını** iade ediyor. Program Aralık 2027'ye kadar devam etmektedir.

> 💬 **Ücretsiz BT Analizi:** [WhatsApp](https://wa.me/4916098665971) veya [E-posta](mailto:info@barashhelvadzhaoglu.com)
> Altyapınızı ücretsiz kontrol ediyoruz — sipariş yok, ürün satışı yok.

---

## Yasal Temel: Gerçekte Ne Zorunludur?

### DSGVO Madde 32 — İşleme Güvenliği

**Kaynak:** [Art. 32 DSGVO](https://gdpr.eu/article-32-security-of-processing/)

> „Veri sorumlusu ve veri işleyen, riske uygun bir koruma düzeyi sağlamak için uygun teknik ve organizasyonel önlemleri alır."

Bu şu anlama gelir: Kişisel verileri işleyen her şirket — yani isimler, e-posta adresleri, sağlık verileri, rezervasyon bilgileri — **teknik koruma önlemleri** oluşturmalıdır. Tavsiye olarak değil, **yasal bir yükümlülük** olarak.

### BSI IT-Grundschutz — Teknik Standart

**Kaynak:** [BSI IT-Grundschutz Kompendium](https://www.bsi.bund.de/grundschutz)

Federal Bilgi Güvenliği Ofisi (BSI), BT-Grundschutz'da DSGVO anlamında "uygun teknik önlemlerin" ne olduğunu somut olarak tanımlar. Alman mahkemeleri ve veri koruma yetkilileri denetimlerde bu standardı baz almaktadır.

**BSI IT-Grundschutz küçük işletmeler için geçerli mi?**
Resmi olarak gönüllüdür — ancak: DSGVO "teknolojinin güncel durumunu" (Stand der Technik) zorunlu kılar. Almanya'da bu durum BSI IT-Grundschutz'a tekabül eder. Buna uymayanlar, bir denetim sırasında neden farklı önlemlerinin eşdeğer olduğunu kanıtlamak zorunda kalabilirler.

---

## Somut Olarak Ne Zorunludur — Önlem Önlem Detaylar

### 1. Firewall — BSI NET.3.2 Uyarınca Yükümlülük

**Yasal Dayanak:** BSI IT-Grundschutz, Modül [NET.3.2 Firewall](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/Kompendium/Bausteine/Infrastruktur/NET_3_2_Firewall.pdf)

BSI NET.3.2.A2 şunu şart koşar:
> „Güvenlik duvarı için bir kurallar dizisi oluşturulmalıdır. Dış ağdan iç ağa otomatik olarak hiçbir veri trafiği girmemelidir."

BSI NET.3.2.A9 ekler:
> „Güvenlik duvarı tüm önemli olayları günlüğe kaydetmelidir (loglama)."

**Pratikte ne anlama gelir:**
- Basit bir DSL yönlendirici (Router), BSI anlamında bir firewall **değildir**.
- Bir UTM-Firewall (örneğin Fortinet FortiGate, Palo Alto) gereklidir.
- Firewall, sadece internet ve iç ağ arasında değil, **tüm** ağ bölgeleri arasında durmalıdır.

**Digitalbonus ile teşvik edilebilir mi:** ✅ Evet — Donanım ve yapılandırma hizmeti.

---

### 2. Ağ Segmentasyonu (VLAN'lar) — BSI NET.1.1 ve DSGVO Madde 25 Uyarınca Yükümlülük

**Yasal Dayanak:**
- BSI IT-Grundschutz, Modül [NET.1.1 Ağ Mimarisi ve Tasarımı](https://www.bsi.bund.de/grundschutz)
- DSGVO Madde 25 — Tasarım Yoluyla Veri Koruma (Privacy by Design)

> „Kişisel veriler, yalnızca görevleri için erişime ihtiyaç duyan kişilerin erişebileceği şekilde işlenmelidir."

**Pratikte ne anlama gelir:**

Aşağıdaki cihaz sınıfları **ayrı ağlarda (VLAN'lar)** çalıştırılmalıdır:

| Ağ Segmenti | İçinde Ne Yer Alır | Ayrım Olmazsa Risk |
|---|---|---|
| **Çalışan Ağı** | PC'ler, Laptoplar | Müşteri verilerine erişim |
| **Sunucu / NAS** | Dosya sunucusu, Yedekleme sistemi | Saldırı anında veri kaybı |
| **IoT Cihazları** | Yazıcılar, IP Kameralar, Smart-TV, UPS | Bilinen açıklar, güncelleme yok |
| **Misafir WLAN** | Müşteriler, Hastalar, Otel misafirleri | Dahili sistemlere erişim |
| **Kasa / POS** | Kart terminali, Kasa sistemi | PCI DSS yükümlülüğü, ödeme verileri |

**Yazıcılar neden tehlikelidir:**
IP yazıcılar genellikle eski donanım yazılımlarına sahiptir ve otomatik güvenlik güncellemeleri yoktur. Muhasebe PC'si ile aynı ağdaki ele geçirilmiş bir yazıcı, saldırganlara tüm verilere doğrudan erişim sağlar.

**IP Kameralar neden tehlikelidir:**
Ucuz IP kameralar (Hikvision, Dahua), şirket ağına giriş noktası olarak uluslararası hacker saldırılarında düzenli olarak kötüye kullanılmaktadır.

**Digitalbonus ile teşvik edilebilir mi:** ✅ Evet — Yönetilebilir anahtarlar (Managed Switches), Access Pointler, yapılandırma hizmeti.

---

### 3. Captive Portal ve Log Saklama ile Misafir WLAN

**Yasal Dayanak:**
- DSGVO Madde 32 — Teknik Koruma Önlemleri
- § 100 TKG (Telekomünikasyon Yasası) — Trafik Verileri
- BSI IT-Grundschutz NET.2.2 — WLAN Kullanımı

**Ne zorunludur:**

**a) Tam İzolasyon:**
Misafir WLAN'ın dahili sistemlere **hiçbir** erişimi olmamalıdır. Bir otel misafiri veya bekleme odasındaki bir hasta; rezervasyon sistemlerine, yazıcılara veya çalışan dosyalarına erişememelidir.

**b) Bağlantı Günlükleri — 12 Ay Saklama Zorunluluğu:**
Halka açık WLAN sunanlar, olası resmi talepler için bağlantı verilerini (IP adresi, bağlantı zamanı, bağlantı süresi) **12 ay** boyunca saklamalıdır.

**c) DSGVO Onaylı Captive Portal:**
Giriş sırasında misafir, veri işleme hakkında bilgilendirilmeli ve aktif olarak onay vermelidir.

**Teknik Uygulama:**
Bağlantı logları firewall (örn. FortiGate) tarafından kaydedilir ve otomatik olarak bir NAS cihazına aktarılır — orada 12 ay boyunca saklanır.

**Digitalbonus ile teşvik edilebilir mi:** ✅ Evet — WLAN donanımı ve yapılandırması.

---

### 4. E-posta Güvenliği — BSI APP.5.3 ve DSGVO Madde 32 Uyarınca Yükümlülük

**Yasal Dayanak:**
- BSI IT-Grundschutz, Modül [APP.5.3 Genel E-posta İstemcisi ve Sunucusu](https://www.bsi.bund.de/grundschutz)
- DSGVO Madde 32 — Yetkisiz erişime ve veri kaybına karşı koruma

BSI APP.5.3.A1 şunu şart koşar:
> „E-postalardaki kötü amaçlı yazılımlara karşı koruma önlemleri alınmalıdır. Gelen ve giden e-postalar kötü amaçlı yazılımlara karşı taranmalıdır."

**Pratikte ne anlama gelir:**
Ionos veya Strato gibi sağlayıcılardaki ek koruması olmayan basit bir e-posta kutusu **yeterli değildir**.

Şunlar gereklidir:
- **Spam Filtreleme:** İstenmeyen toplu e-postaların engellenmesi.
- **Zararlı Yazılım Koruması:** Tehlikeli eklerin (Ransomware, Truva atları) tespiti.
- **Phishing Koruması:** Sahte gönderici adreslerinin tespiti (Business Email Compromise).
- **Loglama:** Filtrelenen tüm e-postaların kanıtı.

**Teknik Çözüm:**
Bulut tabanlı bir E-posta Güvenlik Ağ Geçidi (örn. Hornetsecurity, FortiMail Cloud), tüm gelen e-postaları alıcıya ulaşmadan önce bir güvenlik filtresinden geçirir. Mevcut her e-posta sistemiyle çalışır — Office 365, Google Workspace veya basit Webmail.

**Digitalbonus ile teşvik edilebilir mi:** ✅ Evet — BT güvenlik yazılım lisansı olarak (18 aya kadar).

---

### 5. Uç Nokta Koruması (Antivirüs / EDR) — BSI SYS.2.1 ve DSGVO Madde 32 Uyarınca Yükümlülük

**Yasal Dayanak:**
- BSI IT-Grundschutz, Modül [SYS.2.1 Genel İstemci](https://www.bsi.bund.de/grundschutz)
- DSGVO Madde 32 — Zararlı yazılımlar nedeniyle veri kaybına karşı koruma

BSI SYS.2.1.A6 şunu şart koşar:
> „İstemcilerde bir virüsten koruma programı kurulu ve etkin olmalıdır. Virüsten koruma programı düzenli olarak güncellenmelidir."

BSI SYS.2.1.A7 ekler:
> „Güvenlikle ilgili olaylar günlüğe kaydedilmeli ve anormallikler açısından kontrol edilmelidir."

**Pratikte ne anlama gelir:**

Her PC'de —merkezi yönetim olmaksızın— çalışan tekil bir antivirüs programı BSI standardına **uygun değildir**. Şunlar gereklidir:

- **Merkezi Yönetim:** Bir yönetici tüm cihazların koruma durumunu bir bakışta görebilir.
- **Gerçek Zamanlı Koruma:** Tehditler zarar vermeden tespit edilir.
- **Ransomware Koruması:** Kötü amaçlı yazılımlar tarafından dosya şifrelenmesi engellenir.
- **Loglama:** Tüm güvenlik olayları kaydedilir — olası denetimler için.
- **Aylık Raporlar:** Aktif koruma önlemlerinin kanıtı.

**Teknik Çözüm:**
Bitdefender GravityZone veya ESET Protect gibi merkezi olarak yönetilen EDR çözümleri, tüm cihazların merkezi bir panel üzerinden yönetilmesini sağlar.

**Digitalbonus ile teşvik edilebilir mi:** ✅ Evet — Yazılım lisansları ve kurulum hizmeti.

---

### 6. Veri Yedekleme (Backup) — BSI CON.3 ve GoBD Uyarınca Yükümlülük

**Yasal Dayanak:**
- BSI IT-Grundschutz, Modül [CON.3 Veri Yedekleme Konsepti](https://www.bsi.bund.de/grundschutz)
- GoBD (Uygun Defter Tutma İlkeleri) — Yasal saklama yükümlülükleri
- DSGVO Madde 32 — Kişisel verilerin geri yüklenebilirliği

BSI CON.3.A7 şunu şart koşar:
> „Yedeklenen veriler, veri yedeklemesinin işlevselliğini kontrol etmek için düzenli olarak geri yüklenmelidir."

**3-2-1 Kuralı — Sektör Standardı:**
- **3** Veri kopyası
- **2** Farklı depolama ortamı (örn. NAS + Bulut)
- **1** Kopya bina dışında (örn. AWS Frankfurt)

**Pratikte ne anlama gelir:**
Ara sıra manuel olarak üzerine veri yazılan tek bir harici sabit sürücü BSI standardına **uygun değildir**. Şunlar gereklidir:

- **Otomatik günlük yedekleme** — manuel müdahale yok.
- **Şifreleme** — yedekleme ortamı çalınsa bile veriler korunur.
- **Harici kopya** — yangın veya hırsızlık durumunda yedek korunur.
- **Düzenli geri yükleme testleri** — yedeğin çalıştığının kanıtı.
- **GoBD Uyumluluğu** — muhasebe verileri için 6–10 yıllık saklama süreleri.

**Teknik Çözüm:**
AWS S3 Frankfurt'a (AB veri merkezi, DSGVO uyumlu) otomatik şifreli senkronizasyon sağlayan NAS cihazı (örn. Synology).

**Digitalbonus ile teşvik edilebilir mi:** ✅ Evet — NAS donanımı ve bulut yedekleme kurulumu.

---

## Gerçek Para Cezaları — Denetimlerle Değil, Şikayetlerle Tetiklenir

BayLDA (Bavyera Veri Koruma Denetim Makamı) **düzenli rutin kontroller yapmaz**. Para cezaları şunlar nedeniyle oluşur:

- **Müşteri Şikayetleri** — memnuniyetsiz bir hasta, misafir veya çalışan.
- **Veri İhlalleri** — hacker saldırısı, veri kaybı, yanlışlıkla veri paylaşımı.
- **Rakip Şikayetleri** — rakiplerin ihbarda bulunması.

BayLDA, 2023 yılında DSGVO'nun yürürlüğe girmesinden bu yana en yüksek sayıda para cezasını kesti. Gerçek örnekler: Bavyera'da bir diş hekimi muayenehanesi 3.500 €, perakende sektörü 1.200 € — tekil müşteri şikayetleri ile tetiklendi.

**Önemli:** Bilmemek cezadan muaf tutmaz. DSGVO 2018'den beri yürürlüktedir — her şirketin uyum sağlamak için zamanı vardı.

---

## Digitalbonus Bayern Neleri Teşvik Ediyor?

**Program:** [Digitalbonus Bayern](https://www.digitalbonus.bayern)
**Teşvik Oranı:** Teşvik edilebilir maliyetlerin %50'si
**Maksimum:** 7.500 € (Digitalbonus Standard) — her teşvik alanı için (BT Güvenliği ve Dijitalleşme) birer kez
**Süre:** 31 Aralık 2027'ye kadar
**Başvuru:** Sadece ELSTER kurumsal hesabı üzerinden dijital olarak

| Önlem | Teşvik Edilebilir mi |
|---|---|
| Firewall (Donanım + Lisans + Yapılandırma) | ✅ Evet |
| VLAN ayırımı için Yönetilebilir Switch | ✅ Evet |
| WLAN Access Pointler | ✅ Evet |
| NAS + şifreli Bulut Yedekleme | ✅ Evet |
| E-posta güvenlik lisansı (18 aya kadar) | ✅ Evet |
| Antivirüs/EDR lisansları (18 aya kadar) | ✅ Evet |
| Kurulum ve yapılandırma hizmeti | ✅ Evet |
| Bakım sözleşmesi (18 aya kadar) | ✅ Evet |
| Danışmanlık hizmeti (Toplam maliyetin %50'sine kadar) | ✅ Evet |
| Standart PC'ler, Laptoplar, Yazıcılar | ❌ Hayır |
| Standart ofis yazılımları (Office, Windows) | ❌ Hayır |

**Önemli Şart:** Başvuru, proje **başlamadan önce** yapılmalıdır. Başvuru onayı alınmadan ne sipariş verilmeli ne de sözlü iş emri verilmelidir.

---

## Örnek Hesaplama: Küçük Bir Otel (10 Oda, 5 Çalışan)

| Önlem | Maliyet | Teşvik Sonrası (%50) |
|---|---|---|
| FortiGate Firewall + 1 yıllık lisans | 1.000 € | 500 € |
| Yönetilebilir Switch (VLAN uyumlu) | 500 € | 250 € |
| 3× WLAN Access Point | 900 € | 450 € |
| NAS + AWS Yedekleme kurulumu | 500 € | 250 € |
| E-posta Güvenliği (18 ay) | 400 € | 200 € |
| Antivirüs/EDR 5 cihaz (18 ay) | 300 € | 150 € |
| Kurulum & Yapılandırma | 1.000 € | 500 € |
| 18 aylık Bakım | 900 € | 450 € |
| **Toplam** | **5.500 €** | **2.750 €** |

Otel **2.750 €** öder — Bavyera Eyaleti **2.750 €**'yu üstlenir.

---

## Bu Kimler İçin İlgilidir?

- **Oteller ve Pansiyonlar** — Misafir WLAN, kamera sistemleri, rezervasyon verileri, POS terminalleri
- **Doktor ve Terapi Muayenehaneleri** — Hasta verileri, mesleki gizlilik, DSGVO + §75b SGB V
- **Hukuk Büroları** — Müvekkil gizliliği, katı DSGVO yükümlülükleri
- **Kafeler ve Restoranlar** — Misafir WLAN, kasa sistemi, rezervasyon verileri
- **Dil Okulları** — Öğrenci WLAN, yönetim verileri, öğretmen verileri
- **Küçük Ofisler (2–20 Kişi)** — Kendi BT departmanı olmayanlar

---

## Ne Sunuyoruz: Bağımsız Danışmanlık — Ürün Satışı Değil

Biz ürün satmıyoruz. Kendi sağlayıcılarınızı ve ürünlerinizi seçersiniz — biz planlama, kurulum, yapılandırma ve dokümantasyon konularında yardımcı oluruz.

Bankacılık, sanayi ve otelcilik (Hilton, Marriott, Crown Hotel Group, Wyndham Grand Europa dahil) sektörlerinde **11 yılı aşkın deneyime sahip Kıdemli Ağ Güvenlik Mühendisi** olarak şunları sunuyoruz:

1. **Ücretsiz BT Altyapı Analizi** — Mevcut durumunuza bakıyor ve açıkların nerede olduğunu gösteriyoruz.
2. **Bağımsız Ürün Tavsiyesi** — En pahalı olanı değil, size uygun olanı tavsiye ediyoruz.
3. **Teknik Uygulama** — VLAN yapılandırması, firewall kurulumu, yedekleme kurulumu, e-posta güvenliği.
4. **Digitalbonus Başvuru Hazırlığı** — Teşvik edilebilir önlemlerin dokümantasyonunda yardımcı oluyoruz.
5. **Sürekli Bakım** — Aylık izleme, güncellemeler, sorunlarda muhataplık.

---

## Sonraki Adım: Ücretsiz Analiz

**📱 WhatsApp:** [wa.me/4916098665971](https://wa.me/4916098665971)

**📧 E-posta:** [info@barashhelvadzhaoglu.com](mailto:info@barashhelvadzhaoglu.com)

*Ücretsiz analiz. Onayınız olmadan iş emri yok. Ürün satışı yok — sadece danışmanlık ve teknik uzmanlık.*

---

## İlgili Bağlantılar

- [Digitalbonus Bayern — Resmi Teşvik Programı](https://www.digitalbonus.bayern)
- [DSGVO Madde 32 — İşleme Güvenliği](https://gdpr.eu/article-32-security-of-processing/)
- [BSI IT-Grundschutz Kompendium](https://www.bsi.bund.de/grundschutz)
- [BayLDA — Bavyera Veri Koruma Denetim Makamı](https://www.lda.bayern.de)
- [GoBD — Muhasebe İlkeleri](https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Weitere_Steuerthemen/Abgabenordnung/2019-11-28-GoBD.pdf)