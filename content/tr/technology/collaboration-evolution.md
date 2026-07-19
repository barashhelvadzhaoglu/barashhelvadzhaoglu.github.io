---
title: "Kurumsal İş Birliği Altyapısı: IP Telefonlardan Bulut Çağına"
description: "Kurumsal iş birliğinin evrimi — Cisco CUCM ve IP telefoniden Webex, Teams ve Zoom'a. Bir saha mühendisinin perspektifinden."
date: 2026-04-10
draft: false

cover:
  image: "/img/postimages/collaboration-infrastructure-evolution-cover.webp"
  alt: "Kurumsal İş Birliği Evrimi — IP Telefondan Buluta"
  relative: false

tags: ["İş Birliği", "Cisco", "CUCM", "Webex", "IP Telefon", "Video Konferans", "Teams", "Zoom", "Unified Communications"]
categories: ["Teknoloji"]
keywords:
  - kurumsal iş birliği altyapısı
  - Cisco CUCM unified communications
  - IP telefon evrimi
  - Webex bulut iş birliği
  - kurumsal video konferans
  - Microsoft Teams kurumsal
  - Cisco TelePresence
  - iş birliği toplantı odası sistemleri
  - Webex Board akıllı tahta
  - UCaaS bulut telefon

showToc: true
TocOpen: false
---

# Kurumsal İş Birliği Altyapısı: IP Telefonlardan Bulut Çağına

Kurumsal IT alanında çalışan herkes için yararlı bir düşünce deneyi: 2010 yılında bir şehirdeki konferans odasını başka bir şehirdeki konferans odasına bağlamak için ne gerekiyordu? Şimdi bugün ne gerektiğiyle karşılaştırın.

2010'da her iki uçta da özel bir codec cihazı, çağrı ayarlarını yapılandırmak için nitelikli bir video konferans mühendisi, sağlanmış bir ISDN hattı veya dikkatle yapılandırılmış IP altyapısı ve toplantıdan önce bağlantıyı test etmek için önemli bir hazırlık süresi gerekiyordu. Codec yazılım sürümleri uyuşmadıysa, firewall portları tam olarak doğru değilse veya karşı taraftaki IT ekibi yapılandırmasını farklı yapmışsa çağrı bağlanmıyordu.

Bugün, biri bir Webex veya Teams linki oluşturuyor, bunu bir takvim davetine ekliyor ve herkes bulunduğu yerden — dizüstü bilgisayar, telefon, özel toplantı odası sistemi — tek tıklamayla katılıyor. Toplantı odası donanımı otomatik olarak ne yapacağını biliyor.

Bu iki nokta arasında yaşananlar, son yirmi yılda kurumsal IT'deki en önemli mimari dönüşümlerden birini oluşturuyor. Bu yazı o dönüşümü izliyor.

---

## Bölüm 1: IP Telefon Dönemi — Telefon Bir Ağ Cihazına Dönüştüğünde

### Analogdan IP'ye Geçiş

IP telefondan önce, kurumsal telefon sistemleri PBX (Private Branch Exchange — Özel Şube Santrali) altyapısı üzerinde çalışıyordu — veri ağından tamamen ayrı, özel amaçlı donanım. IT ekibi veri ağını yönetiyordu; tesisler veya telefon ekibi PBX'i yönetiyordu. Bunlar paralel dünyalardı.

IP telefon bunu köklü biçimde değiştirdi. Telefon bir ağ uç noktasına dönüştü — özel bir ses devresine değil, veri ağına bağlanan IP adresi olan başka bir cihaz. PBX'in yerini standart donanım üzerinde çalışan bir çağrı işleme sunucusu aldı.

Cisco için bu, tüm çağrı yönlendirmeyi, çevirme planı yönetimini, sesli posta entegrasyonunu ve telefon sağlamayı yöneten **Cisco Unified Communications Manager (CUCM)** anlamına geliyordu. Bir Cisco IP telefonu açılıyor, TFTP aracılığıyla CUCM'den yapılandırmasını alıyor, SCCP veya SIP aracılığıyla CUCM'e kaydoluyor ve çağrı yapmaya hazır hale geliyordu — tamamen veri ağı üzerinden.

