---
title: "DDoS Koruma Stratejileri: ISP Scrubbing, On-Premise Cihazlar ve Bulut Servisleri"
description: "DDoS koruması rehberi — saldırı türleri, ISP scrubbing, on-premise cihazlar, bulut servisleri ve organizasyonunuz için doğru kombinasyon."
date: 2026-03-30
draft: false

cover:
  image: "/img/postimages/ddos-protection-strategies-cover.webp"
  alt: "DDoS Koruma Stratejileri — ISP Scrubbing, On-Premise, Bulut"
  relative: false

tags: ["DDoS", "Ağ Güvenliği", "Arbor", "Cloudflare", "AWS Shield", "ISP Scrubbing", "On-Premise", "Bulut Güvenliği"]
categories: ["Teknoloji"]
keywords:
  - DDoS koruma stratejileri
  - ISP DDoS scrubbing
  - on-premise DDoS cihazı
  - bulut DDoS koruması
  - Cloudflare DDoS
  - AWS Shield
  - Arbor DDoS
  - Radware DefensePro
  - hibrit DDoS koruması
  - DDoS azaltma karşılaştırması

showToc: true
TocOpen: false
---

# DDoS Koruma Stratejileri: ISP Scrubbing, On-Premise Cihazlar ve Bulut Servisleri

Bir DDoS (Dağıtılmış Hizmet Reddi) saldırısı sistemlerinizi ele geçirmek zorunda değildir. Sadece erişilemez hale getirmesi yeterlidir. Ve diğer güvenlik tehditlerinin aksine, hasar anlık ve tamamen görünürdür — uygulamanız çalışmayı durdurur, müşteriler size ulaşamaz ve gelir durur.

DDoS'u benzersiz biçimde zorlaştıran şey, saldırı trafiğinin paket düzeyinde meşru görünmesidir. Milyonlarca geçerli TCP SYN paketi, milyonlarca geçerli DNS sorgusu, milyonlarca geçerli HTTP isteği — hepsi mükemmel biçimlendirilmiş, hepsi tamamen kasıtlı. Ağınız bunları gerçek trafikle aynı şekilde işler, ve bu tam olarak sorunun ta kendisidir.

DDoS korumasının yasal bir gereklilik olduğu — sadece en iyi uygulama değil — bankacılık altyapısında çalışmış biri olarak, organizasyonların kendilerini gerçekte nasıl koruduğunu aktarmak istiyorum: üç ana yaklaşımın ne olduğu, her birinin ne yapıp yapamadığı ve pratikte nasıl bir araya geldikleri.

---

## Saldırı Yüzeyini Anlamak

Koruma stratejisi seçmeden önce, neye karşı korunduğunuzu net olarak belirlemek faydalıdır. DDoS saldırıları üç kategoriye ayrılır ve temelden farklı azaltma yaklaşımları gerektirirler.

### Volumetrik Saldırılar (Katman 3/4)

En görünür tür. Amaç basittir: internet bağlantınızı taşıyabileceğinden daha fazla trafikle doyurmak.

Yaygın teknikler:
- **UDP flood** — rastgele portlara büyük hacimde UDP paketi göndermek. Hedef her birine "port erişilemez" ICMP yanıtı gönderir, hem gelen hem giden bant genişliğini tüketir.
- **ICMP flood (Ping flood)** — ping istekleriyle bunaltmak.
- **Amplifikasyon saldırıları** — en tehlikeli varyant. Saldırgan, kaynak olarak IP'nizi kullanarak yanlış yapılandırılmış üçüncü taraf sunucularına (DNS çözücüler, NTP sunucuları, memcached örnekleri) küçük istekler gönderir. Bu sunucular size büyük yanıtlar gönderir. DNS amplifikasyonu 50–70× amplifikasyon sağlayabilir; memcached amplifikasyonu 51.000×'e ulaşmıştır.

**Ölçek:** Modern volumetrik saldırılar rutin olarak 1 Tbps'yi aşar. 10 Gbps'lik bir internet bağlantısı buna karşı anlamsızdır — firewall'unuza tek bir paket ulaşmadan doyuma ulaşırsınız.

**Temel içgörü:** ISP uplink'inizi aşan saldırı hacminde volumetrik saldırıları kendi tesislerinizde azaltamazsınız. Trafik bağlantınıza ulaşmadan önce yukarı akışta — ISP veya bulut seviyesinde — filtrelenmelidir.

### Protokol Saldırıları (Katman 3/4)

Bant genişliği yerine ağ cihazı kaynaklarını tüketir.

