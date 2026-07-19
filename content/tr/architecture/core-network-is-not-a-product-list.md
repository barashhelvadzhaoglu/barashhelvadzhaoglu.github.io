---
title: "Switch, Firewall, AP — Doğru Ürünleri Seçmek Neden Yeterli Değildir"
description: "Kurumsal ağlar parçalı mimari yüzünden başarısız olur. Firewall, switching, AP seçimi ve kapasite planlaması üzerine saha incelemesi."
date: 2026-01-02
draft: false
author: "Barash Helvadzhaoglu"
language: "tr"

cover:
  image: "/img/postimages/a-core-network-is-not-a-product-list.webp"
  alt: "Switch, Firewall, AP — Doğru Ürünleri Seçmek Neden Yeterli Değildir"
  relative: false

categories:
  - Network
  - IT Infrastructure
  - Network Architecture

tags:
  - core network
  - firewall
  - switching
  - access point
  - kurumsal ağ
  - network tasarımı
  - network mimarisi
  - üretici seçimi
  - kapasite planlaması

keywords:
  - kurumsal network tasarımı
  - firewall seçim rehberi
  - switch seçimi kurumsal
  - access point mimarisi
  - network kapasite planlaması
  - NGFW vs UTM
  - core network mimarisi
  - sistem odası kablolama
  - Cisco vs Fortinet vs Palo Alto
  - network üretici karşılaştırması
  - kurumsal firewall throughput
  - zero trust network tasarımı
  - network segmentasyon
  - SD-Access mimarisi

toc: true
tocopen: true
---

# Switch, Firewall, AP — Doğru Ürünleri Seçmek Neden Yeterli Değildir
## Mimari, kapasite planlaması ve kimsenin konuşmadığı üretici gerçeği

Kurumsal ağ projelerinin çoğu aynı noktada başlıyor: ürün seçimi. Ve çoğu zaman aynı noktada kırılıyor: ürünlerin birlikte çalışmaması. Çünkü "core network" dediğimiz şey, üç kutunun (switch, firewall, access point) yan yana durması değil; bu üç kutunun birlikte kimlik taşıması, birlikte segment üretmesi, birlikte politika uygulatması ve en önemlisi birlikte operasyon kaldırmasıdır.

Benim yıllardır gördüğüm şu: bir şirketin ağı kötü olduğu için değil, ağın karar mekanizması parçalı olduğu için problem yaşanıyor. En pahalı cihazlar, en iyi lisanslar, en yüksek throughput… Hepsi var; ama olay anında kim neyi biliyor, hangi cihaz hangi bağlamla karar veriyor, trafik nerede ayrışıyor, nerede kontrol ediliyor—bu soruların net cevabı yok. Sonuç: "network var" ama "network davranışı" yok.

Bu yazıda core network'ü üç bacakta ele alacağım: Firewall, Switching, Access (Wi-Fi). Ama başlamadan önce bir şeyi net koymak istiyorum: seçim sürecinde "teknik özellik" kadar belirleyici olan iki faktör var ve çoğu ekip bunları geç fark ediyor: raporlar/validasyon ve support/lifecycle.

{{< figure src="/img/postimages/core-network-architecture-overview.webp" title="Core Network Mimarisine Genel Bakış" >}}

## Raporlar, testler ve "pazarlama gürültüsü"nü filtrelemek

Ürün seçerken bakılacak yerlerden biri, evet, Gartner raporları. Çünkü Gartner gibi raporlar sana bir ürünün "pazardaki konumu" hakkında fikir verir: kim lider, kim vizyoner, kim niş oynuyor. Bu özellikle karar verici tarafı ikna etmekte işe yarar; bütçe masasında "neden bu marka?" sorusuna bir çerçeve sunar.

Ama burada kritik bir tuzak var: Gartner sana senin senaryonda hangisinin doğru olduğunu söylemez. Gartner bir "pazar haritası"dır; senin işin "mimari harita" çizmek. Bu yüzden Gartner'ı bir ilk filtre gibi kullanmak daha doğru: seçenekleri daraltır ama final kararı vermez.

{{< figure src="/img/postimages/filtering-reports-tests-and-marketing-noise.webp" >}}