### Pratikte CUCM Nasıl Görünüyordu

Tipik bir orta ölçekli kurumsal CUCM deployment'ı:

```
CUCM Publisher (birincil)
CUCM Subscriber x2 (yedeklilik için)
CUCM IM & Presence (anlık mesajlaşma)
Unity Connection (sesli posta)
Cisco Emergency Responder
Cisco IP Telefonlar (7900 serisi, 8800 serisi)
```

Çevirme planı — çağrıların nasıl yönlendirildiğini, hangi numaraların dahili olduğunu, hangilerinin trunk erişimi gerektirdiğini, diğer sitelere yapılan çağrıların nasıl işlendiğini belirleyen kurallar bütünü — tamamen CUCM yapılandırmasında yaşıyordu. Bu güçlüydü ama önemli bir uzmanlık gerektiriyordu. 3 ülkede 10 ofisi olan bir şirket için çevirme planı yüzlerce rota deseni, çeviri deseni, arama grubu ve çağrı yönlendirme kuralı içerebiliyordu.

**CUCM yükseltmeleri** başlı başına bir proje niteliğindeydi. Her büyük sürüm dikkatli yükseltme öncesi testler, bir bakım penceresi ve çoğunlukla bir geri alma planı gerektiriyordu. Cisco CUCM yükseltme süreci — sürümleri doğrulama, yükseltme sihirbazını çalıştırma, abone node'ların senkronize olmasını bekleme, tüm telefonların yeniden kaydolduğunu doğrulama — büyük bir küme için saatler alabiliyordu. Hazırlık adımlarını atlamanın sorunların başladığı yer olduğunu yeterince deneyimledim.

### MPLS ve VPN: Çok Siteli Sesi Ücretsiz Kılmak

IP telefonun en zorlayıcı erken iş gerekçelerinden biri siteler arası aramayı oldu. Daha önce İstanbul ofisinden Ankara ofisine yapılan bir çağrı PSTN üzerinden gidiyordu — diğer çağrılar gibi dakika başına ücretlendiriliyordu.

Kurumsal WAN üzerinden IP telefonla aynı çağrı tamamen ağın içinde kalıyordu: İstanbul telefonu → İstanbul CUCM → MPLS/VPN bağlantısı → Ankara CUCM → Ankara telefonu. Sıfır PSTN maliyeti. Düzinelerce ofisi ve günlük yüzlerce siteler arası araması olan şirketler için bu tek başına IP telefon geçişini haklı kılıyordu.

**MPLS** bu dönemde baskın WAN teknolojisiydi — özel, düşük gecikmeli, öngörülebilir. MPLS siteleri hub-and-spoke veya tam örgü topolojisinde birbirine bağlıyor, ses trafiği kaliteli hizmet (QoS) açısından önceliklendiriliyordu.

**IPsec VPN**, MPLS'in çok pahalı olduğu küçük siteler için kullanılıyordu — bir şube ofisi genel merkezine internet üzerinden IPsec aracılığıyla bağlanabilir, merkezdeki CUCM şubedeki telefonlara hizmet verebilirdi.

Bunun için gereken yapılandırma küçümsenmeyecek boyuttaydı. QoS politikaları, ses trafiğinin geçtiği her ağ segmentinde tutarlı olmak zorundaydı. Codec seçimi (G.711 - G.729) çağrı kalitesini bant genişliği tüketimiyle dengelemek zorundaydı. Çağrı Kabul Kontrolü, çok fazla eş zamanlı aramanın bir WAN bağlantısını doyurmasını engellemek zorundaydı. Bunların tümü manuel olarak yapılandırılıyor, yönetilip gideriliyordu.

---

## Bölüm 2: Video Sahneye Giriyor — Ve Beraberinde Karmaşıklık Getiriyor

### Donanım Video Konferans Dönemi

Kurumlarda video konferans yazılımla başlamadı. Özel amaçlı codec cihazlarıyla başladı — video kodlama/kod çözmeyi yöneten, büyük ekranlara bağlanan ve H.323 veya SIP video protokollerini kullanan ISDN veya IP üzerinden iletişim kuran, özel amaçlı donanım.

