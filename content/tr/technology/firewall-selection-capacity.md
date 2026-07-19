---
title: "Firewall Seçimi ve Kapasite Planlaması: Datasheet'lerin Söylemediği Şeyler"
description: "Kurumsal firewall seçimi — gerçek throughput, SSL inspection etkisi, Fortinet, Palo Alto, Cisco ve Check Point karşılaştırması."
date: 2026-04-06
draft: false

cover:
  image: "/img/postimages/firewall-selection-capacity-cover.webp"
  alt: "Kurumsal Firewall Seçimi ve Kapasite Planlaması"
  relative: false

tags: ["Firewall", "NGFW", "Fortinet", "Palo Alto", "Cisco Firepower", "Check Point", "Ağ Güvenliği", "Kapasite Planlaması", "SSL Inspection"]
categories: ["Teknoloji"]
keywords:
  - kurumsal firewall seçim rehberi
  - firewall kapasite planlaması
  - Fortinet vs Palo Alto vs Cisco vs Check Point
  - NGFW SSL inspection throughput
  - firewall throughput gerçek dünya
  - kurumsal firewall karşılaştırması
  - Palo Alto App-ID mimarisi
  - Fortinet FortiGate yüksek throughput
  - Cisco Firepower IPS
  - Check Point firewall yönetimi

showToc: true
TocOpen: true
---

# Firewall Seçimi ve Kapasite Planlaması: Datasheet'lerin Söylemediği Şeyler

Firewall seçim görüşmeleri genellikle iki şekilde ilerler. Ya karar marka tanıdıklığına dayanır — "her zaman X satıcısını kullandık" — ya da üretimde bu sayıların gerçekte ne anlama geldiğini anlamadan datasheet throughput rakamlarına dayanır. Her iki yaklaşım da ya kullanmayacağınız kapasite için fazla ödemeye ya da gerçekte çalıştıracağınız trafik için yetersiz boyutlandırmaya yol açar.

Bankacılık ve üretim ortamlarında yüzlerce Fortinet firewall deploy ettikten ve Palo Alto ile Cisco'yu üretim altyapısında yoğun biçimde kullandıktan sonra, seçim sürecinin yalnızca öneriyi değil sonucu da üstlendiğinizde gerçekte nasıl göründüğünü paylaşmak istiyorum.

Firewall yerleştirme kararlarının arkasındaki mimari bağlam için bakınız: [Switch, Firewall, AP — Doğru Ürünleri Seçmek Neden Yeterli Değil](/tr/architecture/core-network-is-not-a-product-list/)

---

## Herkesi Yanıltan Sayı: Firewall Throughput'u

Her firewall datasheet'i bir throughput rakamıyla başlar. 10 Gbps. 40 Gbps. 100 Gbps. Bu rakamlar gerçektir — ölçüldükleri spesifik koşullarda.

Bu koşullar, sizin üretim ortamınız değildir.

Datasheet throughput'u tipik olarak şunlarla ölçülür:
- Büyük paket boyutları (1518 bayt) — gerçek trafik çok daha küçük paketler içerir
- Güvenlik özellikleri etkin değil — IPS yok, uygulama kontrolü yok, SSL inspection yok
- Sentetik test trafiği — gerçek bir ağın karışık, patlamalı, düzensiz trafiği değil

Üretimde firewall kapasitesini tüketen şeyler:

**PPS (Saniyedeki Paket Sayısı):** Küçük paketler büyük paketlerden daha maliyetlidir. 64 baytlık paketlerden oluşan 1 Gbps'lik trafiği taşıyan bir firewall, 1500 baytlık paketlerden oluşan 1 Gbps'den yaklaşık 20× daha fazla paket işler. Yüksek işlem hızına sahip ortamlar (bankacılık, ticaret, veritabanı replikasyonu), bant genişliği sınırlarından çok önce PPS sınırlarına ulaşır.