- **SYN flood** — el sıkışmayı tamamlamadan milyonlarca TCP SYN paketi göndermek. Hedef her yarı açık bağlantı için bellek ayırır, bağlantı tablosu dolana ve meşru bağlantılar reddedilene kadar.
- **Parçalanmış paket saldırıları** — yeniden birleştirme tamponlarını bunaltan hatalı biçimlendirilmiş veya üst üste binen IP parçaları göndermek.
- **Smurf saldırısı** — sahte kaynak IP'ler kullanan ICMP broadcast amplifikasyonu.

**Ölçek:** Bant genişliğiyle değil, saniyedeki paket sayısıyla (Mpps) ölçülür. Küçük paket boyutlarında 100 Mbps'lik bir SYN flood, orta düzey bir firewall'un bağlantı tablo kapasitesini aşabilir.

**Temel içgörü:** Protokol saldırıları, FPGA tabanlı paket işleme ile özel DDoS donanımı tarafından on-premise azaltılabilir — ancak yalnızca hacim uplink'inizi önceden doyurmadıysa.

### Uygulama Katmanı Saldırıları (Katman 7)

Tespit ve azaltması en zor olanlar. Trafik meşru HTTP/HTTPS'tir — kötü niyetli olan niyet.

- **HTTP flood** — kaynak yoğun uç noktalara (arama, giriş, rapor oluşturma) milyonlarca HTTP GET veya POST isteği göndermek.
- **Slowloris** — çok sayıda bağlantı açmak ve HTTP başlıklarını çok yavaş göndermek, istekleri tamamlamadan bağlantıları açık tutmak. Sunucunun bağlantı havuzunu tüketir.
- **RUDY (R-U-Dead-Yet)** — Slowloris'e benzer ama POST gövdeleri için. Veriyi bir seferde bir bayt gönderir.
- **SSL tüketimi** — TLS el sıkışmalarını başlatmak ama hiçbir zaman tamamlamamak veya el sıkışmaları tamamlayıp hemen yeniden müzakere etmek. Donanım SSL hızlandırması olmayan sunucular için CPU yoğun.

**Ölçek:** Düşük trafik hacimlerinde yıkıcı biçimde etkili olabilir — milyonlarca normal isteği işleyen bir web sunucusunu saniyede birkaç bin istek hedefleyerek çökertebilir.

**Temel içgörü:** Katman 7 saldırıları uygulama destekli azaltma gerektirir. Volumetrik bir scrubbing servisi kötü niyetli bir HTTP flood'u meşru trafikten ayırt edemez.

---

## Üç Koruma Yaklaşımı

Hiçbir tek koruma yaklaşımı tüm ölçeklerdeki tüm saldırı türlerini kapsamaz. Ciddi DDoS maruziyeti olan organizasyonlar tipik olarak bu katmanlardan ikisini veya üçünü birleştirir.

---

## 1. ISP Tabanlı Scrubbing Servisleri

### Nasıl Çalışır

ISP'niz (veya yukarı akış ağ anlaşmalarına sahip uzman bir scrubbing sağlayıcısı), bir saldırı sırasında trafiğinizi bir **scrubbing merkezine** yönlendirir. Scrubbing merkezinde saldırı trafiği filtrelenir ve yalnızca temiz trafik ağınıza iletilir:

```
Normal işlem:
  İnternet → ISP → Ağınız

Saldırı sırasında:
  İnternet → ISP → Scrubbing Merkezi → Temiz trafik → Ağınız
                          │
                   Saldırı trafiği düşürülür
```

Trafik yönlendirmesi tipik olarak iki şekilde tetiklenir:
- **İstek üzerine:** Saldırı tespit edildiğinde ISP ile iletişime geçersiniz. Manuel süreç, yanıt süresi sağlayıcıya bağlıdır.
- **Her zaman açık:** Trafik sürekli olarak scrubbing üzerinden yönlendirilir. Tespit gecikmesi yoktur, ancak gecikme ekler.

### ISP Scrubbing'in Koruduğu Şeyler

ISP scrubbing özellikle **volumetrik saldırılar** için tasarlanmıştır. Altyapınızın yukarı akışında, ağ katmanında çalışır. 10 Gbps bağlantınızı doyuracak bir saldırı, sağlayıcının 10 Tbps+ kapasitesi tarafından size ulaşmadan emilir.

### ISP Scrubbing'in Yapamadıkları

