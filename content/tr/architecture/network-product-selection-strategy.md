---
title: "Ağ Altyapısında Ürün Seçimi: Stratejik Kriterler ve Saha Deneyimleri"
description: "Kurumsal ağlarda ürün seçimi bir kontrol listesinden fazlasıdır. Firewall, switch ve AP değerlendirmesi için saha testi yapılmış çerçeve."
date: 2026-01-02
draft: false
author: "Barash Helvadzhaoglu"
language: "tr"

cover:
  image: "/img/postimages/network-product-selection-strategy.webp"
  alt: "Ağ Altyapısında Ürün Seçimi: Stratejik Kriterler ve Saha Deneyimleri"
  relative: false

categories:
  - Network
  - IT Infrastructure
  - Network Architecture

tags:
  - ürün seçimi
  - core network
  - firewall
  - switching
  - access point
  - kurumsal ağ
  - network stratejisi
  - üretici değerlendirmesi
  - kapasite planlaması
  - saha deneyimi

keywords:
  - ağ ürün seçim kriterleri
  - kurumsal ağ stratejisi
  - firewall üretici değerlendirmesi
  - switch kapasite planlaması
  - sistem odası tasarımı
  - IT operasyonel deneyim
  - ağ üretici karşılaştırması
  - Gartner ağ değerlendirmesi
  - firewall throughput gerçeği
  - ağ lifecycle yönetimi
  - PoE switch planlama
  - wireless controller mimarisi

toc: true
tocopen: true
---

# Ağ Altyapısında Ürün Seçimi: Stratejik Kriterler ve Saha Deneyimleri
## Switch, Firewall ve AP'yi veri sayfasının ötesinde nasıl değerlendirirsiniz

Kurumsal ağ projelerinin çoğu aynı noktada başlıyor: ürün seçimi. Ve çoğu zaman aynı noktada kırılıyor: ürünlerin birlikte çalışmaması. Çünkü "core network" dediğimiz şey, üç kutunun yan yana durması değil; bu üç kutunun birlikte kimlik taşıması, birlikte segment üretmesi, birlikte politika uygulatması ve en önemlisi birlikte operasyon kaldırmasıdır.

Benim yıllardır gördüğüm şu: bir şirketin ağı kötü olduğu için değil, ağın karar mekanizması parçalı olduğu için problem yaşanıyor. En pahalı cihazlar, en iyi lisanslar, en yüksek throughput… Hepsi var; ama olay anında hangi cihaz hangi bağlamla karar veriyor, trafik nerede ayrışıyor, nerede kontrol ediliyor — bu soruların net cevabı yok. Sonuç: "network var" ama "network davranışı" yok.

{{< figure src="/img/postimages/network-product-selection-strategy.webp" title="Stratejik Ürün Seçim Çerçevesi" >}}

Bu yazıda, core network ürünlerini üç bacakta değerlendirmek için sahada test edilmiş bir çerçeveyi paylaşacağım: Firewall, Switching ve Access (Wi-Fi). Ama başlamadan önce: "teknik özellik" kadar belirleyici olan iki faktör var ve çoğu ekip bunları geç fark ediyor — **raporlar/validasyon** ve **support/lifecycle**.

> Bu seçim sürecinin arkasındaki mimari felsefeyi anlamak için: [IT Altyapısı Bir Ürün Koleksiyonu Değildir](/tr/architecture/it-infrastructure-not-a-collection-of-products/)

## Adım 1: Raporları, Testleri ve Pazarlama Gürültüsünü Filtrelemek

Ürün seçerken bakılacak ilk referanslardan biri Gartner raporlarıdır. Gartner gibi raporlar bir ürünün pazar konumu hakkında fikir verir: kim lider, kim vizyoner, kim niş oynuyor. Bu özellikle karar vericileri ikna etmekte işe yarar.

Ama kritik bir tuzak var: **Gartner sana senin senaryonda hangisinin doğru olduğunu söylemez.** Gartner bir pazar haritasıdır; senin işin mimari harita çizmek. Gartner'ı ilk filtre olarak kullanmak daha doğru — seçenekleri daraltır ama final kararı vermez.

{{< figure src="/img/postimages/filtering-reports-tests-and-marketing-noise.webp" title="Raporları ve Pazarlama Gürültüsünü Filtrelemek" >}}

Gartner'a ek olarak, bağımsız laboratuvarların performans ve güvenlik testleri, karşılaştırmalı raporlar ve real-world benchmark'lar işin içine girmeli. Veri sayfasındaki throughput ile gerçek hayatta IPS açıkken, SSL decrypt varken, app-control çalışırken alınan throughput aynı şey değildir. Raporlar burada ikinci filtre olur: "Bu kutu bu yükte ne yapıyor?" sorusuna pazarlama dışı bir cevap ararsın.

