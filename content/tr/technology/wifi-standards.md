---
title: "802.11 Standartları Deep Dive: WiFi 4, 5, 6, 6E ve Gerçekte Ne Değişti"
description: "802.11 kablosuz standartları — n, ac, ax ve be'nin gerçek deployment'lardaki performansı, OFDMA, MU-MIMO, BSS Coloring ve doğru standart seçimi."
date: 2026-05-01
draft: false

cover:
  image: "/img/postimages/wifi-80211-standards-cover.webp"
  alt: "802.11 WiFi Standartları — WiFi 4 5 6 6E Karşılaştırması"
  relative: false

tags: ["WiFi", "802.11ax", "WiFi 6", "802.11ac", "WiFi 5", "OFDMA", "MU-MIMO", "Kablosuz Standartlar"]
categories: ["Teknoloji"]
keywords:
  - 802.11ax WiFi 6 açıklaması
  - WiFi 6 vs WiFi 5 kurumsal
  - OFDMA vs OFDM kablosuz
  - MU-MIMO 802.11ac
  - BSS Boyama 802.11ax
  - WiFi 6E 6GHz bandı
  - WiFi 7 802.11be
  - kablosuz kanal genişliği 80MHz 160MHz
  - TWT hedef uyanma zamanı IoT
  - 802.11 standart karşılaştırması

showToc: true
TocOpen: true
---

# 802.11 Standartları Deep Dive: WiFi 4, 5, 6, 6E ve Gerçekte Ne Değişti

Bu yazı Kurumsal WiFi serisinin bir parçasıdır.