- **Katman 7 koruması:** ISP scrubbing L3/L4'te çalışır. HTTP istek içeriğini analiz edemez.
- **Yavaş ve düşük hacimli saldırılar:** Slowloris, RUDY ve SSL tüketimi volumetrik değildir.
- **Anlık yanıt:** İstek üzerine scrubbing, trafik yönlendirilirken tipik olarak 15–30 dakikalık bir aktivasyon gecikmesine sahiptir.

### ISP Scrubbing Ne Zaman Mantıklıdır

- Birincil tehdidiniz volumetrik saldırılardır (altyapıyı hedef alan en yaygın tür)
- ISP bağlantınız 10 Gbps veya daha azdır
- Donanım maliyetlerini haklı kılamazsınız ama DDoS koruması için düzenleyici gereklilikleriniz vardır
- Maliyet etkin bir temel koruma katmanı istiyorsunuz

---

## 2. On-Premise DDoS Cihazları

### Nasıl Çalışır

Özel bir donanım cihazı (veya sanal cihaz), firewall'unuzun yukarısında, ağınızda inline konumlanır:

```
İnternet → [ISP Router] → [DDoS Cihazı] → [NGFW] → İç Ağ
```

Cihaz tüm trafiği gerçek zamanlı olarak analiz eder ve saldırı paketlerini firewall'unuza veya sunucularınıza ulaşmadan düşürür. Yazılım tabanlı çözümlerin aksine, özel amaçlı DDoS cihazları paket işleme için **FPGA (Alan Programlanabilir Kapı Dizisi)** donanımı kullanır.

### Önde Gelen On-Premise Çözümler

**NETSCOUT Arbor (Peakflow / Sightline / TMS)**
Özellikle bankacılık ve telekom sektöründe baskın kurumsal çözüm. Arbor, on-premise DDoS koruması için sektör standardı olarak yaygın biçimde kabul görür. Platform şunları birleştirir:
- **Sightline:** Akış verileri (NetFlow, sFlow, IPFIX) ve BGP kullanarak trafik analizi ve saldırı tespiti
- **Threat Mitigation System (TMS):** Inline veya out-of-band kullanılan donanım tabanlı scrubbing cihazı
- Arbor'un küresel tehdit istihbaratı ağıyla (ATLAS) entegrasyon

**Radware DefensePro**
Finansal hizmetlerde güçlü. Normal trafiğin dinamik bir temelini oluşturan ve anomalileri tespit eden davranış tabanlı tespit özelliği — bilinen imzalarla eşleşmeyen sıfır-gün DDoS saldırılarına karşı etkili.

**Fortinet FortiDDoS**
Fortinet ekosistemiyle entegre. Tutarlı yönetim için FortiGate firewall'ları zaten çalıştıran organizasyonlar için uygundur.

**F5 BIG-IP AFM (Advanced Firewall Manager)**
F5 serisinde ele alındığı gibi — AFM, BIG-IP platformunun parçası olarak DDoS azaltma özellikleri sağlar. Uygulama teslimi için zaten F5 çalıştıran ve mevcut donanıma DDoS koruması eklemenin maliyet etkin olduğu ortamlara en uygunudur.

### On-Premise Cihazların Koruduğu Şeyler

- **Protokol saldırıları:** SYN flood'lar, parçalanmış paketler, hatalı biçimlendirilmiş başlıklar — firewall'a ulaşmadan donanım hızında işlenir
- **Uygulama katmanı saldırıları:** Davranışsal analizle gelişmiş cihazlar HTTP flood'larını, Slowloris'i ve SSL tüketimini tespit edip azaltabilir
- **Sıfır-gün davranışsal saldırılar:** Hız tabanlı ve davranışsal tespit, bilinen imzalar gerektirmeden saldırı kalıplarını tanımlar

### On-Premise'in Yapamadıkları

**ISP bağlantınızı aşan volumetrik saldırılar:** Veri merkezinizdeki bir on-premise cihaz, 500 Gbps'lik saldırı trafiği 10 Gbps'lik internet bağlantınızı doldurduğunda yardım edemez. Bu temel sınırlamadır.

Bu nedenle on-premise cihazlar ve ISP scrubbing **tamamlayıcıdır, rekabetçi değil**.

---

## 3. Bulut DDoS Koruma Servisleri

### Nasıl Çalışır

Bulut DDoS koruması tüm trafiğinizi sağlayıcının küresel dağıtık ağı üzerinden yönlendirir. Temiz trafik kaynak sunucularınıza teslim edilir; saldırı trafiği kenarda düşürülür:

```
Bulut koruması olmadan:
  Kullanıcı → İnternet → Sunucunuz

Bulut korumasıyla:
  Kullanıcı → [Cloudflare / Akamai / AWS kenar] → Sunucunuz
                          │
                   Saldırı trafiği ağ kenarında düşürülür
```