Gartner'a ek olarak, üreticilerin ya da bağımsız laboratuvarların yaptığı performans ve güvenlik testleri, karşılaştırmalı raporlar, "real-world" benchmark'lar da işin içine girmeli. Çünkü veri sayfasındaki throughput ile, gerçek hayatta IPS açıkken, SSL decrypt varken, app-control çalışırken alınan throughput aynı şey değildir. Raporlar burada bir ikinci filtre olur: "Bu kutu bu yükte ne yapıyor?" sorusuna pazarlama dışı bir cevap ararsın.

## Support ve lifecycle: Projeyi ayakta tutan görünmez kolon

Bir ürünün teknik yetenekleri kadar kritik olan şey, onun destek modeli ve yaşam döngüsüdür. Çünkü network tasarımı yalnızca "kurulum günü"nden ibaret değildir. Asıl mesele 3 yıl sonra ne olacağıdır:
* Bu ürünün EoL / EoS tarihleri nedir?
* Patch, bugfix, security update hızı nasıldır?
* TAC/Support gerçekten erişilebilir mi, escalation süreci nasıl işler?
* RMA süreçleri ve yedek parça gerçekliği nedir?
* Lisans modeli 1 yıl sonra sürpriz çıkarır mı?
* Üretici roadmap'i senin gittiğin yöne mi gidiyor?

Bunu yazıya özellikle koymak istiyorum çünkü sahada en sık gördüğüm problem şu: ekip teknik olarak doğruya yakın bir ürün seçiyor ama support/lifecycle yüzünden 12 ay sonra operasyon kâbusa dönüyor. Sonra suç cihazda kalıyor; oysa sorun cihazın kendisinden çok, seçimin "destek" tarafının ciddiye alınmamasıdır.

## Firewall: UTM mi, NGFW mi, yoksa birden fazla rol mü?

Firewall, günümüzde ağın "kenarındaki güvenlik cihazı" olmayı çoktan geçti. Doğru konumlandırılırsa politika beynidir; yanlış konumlandırılırsa her şeyin üstüne yıkıldığı için darboğaz olur.

Burada en baştan terminolojiyi netlemek iyi olur: UTM ve NGFW kavramları çoğu ortamda birbirine karışıyor.

UTM yaklaşımı genelde "her şey tek kutuda" düşüncesine yakın durur: temel firewall + IPS + web filter + AV + bazı gateway özellikleri… Özellikle daha küçük/orta ölçekli yapılarda, yönetim kolaylığı ve paket yaklaşımı yüzünden tercih edilir.

NGFW ise daha çok uygulama farkındalığı, kullanıcı/kimlik farkındalığı, daha gelişmiş security services ve policy derinliğiyle konumlanır. Bugünün kurumsal ihtiyacında "sadece port-protocol" ile güvenlik yürütmek çoğu zaman yetmez; NGFW burada devreye girer.

Ama asıl kritik nokta şu: bir şirketin ihtiyacı tek bir "firewall tipi" ile bitmeyebilir. Çünkü firewall dediğimiz şey, aslında farklı amaçlar için farklı katmanlarda görev alabilir.

{{< figure src="/img/postimages/firewall-selection.webp" >}}

### Aynı şirkette iki (hatta üç) firewall neden normaldir?

Birçok kurumda şu senaryolar çok makuldür:
* Perimeter/Internet Edge Firewall: İnternet çıkışı, VPN, NAT, inbound/outbound policy.
* Internal Segmentation Firewall (ISFW): İç ağda segmentasyon, east-west kontrol, kritik zonlar.
* Data Center / High-performance FW: DC trafiği, yüksek session, yüksek PPS, düşük latency ihtiyacı.
* Bazı yapılarda ayrıca WAF ya da Cloud FW gibi özel bileşenler.

Bu "iki firewall almak" demek değildir; bu, "iki farklı işi doğru araca vermek" demektir. Tek kutuya her şeyi yığdığında, ya performans kaybedersin ya yönetim kaybedersin ya da güvenlik kaybedersin.

> Bu mimarinin arkasındaki güvenlik felsefesini daha derinlemesine anlamak için: [Zero Trust Zihniyeti: Güvenliği Mimari Olarak Mühendislemek](/tr/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/)

Ve bu bizi doğrudan kapasite planlamasına götürür.