**Eş Zamanlı Oturumlar:** İzlenen her bağlantı, durum tablosunda bellek işgal eder. 2 milyon eş zamanlı oturum kapasiteli bir firewall "2 milyon kullanıcı" anlamına gelmez — tek bir kullanıcı aynı anda düzinelerce açık oturuma sahip olabilir. Yüksek eşzamanlılık ortamları (firewall arkasındaki web sunucuları, veritabanı kümeleri, mikro-servis mimarileri) oturum tablolarını bant genişliğinden daha hızlı tüketir.

**Yeni Oturum Hızı:** Firewall'un saniyede kaç yeni bağlantı kurabileceği. SYN flood koşullarında veya yoğun trafik dönemlerinde, yeni oturum hızı bağlayıcı kısıtlama haline gelir.

**SSL/TLS Inspection:** Kapasite planlamasının en çok yanlış yapıldığı yer burasıdır. SSL inspection etkinleştirildiğinde — HTTPS trafiğini şifre çözme, inceleme, yeniden şifreleme — çoğu platformda throughput önemli ölçüde düşer. Etkinin derecesi satıcıya ve modele göre değişir.

---

## SSL Inspection Gerçeği

Bugün kurumsal trafiğin büyük çoğunluğu HTTPS'tir. Firewall'unuz SSL'i inspect etmiyorsa, trafiğinizin büyük bölümünü inspect etmiyorsunuz demektir. Ancak SSL inspection'ı etkinleştirmenin doğrudan ve önemli bir performans maliyeti vardır.

10 Gbps throughput ile pazarlanan bir firewall, platforma bağlı olarak tam SSL inspection etkinken 2–4 Gbps sunabilir. Bu bir hata veya satıcı eksikliği değildir — SSL şifre çözme hesaplamsal olarak maliyetlidir ve donanım SSL hızlandırması (üst düzey modellerde mevcut), pratikte giriş seviyesi ile orta segment platformları birbirinden ayıran şeydir.

**Önemli olan hesaplama:**

Bir firewall boyutlandırırken soru "ne kadar bant genişliğim var?" değil, "bu bant genişliğinin ne kadarı SSL inspect edilecek?" olmalıdır. Çoğu organizasyon için:
- İnternete giden trafik: neredeyse %100 HTTPS → tümü SSL inspect edilir
- Dahili segmentasyon trafiği: şifreli ve şifresiz uygulama trafiğinin karışımı
- Sunucudan sunucuya trafik: uyumluluk nedeniyle giderek artan oranda TLS

2 Gbps'lik internet bant genişliğiniz varsa ve tamamını inspect etmeyi planlıyorsanız, firewall'u 2 Gbps ham throughput için değil, 2 Gbps SSL inspection throughput'u için boyutlandırın. Bunlar çoğunlukla çok farklı sayılardır.

---

## Çok Firewall Mimarisi: Tek Beden Herkese Uymaz

Birçok üretim ortamında, tüm rolleri üstlenen tek bir firewall, bilinçli bir tasarım seçimi değil, bir tasarım uzlaşısıdır. Farklı trafik türlerinin farklı gereksinimleri vardır:

```
İnternet Edge Firewall:
  → Yüksek SSL inspection throughput'u (trafiğin çoğu HTTPS)
  → VPN sonlandırma kapasitesi
  → İnternetten gelen tehditler için IPS
  → Orta oturum sayısı

Dahili Segmentasyon Firewall'u (Doğu-Batı):
  → Yüksek PPS (dahili trafik genellikle küçük paketlerdir)
  → Çok yüksek eş zamanlı oturum sayısı
  → Daha düşük SSL inspection gereksinimleri (dahili trafik genellikle şifresiz)
  → Yüksek yeni oturum hızı

Veri Merkezi / Sunucu Firewall'u:
  → Aşırı oturum sayıları (sunucular çok sayıda eş zamanlı bağlantıya sahiptir)
  → Düşük gecikme (uygulama performansına duyarlı)
  → Toplu veri transferleri için yüksek throughput
  → Sunucu tarafı exploit'ler için ayarlanmış IPS
```

Üç rol için de aynı firewall modelini kullanmak, en azından birinde uzlaşı anlamına gelir. SSL inspection için optimize edilmiş internet edge firewall'u çoğunlukla doğu-batı segmentasyonu için yanlış seçimdir. Yüksek oturum sayılı DC firewall'u çoğunlukla bir şube ofisi için gereğinden fazla mühendislenmiştir.