### Önde Gelen Bulut Çözümleri

**Cloudflare**
En yaygın bilinen bulut DDoS sağlayıcısı. Cloudflare, dünyanın en büyük anycast ağlarından birini işletiyor — küresel 300+ PoP, 230 Tbps'yi aşan toplam kapasiteyle. Temel özellikler:
- Manuel müdahale olmadan otomatik DDoS azaltma
- Tek bir platformda Katman 3, 4 ve 7 koruması
- WAF entegrasyonu — uygulama güvenliği ve DDoS azaltma aynı sağlayıcıdan
- Altyapı düzeyi koruma için Magic Transit (BGP tabanlı, yalnızca HTTP değil)
- Ölçüsüz DDoS azaltma — saldırılar sırasında GB başına ücret yok

**AWS Shield**
- **Shield Standard:** Tüm AWS kaynakları için otomatik olarak dahildir. Yaygın L3/L4 saldırılara karşı korur.
- **Shield Advanced:** L7 koruması, 7/24 DDoS Yanıt Ekibi erişimi ve AWS WAF ile entegrasyon içeren ücretli katman.
- Önemli AWS altyapısına sahip organizasyonlar için en uygunudur.

**Akamai Prolexic**
Kurumsal odaklı bulut scrubbing platformu. 20+ küresel dağıtık scrubbing merkezi işletiyor. Finansal hizmetler ve medyada güçlü referanslar.

**Azure DDoS Protection**
Azure barındırmalı kaynaklar için Microsoft'un teklifi. Azure'da önemli iş yükleri çalıştıran organizasyonlar için en uygunudur.

### Bulut Korumanın Dezavantajları

- **Gecikme:** Tüm trafik sağlayıcının ağından geçer. Çoğu web uygulaması için kenar PoP'larının eklediği gecikme ihmal edilebilir veya negatiftir. Gecikmeye duyarlı uygulamalar için dikkatli değerlendirin.
- **Gizlilik/uyumluluk:** SSL ile şifresi çözülmüş içerik dahil tüm trafik sağlayıcının altyapısından geçer. Düzenlenmiş sektörlerde dikkatli inceleme gerektirir.
- **DNS bağımlılığı:** DNS tabanlı bulut koruması, saldırganlar kaynak IP'nizi keşfederse atlatılabilir. Kaynak IP'leri yalnızca bulut sağlayıcısının IP aralıklarına izin verecek şekilde firewall düzeyinde koruyun.

---

## Üç Yaklaşımın Karşılaştırması

| | ISP Scrubbing | On-Premise Cihaz | Bulut Servisi |
|---|---|---|---|
| Volumetrik koruma | ✅ | ❌ (bağlantıyla sınırlı) | ✅✅ |
| Protokol saldırısı koruması | ✅ | ✅✅ | ✅ |
| Uygulama katmanı (L7) | ❌ | ✅ (gelişmiş modeller) | ✅✅ |
| Aktivasyon süresi | Dakikalar (istek üzerine) | Anında | Anında |
| Trafik görünürlüğü | Sınırlı | Tam | Sağlayıcıya bağlı |
| Uyumluluk / veri yerelliği | ✅ | ✅✅ | İnceleme gerektirir |
| CapEx | Düşük | Yüksek | Yok |
| OpEx | Orta | Orta | Orta–Yüksek |
| Ölçeklenebilirlik | ISP kapasitesi | Sabit donanım | Neredeyse sınırsız |

---

## Hibrit Model: Ciddi Organizasyonlar Üçünü Nasıl Birleştirir

Yüksek riskli ortamlarda — bankacılık, ödeme işlemcileri, devlet altyapısı, büyük e-ticaret — tek bir koruma katmanı hiçbir zaman yeterli değildir. Standart mimari üçünü birleştirir:

```
Saldırı trafiği
      │
      ▼
[Bulut / ISP Scrubbing]    ← Volumetrik taşmaları size ulaşmadan emer
      │
  Temizlenmiş trafik
      │
      ▼
[On-Premise Cihaz]         ← Protokol saldırılarını ve L7 anomalileri yakalar
      │
      ▼
[NGFW + WAF]               ← Uygulama güvenliği ve politika uygulaması
      │
      ▼
[Uygulama Sunucuları]
```

Her katman diğerlerinin yapamadıklarını halleder. Kombinasyon, DDoS saldırı türlerinin tüm yelpazesine karşı dayanıklı derinlemesine savunma oluşturur.

