---
title: "F5 WAF Deep Dive: ASM ve Advanced WAF ile Uygulama Güvenliği"
description: "F5 WAF teknik inceleme — ASM ve Advanced WAF, pozitif ve negatif güvenlik modelleri, OWASP Top 10, bot savunması ve L7 DoS koruması."
date: 2026-04-22
draft: false

cover:
  image: "/img/postimages/f5-waf-asm-cover.webp"
  alt: "F5 WAF ASM Advanced WAF — Uygulama Güvenliği Mimarisi"
  relative: false

tags: ["F5", "WAF", "ASM", "Advanced WAF", "BIG-IP", "Uygulama Güvenliği", "OWASP", "Bot Savunması", "Web Güvenliği"]
categories: ["Teknoloji"]
keywords:
  - F5 WAF yapılandırması
  - F5 ASM vs Advanced WAF
  - F5 uygulama güvenlik yöneticisi
  - F5 OWASP Top 10 koruması
  - F5 WAF politikası
  - F5 bot savunması
  - F5 L7 DoS koruması
  - F5 WAF şeffaf engelleme modu
  - F5 pozitif güvenlik modeli
  - F5 WAF deployment stratejisi

showToc: true
TocOpen: true
---

# F5 WAF Deep Dive: ASM ve Advanced WAF ile Uygulama Güvenliği

Bu yazı F5 BIG-IP serisinin bir parçasıdır.

> **F5'e yeni misiniz?** Önce platform genel bakışıyla başlayın: [F5 BIG-IP Bir Load Balancer Değil — Uygulama Teslim Platformudur](/tr/technology/f5-bigip-uygulama-teslim-platformu-genel-bakis/)

Büyük resmi zaten anlıyorsanız ve WAF'a derinlemesine inmek istiyorsanız — güvenlik modelleri, OWASP kapsamı, bot savunması ve deployment stratejisi — doğru yerdesiniz.

---

## WAF Nereye Oturur — Nereye Oturmaz

En yaygın yanlış anlama: *"Firewall'umuz var, uygulama katmanında korunuyoruz."*

Yeni nesil bir firewall, bazı L7 protokol farkındalığıyla L3/L4'te çalışır. Port taramalarını, bilinen kötü IP'leri, C2 iletişimini ve açık metin protokollerindeki tanınan exploit'leri engeller. Ancak bir HTTPS POST isteğinin gövdesini inceleyip `username` alanının `' OR 1=1 --` içerip içermediğini belirleyemez.

WAF'ın doldurduğu boşluk budur:

```
NGFW:  IP filtreleme, port kuralları, VPN, stateful inspection, protokol anomalisi
WAF:   HTTP/HTTPS içerik incelemesi — SQL injection, XSS, parametre tampering,
       bot trafiği, credential stuffing, uygulama katmanı DoS
```

F5 WAF, **LTM virtual server'ı üzerinde inline** çalışır. Trafik LTM'nin full proxy'sinden geçer, SSL sonlandırılır ve ardından WAF backend'e ulaşmadan önce şifresi çözülmüş içeriği inceler. Bu konumlama temel avantajdır — WAF, istemciden başlayarak şifrelenmiş trafik dahil her şeyi görür.

---

## ASM ve Advanced WAF Karşılaştırması

F5, BIG-IP'te iki WAF katmanı sunar:

**ASM (Application Security Manager)** — orijinal modül. Öncelikle imza tabanlı. OWASP Top 10, parametre zorunluluğu, çerez koruması ve temel bot tespitini kapsar. Birçok standart BIG-IP lisansına dahildir.

**Advanced WAF (AWAF)** — ASM'nin sahip olmadığı davranışsal yeteneklere sahip yeni modül:

| Özellik | ASM | Advanced WAF |
|---|---|---|
| İmza tabanlı saldırı tespiti | ✅ | ✅ |
| OWASP Top 10 kapsamı | ✅ | ✅ |
| Parametre ve çerez zorunluluğu | ✅ | ✅ |
| Temel bot tespiti (imzalar) | ✅ | ✅ |
| Davranışsal bot savunması | ❌ | ✅ |
| Credential stuffing koruması | ❌ | ✅ |
| JavaScript challenge / CAPTCHA | Sınırlı | ✅ |
| L7 davranışsal DoS azaltma | Sınırlı | ✅ |
| API güvenliği (OpenAPI / Swagger) | Sınırlı | ✅ |
| DataSafe (istemci tarafı şifreleme) | ❌ | ✅ |

Dahili kurumsal uygulamalar için ASM sağlam kapsam sağlar. Yüksek bot maruziyeti, credential stuffing riski veya agresif L7 DoS olan kamuya açık uygulamalar için Advanced WAF önemli ölçüde daha etkilidir.

---

## Güvenlik Politikası Modelleri

### Negatif Güvenlik Modeli (Kara Liste Yaklaşımı)

Bilinen kötü kalıpları engelle. Geri kalanına izin ver.

F5 WAF, bilinen exploit kalıplarıyla eşleşen binlerce **saldırı imzasıyla** gelir:

```
İmza: SQL Injection (Genel)
  Saldırı Türü:  SQL Injection
  Risk:          Kritik
  Kalıp:         SELECT...FROM, INSERT...INTO, OR 1=1, vb. ile eşleşir
