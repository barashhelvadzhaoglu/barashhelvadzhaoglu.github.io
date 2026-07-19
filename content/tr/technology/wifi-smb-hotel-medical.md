---
title: "KOBİ, Oteller ve Muayenehaneler İçin WiFi Tasarımı: Saha Notları"
description: "KOBİ, otel ve muayenehaneler için WiFi tasarım rehberi — yoğunluk planlaması, misafir segmentasyonu, bant genişliği yönetimi ve PMS entegrasyonu."
date: 2026-04-29
draft: false

cover:
  image: "/img/postimages/wifi-smb-hotel-medical-cover.webp"
  alt: "KOBİ Oteller Muayenehaneler İçin WiFi Tasarımı"
  relative: false

tags: ["WiFi", "KOBİ", "Otel WiFi", "Muayenehane", "WLAN Tasarımı", "Misafir Ağı", "Aruba", "Cisco Meraki"]
categories: ["Teknoloji"]
keywords:
  - KOBİ WiFi tasarımı
  - otel WiFi altyapısı
  - muayenehane WiFi
  - misafir ağı segmentasyonu
  - WiFi kullanıcı başına bant genişliği yönetimi
  - otel PMS WiFi entegrasyonu
  - WiFi HIPAA uyumu
  - Aruba Instant On KOBİ
  - Cisco Meraki otel
  - WiFi kapsama planlaması ofis

showToc: true
TocOpen: true
---

# KOBİ, Oteller ve Muayenehaneler İçin WiFi Tasarımı: Saha Notları

Bu yazı Kurumsal WiFi serisinin bir parçasıdır.

