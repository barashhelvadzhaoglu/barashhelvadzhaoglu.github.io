---
title: "Kurumsal WiFi Controller Mimarisi: Cisco ve Aruba WLAN Tasarımı"
description: "Kurumsal kablosuz controller mimarileri — Cisco WLC ile DNA Center, Aruba Mobility Master ile Central, merkezi ve dağıtık tasarımlar."
date: 2026-04-17
draft: false

cover:
  image: "/img/postimages/wifi-controller-architecture-cover.webp"
  alt: "Kurumsal WiFi Controller Mimarisi — Cisco Aruba WLAN Tasarımı"
  relative: false

tags: ["WiFi", "Aruba", "Cisco", "WLAN Controller", "Mobility Master", "DNA Center", "Kurumsal Kablosuz", "Ağ Mimarisi"]
categories: ["Teknoloji"]
keywords:
  - Cisco WLC mimarisi
  - Aruba Mobility Master
  - kurumsal WLAN tasarımı
  - Aruba Central bulut WiFi
  - Cisco DNA Center kablosuz
  - CAPWAP tünel kablosuz
  - mobilite alanı roaming
  - kablosuz controller HA
  - Aruba ClearPass entegrasyonu
  - Cisco ISE kablosuz

showToc: true
TocOpen: true
---

# Kurumsal WiFi Controller Mimarisi: Cisco ve Aruba WLAN Tasarımı

Bu yazı Kurumsal WiFi serisinin bir parçasıdır.

