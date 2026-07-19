---
title: "802.1X Projeleri: Kimliği Ağa Taşıyan Mimariyi Sahada Kurmak"
description: "802.1X projelerinin networkten ziyade AD, PKI ve GPO disiplinine bağlı başarısını ele alan saha tecrübesi dökümanı."
date: 2026-01-14
draft: false

cover:
  image: "/img/postimages/zero-trust-access-layer-802-1x.webp"
  alt: "802.1X Kimlik Tabanlı Ağ Erişim Mimarisi"
  relative: false

tags: ["802.1X", "NAC", "Zero Trust", "PKI", "Active Directory", "Ağ Güvenliği"]
categories: ["Teknoloji"]
keywords:
  - 802.1X
  - NAC kurulumu
  - ağ güvenliği
  - mikro segmentasyon
  - Active Directory
  - PKI
  - sertifika yönetimi
  - Zero Trust
  - Ağ Erişim Kontrolü
showToc: true
TocOpen: false
---

# 802.1X Projeleri: Kimliği Ağa Taşıyan Mimariyi Sahada Kurmak

802.1X projeleri dışarıdan bakınca **network işi** gibi görünür; çünkü dokunulan yer switch portlarıdır, SSID'lerdir, RADIUS'tur. Ama gerçek hayatta 802.1X'in başarısı çoğu zaman network cihazlarının üzerinde değil; **Active Directory düzeninde**, **sertifika altyapısında (PKI)** ve **uç cihaz yönetiminde** belirlenir. Bunun nedeni basit: 802.1X, portun VLAN'ını değil, kurumun **"kimlik modelini"** konuşmaya zorlar. Yani "hangi port hangi VLAN"dan, **"hangi kimlik hangi yetkiyle ağa girer"** düzenine geçersin.

{{< figure src="/img/postimages/8021x-nac-architecture-overview.webp" title="802.1X NAC Mimarisine Genel Bakış" >}}

Bu geçiş, bir kurumun alışkanlıklarını değiştirir. Çünkü 802.1X devreye girdiğinde network, artık **"kablo takınca çalışan"** bir şey olmaktan çıkar; doğrulama geçemeyen cihaz için **karantina**, misafir için **portal**, yanlış OU'da duran bilgisayar için **yanlış VLAN** gibi sonuçlar üretir. Bu yüzden ben 802.1X'i bir özellik olarak değil, **kurumsal bir yetkinlik** olarak görüyorum: kimlik, envanter, politika ve operasyonun aynı masaya oturduğu bir yetkinlik.

**Özet (sadece kilit):**
- 802.1X port güvenliği değil, **kimlik mimarisidir.**
- Başarı network'ten çok **AD/PKI/endpoint disiplinine** bağlıdır.

> Kimlik tabanlı erişimin arkasındaki Zero Trust zihniyeti için: [Zero Trust Zihniyeti: Güvenliği Ürün Değil Mimari Olarak Tasarlamak](/tr/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/)

### 1) Planlama: VLAN planı yoksa 802.1X "kural motoru" değil "kaos motoru" olur

802.1X'e geçerken herkesin ilk refleksi şudur: "RADIUS kurarız, switch'e yazarız, biter." Sahada bunun bittiği yer genelde ilk **pilot kullanıcıdır.** Çünkü pilot kullanıcı bağlanır ve bir anda şu soru çıkar: "Bu kullanıcı hangi VLAN'a gidecek?" İşte 802.1X'in seni zorladığı yer burasıdır.

Eğer kurumda anlamlı bir **VLAN/segmentasyon planı** yoksa, 802.1X devreye alındığında bütün eksikler görünür hale gelir. Muhasebe ile üretim aynı segmentteyse, kamera ile kullanıcı laptop'u aynı ağdaysa, printer VLAN'ı diye bir kavram hiç yoksa; 802.1X bu yapıyı **"otomatikleştiremez"**, sadece **"otomatik şekilde yanlış"** yapar.