Bu teorik değildir — oturum sayısı sınırına ulaşıldığı için internet edge firewall'un belirtilen throughput'unun %30'unda doyuma ulaştığı, DC firewall'unda ise bol throughput rezervi olmasına rağmen PPS sınırları nedeniyle paket düştüğü ağlar gördüm.

---

## Satıcı Saha Notları

Aşağıdakiler doğrudan üretim deneyimine dayanmaktadır. Bunlar kıyaslama karşılaştırmaları değil, operasyonel gözlemlerdir. Satıcı yetenekleri yazılım sürümleri ve yeni donanım nesilleriyle gelişir — her aktif proje için mevcut spesifikasyonları doğrulayın.

### Fortinet FortiGate

Fortinet, üretim firewall deneyimimin büyük bölümünün yoğunlaştığı yerdir — küçük şube deployment'larından bankacılık genel merkezlerine ve büyük üretim ortamlarına kadar.

**FortiGate'in gerçekten üstün olduğu yerler:**

Orta düzeyde güvenlik inspection gereksinimleri olan yüksek throughput ortamları. Fortinet'in özel NP (Ağ İşlemcisi) ve CP (İçerik İşlemcisi) ASIC'leri belirli işlevleri donanıma boşaltır — paket işleme, IPsec VPN ve bazı inspection görevleri genel amaçlı CPU'lar yerine özel silikon üzerinde çalışır. Yüksek bant genişliğinde bu donanım hızlandırması anlamlı bir fark yaratır.

Büyük trafik hacimlerini taşıması gereken ortamlar için — sunucudan sunucuya, büyük dosya transferleri, yüksek bant genişlikli şube bağlantısı — FortiGate, eşdeğer fiyat noktalarında yazılım tabanlı mimarilerin karşılaştıramayacağı throughput sunar.

Fortinet Security Fabric, FortiGate'i FortiSwitch, FortiAP, FortiAnalyzer ve FortiManager ile birlikte çalıştıran organizasyonlar için gerçek bir operasyonel avantajdır. Politika, loglama ve yönetim, çok satıcılı ortamların gerektirdiği entegrasyon çalışmasını azaltacak biçimde birleştirilmiştir.

**FortiGate'in sınırlılıkları:**

Ölçekte derin inspection. IPS, uygulama kontrolü, SSL inspection ve antivirüs yüksek trafikli bağlantılarda aynı anda etkinleştirildiğinde, throughput başlık rakamlarına kıyasla önemli ölçüde düşebilir. Fortinet, bunu yansıtan "tehdit koruması" throughput rakamları yayınlar — ancak bu rakamlar hâlâ spesifik trafik karışımınız ve tam özellik aktivasyonuyla göreceğinizden genellikle iyimserdir.

**Donanım nesil güncellemesi (2024–2025):** Fortinet'in yeni cihaz serisi, SSL inspection kapasitesini önemli ölçüde iyileştirdi. 2025'te Keysight tarafından doğrulanan FortiGate 700G serisi, önceki nesillerin eşdeğer orta segment modellerine göre anlamlı bir iyileştirme olan 14 Gbps'e kadar SSL derin inspection throughput'u elde ediyor. Boyutlandırırken, genel tahminler değil, değerlendirdiğiniz spesifik model ve nesle ait datasheet rakamlarını her zaman kullanın.

**Pratik rehberlik:** Tam SSL inspection deployment'ları için FortiGate boyutlandırırken, üretim trafiği için çalışma tahminim olarak datasheet'teki SSL inspection throughput rakamının %20-30'unu kullanıyorum. Bu muhafazakâr görünebilir, ancak trafik karışımını, eş zamanlı bağlantıları ve loglama yükünü hesaba katar. Math bu rakamda işe yarıyorsa, uygun rezerviniz var demektir.

---

### Palo Alto Networks

Palo Alto'nun mimarisi geleneksel firewall'lardan temelden farklıdır ve bunu anlamak hem güçlü yönlerini takdir etmek hem de kısıtlamalarını planlamak için gereklidir.