> **Kurumsal kablosuz ağa yeni misiniz?** Genel bakışla başlayın: [Kurumsal WiFi Mimarisi: Standartlardan Deployment'a](/tr/technology/kurumsal-wifi-mimarisi-tam-rehber/)

---

## Ortam Türü Neden Ekipman Markasından Daha Önemlidir

Herhangi bir büyük satıcının WiFi 6 AP'si, bir laboratuvarda WiFi 5 AP'sini geride bırakır. Gerçek bir binada, iyi bir deployment ile başarısız bir deployment arasındaki farkın AP donanımıyla neredeyse hiçbir ilgisi yoktur — ortama özgü tasarım kararlarına bağlıdır.

Otelin gereksinimleri, muayenehaneden temel olarak farklıdır. Lojistik deposu, bir hukuk bürosundan tamamen farklı bir yaklaşım gerektirir. AP yalnızca bir radyodur — tasarım, ortamına hizmet edip etmediğini belirler.

Bu yazı, belirli tasarım desenleri, yaygın hatalar ve gerçek deployment'lardan saha notlarıyla üç yaygın deployment senaryosunu ele alır.

---

## Bölüm 1: KOBİ WiFi Tasarımı

### "Sadece Erişim Noktası Ekle" Tuzağı

En yaygın KOBİ WiFi başarısızlığı: biri internet kapsama haritalarına dayanarak iki ya da üç AP kurar, "WiFi her yerde var" diye raporlar ve üç ay sonra herkes WiFi'nin yavaş olduğundan şikayet eder.

Neredeyse her zaman kök nedenler:
- Kabloların çalıştırılmasının kolay olduğu yerlere AP yerleştirme, kapsama alanının gerekli olduğu yerlere değil
- Kullanılabilir veri hızlarında çok büyük bir alanı kapsamaya çalışan tek AP (sinyal gücü ≠ verim)
- Band yönlendirme yok — eski telefonlar ve yazıcılar 2,4 GHz'i monopolize ediyor
- QoS yok — tek bir kullanıcının dosya yedeklemesi, 10 diğer kullanıcının beklediği bant genişliğini tüketiyor
- Misafir/personel ayrımı yok — misafirler kurumsal ağda

### KOBİ İçin Kapsama Planlaması

Tipik ofis ortamları için kaba bir başlangıç noktası:

| Ortam | AP Kapsama Alanı | Notlar |
|---|---|---|
| Açık ofis, düşük yoğunluk | 150–200 m² | Modern WiFi 6 AP'ler, orta istemci sayısı |
| Açık ofis, yüksek yoğunluk | 80–100 m² | Çok istemci, video görüşmeler, yüksek verim |
| İç duvarlarla ofis | 80–120 m² | Duvarlar sinyali zayıflatır; sonuçlandırmadan önce test edin |
| Koridor / otel koridoru | AP başına 20–25 m | Dar kapsama deseni |
| Depo / büyük açık alan | 300–500 m² | Düşük yoğunluk, yüksek tavanlar, RF iyi yayılır |

Bunlar başlangıç noktaları, kural değil. Kapsama alanını doğrulamanın tek yolu site survey — deployment öncesi tahmine dayalı, sonrasında doğrulama.

### Ağ Segmentasyonu Taban Çizgisi

Her KOBİ deployment'ı en azından üç VLAN'a eşlenen üç SSID'ye sahip olmalıdır:

```
SSID: ŞirketAğı     → VLAN 10 (kurumsal cihazlar, tam LAN erişimi)
SSID: MisafirWiFi    → VLAN 20 (yalnızca internet, VLAN 10'dan izole)
SSID: IoT/Yazıcılar  → VLAN 30 (yazıcılar, kameralar, izole)
```

Misafir VLAN'ı **firewall ile zorunlu kılınan izolasyon** olmalıdır — aralarında firewall olmadan yalnızca farklı alt ağ değil. Misafir cihaz internet'e ulaşabilmeli ve başka hiçbir şeye ulaşamamalıdır. Firewall kuralı açıktır: VLAN 20 → yalnızca internet, VLAN 20 → VLAN 10 reddet.

### Band Yönlendirme ve QoS

**KOBİ ortamlarında band yönlendirme:** AP'leri mümkün olduğunda istemcileri 5 GHz'e yönlendirecek şekilde yapılandırın. Modern iş dizüstü bilgisayarları ve telefonların çoğu 5 GHz'e yeteneklidir. Yazıcılar ve eski IoT cihazları çoğunlukla yalnızca 2,4 GHz'i destekler — onları özel IoT SSID'sine yerleştirmek, diğer kullanıcıları etkilemeden bunu yönetir.

**KOBİ için temel QoS:**
- VoIP/video trafiğini işaretleyin veya önceliklendirin (ses için DSCP EF, video için AF41)
- Misafir VLAN'ında kullanıcı başına bant genişliği sınırları belirleyin (örn. cihaz başına 10 Mbps indirme / 5 Mbps yükleme)
- AP platformunuz destekliyorsa uygulama farkında QoS'u değerlendirin (Meraki, Aruba)

### KOBİ İçin Platform Önerisi

| Boyut | Öneri | Neden |
|---|---|---|
| 1–5 AP, IT personeli yok | Aruba Instant On | Basit uygulama tabanlı yönetim, sağlam donanım |
| 5–20 AP, temel IT personeli | Cisco Meraki veya Aruba Central | Bulut yönetimi, iyi görünürlük |
| 20+ AP, IT ekibi | Aruba Central veya Cisco DNA Center | Kurumsal özellikler, politika entegrasyonu |

---

## Bölüm 2: Otel WiFi Tasarımı

### Otel WiFi Zorluğu

Oteller, en zorlu WiFi ortamlarından biridir:

- **Yüksek cihaz yoğunluğu:** Her misafir odası 3–5 cihaza sahip (telefon, dizüstü, tablet, akıllı TV, akıllı saat). 200 odalı bir otel, yoğun kullanım döneminde 600–1000 istemci cihaza sahiptir.
- **Değişken talep:** Kullanım; check-in, akşam yemeği sonrası ve sabahın ilk saatlerinde zirveye çıkar — gündüz çok düşük kullanımla. Ağ, ortalama yükü değil, zirve yükü karşılamalıdır.
- **Gelir bağımlılığı:** "WiFi çalışmıyor", otel incelemelerinde en çok şikayet edilen konudur. Kötü WiFi, misafir memnuniyeti puanlarını doğrudan etkiler.
- **Karma teknik yeterlilik:** Ağ, hem bir teknoloji yöneticisi hem de tatile gelen bir gezgin için sorunsuz çalışmalıdır.

### AP Yerleşimi: Koridor veya Oda İçi

İki temelden farklı yaklaşım:

**Koridor AP'leri:**
- Koridorlara monte AP'ler, odaları duvarların arasından kapsıyor
- Daha az AP sayısı, daha düşük kurulum maliyeti
- Sinyal, misafirlere ulaşmak için 2–3 duvar geçmek zorunda
- Bitişik odaları kapsayan koridor AP'leri arasında aynı kanal girişimi

**Oda İçi AP'ler:**
- Her odada veya diğer her odada AP
- Daha fazla AP sayısı ve kurulum maliyeti
- Mükemmel sinyal kalitesi (AP istemciyle aynı odada)
- Odalar arasında daha iyi izolasyon (daha az girişim)
- Daha karmaşık kablolama

**Saha deneyimi:** Beton duvarlar ve metal çerçeveli odalara sahip modern otel yapısında, koridor AP'leri şaşırtıcı derecede kötü kapsama sağlayabilir — duvarlar 5 GHz sinyallerini önemli ölçüde zayıflatır. Oda içi veya diğer oda AP yerleşimi tipik olarak dramatik biçimde daha iyi misafir deneyimi sunar. Mevcut kablolama ile tadilat projelerinde, WiFi 6 ve dikkatli kanal planlamasıyla koridor AP'leri çoğunlukla pragmatik seçimdir.

### Bant Genişliği Yönetimi: En Kritik Otel Özelliği

Kullanıcı başına bant genişliği yönetimi olmadan, üç cihazda 4K video izleyen bir misafir, 20 diğer misafirin beklediği bant genişliğini tüketir. Misafir deneyimi tamamen aynı anda çevrimiçi olan kişilere bağlı hale gelir.

Kurumsal otel WiFi controller'ları kullanıcı ve cihaz başına hız sınırlamasını destekler:

```
Misafir SSID Politikası:
  Cihaz başına indirme sınırı:  25 Mbps
  Cihaz başına yükleme sınırı:  10 Mbps
  Oda başına maksimum:          75 Mbps (3 cihaz × 25 Mbps)
```

Bu sınırlar, tipik kullanımda kullanıcılar fark etmeden adilliği sağlar — cihaz başına 25 Mbps, HD video akışı, video görüşmeler ve normal tarama için yeterlidir. 4K akışı 15–25 Mbps gerektirir, hâlâ sınır içinde.

Premium WiFi kademeleri (ek ücretli) daha yüksek sınırlara sahip olabilir:

```
Standart Misafir:  Cihaz başına 25 Mbps
Premium Misafir:   Cihaz başına 50 Mbps
Kurumsal VLAN:     Sınırsız (personel ağı)
```

### Misafir Portalı ve Kimlik Doğrulama

Otel misafir portalları üç işleve hizmet eder: tanımlama, şartlar kabul ve süre yönetimi.

**Yaygın kimlik doğrulama modelleri:**

- **Açık kayıt:** Misafir ad ve e-posta girer, şartları kabul eder, erişim alır. Basit, personel müdahalesi yok.
- **Oda numarası doğrulama:** Misafir oda numarası girer (ve isteğe bağlı olarak soyad). Aktif rezervasyonu doğrulamak için PMS ile entegre olur.
- **Kupon tabanlı:** Resepsiyon kupon kodu sağlar. Günlük ziyaretçiler, konferans katılımcıları için kullanışlı.

**PMS (Otel Yönetim Sistemi) entegrasyonu**, oteller için profesyonel standarttır. WiFi sistemi, oda numarasının dolu olduğunu ve rezervasyonun aktif olduğunu doğrulamak için PMS'yi sorgular. Check-out'ta misafirin WiFi erişimi otomatik olarak iptal edilir. Manuel müdahale gerekmez.

WiFi entegrasyonlu yaygın PMS sistemleri: Opera, Protel, Mews, Cloudbeds — tümü büyük WiFi platformları için belgelenmiş entegrasyon API'lerine sahiptir (Aruba, Cisco, Ruckus).

### Otellerde Ağ Segmentasyonu

```
SSID: OtelMisafir    → VLAN 100 (yalnızca internet, hız sınırlı)
SSID: OtelPremium    → VLAN 101 (internet, daha yüksek hız sınırı)
SSID: OtelPersonel   → VLAN 200 (kurumsal LAN, PMS erişimi)
SSID: OtelArkaOfis   → VLAN 300 (yönetim sistemleri, POS)
SSID: OtelIOT        → VLAN 400 (TV'ler, termostatlar, kilitler)
```

Firewall kuralları: Misafir VLAN'ları (100, 101) → yalnızca internet. Personel VLAN'ı (200) → LAN + internet. Misafir ve personel ağları arasında katı izolasyon — istisna yok.

### Konferans ve Etkinlik WiFi'si

Konferans tesisi olan oteller ayrı bir zorlukla karşı karşıyadır: 200'den fazla kişinin cihazlarıyla bir odada olduğu etkinlikler için geçici yüksek yoğunluk deployment'ları.

Geçici taşınabilir AP'ler, bu etkinlikler için kalıcı kapsama alanını destekleyebilir — ancak etkinlik sırasında değil, etkinlikten önce önceden yapılandırılmış ve test edilmiş olmalıdır. Beklenen istemci sayısı ve kullanım desenleri için (hafif tarama, video akışı veya sunum araçları) etkinlik organizatörüyle koordine edin.

---

## Bölüm 3: Muayenehane WiFi Tasarımı

### Sağlık Hizmetlerine Özgü Gereksinimler

Muayenehanelerin, tipik KOBİ değerlendirmelerinin ötesine geçen WiFi gereksinimleri vardır:

**Cihaz çeşitliliği:** Klinik ortamlar alışılmadık bir cihaz karışımına sahiptir — kurumsal ağdaki HP dizüstü bilgisayarlar, EHR erişimi için iPad'ler, tıbbi cihazlar (infüzyon pompaları, hasta monitörleri, taşınabilir görüntüleme ekipmanı), misafir WiFi'sindeki hasta akıllı telefonları ve bina yönetim sistemleri.

**Uyumluluk:** ABD'de HIPAA (Sağlık Sigortası Taşınabilirlik ve Hesap Verebilirlik Yasası) — ve Almanya'da (DSGVO) ve AB'de eşdeğer düzenlemeler — hasta sağlık bilgilerinin (PHI) aktarım sırasında korunmasını gerektirir. PHI taşıyan ağlar için WiFi güçlü şifreleme kullanmalıdır (WPA2-Enterprise veya WPA3). Misafir WiFi'si, klinik ağlardan tamamen izole edilmelidir.

**Erişilebilirlik:** Klinik iş akışları ağ erişimine bağlıdır. Yoğun bir muayenehanede başarısız WiFi ağı gerçek operasyonel aksamaya neden olur — doktorlar hasta kayıtlarına erişemez, EHR sistemleri zaman aşımına uğrar ve personel kağıt çözümlerine başvurur.

### Muayenehaneler İçin Ağ Segmentasyonu

```
SSID: KlinikPersonel  → VLAN 10  (EHR, klinik uygulamalar, tam erişim, WPA2-Enterprise)
SSID: TibbiCihazlar   → VLAN 20  (tıbbi cihazlar, izole, WPA2-PSK)
SSID: HastaWiFi       → VLAN 30  (yalnızca internet, tamamen izole)
SSID: BinaYönetimi    → VLAN 40  (HVAC, erişim kontrolü, izole)
```

Tıbbi cihaz VLAN'ı (VLAN 20) özellikle önemlidir. Birçok tıbbi cihaz dahili olarak şifresiz protokoller kullanır — genel personel veya hasta cihazlarıyla hiçbir zaman ağ segmentini paylaşmamalıdır.

### Tıbbi Cihaz Değerlendirmeleri

WiFi'ye bağlı tıbbi cihazlar çoğunlukla alışılmadık özelliklere sahiptir:
- **Eski işletim sistemleri:** Bazı tıbbi cihazlar gömülü Windows XP veya Windows 7 çalıştırır. Güncellenemezler. Klinik kullanım için ağa erişilebilir olmaları gerekir ancak her şeyden izole edilmelidir.
- **Statik IP'ler:** Pek çok tıbbi cihaz, DHCP yerine statik IP atamaları gerektirir. Bunları dikkatli biçimde belgeleyin.
- **Frekans duyarlılığı:** Bazı eski tıbbi cihazlar yalnızca 2,4 GHz'de çalışır ve 5 GHz'e yetenekli değildir.
- **Düzenleyici sertifikasyon:** WiFi'li tıbbi cihazlar, üreticilerinin sertifikalandırdığı şekilde kullanılmalıdır. WiFi ağını cihaz bağlantısını etkileyen biçimlerde değiştirmek sertifikasyonu geçersiz kılabilir ve uyumluluk yükümlülüğü yaratabilir. Değişiklikleri her zaman cihaz üreticisiyle doğrulayın.

### HIPAA Kablosuz Uyum Kontrol Listesi

ABD muayenehaneleri için (HIPAA) — ve AB için eşdeğer (DSGVO):

- ✅ Klinik ağlarda WPA2-Enterprise veya WPA3-Enterprise (bireysel kullanıcı kimlik bilgileri, paylaşılan PSK değil)
- ✅ Klinik VLAN, misafir/hasta WiFi'sinden tamamen izole
- ✅ Klinik ağlardaki kablosuz trafik aktarım sırasında şifreli
- ✅ Kablosuz controller'da sahte AP tespiti etkin
- ✅ Kimlik doğrulama logları saklanıyor (kim bağlandı, ne zaman, nereden)
- ✅ Tıbbi cihaz ağı, klinik ve misafir VLAN'larından izole
- ✅ Misafir WiFi hizmet şartları belgelenmiş

---

## Tüm Ortamlarda Yaygın Hatalar

**1. Site survey yapmama**
RF ölçümü olmadan kat planlarına dayanarak AP yerleşimi planlamak tahmindir. Duvarlar, mobilyalar, ekipmanlar ve komşu ağlar tümü kapsama alanını kat planlarının yakalayamayacağı biçimlerde etkiler. Kurulumdan önce her zaman tahmine dayalı survey, sonrasında doğrulama survey yapın.

**2. Profesyonel ortamlarda tüketici ekipmanı kullanma**
Tüketici AP'leri (WiFi'li ev router'ları), band yönlendirmeden, uygun roaming desteğinden, kullanıcı başına QoS'tan, VLAN segmentasyonundan ve yönetim görünürlüğünden yoksundur. Başlangıçta çalışıyor gibi görünür ve yük altında veya zamanla sınırlarını ortaya koyarlar.

**3. VLAN segmentasyonu olmadan deployment**
Kurumsal cihazlarla aynı ağda misafir cihazlar, gerçekleşmeyi bekleyen bir güvenlik başarısızlığıdır. Bu, profesyonel ortamlarda isteğe bağlı değildir.

**4. İzleme yok**
Gecenin ortasında yeniden başlayan AP, bir hafta boyunca yanlış AP'ye bağlı kalan istemci, girişime neden olan kanal değişikliği — bunların hiçbiri kablosuz izleme olmadan görünür değildir. AP kullanılabilirliği, istemci sayısı anomalileri ve kanal kullanımı için uyarılar kurun.

**5. Power over Ethernet (PoE) planlamasını görmezden gelme**
Kurumsal AP'ler PoE gerektirir. Birden fazla radyolu bir Cisco veya Aruba WiFi 6 AP, 20–25 watt çeker. Tüm portlar 25W sağlayan 48 portlu bir switch, switch'in toplam PoE bütçesini aşar. Donanım satın almadan önce PoE kapasitesini planlayın.

---

## Temel Çıkarımlar

- WiFi tasarımı ortama özgüdür. Otel için tasarım desenleri temel olarak ofisten farklıdır; bu da muayenehaneden farklıdır.
- **Kullanıcı başına bant genişliği yönetimi**, konaklama ortamlarında pazarlık konusu değildir — onsuz adillik imkânsızdır.
- **PMS entegrasyonu**, otellerde personel müdahalesi olmadan misafir erişim yaşam döngüsünü otomatikleştirir.
- **VLAN segmentasyonu**, her profesyonel ortam için taban çizgisidir — misafir, kurumsal, IoT ve yönetim ağları izole edilmelidir.
- **Tıbbi cihaz WiFi'si** özel yönetim gerektirir — eski işletim sistemi, statik IP'ler, düzenleyici sertifikasyon kısıtlamaları.
- **Site survey** isteğe bağlı değildir — deployment'ın güvenilmeden önce çalışacağını doğrulamanın tek yoludur.

---

## Bu Seri

- 📖 [Kurumsal WiFi Mimarisi Genel Bakış](/tr/technology/kurumsal-wifi-mimarisi-tam-rehber/) ← Buradan başlayın
- 📡 [802.11 Standartları Deep Dive](/tr/technology/wifi-80211-standartlari-wifi4-wifi5-wifi6/)
- 🏢 [Kurumsal Controller Mimarisi: Cisco ve Aruba](/tr/technology/kurumsal-wifi-controller-mimarisi-cisco-aruba/)
- 🔐 [WiFi Güvenliği: WPA3, 802.1X, Sahte AP, Site Survey](/tr/technology/wifi-guvenligi-wpa3-8021x-site-survey/)

## İlgili Yazılar

- 📡 [NAS Yedekleme ve AWS S3 — KOBİ'ler için Veri Güvenliği](/tr/technology/nas-backup-aws-s3-cloud-kobi/) — WiFi'nin yanında KOBİ veri koruma
- 🔐 [802.1X Kimlik Tabanlı Mimari Sahada](/tr/technology/identity-based-microsegmentation-8021x/) — Kurumsal kablosuz için kimlik katmanı
- 🏗️ [IT Altyapısı Ürünler Koleksiyonu Değildir](/tr/architecture/it-infrastructure-not-a-collection-of-products/) — Ağ tasarımında sistem düşüncesi