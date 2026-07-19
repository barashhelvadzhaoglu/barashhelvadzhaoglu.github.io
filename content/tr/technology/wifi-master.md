---
title: "Kurumsal WiFi Mimarisi: Standartlardan Deployment'a — Kapsamlı Rehber"
description: "Kurumsal kablosuz ağ master rehberi — 802.11 standartları, controller mimarileri, KOBİ ve otel tasarımı, roaming, güvenlik ve site survey."
date: 2026-04-01
draft: false

cover:
  image: "/img/postimages/enterprise-wifi-architecture-cover.webp"
  alt: "Kurumsal WiFi Mimarisi — Controller, Standartlar, Güvenlik"
  relative: false

tags: ["WiFi", "Kablosuz", "802.11", "Aruba", "Cisco", "Kurumsal Ağ", "WLAN", "Ağ Güvenliği"]
categories: ["Teknoloji"]
keywords:
  - kurumsal WiFi mimarisi
  - 802.11ax WiFi 6
  - Aruba kablosuz controller
  - Cisco Meraki WiFi
  - kurumsal WLAN tasarımı
  - WiFi güvenliği WPA3
  - otel WiFi altyapısı
  - WiFi site survey Ekahau
  - kablosuz roaming 802.11r
  - KOBİ WiFi tasarımı

showToc: true
TocOpen: false
---

# Kurumsal WiFi Mimarisi: Standartlardan Deployment'a

WiFi, herhangi bir ağın en görünür parçasıdır. Çalıştığında kimse söylemez. Çalışmadığında ise — dakikalar içinde IT ekibi binanın her köşesinden duyar.

Ancak kablosuz ağ oluşturma aldatıcı biçimde karmaşıktır. Bir kullanıcıya "sadece WiFi" gibi görünen şey, birbirleriyle etkileşen kararların bir yığınıdır: hangi 802.11 standardı, hangi frekans bandı, kaç erişim noktası, hangi controller mimarisi, kimlik doğrulamanın nasıl yönetileceği, roaming'in nasıl davranacağı, RF ortamının nasıl yönetileceği. Bunlardan herhangi birini yanlış yaparsanız, kağıt üzerinde iyi görünen ağ üretimde başarısız olur.

Aruba, Cisco Meraki ve Cisco kurumsal platformları kullanarak bankacılık genel merkezleri, üretim tesisleri, oteller, lojistik depoları ve muayenehanelerde kablosuz ağlar tasarladım ve deploy ettim. Bu seri, bu senaryoların her birinde gerçekte önemli olan şeyleri belgeliyor.

---

## Bu Seriyi Nasıl Okuyalım

Bu yazı size **büyük resmi** verir — kurumsal kablosuz mimarisinin neyi içerdiğini, temel kararların neler olduğunu ve her deep dive'ın nereye gittiğini.

**Mühendisseniz** ve belirli bir konuya derinlemesine inmek istiyorsanız — kullanım senaryonuzu kapsayan yazıya atlayın:

- 📡 **[802.11 Standartları Deep Dive: WiFi 4, 5, 6, 6E ve Gerçekte Ne Değişti](/tr/technology/wifi-80211-standartlari-wifi4-wifi5-wifi6/)** — ax, ac, n ve be'nin kapasite, kapsama alanı ve deployment kararları için gerçekte ne anlama geldiği
- 🏢 **[Kurumsal Controller Mimarisi: Cisco ve Aruba WLAN Tasarımı](/tr/technology/kurumsal-wifi-controller-mimarisi-cisco-aruba/)** — Merkezi ve dağıtık kontrol, mobilite alanları, WLC ve bulut yönetimi karşılaştırması
- 🏨 **[KOBİ, Oteller ve Muayenehane İçin WiFi Tasarımı](/tr/technology/wifi-tasarimi-kobi-otel-saglik/)** — Yoğunluk planlaması, misafir segmentasyonu ve beklenti yönetimi üzerine pratik saha notları
- 🔐 **[WiFi Güvenliği: WPA3, 802.1X, Sahte AP Tespiti ve Site Survey](/tr/technology/wifi-guvenligi-wpa3-8021x-site-survey/)** — Kimlik doğrulama, şifreleme, saldırı tespiti ve Ekahau survey metodolojisi