## Firewall kapasite planlaması: Throughput tek başına yalan söyleyebilir

Firewall seçiminde en tehlikeli yanlış, yalnızca "Gbps throughput" rakamına bakmaktır. Çünkü gerçek hayatta firewall'u öldüren şey çoğu zaman throughput değil:
* PPS (packets per second)
* Concurrent session sayısı
* New session rate
* NAT table ve state
* IPS/AV/App-ID açıkken performans
* SSL/TLS decrypt gibi ağır iş yükleri
* Log üretimi ve log'u taşımak (SIEM entegrasyonu)

{{< figure src="/img/postimages/firewall-capacity-planning.webp" title="Firewall Kapasite Planlama Metrikleri" >}}

Örnek bir gerçek: "10 Gbps firewall aldık" cümlesi tek başına anlam taşımaz. Çünkü o 10 Gbps, çoğu vendor datasheet'inde "ideal koşul" ölçümüdür. Senin ortamında IPS, URL filtering, app control, decrypt aktifse; gerçek kapasite dramatik şekilde değişir. Bu yüzden doğru soru şu olmalı:
"Benim açacağım güvenlik özellikleriyle, benim trafik karakterimde, bu firewall ne kadar iş kaldırıyor?"

Bu sorunun cevabı yoksa, seçim risklidir.

## Switching: Port sayısından çok, taşıyabileceği yük ve rolü önemlidir

Switch seçimi çoğu zaman port sayısıyla başlar: kaç adet bakır port, kaç adet fiber port, PoE ihtiyacı var mı yok mu… Bunlar elbette önemlidir ama core network perspektifinden bakıldığında yeterli değildir. Çünkü switch yalnızca uçları bağlayan bir priz değildir; trafiğin nerede yoğunlaşacağını, nerede ayrışacağını ve nerede yukarı taşınacağını belirleyen bir karar noktasıdır.

Özellikle access switch tarafında yapılan en yaygın hata, bugünkü ihtiyaca göre port planlaması yapmaktır. Oysa access katmanı, ağda en hızlı değişen katmandır. Bugün bakır port yeterli görünen bir noktada, yarın yüksek bant genişliği isteyen bir AP, bir kamera ya da farklı bir edge cihaz konumlanabilir. Bu yüzden bakır portların hız kabiliyeti (1G mi, 2.5G/5G mi destekliyor), PoE bütçesinin yalnızca toplam watt değil port başına sürdürülebilirliği ve uplink'lerin gerçek kapasitesi kritik hale gelir.

Uplink konusu genellikle hafife alınır. "2×10G uplink yeter" gibi cümleler çok duyulur ama bu uplink'lerin hangi trafik karakterini taşıyacağı çoğu zaman konuşulmaz. Access katmanında kullanıcı sayısı arttıkça, east-west trafik ve broadcast davranışı değiştikçe, uplink'ler beklenenden çok daha hızlı doygunluğa ulaşabilir. Bu noktada yalnızca uplink hızına değil, switch'in backplane kapasitesine ve oversubscription oranlarına bakmak gerekir.

Edge switch ile datacenter switch arasındaki fark da çoğu projede net çizilmez. Edge switch'ler genellikle kullanıcı ve cihaz yoğunluğu için optimize edilir: çok sayıda port, PoE, erişim odaklı özellikler. Datacenter switch'ler ise yüksek throughput, düşük latency, yüksek PPS ve east-west trafiği kaldıracak mimariyle gelir. Core network tasarlarken "bu switch nerede duracak ve neyi taşıyacak?" sorusu, "kaç portu var?" sorusundan önce gelmelidir.

{{< figure src="/img/postimages/switching-selection.webp" >}}

Inter-VLAN routing kararları da switch seçimiyle doğrudan ilişkilidir. Eğer routing switch üzerinde yapılacaksa, bu switch'in yalnızca L3 desteklemesi yetmez; route scale, TCAM kapasitesi, policy uygulanabilirliği ve bu kararların firewall ile nasıl entegre olacağı düşünülmelidir.

## Access / Wi-Fi: Radyo kadar uplink ve kontrol katmanı da mimarinin parçasıdır