Baskın satıcılar Cisco (TelePresence), Polycom ve Tandberg'di (Cisco 2010'da satın alarak teknolojisini TelePresence ürün hattına entegre etti).

Ürün hattının üst ucundaki Cisco TelePresence IX5000 toplantı odası sistemi, uzaktaki katılımcıların karşısında oturma hissini yaratmak için tasarlanmış üç ekranlı sürükleyici bir kurulumdu. Etkileyici bir mühendislikti. Aynı zamanda son derece pahalıydı: donanım tek başına oda başına yüz binlerce dolara çıkıyor, üstüne özel ağ altyapısı ve IT destek sözleşmeleri geliyordu.

Daha yaygın kullanılan orta segment sistemlerdi — Cisco SX80, Polycom Group Series, Tandberg C serisi uç nokta. Bunlar hâlâ özel donanımdı: bir codec birimi, bir veya iki ekran, bir kamera ve bir mikrofon dizisi. Her odanın kendi cihazı, kendi IP adresi, video altyapısına kendi kaydı vardı.

### Videonun Arkasındaki Altyapı

Kurumsal video aramalarının çalışması için uç nokta donanımından daha fazlası gerekiyordu:

**Cisco VCS (Video Communication Server):** Video için çağrı kontrolü platformu — CUCM'nin video uç noktalar için eşdeğeri. VCS Expressway işletmeden işletmeye aramaları ve harici video bağlantısını yönetiyordu. VCS Control dahili uç noktaları yönetiyordu.

**MCU (Multipoint Control Unit):** İkiden fazla uç noktanın aynı video aramasında olması gerektiğinde, ses ve video akışlarını karıştırmak için MCU gerekiyordu. Cisco Codian MCU, daha sonra MSE 8000 serisi bunu yönetiyordu. Her MCU'nun belirli sayıda eş zamanlı port için lisansı vardı — MCU kapasitesinin tükenmesi daha fazla konferans köprüsü olmadığı anlamına geliyordu.

**Harici bağlantı altyapısı:** Kuruluşunuzun video altyapısının dışındaki birine arama yapmak, geçiş sunucuları, firewall geçiş yapılandırması ve çoğunlukla kuruluşlar arasında federasyon anlaşmaları gerektiriyordu.

**Yapılandırma karmaşıklığı:** 2012'de bir video konferans odası araması planlamak için şunları yapmanız gerekebilirdi: MCU konferans köprüsünü rezerve etmek, her uç nokta için çevirme dizisini yapılandırmak, önceki gün bağlantıyı test etmek, codec uyumluluğunu doğrulamak ve bir şeyler ters gittiğinde arama sırasında hazır bekleyen bir IT personeli bulundurmak.

Bu mühendislerin ne yaptıklarını bilmemesinden değildi — sistemin karmaşıklığı gerçekten bunu gerektiriyordu.

### Kalite Sorunu

Bu dönemde internet üzerinden video görüşme de vardı — tüketiciler için Skype, çeşitli erken kurumsal araçlar. Ancak gerçek kalite gereksinimlerine sahip kurumsal organizasyonlar video için halka açık internete güvenmiyordu. Siteler arası aramalar için özel MPLS ağlarını ve harici aramalar için ISDN kullanıyorlardı. İnternet kalitesi öngörülemezdi, gecikme değişkendi ve paket kaybı video aramalarını izlenemez hale getiriyordu.

Bu iki katmanlı bir gerçeklik yarattı: resmi toplantılar için yüksek kaliteli, pahalı, altyapıya bağımlı video; gayri resmi kullanım için güvenilmez tüketici araçları. İkisi de tatmin edici değildi.

---

## Bölüm 3: Bulut Geçişi — Her Şey Neden Taşındı

### Tetikleyici: İnternet İyileşti

İş birliği altyapısının buluta göçü tek bir kararla veya teknoloji atılımıyla gerçekleşmedi. Halka açık internetin güvenilir biçimde sunabildiği şeylerdeki kademeli bir değişimle gerçekleşti.