```

Bir istek bir imzayla eşleştiğinde, WAF onu engeller (engelleme modunda) veya loglar (şeffaf modda).

**Avantajlar:** Hızlı deployment, düşük başlangıç yanlış pozitifi, bilinen güvenlik açıkları için iyi kapsam.

**Dezavantajlar:** Tanım gereği sıfır-gün saldırılarını tespit edemez. Kararlı saldırganlar bazen kodlama varyasyonları veya parçalanmış payload'lar aracılığıyla imzaları atlayabilir.

### Pozitif Güvenlik Modeli (Beyaz Liste Yaklaşımı)

Yalnızca açıkça tanımlanmış girdilere izin ver. Geri kalanını engelle.

Pozitif güvenlikte, uygulamanızın tam olarak neyi kabul ettiğini tanımlarsınız:

```
Parametre: username
  Tür:         Alfanümerik
  Maks Uzunluk: 64
  Zorunlu:     Evet

Parametre: user_id
  Tür:         Tamsayı
  Min Değer:   1
  Maks Değer:  999999
```

`username=admin' OR 1=1--` içeren bir istek engellenir çünkü tek tırnak ve boşluklar Alfanümerik karakter setinde değildir. Saldırgan, katı bir beyaz listeyi atlayacak bir payload hazırlayamaz.

**Avantajlar:** Sıfır-gün ve bilinmeyen saldırı varyantlarını engeller. İmza eşleştirmesinden temel olarak daha güçlü.

**Dezavantajlar:** Önemli ayarlama çabası gerektirir. Karmaşık, dinamik parametre setlerine sahip uygulamaları doğru biçimde modellemek zordur. Başlangıçta yüksek yanlış pozitif oranı.

### Hibrit Model: Üretim Ortamlarının Gerçekte Kullandığı

Çoğu üretim deployment'ı bir kombinasyon kullanır:

- Uygulamanın büyük bölümü için **negatif model** — düşük bakım yüküyle imzalar
- Yüksek riskli endpoint'ler için **pozitif model** — kimlik doğrulama, ödeme işleme, ayarlama yatırımının değerini kanıtladığı yönetim fonksiyonları

---

## Saldırı İmzaları: Yönetim ve Güncellemeler

F5, saldırı kategorisi ve uygulama platformuna göre düzenlenmiş imzalarla gelir:

```
İmza Setleri:
  Genel Tespit İmzaları (SQL Injection, XSS, Komut Enjeksiyonu)
  Apache Struts İmzaları
  WordPress / Joomla İmzaları
  CVE'ye özgü imzalar (hedeflenmiş exploit payload'ları)
  Yüksek Doğruluk İmzaları (minimum yanlış pozitif için ayarlanmış)
```

F5 düzenli olarak imza güncellemeleri yayınlar. Güncel olmayan imzalar, son açıklanan güvenlik açıklarına karşı WAF etkinliğini önemli ölçüde azaltır.

**İmza staging'i** — yeni imzalar zorunluluktan önce staging moduna alınmalıdır:

```
Yeni İmza Durumu: Staging
  Davranış: İhlalleri logla, engelleme
  Amaç:     Zorunluluğu etkinleştirmeden önce yanlış pozitif olmadığını doğrula
  Süre:     Minimum 1–2 hafta üretim trafiği gözlemi
```