**Mimar veya karar vericiyseniz** ve kablosuz çözümleri değerlendiriyorsanız — burada okumaya devam edin. Bu yazı, RF uzmanlığı gerektirmeden stratejik soruları yanıtlar.

---

## WiFi Mimarisinin Erişim Noktası Sayısından Daha Fazlasını Neden Önemlidir

WiFi deployment'larındaki en yaygın hata: kablosuzu bir miktar problemi olarak ele almak. "Daha iyi WiFi'ye ihtiyacımız var — daha fazla erişim noktası ekleyelim."

Kötü tasarlanmış bir ağa erişim noktası eklemek onu daha da kötüleştirir. Aynı alanda daha fazla AP, daha fazla girişim, daha fazla kanal çakışması, daha fazla roaming olayı ve daha fazla karmaşıklık demektir — kullanıcı deneyiminde orantılı bir iyileşme olmadan.

Kurumsal kablosuz tasarımı erişim noktası yoğunluğu ile ilgili değildir. Şunlarla ilgilidir:

- **Kapasite planlaması:** Kaç eş zamanlı istemci, hangi veri hızlarına ihtiyaç duyarlar, hangi uygulamaları çalıştırıyorlar?
- **RF tasarımı:** Hangi kanallar, hangi güç seviyeleri, hangi band yönlendirme politikaları oluşturmak yerine girişimi önler?
- **Controller mimarisi:** Ağ kararları nasıl verir? Kimlik doğrulama nerede gerçekleşir? Roaming nasıl yönetilir?
- **Güvenlik:** Ağa kim, hangi kimlikle ve ne düzeyde erişimle izin verilir?
- **Operasyonel model:** Kim yönetir, nasıl izlenir, sorunlar nasıl teşhis edilir?

Bunları doğru yaparsanız erişim noktası sayısı bir başlangıç noktası değil, türetilmiş bir hesaplama olur.

---

## 802.11 Standartları: Gerçekte Ne Değişti

IEEE 802.11 standardı, her biri pazarlama amacıyla farklı biçimde markalanmış birden fazla nesil geçirdi:

| Standart | Pazarlama Adı | Maks Teorik Hız | Temel İyileştirme |
|---|---|---|---|
| 802.11n | WiFi 4 | 600 Mbps | MIMO, 5 GHz desteği |
| 802.11ac | WiFi 5 | 3,5 Gbps | MU-MIMO, daha geniş kanallar (80/160 MHz) |
| 802.11ax | WiFi 6 | 9,6 Gbps | OFDMA, BSS Boyama, TWT, yüksek yoğunluk |
| 802.11ax (6 GHz) | WiFi 6E | 9,6 Gbps | Yeni 6 GHz bandı, daha az tıkanıklık |
| 802.11be | WiFi 7 | 46 Gbps | Çok Bağlantılı Çalışma, 320 MHz kanallar |

Pazarlama materyallerindeki teorik hızlar pratikte hiçbir zaman ulaşılmaz. Gerçek deployment'larda önemli olan her nesil için farklıdır:

**WiFi 6 (802.11ax)**, yoğun ortamlarda gerçekten önemli iki yetenek getirdi:
- **OFDMA (Orthogonal Frequency Division Multiple Access):** Bir AP'nin bölünmüş frekans kaynakları üzerinde aynı anda birden fazla istemciye hizmet vermesini sağlar — bir seferde bir istemci iletim yapmak yerine, birden fazla istemci kanalı verimli biçimde paylaşır. Çok sayıda IoT cihazı, telefon ve tablet bulunan ortamlar için kritik.
- **BSS Boyama:** Örtüşen hücreler arasında aynı kanal girişimini azaltan bir mekanizma. Komşu AP'ler iletimlerini "boyar", bu da cihazların "benim AP'm" ile "yan odadaki AP" arasındaki ayrımı daha verimli yapmasını sağlar.

**WiFi 6E**, 6 GHz bandını ekledi — komşu ağlardan ve eski cihazlardan gelen girişimi ortadan kaldıran büyük ölçüde tıkanmamış bir spektrum. Yoğun kentsel ortamlarda önemli avantaj.

**WiFi 7** ortaya çıkıyor ve Çok Bağlantılı Çalışma (MLO) sayesinde tek bir cihazın aynı anda birden fazla bant ve kanalı kullanması — verimi iyileştiriyor ve gecikmeyi azaltıyor. 2026 itibarıyla hâlâ erken kurumsal deployment aşamasında.