İnternet bağlantıları hem kurumlarda (standart hale gelen 100 Mbps ile 1 Gbps WAN bağlantıları) hem de uzak çalışanlar için daha hızlı, güvenilir ve tutarlı hale geldikçe, özel ağ videosu ile internet tabanlı video arasındaki kalite farkı azaldı. Dizüstü bilgisayarlardaki yazılım istemcileri değişken ağ koşullarına uyum sağlamada daha iyi hale geldi. Video codec'leri (H.264, ardından VP9, ardından H.265) daha verimli oldu.

İnternet video kalitesi iş kullanımı için gerçekten kabul edilebilir hale geldiğinde hesap değişti. Pahalı şirket içi altyapı — CUCM kümeleri, VCS sunucuları, MCU köprüleri — zorunluluk yerine yük gibi görünmeye başladı.

### Ekonomik Argüman

Şirket içi unified communications altyapısının önemli süregelen maliyetleri vardı:
- Sunucu donanımı yenileme döngüleri (her 4–5 yılda bir)
- Yazılım lisanslaması (kullanıcı başına, cihaz başına CUCM lisansları)
- Cisco ile destek sözleşmeleri (SmartNet)
- Sistemi yönetmek, yükseltmek ve sorunları gidermek için IT personeli
- Sunucular için veri merkezi alanı, güç ve soğutma

Bulut tabanlı iş birliği bunu kullanıcı başına aylık aboneliğe dönüştürdü. Donanım yenileme yok. Yükseltme projeleri yok. Otomatik özellik güncellemeleri. Azaltılmış IT operasyonel yükü.

500 çalışan ekleyen bir şirket için geleneksel model daha fazla CUCM sunucu kapasitesi, daha fazla lisans, daha fazla telefon satın almak anlamına geliyordu. Bulut modeli aboneliğe 500 lisans eklemek anlamına geliyordu.

### Webex'in Dönüşümü

Cisco'nun Webex'i web konferans ürünü olarak başladı — çevrimiçi toplantılar için ekran paylaşımı ve ses. IP telefon dünyasından tamamen ayrıydı.

Cisco birkaç yıl içinde bu dünyaları sistematik olarak birleştirdi:
- Webex Meetings + CUCM entegrasyonu: kullanıcılar Cisco IP telefonlarından video aramalar başlatabiliyordu
- Webex Teams (şimdi Webex App): ekip mesajlaşması ve arama birleşti
- Webex Calling: birçok organizasyon için şirket içi CUCM'nin yerini alan bulut tabanlı arama hizmeti — çevirme planları, sesli posta, dahili numaralar, tümü bulutta yönetiliyor
- Birleşik Webex App: arama, toplantılar, mesajlaşma ve dosya paylaşımı için tek uygulama

Sonuç: Daha önce şirket içinde CUCM, video için VCS ve sesli posta için Unity Connection'a sahip bir şirket, Webex Calling'e geçerek üçünün de yerine geçen tek bir bulut hizmeti kullanabiliyordu — web portalı üzerinden yönetilen, bakım yapılacak sunucu yok.

---

## Bölüm 4: Çok Platformlu Gerçeklik — Teams, Zoom ve Diğerleri

### Microsoft Teams: Rakip

Microsoft Teams 2017'de bir Slack rakibi olarak piyasaya çıktı. Üç yıl içinde baskın kurumsal iş birliği platformu haline geldi — her boyutuyla teknik açıdan üstün olduğu için değil, zaten orada olduğu için. E-posta ve Office uygulamaları için Microsoft 365 kullanan organizasyonlar Teams'i dahil olarak aldı. Ayrı tedarik, yeni satıcı ilişkisi, ek IT altyapısı gerektirmiyordu.

Teams, PSTN arama özelliği ekledi (Teams Phone, eski adıyla Phone System) — organizasyonların PBX'lerini Teams ile değiştirmesine, Microsoft bulutu aracılığıyla normal telefon aramaları yapıp almasına olanak tanıdı.