Kablosuz ağlar konuşulurken odak genellikle Wi-Fi standardına kayar: Wi-Fi 6, 6E, 7… Oysa pratikte kablosuz performansı sınırlayan şey çoğu zaman hava değil, kablodur. Access point ne kadar güçlü olursa olsun, arkasındaki uplink bunu taşıyamıyorsa teorik hızlar hiçbir anlam ifade etmez.

Bugün pek çok kurumsal AP, 1 Gbps uplink ile sınırlandığında potansiyelinin ciddi bir kısmını kullanamaz. Bu yüzden 2.5G ve 5G bakır uplink desteği, özellikle yoğun kullanıcı olan ortamlarda bir "lüks" değil, doğrudan tasarım gereksinimidir. AP ve switch seçimi bu yüzden ayrı ayrı değil, birlikte yapılmalıdır.

{{< figure src="/img/postimages/wifi-selection.webp" >}}

Wi-Fi tarafında bir diğer kritik konu, controller mimarisidir. Controller'ın desteklediği AP sayısı, eş zamanlı client kapasitesi ve roaming davranışı, ağın gerçek hayattaki stabilitesini belirler. Controller kapasitesi yalnızca lisans sayısı değil; CPU, bellek, session handling ve policy enforcement kapasitesiyle birlikte değerlendirilmelidir.

Ayrıca kablosuz ağlar çoğu zaman "edge" gibi düşünülür ama gerçekte core network'ü en hızlı zorlayan katmandır. AP seçimi yalnızca kapsama alanı hesabı değil; core network davranışını doğrudan etkileyen bir mimari karardır.

## Kapanış: Üretici Seçimi, Mimari Olgunluk ve Gerçekler

Bu noktada şunu özellikle belirtmek istiyorum: aşağıda bahsettiklerim tamamen kişisel saha tecrübelerime ve gözlemlerime dayanıyor. Bir üreticiyi övmek ya da yermekten çok, nerede güçlü olduklarını ve nerede zorlandıklarını açıkça söylemek niyetindeyim.

Cisco ile başlamak doğal. Switching ve routing tarafında hâlâ sektörün en güçlü oyuncularından biri. Özellikle büyük ve karmaşık yapılarda, campus ve datacenter switching konusunda ciddi bir olgunlukları var. Ancak şunu net söylemek gerekir: tüm ürünleri Cisco seçtiğinizde, bu ürünlerin birbiriyle entegrasyonu çoğu zaman bir admin için yorucu ve zahmetli olabiliyor.

Yaklaşık on yıldır gelişimini yakından izlediğim HPE Aruba tarafı ise farklı bir hikâye sunuyor. Switching tarafında Aruba ailesi oldukça yaygın ve sevecen bir kullanıcı kitlesine sahip. Wireless tarafında ise benim kişisel görüşüm, sektördeki en güçlü Wi-Fi çözümlerinden birine sahipler. Kendi başına güçlü bir firewall ürün ailesinin olmaması bu alanda bir eksiklik.

Fortinet tarafı ise çok geniş bir ürün yelpazesi sunuyor. Firewall, switching ve wireless tarafında "tek çatı altında" komple bir çözüm sunabilmeleri ciddi bir avantaj. Fortinet ekosisteminin bana göre en büyük artılarından biri, kullanım ve arayüz kolaylığı.

Palo Alto Networks tarafına geldiğimizde tablo daha net: Palo Alto, firewall konusunda çok güçlü ve bu alanda tartışmasız şekilde lider üreticilerden biri. Application visibility, policy derinliği ve özellikle SASE gibi alanlarda Palo Alto'nun ciddi bir fark yarattığını düşünüyorum.

{{< figure src="/img/postimages/vendor-selection.webp" >}}

Son olarak özellikle altını çizmek istediğim bir nokta var: günümüzde neredeyse tüm büyük üreticiler otomasyon tarafına ciddi yatırım yapıyor. API desteği artık bir "ekstra" değil, doğrudan bir seçim kriteri.

> Altyapınızda gerçek görünürlük oluşturmak için pratik bir çerçeve: [İzleme Zihniyeti: Sadece Görmek Değil, Anlamak ve Proaktif Hareket Etmek](/tr/architecture/monitoring-mindset-not-just-seeing-but-understanding-and-acting-proactively/)

## Sistem Odası ve Kablolama: Kimsenin Konuşmak İstemediği Ama Herkesin Bedelini Ödediği Gerçek