## Adım 2: Support ve Lifecycle — Görünmez Kolon

Bir ürünün teknik yetenekleri hikayenin sadece yarısıdır. Destek modeli ve yaşam döngüsü de aynı derecede kritiktir. Network tasarımı yalnızca kurulum günüyle bitmez. Asıl soru şudur: **3 yıl sonra ne olacak?**

- Bu ürünün EoL / EoS tarihleri nedir?
- Patch, bugfix, security update hızı nasıldır?
- TAC/Support gerçekten erişilebilir mi?
- RMA süreçleri ve yedek parça gerçekliği nedir?
- Lisans modeli 1 yıl sonra sürpriz çıkarır mı?
- Üretici roadmap'i senin gittiğin yöne mi gidiyor?

Sahada en sık gördüğüm problem: ekip teknik olarak doğruya yakın bir ürün seçiyor ama support/lifecycle önceliklendirilmediği için 12 ay sonra operasyon kâbusa dönüyor. Suç cihaza kalıyor — oysa sorun hiçbir zaman cihazın kendisi değildi.

## Adım 3: Firewall Katmanının Değerlendirilmesi

Firewall, ağın "kenarındaki güvenlik cihazı" olmayı çoktan geçti. Doğru konumlandırılırsa mimarinin politika beynidir. Yanlış konumlandırılırsa her şeyin üstüne yıkıldığı darboğaz olur.

**UTM vs NGFW — gerekli bir ayrım:**

UTM yaklaşımı "tek kutuda her şey" felsefesini takip eder: firewall + IPS + web filter + AV + gateway özellikleri. Daha küçük yapılarda yönetim kolaylığı ve paket lisanslama yüzünden tercih edilir.

NGFW ise uygulama farkındalığı, kullanıcı/kimlik bağlamı ve daha derin politika kontrolü etrafında konumlanır. Bugünün kurumsal ihtiyacında yalnızca port/protokol üzerinden güvenlik yürütmek çoğu zaman yetmez.

{{< figure src="/img/postimages/firewall-selection.webp" title="Firewall Seçimi: UTM vs NGFW vs Çoklu Rol" >}}

**Aynı organizasyonda iki veya üç firewall neden normaldir:**
- **Perimeter/Internet Edge Firewall:** İnternet çıkışı, VPN, NAT, inbound/outbound policy
- **Internal Segmentation Firewall (ISFW):** East-west kontrol, iç segmentasyon, kritik zon izolasyonu
- **Data Center / High-performance FW:** DC trafiği, yüksek session, yüksek PPS, düşük latency
- Bazı yapılarda: WAF veya Cloud FW

Bu "iki firewall almak" demek değildir — "iki farklı işi doğru araca vermek" demektir.

> Firewall mimarisinin daha geniş network tasarımı içindeki yerine bakış için: [Switch, Firewall, AP — Doğru Ürünleri Seçmek Neden Yeterli Değildir](/tr/architecture/core-network-is-not-a-product-list/)

## Adım 4: Firewall Kapasite Planlaması — Throughput Yalan Söyleyebilir

Firewall seçiminde en tehlikeli hata yalnızca Gbps throughput rakamına odaklanmaktır. Pratikte firewall'lar throughput yüzünden değil şunlar yüzünden başarısız olur:

- PPS (packets per second)
- Concurrent session sayısı
- New session rate
- NAT table ve state
- Aktif IPS/AV/App-ID ile performans
- SSL/TLS decrypt yükü
- Log üretimi ve SIEM taşıma

Gerçek bir örnek: "10 Gbps firewall aldık" cümlesi tek başına anlam taşımaz. O 10 Gbps çoğu vendor datasheet'inde ideal koşul ölçümüdür. IPS, URL filtering, app control ve decrypt aktifse gerçek kapasite dramatik şekilde değişir. Doğru soru her zaman şudur:

> *"Açacağım güvenlik özellikleriyle ve benim trafik karakterimde — bu firewall gerçekte ne kadar iş kaldırır?"*

Bu sorunun güvenilir bir cevabı yoksa, seçim risklidir.

## Adım 5: Switch Değerlendirmesi — Port Sayısı Değil Rol ve Yük

Switch seçimi çoğu zaman port sayısıyla başlar: bakır port, fiber port, PoE ihtiyacı. Bunlar önemlidir — ama core network perspektifinden yeterli değildir. Switch yalnızca uçları bağlayan bir priz değildir; trafiğin nerede yoğunlaşacağını, nerede ayrışacağını ve nerede yukarı taşınacağını belirleyen bir karar noktasıdır.