**Birlikte çalışabilirlik sorusu:** Farklı organizasyonlardan bir Webex kullanıcısı ve bir Teams kullanıcısı video toplantısı yapmak istiyor. Her ikisi de kendi platformuna sahip. Nasıl bağlanırlar?

Başlangıçta yanıt "bir platform diğerini misafir olarak davet eder"di — işe yarıyordu ama sorunsuz değildi. Bu durum önemli ölçüde gelişti. Cisco ve Microsoft, Webex ile Teams arasında doğrudan birlikte çalışabilirlik geliştirdi. Bir Cisco toplantı odası sistemi Teams toplantısına yerel olarak katılabilir. Teams kullanıcısı herhangi bir şey yüklemeden Webex toplantısına katılabilir.

### Zoom: Sadelik Hamlesi

Zoom, 2020 yılında kurumsal farkındalığa önemli ölçüde girdi. Teknik güçleri — değişken internet bağlantıları üzerinde gerçekten güvenilir video kalitesi, misafirler için hesap gerektirmeyen basit katılım deneyimi — mevcut araçları yetersiz kalan organizasyonlar için çekici hale getirdi.

Zoom'un gösterdiği şey, kullanım kolaylığının özellik derinliği kadar önemli olduğuydu. "Sadece linke tıkla" deneyimi, tüm iş birliği araçları için standart beklenti haline geldi.

### Avaya, 3CX ve Orta Pazar

Her organizasyon Cisco veya Microsoft ölçeğine ihtiyaç duymuyordu. Orta pazarın kendi oyuncuları var:

**Avaya** on yıllardır önemli bir kurumsal telefon satıcısı olmuştur — Aura platformu kurumsal deployment ölçeğinde CUCM ile rekabet eder. Avaya son yıllarda önemli finansal zorluklardan geçti (birden fazla iflas başvurusu), bu da platformundaki müşteriler için belirsizlik yarattı.

**3CX**, yazılım tabanlı bir PBX olarak KOBİ ve orta pazarda popüler hale geldi — Windows veya Linux'a kurulabilir, CUCM lisanslamasından düşük maliyetli, makul özellik seti.

**RingCentral, 8x8, Vonage (şimdi Ericsson):** Platformlarını başından beri bulutta inşa etmiş, şirket içi miras olmayan bulut tabanlı UCaaS sağlayıcıları.

---

## Bölüm 5: Modern Toplantı Odası

### En Çok Ne Değişti

Toplantı odası, dönüşümün en görünür olduğu yerdir. Karşılaştırın:

**2012 toplantı odası:**
- Özel codec (Cisco SX80 veya Polycom Group): 15.000–50.000 dolar
- Duvara monte büyük ekran(lar)
- Pan-tilt-zoom kamera, tavan veya masa üstü mikrofon dizisi
- IT tarafından yönetilen altyapı kaydı
- Harici aramaya katılmak: çevirme dizisini araştırın, manuel girin, karşı tarafın doğru cevap vermesini umun
- Webex veya Skype toplantısına katılmak: mümkün ama belirli yapılandırma gerektiriyordu ve çoğunlukla güvenilir biçimde çalışmıyordu

**2024 toplantı odası:**
- Toplantı odası sistemi (Cisco Room Bar, Webex Board, Logitech Rally Bar, Poly Studio): 1.500–8.000 dolar
- Tek dokunuşla katılım: toplantı odası ekranı yaklaşan takvim toplantılarını gösteriyor; katılmak için dokunun
- Webex, Teams, Zoom ile çalışıyor — çoğunlukla bir yazılım ayarıyla üçü birden
- Toplantıya katılmak için IT müdahalesi gerekmiyor
- Herhangi bir dizüstü bilgisayardan kablosuz içerik paylaşımı
- AI özellikleri: gürültü engelleme, arka plan bulanıklaştırma, aktif konuşmacıyı takip eden otomatik çerçeveleme

Maliyet azalması önemlidir. Operasyonel sadelik iyileşmesi dönüştürücüdür.

### Webex Board ve Akıllı Tahta Özellikleri