Bu yüzden proje başlamadan önce kullanıcı ve cihazları **"sınıflara"** ayırmak gerekir: departmanlar (**muhasebe, finans, HR…**), cihaz tipleri (**printer, IP phone, camera, badge reader…**), sunucu segmentleri (**AD/DC, file, mail, web/DMZ**), misafir segmenti, karantina segmenti. Bu segmentler yalnızca IP planı değildir; aynı zamanda **erişim politikasının zeminidir.** Bunlar 802.1X'ten sonra **"sonradan düşünülürse"**, proje bitmez.

**Özet:**
- **VLAN planı = politika planı.**
- 802.1X, segmentasyon kararını **"ertelenemez"** hale getirir.

### 2) Network hazırlığı: 802.1X devreye girmeden önce her VLAN manuel çalışmalı

802.1X'e geçmeden önce VLAN'ların switch ve firewall üzerinde tanımlı olması yetmez; **manuel test edilmesi** gerekir. Çünkü 802.1X devreye girdiğinde sorun çıktığında kök nedeni ayırmak zorlaşır: VLAN mı yanlış, firewall kuralı mı eksik, RADIUS mu yanlış, sertifika mı bozuk?

Benim sahada en çok önerdiğim akış şu: VLAN'ları oluştur, routing ve firewall kurallarını oturt, sonra bir test portunu **statik VLAN'a** al ve bir kullanıcıyla **"olması gereken erişim"** testlerini yap. Bu manuel test geçmeden 802.1X'e geçmek, gözü kapalı araç kullanmak gibi.

Bu aşamada ayrıca **management network** konusu kritik. Switch'lerin, WLC'nin, AP'lerin yönetim IP'leri ayrı bir **management VLAN'da** olmalı. **"Management VLAN"** yoksa, 802.1X pilotu sırasında bile cihaz yönetim erişimini kaybedip çok gereksiz kriz yaşanıyor.

**Özet:**
- 802.1X'ten önce **VLAN + FW kuralları manuel test edilmeden** ilerlenmez.
- **Management network** ayrı değilse, proje gereksiz risk taşır.

### 3) AD tarafı: OU düzeni olmayan yerde 802.1X hep "istisna yönetimi"ne döner

802.1X projelerinde en kritik noktalardan biri, kullanıcıyı ve bilgisayarı sınıflandırma işinin **"nerede"** yapıldığıdır. Çoğu kurumda kullanıcılar Users altında, bilgisayarlar Computers altında durur; departman ayrımı ya hiç yoktur ya da **"görsel düzen"** seviyesindedir. 802.1X devreye girdiğinde bu yapı yetmez.

Benim sahada **"best practice"** diye gördüğüm yapı şudur: her departman için bir **OU yapısı** oluşturmak ve kullanıcıyı da bilgisayarı da o OU'nun altında tutmak. Kullanıcı **OU=Finance** altında ama bilgisayar dağınıksa, **GPO dağıtımı** bozulur, **sertifika auto-enrollment** bozulur, 802.1X policy eşleştirme bozulur.

Benim önerdiğim yöntem: önce tek bir departmandan tek bir pilot kullanıcı ve pilot cihaz seç. OU taşımayı yap. **1 hafta–10 gün gözlemle.** Sorun çıkarsa OU/GPO düzeltmelerini yaparsın, sonra genişlersin.

**Özet:**
- **OU düzeni**, 802.1X'in görünmeyen omurgasıdır.
- OU taşıma kontrollü yapılmazsa **GPO/erişim** yan etkileri doğar.

### 4) Group Policy: 802.1X projelerinde "tek tek elle ayar" ölçeklenmez

802.1X'i pilotta elle kurarsın; üretime geçince **GPO'suz** yürüyemezsin. **Wired AutoConfig**, **WLAN AutoConfig**, EAP ayarları, sertifika seçimi, authentication öncelikleri... Bunları tek tek elle yönetmek hem hataya açık hem sürdürülemez.

GPO tarafında genelde üç şey yapılır: kablolu 802.1X profillerinin dağıtımı, kablosuz 802.1X profilleri ve **sertifika auto-enrollment**. Ayrıca **"kullanıcı bazlı 802.1X"** ile **"bilgisayar bazlı 802.1X"** aynı anda devredeyken Windows'un hangi sırayla deneyeceği önemlidir. Çoğu tasarımda **"önce bilgisayar auth, sonra kullanıcı auth"** modeli istenir.