### Gerçek Dünya Örneği: Bankacılık Sektörü

Çalıştığım bankacılık ortamında DDoS koruma yığını şöyleydi:

- **Arbor TMS** on-premise — protokol saldırıları için inline scrubbing, anomali tespiti için gerçek zamanlı akış analizi, otomatik trafik yönlendirmesi için BGP ile entegrasyon
- **ISP scrubbing sözleşmesi** — Arbor, uplink'i doyuracak volumetrik saldırı imzaları tespit ettiğinde etkinleştirildi
- **Cloudflare Magic Transit** — WAF entegrasyonuyla always-on bulut düzeyi koruma sağlayan halka açık web uygulamaları için
- **F5 AFM** — uygulama teslim katmanında ek L4 koruması

Bu gereksiz yere yedeklilik değildi — her katman diğerlerinin yapamadıklarını halletti.

---

## DDoS Yanıt Planlaması: Teknik Olmayan Kısım

Teknoloji, DDoS hazırlığının yalnızca bir parçasıdır. Diğer kısım organizasyoneldir:

**Runbook'lar:** Bir saldırı başladığında tam olarak ne yapılacağını belgeleyin. Kim bildirilecek? Kim ISP scrubbing'i etkinleştirecek? Yükseltme yolu ne? Saldırı altında bunu çözmek için doğru zaman değildir.

**İletişim listeleri:** ISP scrubbing etkinleştirme, bulut sağlayıcı desteği, yukarı akış router erişimi, nöbetçi ağ mühendisleri. Hepsi güncel, hepsi test edilmiş.

**Eşikler ve otomasyon:** Otomatik azaltmanın ne zaman devreye gireceğini ve insan incelemesinin ne zaman gerekli olduğunu tanımlayın. Tam manuel yanıtlar modern saldırı oranları için çok yavaştır.

**Düzenli test:** Hiç test edilmemiş bir DDoS koruma yığını, gerçekte güvenmediğiniz bir DDoS koruma yığınıdır. ISP'niz ve bulut sağlayıcınızla periyodik testler planlayın.

**Olay sonrası inceleme:** Her önemli saldırının ardından, neyin işe yaradığını, neyin yaramadığını ve saldırı trafiğinin neye benzediğini gözden geçirin. DDoS taktikleri evrilir — koruma stratejiniz de öyle olmalıdır.

---

## Temel Çıkarımlar

- DDoS saldırıları üç temel olarak farklı türde gelir — volumetrik, protokol ve uygulama katmanı — ve her biri farklı azaltma gerektirir.
- **Hiçbir tek koruma katmanı tüm saldırı türlerini kapsamaz.** Volumetrik saldırılar yukarı akış scrubbing kapasitesi gerektirir; protokol saldırıları donanım hızında paket işleme gerektirir; L7 saldırıları uygulama destekli analiz gerektirir.
- **ISP scrubbing**, çok büyük volumetrik saldırılar için tek seçenektir — saldırı bağlantınıza ulaşmadan emilmelidir.
- **On-premise cihazlar** (Arbor, Radware, F5 AFM) ayrıntılı görünürlük, uyumluluk dostu şirket içi işleme ve etkili protokol/L7 koruması sağlar — ancak ISP bağlantı kapasitesini aşan saldırıları kaldıramaz.
- **Bulut servisleri** (Cloudflare, AWS Shield, Akamai) büyük ölçek, küresel dağılım ve donanım yatırımı olmadan always-on koruma sunar — ancak trafik yönlendirmesini üçüncü taraf altyapıdan geçirir.
- Yüksek riskli ortamlarda, üç katman birlikte çalışır. Bu aşırı mühendislik değildir — ciddiye alınan organizasyonların pratikte kullandığı mimaridir.

---

## İlgili Yazılar

- 🛡️ [F5 BIG-IP Platform Genel Bakış](/tr/technology/f5-bigip-application-delivery-platform-overview/) — DDoS savunmanın derinliğinin bir parçası olarak F5 AFM
- 🔐 [Zero Trust Zihniyeti: Güvenliği Bir Mimari Olarak Mühendislemek](/tr/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — Zero Trust çerçevesinde DDoS koruması
- 🛡️ [Network Packet Broker (NPB) Masterclass](/tr/posts/network-packet-broker-masterclass/) — DDoS adli analizi için gerekli trafik görünürlüğü
- 📊 [İzleme Doğru Yapıldığında](/tr/architecture/monitoring-not-just-seeing/) — Proaktif izleme yoluyla DDoS'u erken tespit etmek