Cisco'nun Webex Board'u (şimdi Webex Desk ve Room ürün hattının bir parçası), bağımsız video konferansın hiçbir zaman sahip olmadığı bir özellik ekledi: **dijital tahta**.

Webex Board aynı anda dokunmatik ekran, video konferans sistemi ve tahta. Bir toplantıda katılımcılar doğrudan tahta yüzeyine çizebilir. Uzak katılımcılar tahtayı gerçek zamanlı görür. Toplantı sırasında tahtaya yazılan içerik otomatik olarak kaydedilir ve toplantı sonrasında dosya olarak paylaşılır.

### Logitech'in Etkisi

Logitech, kurumsal toplantı odası pazarına tüketici çevre birimi tarafından girdi ve ciddi bir oyuncu haline geldi. Rally Bar ve Rally Bar Mini sistemleri, kamerayı entegre hoparlör ve mikrofonla birleştiren bar biçimli sistemler — bir ekranın üstüne veya altına yerleştirilmek üzere tasarlandı.

Önem: kurumsal düzeyde toplantı odası özelliği, tüketici düzeyinde fiyatlandırmayla. Microsoft Teams veya Zoom Rooms sertifikalı bir Logitech Rally Bar, Cisco veya Poly toplantı odası sisteminin çok altında bir fiyata mal oluyor. Onlarca küçük toplantı odası donatmak isteyen organizasyonlar için bu fiyat noktası, daha önce ekonomik olmayan her odayı donatmayı mümkün kılıyor.

---

## Bölüm 6: CUCM Yükseltmeleri — Pratik Bir Not

Şirket içinde Cisco CUCM çalıştıran organizasyonlar için yükseltmeler hâlâ önemli bir operasyonel olaydır. Birden fazla büyük sürüm yükseltmesinden geçmiş biri olarak birkaç gözlem:

**Hazırlık, asıl işin kendisidir.** Yanlış giden bir CUCM yükseltmesi neredeyse her zaman atlanan bir hazırlık adımına kadar izlenebilir. Her yükseltmeden önce:
- Tüm uç noktaların hedef CUCM sürümü için desteklenen yazılımı çalıştırdığını doğrulayın
- Tüm özel yapılandırmaları belgeleyin (CTI yol noktaları, arama grupları, çeviri desenleri)
- Mümkünse lab ortamında yükseltme sonrasında çevirme planı işlevini test edin
- Yedeklemenin tamamlandığını ve geri yüklenebilir olduğunu doğrulayın

**Önce Publisher, sonra subscriber'lar.** Yükseltme sırası önemlidir. CUCM Publisher önce yükseltilir. Subscriber'lar Publisher tam olarak yükseltilip sağlıklı olana kadar eski sürümde kalır, ardından her Subscriber sırayla yükseltilir.

**Yükseltme sonrası doğrulama.** Her subscriber yükseltmesinden sonra: tüm telefonların yeniden kayıt olduğunu doğrulayın, gelen ve giden PSTN aramalarını test edin, siteler arası aramaları test edin, sesli posta entegrasyonunu doğrulayın. Tüm çağrı yolları doğrulanana kadar başarı ilan etmeyin.

**Geçiş yolu:** Eski CUCM sürümlerindeki pek çok Cisco müşterisi, Cisco'nun şirket içi CUCM'nin bulut yedeği olan Webex Calling'e yönlendiriliyor. Geçiş, telefon numaralarını taşımayı, çevirme planı mantığını bulutta yeniden oluşturmayı ve Webex App'i softphone istemcisi olarak kullanıma almayı içeriyor.

---

## Bugünkü Durum

Kurumsal iş birliği pazarı, on yıl önce olası görünmeyecek birkaç şeyde birleşti:

**Önce yazılım:** Çoğu kullanıcı için birincil arayüz fiziksel bir telefon değil, Webex App, Teams, Zoom gibi bir yazılım istemcisi.

**Bulut tabanlı operasyonlar:** Yeni deployment'lar büyük ölçüde bulut tabanlı. Şirket içi CUCM buna sahip organizasyonlar tarafından sürdürülüyor, ancak yeni deployment'lar artık nadiren UCaaS alternatiflerinden önce bunu tercih ediyor.