**Özet:**
- GPO olmadan 802.1X üretime taşınmaz.
- **Auth sırası (machine vs user)** sahada fark yaratır.

### 5) RADIUS / NPS / NAC: "Konuşuyor" yetmez; hangi cevabı verdiği önemlidir

RADIUS tarafı çoğu ekipte "Switch'i tanıttık, secret verdik, oldu" gibi görülür. Bu sadece iletişimin başladığı yerdir. Asıl konu: RADIUS, switch'e hangi **VLAN / hangi ACL / hangi policy** cevabını veriyor?

- Basit dünyada RADIUS sadece **"accept/reject"** döner, VLAN statik kalır.
- Olgun dünyada RADIUS **"accept"** ile birlikte **dinamik VLAN** atar, **dACL/ACL** iter.

Sahada sık yapılan hata: network cihazlarını RADIUS client olarak tanımlarken **management IP** yerine farklı IP'ler kullanmak, yanlış **VRF/route** yüzünden RADIUS'a erişememek, **source-interface** yanlışlığı… Ben her projede önce en basit testle başlarım: switch'ten RADIUS'a reachability, RADIUS'ta log, sonra bir test port.

**Özet:**
- RADIUS "iletişim kurdu" diye proje bitmez; **"hangi policy cevabı dönüyor"** önemlidir.
- **Reachability/source-interface/VRF** hataları en klasik kök nedendir.

{{< figure src="/img/postimages/8021x-nac-posture-vlan-workflow.webp" title="NAC Posture Assessment ve VLAN Atama Akışı" >}}

### 6) EAP yöntemleri: PEAP mi, EAP-TLS mi, Computer mı User mı?

**PEAP (kullanıcı adı/şifre) neden pratik ama riskli:** PEAP kolaydır ama kullanıcı kişisel laptop'undan veya telefonundan da aynı kullanıcı adı/şifreyle ağa girebilir. **Zero Trust** mantığında hedef, sadece kullanıcıyı değil cihazı da doğrulamaktır.

**Computer authentication neden iyi ama bazı organizasyonlarda can yakar:** Bilgisayar doğrulaması kişisel cihazları engeller. Ancak ortak bilgisayar kullanılan yerlerde kullanıcı bazlı segmentasyon istiyorsan tek başına yeterli olmaz.

**EAP-TLS (sertifika) neden "en doğru" ama neden disiplin ister:** EAP-TLS'de **şifre sızsa bile sertifika yoksa erişim yoktur.** Ancak **PKI'nın** ayakta durması, template'lerin doğru olması, auto-enrollment'ın doğru işlemesi şarttır.

**Özet:**
- PEAP pratik ama **"kurumsal cihaz"** güveni zayıf kalır.
- **Computer auth** güçlü ama ortak PC senaryolarında sınırlıdır.
- **EAP-TLS** en güvenlisi; **PKI disiplini** şarttır.

### 7) PKI ve Certificate Template'ler: 802.1X'in sessiz kırılma noktası

EAP-TLS tasarlıyorsan, **Windows Certificate Services (AD CS)** üzerinde en az iki şey düşünmek zorundasın:
1. **İstemci sertifikaları:** (User certificate, Computer certificate)
2. **RADIUS server'ın** sunacağı server certificate

İstemci sertifikalarının dağıtımı çoğu yapıda **auto-enrollment** ile yapılır. Sahada en sık görülen hata: template hazırlanır ama güvenlik izinleri yanlış olduğu için kullanıcı/cihaz sertifika alamaz; ya da alır ama yanlış **EKU/KeyUsage** yüzünden EAP-TLS'de kullanılamaz.