**App-ID mimarisi:**

Palo Alto, trafiği ne yapacağına karar vermeden önce uygulamaya göre tanımlar. Her oturum, yalnızca hangi portu kullandığını değil, neyi temsil ettiğini belirlemek için analiz edilir. Port 80, port 8080 veya özel bir port üzerindeki HTTP, hepsinde çalışan spesifik uygulama olarak tanımlanır.

Bu, güvenlik açısından mimari olarak güçlüdür: politika "X alt ağından TCP 443'e izin ver" yerine "satış ekibinden Salesforce'a izin ver" üzerine kuruludur. Bilinmeyen uygulamalar — bilinen hiçbir uygulama imzasıyla eşleşmeyen trafik — varsayılan olarak potansiyel olarak şüpheli kabul edilir. Tanınmayan trafiğin geçmesini istiyorsanız açıkça izin vermeniz gerekir.

**Bunun yarattığı güvenlik avantajı:**

Tehdit modelinin tam uygulama görünürlüğü gerektirdiği ortamlarda — finansal hizmetler, düzenlenmiş sektörler, katı uyumluluk gereksinimleri olan ortamlar — Palo Alto'nun yaklaşımı gerçek güvenlik derinliği yaratır. Politika modeli, her trafik türü için açık kararlar almayı zorlar. Hiçbir şey incelenmeden geçemez. Olgun güvenlik ekiplerine sahip güvenlik odaklı organizasyonlar için bu önemli bir avantajdır.

**Operasyonel takas:**

Palo Alto'yu güvenlik odaklı ortamlarda güçlü kılan aynı mimari, diğerlerinde sürtünme yaratır. Bilinmeyen veya olağan dışı uygulamalar araştırma ve açık politika kararları gerektirir. Özel güvenlik ekipleri olmayan veya çeşitli, gelişen uygulama setlerine sahip ortamlarda, uygulama tabanlı bir politika modelini sürdürmenin operasyonel yükü önemli olabilir.

Küçük ve orta ölçekli organizasyonlar için veya birincil gereksinimin maksimum güvenlik derinliği yerine makul güvenlikli bağlantı olduğu ortamlarda, bu takas değmeyebilir. Operasyonel model, her organizasyonun sahip olmadığı bir güvenlik olgunluk düzeyini varsayar.

**Panorama:**

Panorama aracılığıyla Palo Alto firewall'larının merkezi yönetimi, bireysel cihazları yönetmekten önemli ölçüde daha yeteneklidir. Çok firewall ortamları için Panorama, Palo Alto'yu ölçekte işletmek için fiilen gereklidir. Panorama olmadan yönetim yükü alternatiflere oranla orantısızdır.

**SASE liderliği (2025 güncellemesi):** Palo Alto'nun bulut güvenlik platformu (Prisma SASE), en güçlü büyüme alanlarından biri haline geldi — 2025'e kadar üç ardışık yıl Gartner SASE Lideri seçildi, yıllık %35 büyümeyle 1,3 milyar dolar ARR. Organizasyonunuz yalnızca bir perimeter firewall değil, daha geniş bir güvenlik platformunu değerlendiriyorsa bu bilgi ilgilidir.

---

### Cisco Firepower (Şimdi Cisco Secure Firewall)

Cisco'nun NGFW hikayesinin anlaşılmaya değer bir geçmişi var. Orijinal ASA (Adaptive Security Appliance) güçlü bir stateful firewall'du — güvenilir, yaygın biçimde deploy edilmiş, ancak yeni nesil yetenekler açısından sınırlı. Cisco'nun yanıtı, IPS teknolojisi (Snort tabanlı) gerçekten güçlü olan ve olan Sourcefire'ı satın almak ve Firepower platformunu ASA mimarisinin üzerine inşa etmek oldu.

**Firepower'ın güçlü olduğu yerler:**

IPS yeteneği gerçektir. Sourcefire'ın tehdit istihbaratı ve tespiti, şimdi Cisco Talos (dünyanın en büyük tehdit istihbaratı organizasyonlarından biri), Firepower'ın IPS'ini genel olarak saygın bir tespit kalitesiyle güçlendirir. IPS'in birincil güvenlik gereksinimi olduğu ortamlar için Cisco ciddi bir yetenek sunar.