**Temel olarak birlikte çalışabilirlik:** İş birliği sisteminizin diğer organizasyonların sistemleriyle — platform ne olursa olsun — iletişim kurabilmesi beklentisi artık standart.

**Toplantı odası sistemleri erişilebilir teknoloji olarak:** Toplantı odası sistemleri, herhangi bir önceki noktadan daha basit şekilde kullanıma alınır, kullanılır ve bakımı yapılır hale geldi.

Özelleşmiş bir Cisco iş birliği mühendisinin yapılandırıp bakımını yaptığı altyapının yerini büyük ölçüde genel amaçlı bir IT yöneticisinin işletebileceği yönetilen bulut hizmetleri aldı. Bu eski altyapının eleştirisi değil — zamanında gerçekten gelişmiş bir mühendisliğin ürünüydü. Altta yatan karmaşıklığın ne kadar soyutlandığının gözlemidir.

CUCM, Expressway, TelePresence ve tam Cisco iş birliği yığını üzerine kariyer inşa eden mühendisler için: o bilgi değersiz hale gelmedi. Mimari düşünme — çevirme planlarının nasıl çalıştığı, çağrı yönlendirme mantığının nasıl yapılandırıldığı, QoS'un ses kalitesi için ne anlama geldiği, codec seçiminin neden önemli olduğu — doğrudan şirket içi altyapının yerini alan bulut platformlarını anlamaya aktarılır. Uygulama detayları değişti. Prensipler değişmedi.

---

## Temel Çıkarımlar

- **IP telefonun orijinal iş gerekçesi**, MPLS/VPN aracılığıyla siteler arası aramalarda maliyet azaltmaktı — bu tek başına pek çok kurumsal PBX'ten IP telefona geçişi haklı kıldı.
- **Donanım video konferans** kalite sundu ancak muazzam altyapı maliyeti ve operasyonel karmaşıklıkla — yaygın benimsemenin önündeki darboğaz.
- **Bulut iş birliği**, internet kalitesi yeterince iyileştiğinde ve şirket içi altyapıyla ekonomik karşılaştırma kesin olarak değiştiğinde uygulanabilir hale geldi.
- **Webex**, bir toplantı aracından CUCM, VCS ve Unity Connection'ın tek bir bulut hizmetinde yerini alan tam bir UCaaS platformuna dönüştü.
- **Teams**, saf teknik üstünlük değil dağıtım avantajıyla pazarı dönüştürdü — Microsoft 365 çalıştıran organizasyonlarda zaten deploy edilmişti.
- **Toplantı odası donanımı**, herhangi bir organizasyonun ölçekte kullanıma alabileceği 3.000 dolarlık erişilebilir barlara dönüşerek 30.000 dolar+ özel sistemlerden çıktı.
- **CUCM yükseltmeleri**, hâlâ şirket içinde bulunan organizasyonlar için önemli operasyonel olaylar olmaya devam ediyor — hazırlık ve sıra, yükseltmenin kendisinden daha önemli.
- **Platformlar arası birlikte çalışabilirlik** artık beklenen, istisnai değil — Webex odaları Teams toplantılarına katılıyor, Teams kullanıcıları Webex toplantılarına katılıyor.

---

## İlgili Yazılar

- 🔐 [Zero Trust Zihniyeti: Güvenliği Bir Mimari Olarak Mühendislemek](/tr/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — Bulut iş birliği ortamları için güvenlik mimarisi
- 🏗️ [IT Altyapısı Ürünler Koleksiyonu Değildir](/tr/architecture/it-infrastructure-not-a-collection-of-products/) — İş birliği platformları için de geçerli sistem düşüncesi
- 📊 [İzleme Doğru Yapıldığında](/tr/architecture/monitoring-not-just-seeing/) — İş birliği altyapısını proaktif olarak izleme
- 🔧 [SecureCRT ve SuperPutty](/tr/technology/securecrt-superputty-network-engineer-guide/) — İş birliğinin üzerinde çalıştığı şirket içi altyapıyı yönetmek için araçlar