**NPS (veya NAC)** istemciye bir server certificate sunar. İstemci bu sertifikaya güvenmezse **"man-in-the-middle"** gibi algılar ve bağlanmaz. Bu yüzden RADIUS server sertifikasının zinciri (CA) istemciye güvenilir olarak dağıtılmalıdır — bunun pratik yolu **Root CA** ve intermediate CA'ları GPO ile **"Trusted Root Certification Authorities"** alanına basmaktır.

Ayrıca NPS, istemcinin sunduğu sertifikayı doğrularken **CRL kontrolü** yapmak isteyebilir. CRL erişimi bozuksa, doğrulama gecikir veya fail olur. Bu detay sahada **"arada bağlanmıyor"** gibi sinir bozucu problemlerin klasik sebebidir.

**Özet:**
- **Template izinleri/amaçları** yanlışsa TLS biter.
- **Auto-enrollment + CA trust** dağıtımı GPO ile standardize edilmelidir.
- **CRL erişimi** bir gün patlayınca herkes "802.1X bozuldu" sanır.

### 8) Switch portunda Dot1X ve MAB birlikte: sıranın doğru yazılması gerçek hayatı kurtarır

Sahada en yaygın ve en mantıklı model: **önce dot1x dene; dot1x fail olursa MAB'a düş.** Çünkü laptop gibi akıllı uçlar 802.1X yapabilsin; printer/kamera gibi akıllı olmayanlar MAB ile yürüsün.

**MAB'ı yanlış önceliklendirdiğinde**, domain'e bağlı laptop bile MAB ile bağlanıp yanlış VLAN'a düşebilir. **"Tek tek port bazlı ilerlemek"** yaklaşımı kritik: **departman departman ilerlemek**; her departmanda önce 1–2 pilot kullanıcı, 1 hafta gözlem, sonra genişleme.

**Özet:**
- **Dot1X → fail olursa MAB** sırası çoğu ortam için en sağlıklısıdır.
- **Port bazlı kontrollü rollout**, "bir günde geçiş"ten daha hızlı bitirir.

### 9) Profiling: "Sadece MAC" dönemi bitti

**MAC authentication**, tek başına artık yeterli güvenlik değildir. Bu yüzden gelişmiş NAC çözümleri **profiling** yapar: **OUI kontrolü**, **DHCP fingerprint**, **CDP/LLDP**, cihaz açıklaması birlikte değerlendirilir. Böylece sahte cihazın **"ben printerım"** diyerek MAB üzerinden VLAN alması zorlaşır.

**Özet:**
- **MAC tek başına kimlik değildir**; profiling kimliğe yaklaşır.
- Birden fazla sinyal kullanmak sahadaki suistimali azaltır.

### 10) Quarantine VLAN ve Guest VLAN: İkisi aynı şey değil

**Quarantine:** şirketin cihazı/hesabı var ama doğrulamadan geçemiyor. **Karantina VLAN'ın amacı** cihazı tamamen kesmek değil; problemi çözebileceği **minimum erişimi** vermektir — AD'ye/CA'ya erişsin, şifre değiştirsin.

**Guest:** şirketin cihazı değil. Burada genelde sadece **internete** izin verirsin; AD/kerberos/LDAP gibi iç kaynaklara erişim hiç gereksizdir.

**Özet:**
- **Quarantine "bizim ama sorunlu"**; **Guest "bizden değil"**.
- İkisini aynı VLAN'a koymak pratikte güvenlik ve operasyonu bozar.

### 11) Guest portal: Sponsor login, SMS, sosyal login ve MAC randomization gerçeği

**Sponsor login** yaklaşımı kurumsal yapılarda çok işe yarar: misafir "kimi ziyaret ediyorum" der; sistem AD'den o kişiyi bulur; onay maili/push gider; onaylanınca misafir internete çıkar.

Modern telefonlar Wi-Fi'de **MAC randomization** yaptığında, kullanıcı Wi-Fi'yi kapatıp açınca cihaz "yeni cihaz" gibi görünebilir ve tekrar doğrulama ister. Bu kullanıcı deneyimini bozar — helpdesk'e **"internet gitti"** çağrısı yağar.

**Özet:**
- Portal modeli güvenlik kadar **UX tasarımıdır.**
- **MAC randomization** misafir akışını bozabilir; buna göre tasarlanmalıdır.