Network projelerinde en çok konuşulan konular genelde en "parlak" olanlardır. Ama sahada yaşanan problemlerin önemli bir kısmı, bu ürünlerden çok daha temel bir yerde başlar: sistem odası tasarımı ve kablolama altyapısı.

Benim yıllar içinde defalarca gördüğüm bir gerçek var: ne kadar iyi ürünler seçersen seç, ne kadar doğru mimari kurgularsan kurgula; eğer sistem odası ve kablolama altyapısı zayıfsa, o ağ eninde sonunda problem üretir.

Sistem odası çoğu kurumda hâlâ bir "eşya odası" gibi ele alınıyor. İlk başta küçük bir alana birkaç rack konuyor, işler büyüdükçe aynı odaya yeni cihazlar ekleniyor, kablolar üst üste geliyor, geçici çözümler kalıcı hale geliyor. İşte asıl risk tam burada başlıyor.

{{< figure src="/img/postimages/server-room-and-cabling.webp" >}}

Bir sistem odası yalnızca cihazların durduğu bir yer değildir. O oda, ağın kalbidir. Isı, enerji, hava akışı, erişilebilirlik ve düzen; hepsi birlikte düşünülmelidir.

Kablolama altyapısı ise genelde "bir kere yapılır ve unutulur" diye düşünülür. Oysa kablolama, network'ün en uzun ömürlü parçasıdır. Switch'i, firewall'u, access point'i değiştirirsin; ama kablo orada kalır.

Fiber ve bakır kabloların nerede, hangi amaçla kullanılacağı da mimari bir karardır. Patch panel düzeni, kablo etiketleme, rack içi ve rack arası kablo yönetimi doğrudan operasyonel konulardır.

Benim bakış açıma göre sistem odası ve kablolama, core network tasarımının "alt katmanı" değildir; temelidir. İyi çalışan bir network'ün arkasında çoğu zaman iyi tasarlanmış bir sistem odası ve temiz bir kablolama altyapısı vardır. Kimse bunu fark etmez; çünkü zaten sorun çıkmaz. Ve bana göre bu, bir altyapı tasarımının alabileceği en büyük övgüdür.

## Not

Bu makale ilk olarak **Substack**'te daha kısa, anlatısal bir biçimde yayınlanmıştı.
Bu versiyon, serinin mimari temelini genişletiyor.

👉 **Makaleyi Substack'te okuyun:** [Burayı Tıklayın](https://substack.com/home/post/p-183952844)

---

## İlgili Yazılar

Bu yazıyı faydalı bulduysanız, şu yazılar da ilginizi çekebilir:

**Mimari & Güvenlik Tasarımı**
- 📐 [IT Altyapısı Bir Ürün Koleksiyonu Değildir](/tr/architecture/it-infrastructure-is-not-a-collection-of-products/) — Bu serinin temel yazısı
- 🛡️ [Zero Trust Zihniyeti: Güvenliği Mimari Olarak Mühendislemek](/tr/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — Zero Trust neden bir ürün değil, bir felsefedir
- 📊 [İzleme Zihniyeti: Sadece Görmek Değil, Anlamak ve Proaktif Hareket Etmek](/tr/architecture/monitoring-mindset-not-just-seeing-but-understanding-and-acting-proactively/) — Altyapınızda gerçek görünürlük nasıl inşa edilir

**Teknik Mühendislik**
- 🛠️ [Ağın Arka Kapısı: Next-Gen Console Server Mimarisi](/tr/posts/next-gen-console-server-terminal-server-architecture/) — Her şey kesildiğinde out-of-band erişim
- 🛡️ [Network Packet Broker (NPB) Masterclass](/tr/posts/network-packet-broker-npb-masterclass/) — Gelişmiş trafik görünürlüğü ve güvenlik stratejisi
- 🔐 [802.1X Projelerinde Başarı: Saha Deneyimleri](/tr/posts/unlocking-success-in-802-1x-projects-field-insights/) — Kurumsal ağlarda kimlik tabanlı erişim
- ⚙️ [Nexus Yazılım Yükseltme Rehberi](/tr/posts/cisco-nexus-nxos-upgrade-guide/) — Kesintisiz NX-OS yükseltme adım adım