**En yaygın access layer hatası:** yalnızca bugünün ihtiyacına göre planlama yapmak. Access katmanı ağda en hızlı değişen katmandır. Bugün yeterli görünen 1G bakır bir noktada yarın yüksek bant genişliği isteyen AP veya edge cihaz konumlanabilir. Multi-Gig portlar (2.5G/5G), port başına PoE sürdürülebilirliği ve uplink'lerin gerçek kapasitesi kritik hale gelir.

Uplink'ler sürekli hafife alınır. "2×10G uplink yeter" çok duyulur — trafik karakteri analiz edilmeden. Kullanıcı sayısı arttıkça ve east-west trafik değiştikçe, uplink'ler beklenenden çok daha hızlı doygunluğa ulaşır. Backplane kapasitesi ve oversubscription oranları uplink hızı kadar önemlidir.

{{< figure src="/img/postimages/switching-selection.webp" title="Switch Seçimi: Access vs Core vs Data Center" >}}

**Edge switch vs datacenter switch:** bu sınır çoğu projede net çizilmez. Edge switch'ler port yoğunluğu ve PoE için optimize edilir; datacenter switch'leri throughput, düşük latency, yüksek PPS ve east-west trafik için gelir. Tek cihazdan her ikisini beklemek ya maliyeti gereksiz artırır ya da performansı düşürür.

Core network tasarlarken **"Bu switch nerede duracak ve neyi taşıyacak?"** sorusu **"Kaç portu var?"** sorusundan önce gelmelidir.

## Adım 6: Kablosuz — Uplink ve Controller Mimarisi

Kablosuz konuşulurken odak Wi-Fi standardına kayar: Wi-Fi 6, 6E, 7. Pratikte kablosuz performansı çoğu zaman radyo değil kablo sınırlar. AP ne kadar güçlü olursa olsun, uplink bunu taşıyamıyorsa teorik hızlar anlamsızdır.

Pek çok kurumsal AP, 1 Gbps uplink ile sınırlandığında potansiyelinin önemli bir kısmını kullanamaz. 2.5G ve 5G bakır uplink desteği yüksek yoğunluklu ortamlarda lüks değil, doğrudan tasarım gereksinimidir. Ve kritik nokta: AP 2.5G destekliyorsa ama bağlı olduğu switch portu desteklemiyorsa, tüm yatırım boşa gider. **AP ve switch seçimi birlikte yapılmalıdır.**

{{< figure src="/img/postimages/wifi-selection.webp" title="Kablosuz Mimarisi: AP, Uplink ve Controller" >}}

Controller mimarisi de kritiktir. Desteklenen AP sayısı, eş zamanlı client kapasitesi ve roaming davranışı gerçek hayat stabilitesini belirler. "500 AP destekler" yazan controller yüksek yoğunluklu ortamlarda çok daha erken zorlanabilir. Controller kapasitesi yalnızca lisans sayısıyla değil; CPU, bellek, session handling ve policy enforcement ile birlikte değerlendirilmelidir.

Kablosuz ağlar çoğu zaman edge katmanı gibi görünür ama core network'ü en hızlı zorlayan katmandır. AP seçimi kapsama hesabı değil — core network davranışını doğrudan etkileyen mimari bir karardır.

## Adım 7: Üretici Değerlendirmesi — Saha Gerçekleri

Aşağıdakiler tamamen kişisel saha deneyimlerime dayanıyor. Amaç övmek veya yermek değil — her üreticinin nerede güçlü, nerede zorlandığını açıkça söylemek.

**Cisco,** switching ve routing tarafında hâlâ sektörün en güçlü oyuncularından biri. Wireless uzun yıllardır olgun. Firewall tarafında özellikle Sourcefire gibi satın almalarla ciddi gelişim gösterdiler.
Uyarı: tüm ürünleri Cisco seçtiğinizde entegrasyon çoğu zaman yorucu olabilir. Her şey mümkün ama genellikle "kolay" değil.

**HPE Aruba,** Juniper dahil olmak üzere satın almalarla portföyü önemli ölçüde büyüdü. Switching yaygın ve sevilen. Wireless benim kişisel görüşüme göre sektörün en güçlülerinden biri.
Güçlü bir native firewall ürün ailesinin olmaması bu alanda eksiklik olmaya devam ediyor.

**Fortinet,** tek çatı altında firewall, switching ve wireless sunan en geniş portföylerden birine sahip. Firewall kökenli güçleri tartışmasız. Switching daha geç olgunlaştı ama sahada giderek daha fazla görülüyor.
En büyük operasyonel avantaj: entegrasyon ve yönetim kolaylığı. Sınırlı IT ekiplerinde bu fark çok net hissediliyor.