> **Kurumsal kablosuz ağa yeni misiniz?** Genel bakışla başlayın: [Kurumsal WiFi Mimarisi: Standartlardan Deployment'a](/tr/technology/kurumsal-wifi-mimarisi-tam-rehber/)

---

## Controller Mimarisi Neden Önemli

Bir erişim noktası yalnızca bir radyo vericisidir. Onu kurumsal bir ağın parçası yapan — tutarlı politika, kesintisiz roaming, merkezi yönetim ve güvenlik entegrasyonu ile — arkasındaki controller mimarisiddir.

Controller mimarisini yanlış kurarsanız şunları elde edersiniz:
- Binalar veya katlar arasında roaming başarısızlıkları
- Farklı AP gruplarında tutarsız güvenlik politikaları
- İstemci bağlantılarını yavaşlatan kimlik doğrulama darboğazları
- Rutin değişiklikleri çok adımlı operasyonlara dönüştüren yönetim karmaşıklığı

Doğru kurarsanız, kablosuz ağ kablolu altyapının bir uzantısı gibi davranır — tutarlı, yönetilebilir ve kimlik ve güvenlik sistemleriyle entegre.

---

## Üç Mimari Model

### Model 1: Merkezi Controller (Geleneksel)

Tüm zeka controller'da bulunur. AP'ler "ince"dir — RF iletir ve tüm trafiği controller'a yönlendirir:

```
[AP] ──CAPWAP veri tüneli──→ [WLC] → Çekirdek Switch → Ağ
[AP] ──CAPWAP veri tüneli──→ [WLC]
[AP] ──CAPWAP veri tüneli──→ [WLC]
```

**CAPWAP (Control and Provisioning of Wireless Access Points)**, AP'ler ile controller arasındaki protokoldür. Şunları taşır:
- **Kontrol düzlemi:** AP kaydı, yapılandırma, RF yönetimi, roaming kararları
- **Veri düzlemi:** İstemci trafiği (merkezi modda, tüm istemci verisi controller'dan geçer)

**Avantajlar:**
- Tüm istemciler ve trafik üzerinde merkezi görünürlük
- Controller alanı içinde kesintisiz roaming — istemci durumu controller'da kalır, AP'de değil
- Tutarlı politika uygulaması — her istemci aynı controller'dan geçer

**Dezavantajlar:**
- WLC tek hata noktasıdır (HA çifti gerektirir)
- Trafik hairpin gecikme ve controller bant genişliği tüketimi ekler
- Ölçeklendirme controller kapasitesi eklemeyi gerektirir

**Kullanıldığı yer:** Şirket içi altyapıya sahip büyük kampüs deployment'ları, yerel trafik kontrolü gerektiren düzenlenmiş ortamlar.

### Model 2: Dağıtık / FlexConnect

Controller'ın yapılandırma ve politikayı yönettiği, ancak istemci veri trafiğinin AP'de veya şube switch'inde yerel olarak anahtarlandığı hibrit bir model:

```
Merkezi Site:               Şube Sitesi:
[WLC]                       [AP FlexConnect] ──yerel switch──→ LAN
  │                          │
  └──WAN──────────yalnızca CAPWAP kontrolü──
```

FlexConnect modunda, AP şubede mevcut olan VLAN'lar için yerel anahtarlama yapar. WAN bağlantısı başarısız olursa, istemciler yerel kaynaklara erişmeye devam edebilir — AP önbelleğe alınmış yapılandırmayla bağımsız modda çalışır.

**Kullanıldığı yer:** Tüm trafiği genel merkeze yönlendirmenin pratik olmayacağı, merkezi bir WLC'ye WAN üzerinden bağlı şube ofisleri.

### Model 3: Bulut Yönetimli

Yönetim ve yapılandırma bir bulut platformu tarafından yönetilir. Veri trafiği doğrudan yerel ağa gider — hairpin yok:

```
[AP] ──veri──→ Yerel switch → Ağ (doğrudan, controller hairpin yok)
[AP] ──yönetim tüneli──→ Bulut Panosu (yapılandırma, izleme)
```

AP'ler yapılandırma ve telemetri için bulutla iletişim kurar, ancak istemci verisi asla yerel ağı terk etmez. Bulut bağlantısı kesilirse, AP'ler son bilinen yapılandırmalarıyla çalışmaya devam eder.

**Kullanıldığı yer:** Her sitede özel ağ personeli olmayan çok siteli organizasyonlar, KOBİ ortamları, perakende zincirleri, konaklama.

---

## Cisco Kablosuz Mimarisi

### Geleneksel: Cisco WLC + Lightweight AP'ler

Klasik Cisco kurumsal kablosuz mimarisi:

- **Cisco WLC (Wireless LAN Controller):** Donanım cihazları (9800 serisi, eski 5508, 8540) veya sanal (C9800-CL). Modele bağlı olarak binlerce AP'ye kadar yönetir.
- **Lightweight AP'ler (LWAPP/CAPWAP):** CAPWAP modunda çalışan Cisco Catalyst ve Aironet AP'ler.

**HA yapılandırması:** WLC çiftleri, Stateful Switchover (SSO) ile Aktif-Yedek modunda çalışır. İstemci oturumları yedek WLC'ye yansıtılır — failover istemcilere şeffaftır.

```
WLC-Birincil (Aktif)  ←── HA bağlantısı ──→  WLC-İkincil (Yedek)
       │                                              │
    [AP'ler]                                       [AP'ler]
```

**Mobilite Grubu:** Aynı kampüsteki birden fazla WLC, Mobilite Grubu oluşturur — istemciler, farklı WLC'ler tarafından yönetilen AP'ler arasında kesintisiz Katman 2 veya Katman 3 mobilitesiyle dolaşabilir.

### Modern: Cisco DNA Center + Catalyst Center

Cisco'nun mevcut kurumsal platformu:

- **Catalyst Center (eski adıyla DNA Center):** Yönetim, otomasyon ve güvence platformu. Özel donanım cihazları üzerinde çalışır.
- **SD-Access:** Cisco'nun kampüs fabric teknolojisi — kablosuz ve kablolu portlar, tutarlı VLAN ve SGT (Security Group Tag) atamasıyla aynı politika fabric'ine katılır.
- **AI geliştirilmiş RRM:** Tarihsel RF verilerine dayalı kanal ve güç atamalarını optimize etmek için makine öğrenmesi kullanan Radyo Kaynak Yönetimi.

**ISE entegrasyonu:** Cisco Identity Services Engine, 802.1X kimlik doğrulaması ve politika sağlar. Bir istemci bağlandığında, ISE onu doğrular, bir güvenlik grubu atar ve DNA Center karşılık gelen ağ politikasını uygular — istemci kablolu veya kablosuz olsun tutarlı.

### Cisco Meraki: Bulut Yönetimli Sadelik

Meraki, Cisco'nun kurumsal esneklik yerine operasyonel sadelik için tasarlanmış bulut yönetimli platformudur:

- **Pano:** Tüm yönetim tek bir bulut portalı üzerinden. Sıfır şirket içi controller donanımı.
- **Otomatik sağlama:** Yeni AP'ler bağlandığında otomatik olarak sağlanır — manuel yapılandırma yok.
- **Entegre güvenlik:** Meraki AP'ler yerleşik IDS/IPS, içerik filtreleme ve trafik analitiği içerir.
- **MX entegrasyonu:** Meraki kablosuz, Meraki MX güvenlik cihazlarıyla yerel olarak entegre olur — kablolu ve kablosuz arasında birleşik politika.

**Takas noktaları:** Karmaşık kurumsal politikalar için Catalyst Center'dan daha az esnek. Tüm yönetim bulut bağlantısı gerektirir (AP'ler çevrimdışı olsa da çalışmaya devam eder, ancak yapılandırılamaz). Abonelik tabanlı lisanslama.

**Meraki'nin üstün olduğu yer:** Çok siteli perakende, konaklama, KOBİ, şube ofisleri — operasyonel sadelik ve hızlı deployment'ın derin kurumsal özelleştirmeden daha önemli olduğu herhangi bir senaryo.

---

## Aruba Kablosuz Mimarisi

### Geleneksel: Aruba Mobility Master + Mobility Controller'lar

Aruba'nın şirket içi kurumsal mimarisi:

- **Mobility Master (MM):** Üst düzey yönetim ve orkestrasyon platformu. Veri trafiğini iletmez — yalnızca kontrol düzlemi.
- **Mobility Controller'lar (MC):** Yerel AP'leri için AP yönetimini, istemci kimlik doğrulamasını ve veri iletimini yöneten dağıtık controller'lar.
- **AP'ler:** Atanmış controller'larına bağlı, "kampüs AP" modunda Aruba erişim noktaları.

```
[Mobility Master]
        │
   ┌────┴────┐
[MC-1]     [MC-2]      ← Dağıtık controller'lar
  │           │
[AP'ler]   [AP'ler]
```

**Mobility Master hiyerarşisi**, yönetim karmaşıklığını veri düzlemi ölçeğinden ayırır. MM, küresel politikayı, yazılım yönetimini ve RF planlamasını yönetir. Controller'lar yerel AP yönetimini ve istemci verilerini yönetir. Bu mimari, büyük, çok binali kampüsler için iyi ölçeklenir.

**Küme mobilitesi:** Aynı kümede bulunan controller'lar istemci durumunu paylaşır. Aynı kümedeki farklı controller'lardaki AP'ler arasında roaming kesintisizdir — istemcinin kimlik doğrulaması ve oturumu onunla birlikte taşınır.

### Modern: Aruba CX + AOS 10

Aruba'nın mevcut mimarisi (AOS 10) dağıtık, fabric entegre bir modele doğru kayıyor:

- AP'lerin daha fazla yerel zekası var — kimlik doğrulama ve politika uygulaması, her paket için controller katılımı olmadan AP'de gerçekleşebilir
- Birleşik kablolu/kablosuz politika için Aruba CX switching fabric ile entegrasyon
- Yönetim düzlemi olarak Aruba Central — bulut tabanlı, birçok deployment için şirket içi Mobility Master'ın yerini alıyor

### Aruba Central: Bulut Yönetimli Kurumsal

Cisco Meraki'den farklı olarak (sadelik için tasarlanmış), Aruba Central kurumsal kaliteli bulut yönetimi olarak konumlandırılmıştır:

- Bulut yönetimi aracılığıyla tam kurumsal politika yetenekleri
- AI destekli ağ içgörüleri ve anomali tespiti
- 802.1X kimlik doğrulaması için ClearPass entegrasyonu (yalnızca şirket içi değil, bulut bağlantılı)
- Çok büyük deployment'lar için destek (binlerce AP, yüzlerce site)

**ClearPass entegrasyonu**, Aruba'nın en güçlü farklılaştırıcısıdır: 802.1X, cihaz profillemesi, misafir portalı, posture değerlendirmesi ve dinamik VLAN atamasını yöneten özel bir NAC platformu. ClearPass, kapsamlı kimlik tabanlı ağ erişimi için Active Directory, LDAP ve üçüncü taraf MDM sistemleriyle entegre olur.

---

## Roaming Mimarisi: Kritik Tasarım Kararları

### Katman 2 Roaming

İstemci AP-1'den AP-2'ye geçer, her ikisi de aynı VLAN'da ve aynı controller tarafından yönetilir. İstemcinin IP adresi değişmez. Roaming hızlı ve şeffaftır.

```
AP-1 (VLAN 10) ──→ İstemci dolaşır ──→ AP-2 (VLAN 10)
Aynı alt ağ, aynı controller, istemci IP değişmez
```

### Katman 3 Roaming

İstemci alt ağlar arasında geçer — farklı controller'lardaki veya binalardaki farklı VLAN'lar. Özel yönetim olmadan, istemcinin yeni bir IP adresine ihtiyacı olur ve aktif oturumlar kesilir.

Kurumsal controller'lar, **mobilite tüneli** aracılığıyla Katman 3 roaming'i yönetir — orijinal controller ("anchor") istemcinin orijinal IP adresini korur ve trafiği istemcinin mevcut controller'ına ("foreign") tünel üzerinden iletir:

```
İstemci AP-1'e bağlanır (Bina A, VLAN 10, Controller-1)
İstemci AP-2'ye dolaşır (Bina B, VLAN 20, Controller-2)

Controller-2 (foreign) ──mobilite tüneli──→ Controller-1 (anchor)
İstemci IP: hâlâ VLAN 10'dan 192.168.10.x
Oturum: kesintisiz
```

Bu ek yük ekler — dolaşan istemcinin trafiği controller'lar arası tüneli geçmek zorundadır. Çoğu uygulama için bu ihmal edilebilir düzeydedir. Gecikmeye duyarlı uygulamalar (VoIP, gerçek zamanlı video) için anchor-to-foreign tünel uzunluğunu en aza indirin.

### Hızlı Roaming: 802.11r/k/v

Standartlar yazısında ele alındığı gibi, kurumsal deployment'ların tüm üç hızlı roaming protokolünü etkinleştirmesi gerekir. Controller perspektifinden:

- **802.11r:** Controller, istemci mevcut AP'den bağlantısını kesmeden önce hedef AP ile istemciyi önceden doğrular. Controller düzeyinde koordinasyon gerektirir.
- **802.11k:** Controller, komşu AP bilgilerini istemcilere sağlar. İstemciler bunu daha iyi roaming kararları vermek için kullanır.
- **802.11v:** Controller, bir istemcinin belirli bir AP'ye dolaşmasını önerebilir veya talep edebilir — yük dengeleme ve yapışkan istemci yönetimi için kullanışlı.

**Opportunistic Key Caching (OKC):** WPA2-Enterprise (802.1X) kullanan ağlar için OKC, istemcinin yeni bir AP'ye dolaşırken önbelleğe alınmış bir PMK'yı (Pairwise Master Key) yeniden kullanmasına olanak tanır ve tam 802.1X yeniden doğrulamasını önler. 802.1X ağlarında roaming süresini önemli ölçüde azaltır.

---

## Radyo Kaynak Yönetimi

Kurumsal controller'lar, Radyo Kaynak Yönetimi (RRM) aracılığıyla RF ortamını sürekli olarak optimize eder:

### İletim Gücü Kontrolü

Controller, AP'ler arasında RSSI'yi (sinyal gücü) izler. Bir AP komşulardan güçlü sinyaller algılarsa, iletim gücünü azaltır — bitişik hücrelerle girişimi azaltırken kapsama alanını korur.

**Kapsama boşluğu tespiti:** Bir istemci düşük RSSI bildirirse, controller kapsama boşluklarını önlemek için AP'nin iletim gücünü artırabilir. Bu kapsama boşluklarını önler ancak komşu AP'lerle girişim karşı dengelenmelidir.

### Dinamik Kanal Atama

Controller RF ortamını tarar ve aynı kanaldaki girişimi en aza indirmek için kanallar atar:
- AP'ler komşu AP sinyallerini ve istemci girişimini raporlar
- Controller bir RF topoloji haritası oluşturur
- Kanallar, aynı kanaldaki AP'ler arasındaki ayrımı en üst düzeye çıkarmak için atanır

Cisco'da bu **RRM (Radyo Kaynak Yönetimi)**'dir. Aruba'da ise **ARM (Adaptive Radio Management)**. Her ikisi de özerk çalışır, ancak bilinen RF zorluklarında manuel geçersiz kılmadan yararlanır.

### İstemci Yük Dengeleme

Birden fazla AP aynı alanı kapladığında (örtüşen hücreler), controller istemcileri AP'ler arasında dağıtabilir:
- Her ikisi de kapsama alanındayken yeni istemcileri daha az yüklü AP'ye yönlendirin
- Aşırı yüklü AP'lerden daha az yüklü komşulara istemci taşıyın

Bu dikkatli ayarlama gerektirir — agresif yük dengeleme istemcilerin gereksiz yere dolaşmasına neden olur.

---

## Controller Mimarisinde HA ve Yedeklilik

### WLC HA (Cisco)

Cisco 9800 WLC'ler, **High Availability SSO (Stateful Switchover)** destekler:

```
WLC-Aktif ──RP (Yedeklilik Portu)──→ WLC-Yedek
     │                                      │
Yapılandırma yansıtıldı              İstemci oturumları yansıtıldı
```

Aktif WLC başarısız olduğunda, yedek tam istemci oturum durumuyla devralır — istemciler yeniden bağlanmaz. AP'ler CAPWAP tünellerini korur; geçiş şeffaftır.

**N+1 yedeklilik:** Büyük deployment'larda, birden fazla WLC AP yükünü paylaşır. Biri başarısız olursa, AP'leri kalan WLC'lere yeniden kaydeder. AP geri dönüş önceliklerini yapılandırmayı gerektirir.

### Aruba Controller HA

Aruba, birden fazla controller'ın AP ve istemci yükünü paylaştığı **Aktif-Aktif** küme yapılandırmalarını destekler:

```
[MC-1] ←─ küme ─→ [MC-2] ←─ küme ─→ [MC-3]
  │                   │                   │
[AP'ler]           [AP'ler]           [AP'ler]
```

MC-1 başarısız olursa, AP'leri MC-2 ve MC-3'e dağıtır. İstemci oturumları küme durum paylaşımı aracılığıyla korunur.

### Bulut Yönetimi Dayanıklılığı

Bulut yönetimli AP'ler (Meraki, Aruba Central), bulut bağlantısı kesilmesi sırasında çalışmaya devam eder:
- AP'ler son bilinen yapılandırmayı korur
- İstemciler normal şekilde bağlanıp dolaşabilir
- Yönetim operasyonları (yapılandırma değişiklikleri, izleme) bulut bağlantısı gerektirir

İnternet bağlantısından bağımsız olarak garantili yönetim erişimi gerektiren ortamlar için, şirket içi controller mimarisi daha uygun olmaya devam eder.

---

## Kimlik Sistemleriyle Entegrasyon

### Cisco ISE Entegrasyonu

802.1X için Cisco ISE kullanan deployment'lar için:

```
İstemci WiFi'ye bağlanır
      ↓
AP, ISE'ye RADIUS isteği gönderir (WLC aracılığıyla)
      ↓
ISE, Active Directory'e karşı doğrular
      ↓
ISE döndürür: VLAN ataması + Security Group Tag
      ↓
WLC politikayı uygular: istemci doğru VLAN'a yerleştirilir
      ↓
DNA Center, SGT tabanlı politikayı uçtan uca uygular
```

ISE posture değerlendirmesi, tam ağ erişimi vermeden önce cihaz uyumluluğunu da kontrol edebilir (AV durumu, işletim sistemi yama seviyesi) — kablolu ve kablosuz istemciler için özdeş davranış.

### Aruba ClearPass Entegrasyonu

ClearPass, Aruba deployment'ları için eşdeğer yetenekler sağlar:

- RADIUS aracılığıyla 802.1X kimlik doğrulaması
- 802.1X supplicant'ı olmayan cihazlar için MAC Authentication Bypass (MAB)
- Cihaz profilleme — DHCP, HTTP User-Agent ve CDP/LLDP sinyallerine dayalı cihaz türünü (telefon, dizüstü, yazıcı, IoT) tanımlama
- Misafir portalı — kendi kendine kayıt veya sponsor onayı iş akışları
- Kullanıcı kimliğine, cihaz türüne ve posture'a dayalı dinamik VLAN ve rol ataması

ClearPass'ın **OnGuard** ajanı posture değerlendirmesi yapar — kurumsal dizüstü bilgisayarların güncel AV, gerekli yamalar ve onaylı yazılıma sahip olup olmadığını kontrol eder.

---

## Temel Çıkarımlar

- Controller mimarisi roaming kalitesini, politika tutarlılığını ve operasyonel karmaşıklığı belirler — yalnızca yönetim kolaylığını değil.
- **Merkezi WLC**, trafik hairpin ve tek hata noktası riski pahasına kesintisiz roaming ve tutarlı politika sağlar (HA ile hafifletilir).
- **Bulut yönetimi** (Meraki, Aruba Central), şirket içi donanım olmadan operasyonel sadelik ve çok siteli ölçek sunar.
- **Hızlı roaming (802.11r/k/v + OKC)**, ses ve video uygulamaları için controller düzeyinde etkinleştirilmelidir — varsayılan yapılandırma nadiren optimaldir.
- **ISE/ClearPass entegrasyonu**, kablosuzu "bir ağ"dan "kimlik bilincine sahip bir politika uygulama noktası"na dönüştürür — kablolu ve kablosuz için tutarlı davranış, hepsi kimin ve neyin bağlandığına dayalı.

---

## Bu Seri

- 📖 [Kurumsal WiFi Mimarisi Genel Bakış](/tr/technology/kurumsal-wifi-mimarisi-tam-rehber/) ← Buradan başlayın
- 📡 [802.11 Standartları Deep Dive](/tr/technology/wifi-80211-standartlari-wifi4-wifi5-wifi6/)
- 🏨 [KOBİ, Oteller ve Muayenehane İçin WiFi Tasarımı](/tr/technology/wifi-tasarimi-kobi-otel-saglik/)
- 🔐 [WiFi Güvenliği: WPA3, 802.1X, Sahte AP, Site Survey](/tr/technology/wifi-guvenligi-wpa3-8021x-site-survey/)

## İlgili Yazılar

- 🔐 [802.1X Kimlik Tabanlı Mimari Sahada](/tr/technology/identity-based-microsegmentation-8021x/) — 802.1X deployment'ına derinlemesine bakış
- 🏗️ [IT Altyapısı Ürünler Koleksiyonu Değildir](/tr/architecture/it-infrastructure-not-a-collection-of-products/) — Kablosuz için sistem düşüncesi
- 📊 [İzleme Doğru Yapıldığında](/tr/architecture/monitoring-not-just-seeing/) — Kablosuz altyapıyı proaktif olarak izleme