→ **[802.11 Standartları Deep Dive](/tr/technology/wifi-80211-standartlari-wifi4-wifi5-wifi6/)**

---

## Controller Mimarisi: Zekanın Nerede Yaşadığı

Kurumsal kablosuz ağlarda iki temel mimari model vardır:

### Merkezi Controller (Geleneksel Kurumsal)

Tüm erişim noktaları "ince"dir — RF iletimini yönetirler ancak tüm trafiği ve tüm kontrol kararlarını merkezi bir Kablosuz LAN Controller'a (WLC) gönderirler:

```
[AP] ──CAPWAP tüneli──→ [WLC] → Çekirdek Ağ
[AP] ──CAPWAP tüneli──→ [WLC]
[AP] ──CAPWAP tüneli──→ [WLC]
```

WLC, kimlik doğrulamayı, roaming kararlarını, RF yönetimini, güvenlik politikasını ve trafik iletimini yönetir. AP'ler birbirinin yerine geçebilir — birini kaldırın ve yerine başkasını takın; WLC yapılandırmayı yönetir.

**Güçlü yönler:** Merkezi görünürlük, tutarlı politika uygulaması, controller alanı içinde kesintisiz roaming.

**Zayıf yönler:** WLC tek hata noktasıdır (HA çiftleriyle hafifletilir). Trafik, yerel iletişim için bile WLC üzerinden geçer. Ölçeklendirme WLC kapasitesi eklemeyi gerektirir.

Cisco'nun kampüs kablosuz platformu ve Aruba'nın Mobility Master/Controller mimarisi baskın örneklerdir.

### Bulut Yönetimli (Modern Yaklaşım)

Erişim noktalarının daha fazla zekası vardır. Yönetim, yapılandırma ve görünürlük buluttadır; veri düzlemi trafiği doğrudan ağa gider:

```
[AP] ──veri──→ Çekirdek Ağ (doğrudan, hairpin yok)
[AP] ──yönetim tüneli──→ Bulut Panosu
```

**Güçlü yönler:** Şirket içi controller donanımı yok. Dağıtık siteler arasında daha kolay yönetim. Yerleşik izleme ve analitik. Daha düşük operasyonel karmaşıklık.