Cisco'nun daha geniş ekosistemiyle entegrasyon — ISE, Umbrella, Stealthwatch (şimdi Secure Network Analytics), SecureX — giderek daha tutarlı hale gelmiş ve son yıllarda önemli ölçüde iyileşmiştir.

**Yönetim zorluğu:**

Cisco Firepower, tarihsel olarak yönetim karmaşıklığı nedeniyle eleştirilmiştir. Firepower Management Center (FMC) olmadan Firepower çalıştırmak, görünürlük ve politika yönetiminde önemli sınırlamaları kabul etmek anlamına gelir. FMC'nin kendisi, alternatiflere göre daha dik bir öğrenme eğrisine sahiptir.

Platform önemli ölçüde olgunlaşmış ve Cisco yönetim deneyimini iyileştirmeye yoğun yatırım yapmıştır. 2024'te Cisco, Cisco Defense Orchestrator'ı **Security Cloud Control** olarak yeniden adlandırdı — FMC, ASA ve diğer Cisco güvenlik ürünlerini tek bir arayüzde birleştiren, yapay zeka destekli bir bulut yönetim platformu. Artık politika kuralı oluşturma için AI Asistanı, proaktif öneriler için AIOps içgörüleri ve şirket içi altyapı yükünü azaltan bulut tabanlı FMC içeriyor. Bu, eski yalnızca FMC modeline göre anlamlı bir iyileştirmedir. Daha basit firewall platformlarından gelen ekipler hâlâ bir uyum dönemi yaşayacak, ancak fark birkaç yıl öncesine kıyasla daralmıştır.

**Mimari bağlam:**

Cisco, ISE'nin kimlik, Catalyst'ın switching ve DNA Center / Catalyst Center'ın merkezi yönetim sağladığı Cisco ekosistemi yatırımına zaten derinden dahil olmuş ortamlarda en güçlüdür. Bu ortamlarda Firepower tutarlı biçimde uyum sağlar. Çok satıcılı ortamlarda entegrasyon hikayesi daha fazla çalışma gerektirir.

---

### Check Point

Check Point, 1990'larda firewall teknolojisini ana akım haline getiren orijinal kurumsal firewall satıcılarından biridir. Mimarileri bu mirası yansıtır: olgun, güvenlik odaklı ve yöneticilere önemli kontrol sağlayan ancak karşılık gelen uzmanlık gerektiren bir işletim sistemi (Linux tabanlı Gaia) etrafında inşa edilmiş.

**Check Point'in güçlü olduğu yerler:**

Güvenlik politikası derinliği ve inspection kalitesi. Check Point'in politika modeli ayrıntılıdır ve inspection yetenekleri olgunlaşmıştır. Güvenlik politikası karmaşıklığının yüksek olduğu ortamlarda — çok sayıda kural, çok sayıda istisna, ayrıntılı loglama gereksinimleri — Check Point'in yönetim altyapısı (SmartConsole, yönetim sunucusu, log sunucusu ayrımı) ölçeği iyi karşılar.

Platformu bilen güvenlik operasyon ekiplerine sahip organizasyonlar için Check Point yetenekli ve saygın bir seçimdir.

**Operasyonel gerçeklik:**

Check Point'in yönetim modeli diğer satıcılardan farklıdır. Yönetim, zorunluluktan ayrıdır — Security Management Server (SMS) olan yönetim sunucusu, zorunluluk gateway'lerinden ayrıdır. Bu ayrımla, politika kurulum süreciyle ve temel Gaia OS ile çalışmak gerçek uzmanlık gerektirir.

Bir ağ mühendisinin perspektifinden Check Point, operasyonel olarak en şeffaf platform değildir. Linux yönetimine aşinalık önemli ölçüde yardımcı olur. Nesne modeli ve kural tabanı yapısı hakkında sağlam bir anlayış olmadan politika yönetimi, zamanla biriken karmaşıklığa yol açar.

---