**Palo Alto Networks,** firewall alanında açık ara lider — switching ve wireless'a bilinçli olarak girmiyor. Uygulama görünürlüğü, politika derinliği ve SASE liderliğinde en belirgin farkı yaratıyorlar.

{{< figure src="/img/postimages/vendor-selection.webp" title="Üretici Karşılaştırması: Saha Gerçeği" >}}

Pratikte organizasyonlar tüm kombinasyonları kullanır: tek vendor, çift vendor veya best-of-breed. Bu kararlar teknik olduğu kadar organizasyoneldir.

Kişisel görüşüm: ekip olgunsa her katman için uzmanlaşmış üreticiler teknik olarak daha güçlü sonuçlar üretir. Basitlik ve tek destek kanalı daha önemliyse tek vendor yaklaşımı tamamen geçerlidir.

**Son nokta:** API desteği artık bonus değil, seçim kriteridir. "Bu mimariyi nasıl otomatik yöneteceğim?" sorusu switch, firewall ve AP seçiminden önce gelmelidir. Bana göre doğru core network tasarımı tam burada başlar.

## Sistem Odası ve Kablolama: Kimsenin Konuşmak İstemediği Ama Herkesin Bedelini Ödediği Gerçek

Network projelerinde en çok konuşulan konular genelde en parlak olanlardır. Ama sahada yaşanan problemlerin önemli bir kısmı çok daha temel bir yerde başlar: sistem odası tasarımı ve kablolama altyapısı.

Ne kadar iyi ürünler seçersen seç — sistem odası ve kablolama zayıfsa, o ağ eninde sonunda problem üretir. Ve bu problemler "network arızası" gibi görünür ama kök sebep neredeyse hiçbir zaman gerçekten network değildir.

{{< figure src="/img/postimages/server-room-and-cabling.webp" title="Sistem Odası ve Kablolama: Konuşulmayan Temel" >}}

Sistem odası çoğu kurumda hâlâ eşya odası gibi ele alınıyor. Kablolar üst üste geliyor, geçici çözümler kalıcı hale geliyor. Kimsenin dokunmak istemediği ama herkesin bağımlı olduğu bir alan oluşuyor. Asıl risk tam burada başlıyor.

Isı, enerji, hava akışı, erişilebilirlik ve düzen birlikte düşünülmelidir. Yedekli güç kaynakları satın alınır ama farklı enerji hatlarına gidip gitmediği kontrol edilmez. UPS var denir ama kapasite hesabı yapılmaz. Bunlar kağıt üzerinde küçük detay gibi görünür — kriz anında tüm mimariyi anlamsız kılar.

Kablolama ağın en uzun ömürlü parçasıdır. Switch, firewall ve AP değişir — kablo kalır. Bugünkü ihtiyaca göre kablolama yapmak garantili bir hatadır. 1G altyapısı 2.5G/5G AP'lerle hızla sınıra dayanır.

Benim bakış açıma göre sistem odası ve kablolama core network tasarımının "alt katmanı" değil; temelidir. İyi çalışan bir network kimsenin fark etmediği şeydir — çünkü sorun çıkmaz. Ve bu, bir altyapı tasarımının alabileceği en büyük övgüdür.

## Not

Bu makale ilk olarak **Substack**'te daha kısa, anlatısal bir biçimde yayınlanmıştı.
Bu versiyon, serinin mimari temelini genişletiyor.

👉 **Makaleyi Substack'te okuyun:** [Burayı Tıklayın](https://substack.com/home/post/p-183952844)

---

## İlgili Yazılar

**Mimari & Strateji**
- 📐 [IT Altyapısı Bir Ürün Koleksiyonu Değildir](/tr/architecture/it-infrastructure-not-a-collection-of-products/) — Bu serinin temel yazısı
- 🏗️ [Switch, Firewall, AP — Doğru Ürünleri Seçmek Neden Yeterli Değildir](/tr/architecture/core-network-is-not-a-product-list/) — Mimari öncelikli core network tasarımı
- 🛡️ [Zero Trust Zihniyeti: Güvenliği Bir Mimari Olarak Mühendislemek](/tr/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — Mimari olarak güvenlik

**Teknik Mühendislik**
- 📊 [İzleme Zihniyeti: Sadece Görmek Değil, Anlamak ve Proaktif Hareket Etmek](/tr/architecture/monitoring-mindset-not-just-seeing-but-understanding-and-acting-proactively/) — Operasyonel görünürlük
- 🛠️ [Ağın Arka Kapısı: Next-Gen Console Server Mimarisi](/tr/posts/next-gen-console-server-terminal-server-architecture/) — Out-of-band erişim
- 🛡️ [Network Packet Broker (NPB) Masterclass](/tr/posts/network-packet-broker-npb-masterclass/) — Trafik görünürlüğü ve güvenlik stratejisi