### 12) Posture: 802.1X'in "son kalesi" ama yanlış kurarsan operasyonu yorar

**Posture**, kullanıcı/cihaz kimliği doğru olsa bile, cihazın güvenlik durumu uygun değilse erişimi sınırlamaktır. Posture kontrolünde tipik olarak şunlar sorgulanır: **OS versiyonu, patch seviyesi, disk encryption durumu, AV var mı ve güncel mi, EDR agent çalışıyor mu.**

Posture'un bir bedeli var: çoğu zaman endpoint üzerinde **agent** gerekir. Bu yüzden mümkünse **"yeni agent" eklemek yerine, zaten kurulu olan ajanları reuse etmek** akıllıcadır. **Cisco** ortamında **AnyConnect**, **Fortinet** tarafında **FortiClient**, bazı yapılarda **Trellix** gibi EDR/AV ajanları kullanılabilir.

Posture tasarımında en çok önerdiğim pratik yaklaşım: posture'u ilk aşamada **"deny"** mekanizması olarak değil, **"gözlem ve raporlama"** mekanizması olarak başlat. **Posture, bir günde değil, bir süreçte olgunlaşır.**

**Özet:**
- **Posture "kimlik + sağlık" kontrolüdür**; drift'i yakalar.
- Yeni agent maliyetlidir; mevcut agent'ları **reuse etmek** akıllıcadır.
- İlk gün deny değil; **önce ölç, sonra sıkılaştır.**

### 13) Temel 802.1X → Profiling/Portal → Posture: Olgunluk seviyeleri

- **Seviye 1:** Dot1X + MAB — Windows NPS ile olur. Düşük maliyet, sınırlı yetenek.
- **Seviye 2:** Profiling + Guest Portal — **Cisco ISE, Aruba ClearPass** devreye girer. İş "cihazı tanıma ve misafiri yönetme"ye döner.
- **Seviye 3:** Posture — En çok güvenlik getirisi, en yüksek operasyonel maliyet. Organizasyonun **endpoint yönetim kabiliyeti, agent stratejisi ve helpdesk kapasitesi** gerçekçi değerlendirilmelidir.

### Kapanış: 802.1X "kurulum" değil, kurum içi sözleşmedir

802.1X projeleri teknik olarak switch'te birkaç komut, RADIUS'ta birkaç policy gibi görünebilir. Ama gerçekte 802.1X, kurum içinde şu sözleşmeyi zorunlu kılar: **"Kimlik nasıl taşınır, cihaz nasıl tanınır, misafir nasıl yönetilir, sorunlu cihaz nereye düşer, güvenlik hangi noktada başlar?"**

802.1X'in başarısı cihazların gücünden çok, **AD düzeninin, GPO disiplininin, PKI yönetiminin ve kademeli rollout** kültürünün toplamıdır. 802.1X'i böyle ele aldığında, sadece güvenliği artırmazsın; **operasyonu da merkezileştirirsin.**

---

## İlgili Yazılar

**Mimari & Güvenlik**
- 🔐 [Zero Trust Zihniyeti: Güvenliği Ürün Değil Mimari Olarak Tasarlamak](/tr/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — Kimlik tabanlı erişimin mimari temeli
- 🏗️ [IT Altyapısı Bir Ürün Koleksiyonu Değildir](/tr/architecture/it-infrastructure-not-a-collection-of-products/) — Sistem düşüncesi ve ürün seçimi
- 📊 [Monitoring Zihniyeti: Sadece Görmek Değil, Anlamak](/tr/architecture/monitoring-not-just-seeing/) — Policy ihlallerini tırmanmadan yakalamak

**Pratik Mühendislik**
- 🛡️ [Network Packet Broker (NPB) Masterclass](/tr/posts/network-packet-broker-masterclass/) — Trafik görünürlüğü ve güvenlik stratejisi
- 🎯 [Ağ Altyapısında Ürün Seçimi: Stratejik Kriterler](/tr/architecture/network-product-selection-strategy/) — NAC vendor değerlendirmesi