## HA Mimarisi: Aktif-Yedek ve Aktif-Aktif

Kurumsal firewall deployment'ları yüksek erişilebilirlik gerektirir. İki modelin farklı özellikleri vardır:

**Aktif-Yedek:**
- Bir firewall tüm trafiği işler; yedek izler ve arızada devralır
- Oturum durumu yedeğe senkronize edilir — failover kurulu bağlantılara şeffaftır
- Sorun giderme daha basit — herhangi bir zamanda tüm trafik tek cihazdan
- Normal işlemde donanım kapasitesinin %50'sini boşa harcar
- Çoğu kurumsal edge deployment için standart seçim

**Aktif-Aktif:**
- Her iki firewall da aynı anda trafiği yönetir, tipik olarak farklı trafik akışları veya bölgeler için
- Yapılandırmak ve sorun gidermek daha karmaşık — asimetrik routing'den kaçınılmalı
- Her iki cihazı da kullanır, ancak durum senkronizasyonunu karmaşıklaştırır
- Tek cihazın karşılayamayacağı çok yüksek throughput gereksinimleri için daha uygun
- Dikkatli trafik mühendisliği gerektirir — asimetrik akışlar (FW-1 üzerinden istek, FW-2 üzerinden yanıt) oturum düşüşlerine neden olur

Pratikte Aktif-Yedek, kurumsal deployment'ların büyük çoğunluğu için doğru seçimdir. HA yükü hesaba katıldığında tek bir cihazın sağlayabileceğinden gerçekten daha fazla throughput'a ihtiyaç duymadıkça, Aktif-Aktif'in throughput faydası operasyonel karmaşıklığı haklı kılmaz.

---

## Politika Hijyeni: Yavaş Yavaş Biriken Sorun

Firewall kapasitesi yalnızca bir donanım sorusu değildir. Kural tabanı karmaşıklığı arttıkça firewall performansı düşer — özellikle kural tabanları düzenli temizlik yapılmadan büyüdüğünde.

Trafiğin çoğunun ilk 50 kuralda eşleştiği 5.000 kurallı bir kural tabanı, trafiğin yüzlerce kural genelinde dağıldığı 5.000 kurallı bir tabanla çok farklı performans gösterir. Her paket, eşleşene veya örtük redde ulaşana kadar kural tabanını yukarıdan aşağıya doğru geçer.

**Kural hijyeni pratikte ne anlama gelir:**

- Hiçbir zaman eşleşmeyen kurallar (gölge kurallar, eski kurallar) üç ayda bir tespit edilmeli ve kaldırılmalıdır
- Yüksek trafikli kurallar kural tabanının üst kısmına yerleştirilmelidir
- Aşırı geniş kurallar (loglama devre dışı bırakılmış herhangi/herhangi izinler) belgelenmeli ve gözden geçirilmelidir
- Platform desteklediğinde uygulamaya özgü kurallar port tabanlı kuralların yerini almalıdır

FortiManager, Panorama ve FMC'nin hepsinde kural kullanım istatistikleri ve gölge kural tespiti bulunur. Bu araçları kullanmak, periyodik temizlik alıştırması değil, sorumlu firewall operasyonunun bir parçasıdır.

---

## Kapasite Planlaması: Pratik Çerçeve

Bir firewall boyutlandırırken şu metrikleri sırayla işleyin:

**1. Temel trafik karakterizasyonu**
- Mevcut zirve bant genişliği nedir (ortalama değil)?
- SSL/HTTPS yüzdesi nedir?
- Zirvede eş zamanlı oturum sayısı nedir?
- Zirvede yeni oturum hızı nedir?

**2. Büyüme projeksiyonu**
- 3 yıllık yaşam döngüsü için beklenen zirvenin %40–50 üzerinde rezerv ekleyin
- Eklenecek yeni uygulama ve hizmetleri hesaba katın

**3. Özellik etkisi**
- Hangi güvenlik özellikleri etkinleştirilecek? (IPS, SSL inspection, App-ID, AV)
- Ham throughput değil, satıcının "tehdit koruması" throughput rakamlarını kullanın
- SSL inspection için özellikle: tahmini HTTPS yüzdenizi kullanarak satıcı boyutlandırma araçlarıyla doğrulayın