**Zayıf yönler:** Yönetim için bulut bağlantısına bağımlı (AP'ler buluta ulaşılamazsa çalışmaya devam eder). Karmaşık kurumsal politikalar için daha az esnek.

Cisco Meraki ve Aruba Central, önde gelen bulut yönetimli platformlardır.

### Dağıtık / Kampüs Fabric

Modern büyük kampüs deployment'ları çoğunlukla kablosuzu daha geniş ağ fabric'ine entegre eder — AP'ler, cihaz kablo veya kablosuz bağlansın tutarlı erişim kontrolüyle kimlik tabanlı VLAN atamasıyla kablolu portlarla aynı politika ve segmentasyon modeline katılır.

SD-Access ile Cisco DNA Center ve Central ile Aruba CX bu yaklaşımın örnekleridir.

→ **[Kurumsal Controller Mimarisi Deep Dive](/tr/technology/kurumsal-wifi-controller-mimarisi-cisco-aruba/)**

---

## KOBİ, Otel ve Muayenehane: Tasarım Prensipleri

Tüketici WiFi ekipmanı, profesyonel ortamlarda düşük kalite nedeniyle değil — yoğunluk, yönetim gereksinimleri veya bu ortamların güvenlik beklentileri için tasarlanmadığı için başarısız olur.

### KOBİ (Küçük ve Orta Ölçekli İşletme)

Tipik KOBİ zorluğu: arka ofiste veya toplantı odasında WiFi'nin yavaş olduğundan şikayet eden personel — resepsiyonda tam sinyal olmasına rağmen. Kök nedenler neredeyse her zaman şunlardır:

- RF kapsamı yerine kablolama kolaylığına göre yerleştirilen AP'ler
- Kullanılabilir veri hızlarında fiziksel olarak kapsaması imkânsız bir katı kapsama almaya çalışan tek AP
- Band yönlendirme yok — yeni cihazlar beklerken eski cihazlar 2,4 GHz'i monopolleştiriyor
- QoS yok — video görüşmeleri dosya yedeklemeleriyle eşit rekabet ediyor

KOBİ kablosuz tasarım prensipleri:
- Ofis ortamlarında **150–200 m² başına bir AP** planlayın (evrensel kural değil, tipik yükler için gerçekçi bir başlangıç noktası)
- Her zaman misafir ve kurumsal trafiği ayırın (farklı SSID'ler, farklı VLAN'lar, aralarında firewall politikası)
- Operasyonel sadelik için bulut yönetimli AP'ler kullanın (Aruba Instant On, Meraki Go, Cisco Business)

### Otel WiFi'si

Oteller belirli bir zorluk sunar: odalarda yüksek istemci yoğunluğu (her misafir 3–5 cihaz getirir), günün saatine göre son derece değişken talep ve "WiFi"nin sıcak su gibi bir hizmet olduğu beklentisi — her zaman mevcut, hiçbir zaman düşünülmeyen.

Temel otel WiFi tasarım kararları:
- **AP yerleşimi:** Odaları kapsayan koridor AP'leri ve oda içi AP'ler karşılaştırması. Oda içi AP'ler odalar arasında daha iyi sinyal izolasyonu sağlar (daha az girişim) ancak daha yüksek deployment maliyeti ve bakım karmaşıklığı.
- **Bant genişliği yönetimi:** Kullanıcı başına hız sınırlama, tek misafirin paylaşılan uplink'i doyurmasını önler. Tek bir 4K video akışının düzinelerce diğer kullanıcıyı etkileyebildiği ortamlarda gerekli.
- **Misafir portalı:** Kimlik doğrulama, şartlar kabul, potansiyel olarak oda numarası doğrulama. Otomatik sağlama için PMS (Otel Yönetim Sistemi) ile entegrasyon.
- **Personel ve misafir ağı:** Tamamen ayrı — personel ağına hiçbir koşulda misafir ağından erişilememeli.

→ **[KOBİ, Oteller ve Muayenehane İçin WiFi Tasarımı Deep Dive](/tr/technology/wifi-tasarimi-kobi-otel-saglik/)**

---

## Roaming ve Band Yönlendirme

### Roaming: Göründüğünden Neden Daha Zordur

Roaming — bir istemcinin bir AP'den diğerine geçişi — pek çok kablosuz deployment'ın sessizce başarısız olduğu yerdir. Belirtiler "WiFi sorunları" gibi görünür ama kök neden roaming davranışıdır.

**Yapışkan istemci sorunu:** Bir istemci cihaz, AP değil, ne zaman dolaşacağına kendisi karar verir. 30 metre ötedeki AP-1'e güçlü bağlantısı olan bir dizüstü bilgisayar, 5 metre ötedeki AP-2'ye dolaşmayı reddedebilir, çünkü AP-1'e bağlantısı teknik olarak hâlâ işlevseldir. AP, istemciyi dolaşmaya zorlayamaz (istemci yönlendirme mekanizmaları kullanmadan).

**Hızlı roaming protokolleri:**
- **802.11r (Fast BSS Transition):** İstemcinin mevcut AP'den tam olarak bağlantısını kesmeden önce hedef AP ile önceden kimlik doğrulama yaparak roaming süresini azaltır. Bağlantı kesintilerinin görüşme düşmelerine neden olduğu ses ve video uygulamaları için gerekli.
- **802.11k (Komşu Raporları):** AP, istemciye yakındaki AP'lerin ve sinyal güçlerinin listesini sağlar, istemcilerin daha iyi roaming kararları vermesine yardımcı olur.
- **802.11v (BSS Geçiş Yönetimi):** AP'lerin bir istemcinin farklı bir AP'ye dolaşmasını önermesine veya talep etmesine olanak tanır — ağa istemci roaming davranışı üzerinde biraz etki verir.

Kurumsal deployment'larda, en iyi roaming davranışı için üç protokolün (topluca 802.11r/k/v olarak adlandırılır) birlikte etkinleştirilmesi gerekir.

### Band Yönlendirme

Çift bantlı AP'ler hem 2,4 GHz hem de 5 GHz üzerinde yayın yapar. Kendi tercihlerine bırakıldığında, birçok istemci 2,4 GHz'i seçer — daha uzun menzili vardır ve tanıdıktır. Ancak 2,4 GHz'in (çoğu bölgede) yalnızca 3 örtüşmeyen kanalı vardır, komşu ağlar ve IoT cihazları tarafından yoğun biçimde kullanılır ve daha düşük verim sağlar.

Band yönlendirme, yetenekli istemcileri 5 GHz'e (veya WiFi 6E deployment'larında 6 GHz'e) iter:
- 2,4 GHz probe yanıtlarını geciktir — yanıt bekleyen istemciler 5 GHz'i dener
- Aktif yönlendirme — controller 5 GHz'e yetenekli istemcileri tanımlar ve 2,4 GHz ilişkisini reddeder

Tüm istemciler agresif band yönlendirmeye iyi yanıt vermez. Eski veya daha az yetenekli cihazlar için yönlendirme ile bağlantı arasındaki dengeyi bulun.

---

## WiFi Güvenliği: Çoğu Ekibin Yanlış Yaptığı Katman

WiFi güvenliği yalnızca SSID'deki bir şifre değildir. Kurumsal ortamlarda kimlik doğrulama mimarisini, şifreleme standartlarını, ağ segmentasyonunu ve sahte altyapıyı izlemeyi içerir.

### Kimlik Doğrulama: PSK'dan 802.1X'e

**WPA2-PSK / WPA3-SAE (Önceden Paylaşılan Anahtar):** Tüm kullanıcılar için tek şifre. Basit, ancak kritik zayıflıkları var: bir sızdırılan şifre tüm kullanıcıları tehlikeye atar, bireysel hesap verebilirlik yoktur ve iptal her yerde şifreyi değiştirmeyi gerektirir.

**WPA2/WPA3-Enterprise (802.1X):** Her kullanıcı, bireysel kimlik bilgileriyle (kullanıcı adı/şifre, sertifika veya akıllı kart) bir RADIUS sunucusuna (Windows NPS, Cisco ISE, Aruba ClearPass) karşı kimlik doğrular. Faydaları:
- Bireysel hesap verebilirlik — tam olarak hangi kullanıcının bağlı olduğunu bilirsiniz
- Ayrıntılı iptal — diğerlerini etkilemeden tek kullanıcıyı devre dışı bırakın
- Dinamik VLAN ataması — kimlik, departman veya cihaz türüne göre kullanıcıları farklı VLAN'lara yerleştirin
- Grup üyeliğine dayalı otomatik erişim için Active Directory ile entegrasyon

Hassas veriler işleyen herhangi bir kurumsal ortam için 802.1X isteğe bağlı değildir — taban çizgisidir.

### Şifreleme: WPA3 ve Neden Önemlidir

WPA3, WPA2'nin PSK el sıkışmasının yerini alan **SAE (Simultaneous Authentication of Equals)** getirdi. Kritik iyileştirme: SAE **ileri gizlilik** sağlar — el sıkışmayı yakalamak ve daha sonra şifreyi elde etmek, daha önce yakalanan trafiğin şifresini çözmeye izin vermez.

WPA2 (PMKID saldırılarıyla), yakalanan el sıkışmalarının çevrimdışı kaba kuvvet kırılmasına olanak tanıyordu. WPA3 bu saldırı vektörünü ortadan kaldırır.

802.1X kullanan kurumsal deployment'lar için, 192 bit güvenlik modundaki WPA3-Enterprise mevcut en güçlü kablosuz şifrelemeyi sağlar.

### Sahte AP Tespiti

Sahte AP, ağınıza bağlı yetkisiz bir erişim noktasıdır — kötü niyetle yerleştirilen veya ofise ev yönlendiricisi getiren iyi niyetli bir çalışan.

Kurumsal kablosuz controller'lar RF ortamını sürekli olarak AP'ler için tarar. Kablolu ağınızın BSSID'si veya SSID'siyle eşleşen bir AP tespit edildiğinde, sahte olarak işaretlenir ve — çoğu platformda — otomatik olarak çevrelenebilir (controller, sahte AP'ye bağlanan istemcilere kimlik doğrulama iptali çerçeveleri gönderir).

→ **[WiFi Güvenliği Deep Dive: WPA3, 802.1X, Sahte AP Tespiti ve Site Survey](/tr/technology/wifi-guvenligi-wpa3-8021x-site-survey/)**

---

## Site Survey: Çoğu Projenin Atladığı Adım

Site survey, AP deployment öncesinde ve sonrasında RF ortamının sistematik olarak ölçülmesidir. Bu adımı atlamak, "WiFi deployment yaptık ama düzgün çalışmıyor" durumlarının en yaygın nedenidir.

**Tahmine dayalı survey (deployment öncesi):** Beklenen kapsama alanını modellemek için bir kat planı ve duvar malzemeleriyle RF simülasyon yazılımı (Ekahau Site Survey sektör standardıdır) kullanın. Herhangi bir şey kurmadan AP yerleşimini, kanal atamalarını ve güç seviyelerini belirleyin.

**Doğrulama surveyi (deployment sonrası):** Ekahau çalıştıran bir dizüstü bilgisayarla alanı yürüyerek gerçek sinyal gücünü, gürültü tabanını, kanal kullanımını ve roaming davranışını ölçün. Tahmine dayalı modelle karşılaştırın ve gerektiğinde AP yerleşimini veya ayarlarını düzenleyin.

Site survey'in ortaya koyduğu şeyler:
- Tahmine dayalı modelin öngörmediği kapsama boşlukları (beklenmedik girişim kaynakları, beklenenden daha fazla zayıflatan duvar malzemeleri)
- Komşu ağlardan kanal tıkanıklığı
- Kendi AP'leriniz arasındaki aynı kanal girişimi
- İstemcilerin AP'ler arasında bağlantıyı kaybettiği roaming ölü noktaları

Uygun bir site survey'in maliyeti, kurulumdan sonra önemli yeniden çalışma gerektiren kablosuz deployment maliyetiyle karşılaştırıldığında küçüktür.

→ **[WiFi Güvenliği Deep Dive, Site Survey metodolojisini içerir](/tr/technology/wifi-guvenligi-wpa3-8021x-site-survey/)**

---

## Doğru Platformu Seçme

| Senaryo | Önerilen Platform |
|---|---|
| Küçük ofis, basit yönetim | Aruba Instant On, Cisco Business, Meraki Go |
| IT personeli olan KOBİ | Cisco Meraki, Aruba Central (bulut yönetimli) |
| Kurumsal kampüs, karmaşık politika | Aruba Mobility Master, Cisco DNA Center |
| Otel / konaklama | Aruba, Cisco Meraki (PMS entegrasyonu ile) |
| Sağlık / düzenlenmiş ortam | Aruba ClearPass + Mobility Master, Cisco ISE + WLC |
| Yüksek yoğunluklu mekanlar | Cisco (Catalyst Center), Aruba (AOS 10) |
| Çok siteli, merkezi yönetim | Cisco Meraki, Aruba Central |

---

## Bu Seri

- 📡 **[802.11 Standartları Deep Dive](/tr/technology/wifi-80211-standartlari-wifi4-wifi5-wifi6/)** — WiFi 4, 5, 6, 6E ve 7: ne değişti, pratikte ne önemli
- 🏢 **[Kurumsal Controller Mimarisi](/tr/technology/kurumsal-wifi-controller-mimarisi-cisco-aruba/)** — Cisco ve Aruba mimarileri, merkezi ve bulut karşılaştırması, mobilite alanları
- 🏨 **[KOBİ, Oteller ve Muayenehane İçin WiFi Tasarımı](/tr/technology/wifi-tasarimi-kobi-otel-saglik/)** — Gerçek dünya deployment senaryolarında pratik saha notları
- 🔐 **[WiFi Güvenliği: WPA3, 802.1X, Sahte AP, Site Survey](/tr/technology/wifi-guvenligi-wpa3-8021x-site-survey/)** — Kimlik doğrulama, şifreleme, saldırı tespiti, Ekahau metodolojisi

---

## İlgili Yazılar

- 🔐 [802.1X Kimlik Tabanlı Mimari Sahada](/tr/technology/identity-based-microsegmentation-8021x/) — Kurumsal WiFi güvenliğini işlevsel kılan kimlik katmanı
- 🏗️ [IT Altyapısı Ürünler Koleksiyonu Değildir](/tr/architecture/it-infrastructure-not-a-collection-of-products/) — Kablosuz tasarımın arkasındaki sistem düşüncesi
- 🎯 [Ağ Altyapısı Ürün Seçimi: Stratejik Kriterler](/tr/architecture/network-product-selection-strategy/) — Kablosuz satıcıları nesnel olarak nasıl değerlendirirsiniz