Staging, yeni imzaları üretim kullanıcılarını etkilemeden önce uygulamanıza özgü trafik karşısında doğrulamanıza olanak tanır.

---

## OWASP Top 10 Kapsamı

F5 WAF, imzalar ve politika zorunluluğunun kombinasyonu aracılığıyla tüm on OWASP Top 10 kategorisini ele alır:

**A01 — Kırık Erişim Kontrolü:** URL erişim kalıplarını zorla, yetkisiz kaynaklardan yönetim yollarına yönelik istekleri engelle.

**A02 — Kriptografik Hatalar:** Yanıtlarda hassas veri kalıplarını tespit et (kredi kartı numaraları, SSN'ler); kazara açığa çıkmayı engelle.

**A03 — Enjeksiyon (SQL, Komut, LDAP, XSS):** İmza tespitinin birincil gücü. Tüm enjeksiyon türlerinde enjeksiyon payload'larını özellikle hedef alan yüzlerce imza.

**A04 — Güvensiz Tasarım:** Beklenen uygulama akışlarını zorla; tanımlı gezinme yolları dışındaki URL'lere zorla gezinmeyi engelle.

**A05 — Güvenlik Yanlış Yapılandırması:** Varsayılan yönetici arayüzlerine, yedek dosyalara, yapılandırma endpoint'lerine ve sürüm ifşa sayfalarına erişimi tespit et ve engelle.

**A06 — Savunmasız Bileşenler:** Popüler framework'lerdeki bilinen CVE'ler için imza kapsamı (Apache Struts, Spring, Log4j, vb.).

**A07 — Kimlik Doğrulama Hataları:** Advanced WAF, credential stuffing koruması ekler — otomatik kimlik bilgisi test saldırılarını tespit edip hız sınırlar.

**A08 — Yazılım ve Veri Bütünlüğü Hataları:** Sınırlı doğrudan WAF kapsamı — öncelikle bir uygulama tasarımı endişesi. WAF, seri kaldırma işlemini kullanan bazı enjeksiyon girişimlerini tespit edebilir.

**A09 — Loglama ve İzleme Hataları:** WAF, merkezi görünürlük için SIEM'e entegre olan ayrıntılı istek loglama ve ihlal takibi sağlar.

**A10 — SSRF (Sunucu Tarafı İstek Sahteciliği):** İmzalar, istek parametrelerindeki ve başlıklardaki yaygın SSRF kalıplarıyla eşleşir.

---

## Bot Savunması (Advanced WAF)

İnternet trafiğinin önemli bir bölümü otomatiktir. Tüm botlar kötü niyetli değildir — arama motoru tarayıcıları, izleme sistemleri ve RSS okuyucuları meşrudur. Advanced WAF'ın bot savunması bunları birbirinden ayırır.

### Tespit Katmanları

**İmza tabanlı bot tespiti:** Bilinen bot User-Agent dizelerini F5'in bot veritabanıyla eşleştir. Hızlı ama User-Agent başlığını değiştirerek kolayca atlanabilir.

**JavaScript challenge:** Yanıta şeffaf bir JavaScript challenge'ı ekle. Meşru tarayıcılar bunu sessizce yürütür; JavaScript render etmeyen temel botlar challenge'ı başarısız geçer. Yalnızca imza eşleştirmesinden önemli ölçüde daha etkili.

**CAPTCHA challenge:** JS challenge'ı başarısız geçen veya şüpheli kalıplarla eşleşen trafik için bir CAPTCHA sun. İkincil challenge olarak kullanılır — birincil savunma olarak değil (normal trafik için çok rahatsız edici).

**Davranışsal analiz:** Zaman içinde istek kalıplarını izle. `/api/auth/login`'e saniyede 500 istek yapan bir istemci neredeyse kesinlikle bir bottur — JavaScript challenge'ını geçip geçmediğinden bağımsız olarak.

**Tarayıcı parmak izi:** Advanced WAF, gerçek tarayıcıları baş olmayan otomasyon araçlarından (Puppeteer, Playwright, Selenium) ayırt etmek için tarayıcı özelliklerini toplar (canvas render, JavaScript motor zamanlaması, TCP/TLS parmak izi).

### Bot Kategorileri ve Yanıtları

```
Bot Kategorisi         Yanıt
────────────────────────────────────────
Arama motorları        İzin ver (DNS ters arama ile doğrulanmış)
İzleme araçları        İzin ver (IP ile beyaz listeye alınmış)
Bilinmeyen botlar      JS challenge
Şüpheli botlar         CAPTCHA challenge
Bilinen kötü niyetli   Hemen engelle
Credential stuffers    Engelle + uyar
```

---

## L7 DoS Koruması

Katman 7 DoS saldırıları büyük trafik hacmine ihtiyaç duymaz. Yavaş bir endpoint'i hedef alan az sayıda istek, sunucu kaynaklarını tüketebilir:

```
Saldırı örneği:
  /reports/generate?type=full adresine 100 eş zamanlı istek
  Her biri 30 saniyelik bir veritabanı sorgusu tetikler
  Veritabanı CPU → %100
  Diğer tüm kullanıcılar: zaman aşımları
  Tüketilen ağ bant genişliği: minimal
  Geleneksel DDoS tespiti: olağandışı bir şey görmez
```

Advanced WAF'ın L7 DoS tespiti:

**Stres tabanlı tespit:** Backend sunucu yanıt gecikmesini birincil sinyal olarak izler. Gecikme temel seviyenin üzerine çıktığında WAF otomatik olarak hız sınırlaması uygular. Bu uyarlanabilirdir — yalnızca istek hacmi eşiklerine değil, gerçek sunucu stresine yanıt verir.

**TPS tabanlı tespit:** Kaynak IP başına veya URL başına saniyedeki istek sınırlarını zorlar.

**Davranışsal temel:** Zaman içinde URL başına normal trafik kalıplarını öğrenir. Bir URL öğrenilen temel çizgisinden önemli ölçüde saptığında otomatik uyarı — normalde dakikada 20 istek alan bir URL'nin aniden 5.000 alması, mutlak sayılardan bağımsız olarak anormaldir.

---

## Deployment Stratejisi: Şeffaftan Engellemeye Geçiş

En yaygın WAF deployment başarısızlığı, doğrudan engelleme moduna geçmektir. Engelleme modundaki her yanlış pozitif meşru bir kullanıcının iş akışını bozar, helpdesk ticket'ı üretir ve WAF değerini kanıtlamadan önce organizasyonel güveni yok eder.

Doğru yaklaşım her zaman aşamalıdır:

### Faz 1 — Şeffaf Mod (1–4. Haftalar)

```
Zorunluluk Modu: Şeffaf
İhlalde eylem: Yalnızca logla — engelleme yok
```

Deploy edin ve toplayın. İhlal loglarını her gün gözden geçirin. Şunları tespit edin:
- İmzaları tetikleyen meşru uygulama davranışı (yanlış pozitifler)
- Tespit edilen gerçek saldırılar (doğru pozitifler)
- Her uygulama parametresi için tipik değerler ve kalıplar

### Faz 2 — Politika Ayarlama (2–6. Haftalar, Faz 1 ile çakışıyor)

Şeffaf mod verilerine dayanarak politikayı ayarlayın:

**Onaylanan yanlış pozitifler için istisnalar ekleyin:**
```
Parametre: search_query
  İzin ver: Özel karakterler (%, *, ?)
  Neden: Uygulama meşru olarak joker karakter arama operatörlerini kabul ediyor
```

**Sorunlu imzaları devre dışı bırakmak yerine staging'e alın:**
```
İmza: XSS Genel (bu uygulama için yüksek yanlış pozitif oranı)
  Durum: Staging → logla ama engelleme
  Gözden geçir: 2 ek hafta veri sonrasında
```

**Kritik endpoint'ler için pozitif güvenlik kuralları oluşturun:**
```
URL: /api/auth/login
  username  → Alfanümerik, maks 64 karakter
  password  → Herhangi, maks 128 karakter, değeri asla loglama
  mfa_code  → Yalnızca sayısal, tam olarak 6 karakter
```

### Faz 3 — Seçici Engelleme (6. Hafta+)

Engelleme modunu kademeli olarak etkinleştirin — en yüksek güvenilirlikli imzalarla başlayın:

```
Zorunluluk Modu: Engelleme
Yüksek güvenilirlikli imzalar: Engelle
Orta güvenilirlikli imzalar: Yalnızca alarm (logla + uyar, engelleme yok)
Yeni/yakın zamanda eklenen imzalar: Staging
```

Bu, şeffaftan engellemeye geçişte bir yanlış pozitif dalgasını önler. İmzaları güven arttıkça şu hattı izleyerek ilerletin: Staging → Alarm → Engelleme.

### Faz 4 — Süregelen Bakım

WAF bir kere ayarla unut aracı değildir:

- **Aylık:** F5 imza güncellemelerini uygula; staging'deki yeni imzaları gözden geçir
- **Her uygulama deployment'ında:** Yeni parametreler, URL'ler veya değişen uygulama davranışı için WAF politikasını güncelle
- **Haftalık:** İhlal log eğilimlerini gözden geçir; ani artışları ve yeni saldırı kalıplarını araştır
- **Üç aylık:** Tam yanlış pozitif denetimi; bayatlamış istisnaları kaldır; bot trafik eğilimlerini gözden geçir

---

## Loglama ve SIEM Entegrasyonu

WAF, her ihlal için ayrıntılı loglar üretir — olay müdahalesi, uyumluluk ve tehdit istihbaratı için gerekli:

```
Zaman Damgası:      2026-03-14 09:23:41 UTC
İstemci IP:         203.0.113.42
İstek:              POST /api/auth/login HTTP/1.1
İhlal Edilen Param: username
İhlal:              SQL Injection
Eşleşen İmza:       200000007 (SQL Injection Generic)
Saldırı Türü:       SQL Injection
Önem Derecesi:      Kritik
Eylem:              Engellendi
Destek ID:          12345678901234
```

Bankacılık ortamında WAF logları Splunk'a iletildi:
- SOC tarafından görülebilen gerçek zamanlı saldırı panoları
- Firewall ve IPS olaylarıyla korelasyon — aynı anda WAF ihlallerini VE IPS alarmlarını tetikleyen bir IP yüksek önceliklidir
- Kritik önem dereceli ihlaller için otomatik çağrı
- Aylık PCI DSS uyumluluk raporlaması

---

## Temel Çıkarımlar

- WAF **L7'de** korur — NGFW'lerin uygulamaya özgü saldırılar için etkili biçimde inceleyemediği katman.
- **ASM** standart kurumsal ihtiyaçları karşılar. **Advanced WAF**, bot maruziyeti, credential stuffing riski veya L7 DoS tehditlerine sahip kamuya açık uygulamalar için haklı kılınır.
- **Hiçbir zaman doğrudan engelleme moduna gitmeyin.** Şeffaf → ayarlama → seçici engelleme → tam engelleme, tek güvenilir yoldur.
- **Negatif model** hızlı deploy edilir. **Pozitif model** daha güçlüdür ancak önemli ayarlama yatırımı gerektirir — yüksek riskli endpoint'lere seçici olarak uygulayın.
- WAF **süregelen bakım** gerektirir — imza güncellemeleri, uygulama değiştiğinde politika değişiklikleri, düzenli yanlış pozitif gözden geçirme.
- **SIEM entegrasyonu** WAF'ı bir engelleme aracından tüm güvenlik operasyon fonksiyonu için bir istihbarat kaynağına dönüştürür.

---

## Bu Seri

- 📖 [F5 BIG-IP Platform Genel Bakış — Tüm Modüller](/tr/technology/f5-bigip-uygulama-teslim-platformu-genel-bakis/) ← F5'e yeniyseniz buradan başlayın
- 🔧 [F5 LTM Deep Dive](/tr/technology/f5-ltm-virtual-server-irule-ssl-offloading-ha/)
- 🌐 [F5 GTM ve GSLB Deep Dive](/tr/technology/f5-gtm-gslb-global-traffic-management/)

## İlgili Yazılar

- 🔐 [Zero Trust Zihniyeti: Güvenliği Bir Mimari Olarak Mühendislemek](/tr/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — WAF'ın Zero Trust'taki yeri
- 🛡️ [802.1X Kimlik Tabanlı Mimari Sahada](/tr/technology/identity-based-microsegmentation-8021x/) — Ağ katmanlarında derinlemesine savunma
- 📊 [İzleme Doğru Yapıldığında](/tr/architecture/monitoring-not-just-seeing/) — WAF loglarını proaktif izlemeye entegre etmek
- 🛡️ [Network Packet Broker (NPB) Masterclass](/tr/posts/network-packet-broker-masterclass/) — WAF ile birlikte tam trafik görünürlüğü