**4. HA yükü**
- Aktif-Yedek: her birimi trafiğin %100'ü için boyutlandırın (yedek tam yükü karşılayabilmelidir)
- Yedek kapasitesini kullanmayı planlamayın — failover için hazır olmalıdır

**5. Yönetim ve loglama**
- Yüksek loglama oranları firewall'un kendi CPU'sunu tüketir
- Harici log yönetimi (FortiAnalyzer, Panorama, FMC) ölçekte isteğe bağlı değildir

Basit bir boyutlandırma örneği:
```
Ortam:
  Zirve bant genişliği: 2 Gbps
  SSL yüzdesi: %80 (1,6 Gbps HTTPS)
  IPS + App-ID + SSL inspection: hepsi etkin
  3 yıllık büyüme rezervi: %50

Gerekli SSL inspection throughput'u:
  1,6 Gbps × 1,5 (büyüme) = 2,4 Gbps

≥ 2,4 Gbps SSL inspection throughput'u için derecelendirilen model seçin
(2,4 Gbps ham throughput için değil)
```

---

## Temel Çıkarımlar

- **Datasheet throughput'u üretim throughput'u değildir.** SSL inspection, IPS ve uygulama kontrolü efektif throughput'u önemli ölçüde azaltır. Ham rakamlar değil, tehdit koruması veya SSL inspection rakamlarına göre boyutlandırın.
- **SSL inspection kapasitesi**, çoğu internet edge deployment için bağlayıcı kısıtlamadır. Trafiğin büyük çoğunluğu HTTPS'tir ve inspect etmek maliyetlidir.
- **Fortinet**, donanım hızlandırmasının önemli olduğu yüksek throughput ortamlarında üstündür. Ölçekte tam derin inspection, dikkatli model seçimi gerektirir — tüm özellikler etkinleştirildiğinde throughput önemli ölçüde düşer.
- **Palo Alto**, en derin uygulama görünürlüğü ve en katı politika modelini sunar. Mimari güvenlik-olgun organizasyonlar için güçlüdür; özel güvenlik ekipleri olmayanlar için operasyonel yük ekler. Çok cihazlı yönetim için Panorama fiilen gereklidir.
- **Cisco Firepower**, güçlü IPS (Talos istihbaratı) ve Cisco ekosistemi entegrasyonu sunar. Yönetim karmaşıklığı gerçektir — FMC, platformun değerini gerçekleştirmek için gereklidir.
- **Check Point**, derin politika kontrolüyle olgun ve güvenlik odaklıdır. Etkili biçimde işletmek için Linux/Gaia OS aşinalığı ve disiplinli kural tabanı yönetimi gerektirir.
- **Çok firewall mimarisi** — edge, dahili segmentasyon ve DC için farklı firewall'lar — çoğunlukla her şey için tek platform yerine doğru yanıttır.
- **Kural hijyeni** yalnızca ev düzeni değil, bir performans ve güvenlik sorunudur. İhmal edilen kural tabanları her ikisini de bozar.

---

## İlgili Yazılar

- 🏗️ [Switch, Firewall, AP — Doğru Ürünleri Seçmek Neden Yeterli Değil](/tr/architecture/core-network-is-not-a-product-list/) — Firewall yerleştirme için mimari bağlam
- 🔐 [Zero Trust Zihniyeti: Güvenliği Bir Mimari Olarak Mühendislemek](/tr/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — Firewall tasarımının arkasındaki politika felsefesi
- 🛡️ [DDoS Koruma Stratejileri](/tr/technology/ddos-koruma-stratejileri-isp-scrubbing-on-premise-bulut/) — Firewall'un yukarısında ne var
- 🛡️ [F5 WAF Deep Dive](/tr/technology/f5-waf-asm-advanced-waf-uygulama-guvenligi/) — Firewall politikasını tamamlayan Katman 7 koruması
- 📊 [İzleme Doğru Yapıldığında](/tr/architecture/monitoring-not-just-seeing/) — Firewall davranışını görünür kılmak