> **Kurumsal kablosuz ağa yeni misiniz?** Genel bakışla başlayın: [Kurumsal WiFi Mimarisi: Standartlardan Deployment'a](/tr/technology/kurumsal-wifi-mimarisi-tam-rehber/)

---

## Pazarlama Sayılarının Sorunu

Her WiFi nesli etkileyici teorik verim rakamlarıyla gelir. 802.11ac 3,5 Gbps vaat etti. 802.11ax 9,6 Gbps vaat ediyor. Pratikte, gerçek bir ortamdaki tek bir istemci WiFi 5'te nadiren 400–600 Mbps'i ve WiFi 6'da 800 Mbps–1,2 Gbps'i aşar.

Bu bir aldatmaca değildir — ideal koşullar altında teorik hızlar matematiksel olarak doğrudur. Teori ile pratik arasındaki boşluk şundan kaynaklanır:

- Teorik hızlar, aynı anda maksimum kanal genişliği (160 MHz), maksimum uzamsal akış (8) ve maksimum modülasyon (1024-QAM) varsayar
- Gerçek istemcilerin 8 değil, 1–2 uzamsal akışı vardır
- Kanal genişliği, düzenleyici kurallar ve girişimden kaçınma ile sınırlıdır
- Sinyal zayıflaması, artan mesafeyle birlikte modülasyonu daha düşük hızlara düşürür

Kurumsal kablosuz seçiminde gerçekte önemli olan, zirve verim değildir — standardın yük altında, yoğun istemci ortamlarında ve tıkalı RF koşullarında nasıl davrandığıdır. Nesiller gerçekte burada farklılaşır.

---

## 802.11n (WiFi 4): Temel

2009'da yayınlandı. Temel olmaya devam eden iki teknolojiyi tanıttı:

**MIMO (Multiple Input, Multiple Output):** Hem AP'de hem de istemcide birden fazla anten, aynı kanalda eş zamanlı olarak iletim ve alım yapar. 2×2 MIMO AP, 2 verici ve 2 alıcı anten kullanarak tek antenli (SISO) tasarımlara kıyasla verimi etkili biçimde ikiye katlar. Kurumsal AP'ler yaygın olarak 3×3 veya 4×4 MIMO kullanır.

**5 GHz desteği:** 802.11n hem 2,4 GHz hem de 5 GHz üzerinde çalışan ilk standarttır. 5 GHz bandı, daha fazla örtüşmeyen kanala sahiptir (çoğu bölgede 2,4 GHz'deki 3'e karşılık 25) ve komşu ağlardan ve mikrodalga fırınlardan daha az girişim yaşar.

**Kanal bağlama:** 40 MHz kanallar (iki 20 MHz kanalın bağlanması), kanal kullanılabilirliği pahasına teorik verimi ikiye katladı.

**2026'daki pratik gerçeklik:** 802.11n donanımı kullanım ömrünü tamamlamış. Herhangi bir yeni deployment, en azından 802.11ac kullanmalıdır. 802.11n'yi anlamak, birçok kurumsal ortamda hâlâ mevcut olan eski cihazları yönetmek için önemlidir.

---

## 802.11ac (WiFi 5): 5 GHz'e Geçiş

2013'te (Wave 1), 2016'da (Wave 2) yayınlandı. 802.11n üzerinde önemli iyileştirmeler:

**Yalnızca 5 GHz:** 802.11ac yalnızca 5 GHz üzerinde çalışır. Bu, 2,4 GHz bandını eski/IoT kullanımına zorlayarak yüksek verimli istemcileri daha az tıkalı 5 GHz spektrumuna taşıdı.

**Daha geniş kanallar:** 80 MHz kanallar (Wave 1) ve 160 MHz kanallar (Wave 2). 80 MHz kanal, 20 MHz kanalın yaklaşık 4× veri hızını sağlar — ancak 4× spektrum tüketir. Çok sayıda AP'li yoğun deployment'larda, 80 MHz kanallar ciddi aynı kanal girişimine neden olur. Birçok kurumsal deployment, kanal kullanılabilirliğini korumak için 40 MHz kullanır.

**256-QAM:** 802.11n'nin 64-QAM'inden daha yüksek modülasyon yoğunluğu. Aynı sinyal gücünde sembol başına daha fazla bit — ancak daha iyi sinyal kalitesi gerektirir.

**MU-MIMO (Wave 2):** 802.11ac Wave 2, **çok kullanıcılı MIMO**'yu aşağı yön için tanıttı. Bir seferde tek bir istemciye iletmek (SU-MIMO) yerine, AP farklı istemcilere yönlendirilmiş farklı destekler kullanarak aynı anda 4 istemciye iletim yapabilir.

**MU-MIMO sınırlılığı:** Wave 2 MU-MIMO yalnızca aşağı yönde (AP'den istemciye) çalışır. Yukarı yön (istemciden AP'ye) hâlâ tek kullanıcılıdır. İstemcilerin MU-MIMO'nun etkili çalışması için uzamsal olarak farklı konumlarda olması gerekir — pratikte fayda genellikle teorikten daha az dramatiktir.

**Pratik etki:** WiFi 5, en yaygın deploy edilen kurumsal standart olmaya devam ediyor. 2016 ile 2021 arasında deploy edilen kurumsal AP'lerin çoğu 802.11ac Wave 2'dir. Tipik ofis iş yükleri için performans mükemmeldir.

---

## 802.11ax (WiFi 6): Yoğunluk İçin Tasarlandı

2019'da yayınlandı. WiFi 6, öncelikle daha hızlı tek istemci verimi değil — **yüksek yoğunluklu ortamlarda verimlilik** hedefledi. Bu temel ayrımdır.

### OFDMA: En Önemli WiFi 6 Özelliği

802.11n ve 802.11ac'da kanal, bir seferde bir istemciye tahsis edilir. Bir istemcinin yalnızca küçük bir onaylama göndermesi gerekmesi durumunda bile, diğer istemciler beklerken kanalı tutar:

```
WiFi 5 (OFDM — zaman bölmesi):
  Zaman: |─ İstemci A ─|─ İstemci B ─|─ İstemci C ─|─ İstemci A ─|
  Kanal: Bir seferde bir istemciye %100 tahsis edilmiş
```

WiFi 6, LTE/5G hücresel ağdan ödünç alınan **OFDMA**'yı (Orthogonal Frequency Division Multiple Access) tanıttı. Kanal, **Kaynak Birimleri (RU)** adı verilen alt kanallara bölünür ve birden fazla istemci farklı RU'larda eş zamanlı olarak hizmet alabilir:

```
WiFi 6 (OFDMA — frekans + zaman bölmesi):
  Zaman: |─────────── Tek TXOP ────────────|
         | İstemci A | İstemci B | İstemci C |
         | (küçük)   | (küçük)   | (büyük veri) |
  Kanal: birden fazla istemci arasında eş zamanlı olarak alt bölünmüş
```

**Neden pratikte önemlidir:**
- IoT cihazları, telefonlar ve tabletler sık sık küçük paketler gönderir (onaylamalar, yaşatma mesajları, sensör verileri). WiFi 5 altında, bu küçük iletimlerin her biri tam kanalı tutar.
- OFDMA, AP'nin bu küçük iletimleri bir araya getirerek, tek bir WiFi 5 iletiminin alacağı sürede birden fazla istemciye hizmet vermesine olanak tanır.
- Yoğun ortamlarda (konferans odaları, sınıflar, açık ofisler), bu, kanal tıkanmasını önemli ölçüde azaltır ve tüm istemciler için genel verimi iyileştirir.

OFDMA, WiFi 5'in yalnızca aşağı yön MU-MIMO'sunun aksine, WiFi 6'da hem aşağı yöne hem de yukarı yöne uygulanır.

### BSS Boyama: Aynı Kanal Girişimini Azaltma

Yoğun AP deployment'larında, komşu AP'ler çoğunlukla kanalları paylaşır. 802.11n/ac altında, bir istemci cihazı kanalında etkinlik algıladığında beklemek zorundadır — o etkinlik kesinlikle girişim yapamayacak bitişik binalardaki bir AP'den gelse bile.

WiFi 6 BSS Boyama, her Temel Servis Setine bir "renk" (sayısal etiket) atar. Cihazlar, kendi BSS'lerinden gelen iletimler ile aynı kanalı paylaşan diğer BSS'lerden gelen iletimler arasında ayrım yapabilir:

```
BSS Boyama olmadan:
  İstemci AP-1'i duyar (kendi ağı) → bekler
  İstemci AP-2'yi duyar (komşu)    → da bekler (gereksiz)

BSS Boyama ile:
  İstemci AP-1'i duyar (aynı renk)     → bekler (ilgili)
  İstemci AP-2'yi duyar (farklı renk, düşük RSSI) → iletim yapar (yeniden kullanım)
```

Pratikte, BSS Boyama yoğun deployment'larda uzamsal yeniden kullanımı iyileştirir — daha fazla AP, aşırı girişime neden olmadan örtüşen kanallarda çalışabilir.

### Target Wake Time (TWT): IoT Pil Ömrü

WiFi 6, AP'lerin IoT ve pil güçlü cihazlar için belirli uyanma zamanları planlamasına olanak tanıyan TWT'yi tanıttı. Cihazlar, veri bekleyerek radyolarını sürekli aktif tutmak yerine, yalnızca planlanan aralıklarda uyuyup uyanır.

**Kurumsal ilgi:** Binalar, WiFi bağlantılı sensörleri, kameraları, erişim kontrol okuyucularını ve varlık takip etiketlerini giderek artan oranda bünyesinde barındırıyor. TWT, bu cihazların işlevselliğini etkilemeden pil ömrünü dramatik biçimde uzatır.

### 1024-QAM ve Daha Yüksek Verim

WiFi 6, 1024-QAM (WiFi 5'in 256-QAM'ına karşılık) destekler — sembol başına 8 bit yerine 10 bit kodlar. Yakın mesafede mükemmel sinyal kalitesiyle yaklaşık %25 verim iyileştirmesi. Çoğu deployment için OFDMA'dan daha az önemli.

---

## 802.11ax (WiFi 6E): 6 GHz Bandı

WiFi 6E, **6 GHz bandına** (çoğu bölgede 5,925–7,125 GHz) genişletilmiş 802.11ax'tır. 6 GHz bandı şunları sağlar:

- **1.200 MHz yeni spektrum** — 5 GHz'de mevcut 500 MHz'e kıyasla
- **59'a kadar örtüşmeyen 20 MHz kanalı** — 5 GHz'de 25'e karşılık (bölgeye bağlı)
- **Eski cihaz yok:** 6 GHz bandı yalnızca WiFi 6E/7. 802.11n veya 802.11ac cihazı orada yok. Eski protokollerden girişim yok.
- **Tıkanma olmadan geniş kanallar:** 160 MHz kanallar, 5 GHz'de neden oldukları kanal tükenmesi olmadan 6 GHz'de pratiktir.

**Sınırlılık:** 6 GHz, daha yüksek frekans zayıflaması nedeniyle 5 GHz'den daha kısa menzile sahiptir. AP'lerin istemcilere yakın olduğu yüksek yoğunluklu iç mekân ortamları için mükemmeldir. Açık hava veya uzun menzilli deployment'lar için daha az kullanışlıdır.

**İstemci benimsenmesi:** WiFi 6E yetenekli istemciler (akıllı telefonlar, dizüstü bilgisayarlar) 2026 itibarıyla giderek daha yaygın hale geliyor. 6E destekli kurumsal AP'ler tipik olarak üç bantlı çalışır: 2,4 GHz (eski), 5 GHz (ana akım) ve 6 GHz (yüksek verim, düşük tıkanıklık).

---

## 802.11be (WiFi 7): Ortaya Çıkıyor

802.11be / WiFi 7, 2024'te tamamlandı ve 2026 itibarıyla erken kurumsal deployment aşamasında. Temel yenilikler:

**Çok Bağlantılı Çalışma (MLO):** Tek bir istemci bağlantısı aynı anda birden fazla bant ve kanalı kullanabilir — örneğin 5 GHz ve 6 GHz üzerinde eş zamanlı iletim. Bu, verim toplamayı iyileştirir ve bağlantı kesilmesi olmadan bantlar arasında kesintisiz roaming sağlar.

**320 MHz kanallar:** 6 GHz'de mevcut. WiFi 6E'nin 160 MHz maksimumunun kanal genişliğini ikiye katlar.

**4096-QAM:** Mükemmel sinyal koşulları gerektiren daha yüksek modülasyon. Yakın mesafede 1024-QAM üzerinde yaklaşık %20 verim iyileştirmesi.

**Kurumsal hazırlık:** WiFi 7 AP'ler Cisco, Aruba ve diğerlerinden temin edilebilir. İstemci desteği büyüyor ancak henüz evrensel değil. Yeni deployment'lar için WiFi 7 AP'ler, WiFi 5 ve WiFi 6 istemcilerle uyumlu kalırken altyapıyı geleceğe hazırlar.

---

## Kanal Planlaması: Teori Gerçeklikle Buluşuyor

Standartları anlamak yalnızca yarı resimdir. Kanalları nasıl yapılandırdığınız, WiFi 6 deployment'ınızın WiFi 5 deployment'ınızı geride bırakıp bırakmayacağını belirler.

### 2,4 GHz: Yalnızca 3 Kullanılabilir Kanal

Çoğu bölgede 2,4 GHz'in 14 kanalı tanımlı ancak yalnızca **3 örtüşmeyen** kanalı var (kanal 1, 6, 11). Kanal 2, 3, 4, 5 üzerindeki herhangi bir AP, kanal 1 ve 6 ile kısmen örtüşür — girişime neden olur.

Yoğun deployment'larda 2,4 GHz bandı, yüksek verimli istemciler için esasen kullanılamaz. Eski cihazlar ve IoT için ayırın ve yetenekli istemcileri 5 GHz veya 6 GHz'e yönlendirin.

### 5 GHz: Kanal Genişliği Takasları

5 GHz, 25 örtüşmeyen 20 MHz kanala sahiptir (bölgeye bağlı). Kanal genişlikleri:

```
20 MHz kanallar:   25 örtüşmeyen kanal mevcut
40 MHz kanallar:   12 örtüşmeyen kanal
80 MHz kanallar:    6 örtüşmeyen kanal
160 MHz kanallar:   3 örtüşmeyen kanal
```

Bir kampüsü kapsayan 20 AP'li bir deployment'da, 80 MHz kanallar kullanmak yalnızca 6 benzersiz kanalın mevcut olduğu anlamına gelir — her AP, komşusunun da kullandığı bir kanaldadır. Aynı kanal girişimi performansı düşürür.

**Kurumsal öneri:** Yoğun deployment'larda, kanal kullanılabilirliğini korumak için 5 GHz'de 40 MHz kanallar kullanın. 80 MHz+'yı düşük yoğunluklu alanlar veya spektrumun bol olduğu 6 GHz için ayırın.

### Otomatik Kanal Ataması (ACA)

Kurumsal controller'lar (Cisco RRM, Aruba ARM), RF ortamı ölçümlerine dayalı olarak kanalları otomatik olarak atar ve iletim gücünü ayarlar. Bu, genellikle başlangıç deployment'ı için güvenilirdir, ancak deployment sonrası survey ile doğrulanmalıdır — otomatik algoritmalar bazen karmaşık RF ortamlarında suboptimal seçimler yapar.

---

## Deployment'ınız İçin Doğru Standardı Seçme

| Ortam | Öneri | Neden |
|---|---|---|
| Yeni kurumsal kampüs | Minimum WiFi 6, WiFi 6E tercih edilir | OFDMA yoğunluk faydası, geleceğe hazırlık |
| Yüksek yoğunluk (konferans, sınıf) | WiFi 6 veya 6E | OFDMA yoğunluk için gerekli |
| IoT ağırlıklı ortam | WiFi 6 | Pil güçlü cihazlar için TWT |
| KOBİ / küçük ofis | WiFi 6 AP | Uygun maliyetli, tüm istemcileri destekler |
| Açık hava / uzun menzil | WiFi 6 (5 GHz) | 6 GHz'den daha iyi menzil |
| Eski cihaz ağırlıklı | WiFi 6 AP (geriye dönük uyumlu) | Tüm 802.11 standartları geriye dönük uyumlu |
| Yeni yapı, geleceğe hazırlık | WiFi 7 | MLO, 6 GHz, 320 MHz kanallar |

**Önemli not:** WiFi 6 AP'ler tüm önceki istemcileri destekler — 802.11n, 802.11ac, 802.11ax istemcilerin tamamı aynı AP'ye bağlanır. AP, her istemciyle karşılıklı desteklenen en iyi yetenekleri müzakere eder.

---

## Temel Çıkarımlar

- Pazarlama verim rakamları pratikte elde edilemez — standartları zirve hızlarına değil, yoğunluk ve verimlilik iyileştirmelerine göre değerlendirin.
- **OFDMA**, kurumsal deployment'lar için WiFi 6'nın en etkili yeniliğidir — kanalın yüksek yoğunluklu ortamlarda nasıl paylaşıldığını dönüştürür.
- **BSS Boyama**, komşu AP'ler arasındaki gereksiz kanal çakışmasını azaltır.
- **WiFi 6E'nin 6 GHz bandı**, tıkanmamış spektrum ve pratik geniş kanallar sağlar — yoğun iç mekân ortamları için en önemli deployment iyileştirmesi.
- **Kanal genişliği planlaması**, standart kadar önemlidir — 5 GHz'deki 160 MHz kanallar, yoğun deployment'larda genellikle yardımdan çok zarar verir.
- WiFi 7 / 802.11be MLO'yu tanıtıyor ve erken deployment aşamasında — yeni altyapı yatırımları için değerlendirmeye değer.

---

## Bu Seri

- 📖 [Kurumsal WiFi Mimarisi Genel Bakış](/tr/technology/kurumsal-wifi-mimarisi-tam-rehber/) ← Buradan başlayın
- 🏢 [Kurumsal Controller Mimarisi: Cisco ve Aruba](/tr/technology/kurumsal-wifi-controller-mimarisi-cisco-aruba/)
- 🏨 [KOBİ, Oteller ve Muayenehane İçin WiFi Tasarımı](/tr/technology/wifi-tasarimi-kobi-otel-saglik/)
- 🔐 [WiFi Güvenliği: WPA3, 802.1X, Sahte AP, Site Survey](/tr/technology/wifi-guvenligi-wpa3-8021x-site-survey/)

## İlgili Yazılar

- 🔐 [802.1X Kimlik Tabanlı Mimari Sahada](/tr/technology/identity-based-microsegmentation-8021x/) — Kablosuz güvenlik için kimlik katmanı
- 🏗️ [IT Altyapısı Ürünler Koleksiyonu Değildir](/tr/architecture/it-infrastructure-not-a-collection-of-products/) — Kablosuz tasarım için sistem düşüncesi