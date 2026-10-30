---
title: "Cisco DNA Center / Catalyst Center: Ne Zaman Mantıklıdır, Ne Zaman Değildir?"
description: "Cisco DNA Center hakkında dürüst bir değerlendirme — kurulum maliyetleri, karmaşıklığı, ISE entegrasyonu ve daha küçük ölçekli organizasyonların ne zaman başka çözümlere yönelmesi gerektiği."
date: 2026-10-31T00:30:00+01:00
draft: false

cover:
  image: "/img/postimages/cisco-dna-center-architecture-cover.webp"
  alt: "Cisco DNA Center Catalyst Center Mimari Rehberi"
  relative: false

tags: ["Cisco", "DNA Center", "Catalyst Center", "SD-Access", "ISE", "Ağ Otomasyonu", "Kampüs Ağı", "Kurumsal Mimari"]
categories: ["Mimari"]
keywords:
  - Cisco DNA Center mimarisi
  - Catalyst Center kurumsal
  - DNA Center ve geleneksel kampüs karşılaştırması
  - Cisco SD-Access tasarımı
  - DNA Center ISE entegrasyonu
  - DNA Center maliyet gerekçelendirmesi
  - Cisco fabric ağı
  - DNA Center cluster gereksinimleri
  - kampüs ağı otomasyonu
  - Cisco DNA Center avantajları dezavantajları

showToc: true
TocOpen: false
aliases:
  - "/tr/architecture/cisco-dna-center-catalyst-center-architecture-guide/"
---

# Cisco DNA Center / Catalyst Center: Ne Zaman Mantıklıdır, Ne Zaman Değildir?

Cisco DNA Center — yeni adıyla Catalyst Center — pazarlama söylemleri ile saha gerçeklerinin ciddi şekilde ayrıştığı platformlardan biridir. Pazarlama tarafındaki hikaye oldukça etkileyicidir: tüm kampüs ağınız için tek bir yönetim ekranı (single pane of glass), otomatik yapılandırma dağıtımı (provisioning), yapay zeka destekli analitik ve niyet tabanlı ağ yönetimi (intent-based networking). Saha gerçekliği ise bu seviyeye ulaşmanın ciddi bir yatırım, büyük bir ön hazırlık ve birçok şirketin küçümsediği bir kurumsal olgunluk gerektirdiğidir.

DNA Center'ı, Cisco tarafından başarı hikayesi olarak yayımlanan ve Türkiye'deki ilk büyük ölçekli DNA Center ve Stealthwatch entegrasyonlarından biri olan bir üretim tesisi projesi de dahil olmak üzere büyük kurumsal ortamlarda canlıya aldım. Bu deneyim, platformun gerçekten sundukları ve nerede zorluk çıkardığı konusunda bana net bir bakış açısı kazandırdı.

Bu makale dürüst bir mimari değerlendirmedir — ne bir ürün pazarlaması ne de kestirip atan bir reddediş. Soru, DNA Center'ın iyi ya da kötü olup olmadığı değildir. Soru, sizin özel durumunuz için doğru araç olup olmadığıdır.

---

## DNA Center / Catalyst Center Gerçekte Nedir?

DNA Center bir ağ yönetimi, otomasyon ve güvence (assurance) platformudur. Özel fiziksel appliance'lar üzerinde çalışır ve tüm kampüs ağı üzerinde merkezi kontrol sağlar:

- **Design (Tasarım):** Ağ hiyerarşisini (lokasyonlar, binalar, katlar) tanımlama ve ayarları ölçeklenebilir şekilde uygulama
- **Policy (Politika):** Kimin neye erişebileceğini tanımlama; politikaları kablolu ve kablosuz ağlarda tutarlı bir şekilde uygulama
- **Provision (Dağıtım):** Şablonlar (templates) aracılığıyla switch, AP ve router'lara yapılandırmaları otomatik olarak yükleme
- **Assurance (Güvence):** Yönetilen tüm cihazlardan telemetri verisi toplama, sağlık gösterge panelleri (health dashboards), kullanıcı deneyimi metrikleri ve anomali tespiti sunma
- **Automation (Otomasyon):** İş akışları, ITSM entegrasyonu ve otomatik sorun giderme (automated remediation)

Temelde yatan kampüs fabric teknolojisi **SD-Access**'tir — Cisco'nun veri düzleminde (data plane) VXLAN, kontrol düzleminde (control plane) LISP ve politika motoru olarak ISE kullandığı yazılım tanımlı kampüs mimarisi. DNA Center, bu fabric yapısını orkestre eden yönetim platformudur.

---

## Maliyet Gerçeği: Bu Kurumsal Bir Yatırımdır

İlk olarak en önemli konuyu ele alalım, çünkü diğer tüm detayların durumunuzla ilgili olup olmadığını belirleyen şey budur.

### Donanım Appliance Maliyeti

DNA Center, Cisco'nun özel DN2-HW-APL appliance'ı üzerinde çalışır. Tek nodlu bir kurulum (daha küçük ortamlar için uygundur) bir appliance gerektirir. **Canlı bir üretim (production) ortamı için gereken cluster ise üç appliance gerektirir** — biri yönetim, biri politika, biri veri toplama için — ve bir HA (High Availability) cluster olarak yapılandırılır.

Üç nodlu bir cluster'ın donanım maliyeti oldukça yüksektir. Henüz yazılım lisanslamasına geçmeden bile, küçük ve orta ölçekli projeleri doğrudan eleyen ciddi bir sermaye harcamasından (CAPEX) bahsediyoruz. Bu, "olsa iyi olurdu" diye kurulacak bir platform değildir — ortamınızın ölçeği bunu haklı çıkardığı için kurulur.

### Yazılım Lisanslaması

DNA Center lisanslaması abonelik tabanlıdır; cihaz başına ve yıllık olarak hesaplanır. Lisans seviyeleri (Essentials, Advantage, Premier) hangi özelliklerin kullanılabileceğini belirler. Gelişmiş assurance, AI analitiği ve SD-Access yeteneklerini içeren tam özellik seti daha üst seviye lisanslar gerektirir.

500 switch'e sahip bir organizasyon için yıllık lisans maliyeti, donanım yatırımının üzerine ciddi bir sürekli operasyonel gider (OPEX) ekler.

### Dürüst Bir Ölçek Eşiği

Saha deneyimlerime dayanarak: DNA Center, **yüksek sayıda switch'iniz** olduğunda — tipik olarak birden fazla lokasyonda yüzlerce veya daha fazla yönetilen cihaz aralığında — ekonomik ve operasyonel olarak anlamlı olmaya başlar. Bu eşiğin altında, maliyet-fayda dengesini gerekçelendirmek zordur.

Küçük ve orta ölçekli organizasyonlar için DNA Center için gereken yatırım — donanım, lisanslama, kurulum süresi, eğitim — başka alanlara yönlendirilse daha iyidir. İyi izleme (monitoring) araçlarına sahip, doğru tasarlanmış geleneksel bir kampüs ağı, bu maliyetin çok küçük bir kısmıyla benzer bir günlük operasyonel değer sunar.

> **Herhangi bir DNA Center değerlendirmesinden önceki temel soru:** Kaç lokasyonda, kaç mühendisle kaç ağ cihazı yönetiyorsunuz? Yanıtınız "birkaç yüz cihazdan az, bir veya iki lokasyon, tek bir ağ ekibi" ise, önce alternatiflere bakın.

---

## Kurulum Gerçeği: Karmaşık, Zaman Alıcı ve Hata Kabul Etmeyen

Organizasyonları şaşırtan ikinci büyük faktör, ilk kurulum ve yapılandırmanın ne kadar detaylı ve meşakkatli olduğudur.

### İlk Kurulum Hızlı Değildir

Bir DNA Center cluster'ını ayağa kaldırmak, mevcut ağınızla entegre etmek ve çalışır duruma getirmek hafta sonu bitecek bir iş değil, haftalar süren bir projedir. Bu süreç şunları içerir:

- Fiziksel appliance kurulumu ve cluster oluşturma
- Ağ hiyerarşisinin tanımlanması (lokasyon, bina, kat yapısı)
- Cihaz keşfi (discovery) ve onboarding
- Cihaz yapılandırmaları için şablon (template) tasarımı
- ISE entegrasyonu (politika özellikleri kullanılacaksa)
- AP'ler yönetilecekse kablosuz ağ entegrasyonu
- Assurance veri toplama yapılandırması

Bu adımların her birinin bağımlılıkları vardır. Şablon tasarımı, ağınızın nasıl görünmesi gerektiğini anlamayı ve bunu tekrarlanabilir bir yapılandırma olarak kodlamayı gerektirir — bu da DNA Center'dan önce yapılmış olması gereken ağ standartlaştırma çalışmasının, kurulumun bir parçası olarak tamamlanması gerektiği anlamına gelir.

### Ön Gereksinim Problemi

DNA Center, gerçek dünyadaki bir çok ortamda bulunmayan bir ağ standartlaşması seviyesi varsayar. Switch'lerinizde tutarsız yapılandırmalar, standart olmayan isimlendirme kuralları veya yıllar içinde organik olarak gelişmiş eski yapılar varsa, DNA Center kurulumu platformun cihazları güvenilir bir şekilde yönetebilmesinden önce tüm bunları düzeltmenizi zorunlu kılar.

Bu aslında gizli bir faydadır — DNA Center sizi iyi pratikleri uygulamaya zorlar. Ancak ön hazırlık çalışmaları beklenenden daha fazla olduğu için kurulum projesinin genellikle planlanandan uzun sürmesi anlamına gelir.

### "Kur ve Unut" Bir Seçenek Değildir

DNA Center bir kez kurup kendi haline bırakacağınız bir platform değildir. Sürekli ilgi gerektirir:

- Appliance'ın kendisi için yazılım güncellemeleri (düzenli bakım pencereleri)
- Ağ standartları değiştiğinde şablon güncellemeleri
- Erişim gereksinimleri geliştikçe ISE politika güncellemeleri
- Yönettiği ağın yanı sıra platformun kendi sağlığının izlenmesi

DNA Center'ı işletmek için özel kaynak ayırmadan kuran organizasyonlar, platform gerçek ağ durumuyla senkronizasyonunu kaybettikçe sunduğu değerin zamanla azaldığını görürler.

---

## Stabilizasyondan Sonra Elde Ettikleriniz: Gerçek Değer

DNA Center kurulduktan, yapılandırıldıktan ve stabilize edildikten sonra — ki bu zaman ve çaba gerektirir — operasyonel tablo önemli ölçüde değişir. Platform, harcanan maliyetin karşılığını tam olarak burada verir.

### Kablolu ve Kablosuz Ağlar İçin Tek Ekranda Yönetim

En hızlı görülen operasyonel fayda: her şeyin tek bir yerde görünür olmasıdır. Kablolu switch'ler, kablosuz AP'ler, router'lar, WAN bağlantıları — hepsi tek bir arayüzden yönetilir ve izlenir. Ağı ayrı araçlarla yönetilen kopuk alanlar olarak değil, bir bütün olarak görürsünüz.

Bu kulağa basit gelebilir; ancak kablolu ağ ekibi ile kablosuz ağ ekibinin tarihsel olarak farklı araçlar kullandığı ve farklı görünürlüğe sahip olduğu büyük ortamlarda, bu birleşik görünüm sorunların teşhis edilme şeklini gerçekten değiştirir. Daha önce birden fazla kaynaktan gelen verileri ilişkilendirmeyi gerektiren bir istemci (client) bağlantı sorunu, tek bir iş akışında tüm hat boyunca — istemciden AP'ye, switch'e ve firewall'a kadar — izlenebilir.

### Yerleşik Loglama ve Geçmişe Dönük Analiz

DNA Center, yönetilen cihazlardan telemetri verilerini toplar ve saklar. Port (interface) istatistikleri, istemci bağlantı geçmişi, topoloji değişiklikleri, yapılandırma değişiklikleri — hepsi loglanır ve sorgulanabilir durumdadır.

Pratik değeri şudur: Geçen Salı gece saat 02:00'de bir sorun yaşandığında, geriye dönüp ağın o andaki durumunu tam olarak görebilirsiniz. Port kullanımı, istemci sayıları, hata oranları, yapılandırma durumu. Bu geçmişe dönük görünürlük, geleneksel ağ yönetiminde genellikle eksik olan bir şeydir — cihazlar logları kendi içlerinde tutar, ancak olay gerçekleştikten sonra yüzlerce cihaz arasında bu logları ilişkilendirmek manuel ve yavaştır.

Bu aynı zamanda ağ cihazı verileri için **mutlaka ayrı bir üçüncü taraf loglama platformuna ihtiyacınız olmadığı** anlamına gelir. DNA Center, yönetilen cihazlar için bu işlevi üstlenerek sistem mimarinizdeki araç sayısını azaltır.

### Otomasyon: Operasyonel Çarpan Etkisi

Şablonlar ve iş akışları kurulduktan sonra, yeni cihazların veya lokasyonların yapılandırılması (provisioning) ciddi şekilde hızlanır. Tamamen DNA Center tarafından yönetilen mevcut bir kampüse yeni bir bina eklemek şunları içerir:
- Yeni switch'lerin fiziksel olarak bağlanması
- Cihaz keşfinin (discovery) çalıştırılması
- Mevcut lokasyon şablonunun uygulanması
- Bitti

Daha önce her bir cihazın bir terminal oturumundan manuel olarak yapılandırılmasını gerektiren ve büyük bir lokasyon için günlerce sürebilecek işler, şablon çalışması halihazırda yapılmış olduğunda birkaç saate veya daha kısa süreye iner.

Aynı durum toplu değişiklikler için de geçerlidir: 200 switch üzerinde bir VLAN'ı güncellemek, ağ genelinde yeni bir QoS politikası uygulamak, tüm yönetilen cihazlarda kimlik bilgilerini (credentials) yenilemek. Daha önce betik (scripting) yazmayı veya manuel tekrarları gerektiren operasyonlar, şablon odaklı iş akışlarına dönüşür.

### Fabric Mimarisi: Kampüsünüzde VXLAN Kullanımı

SD-Access fabric yapısını kuran organizasyonlar için DNA Center, temelde çok farklı bir kampüs mimarisinin üzerindeki yönetim katmanıdır. Geleneksel bir kampüs ağında, VLAN'lar switch'ler arasında 802.1Q trunking kullanılarak taşınır — yani Layer 2 alanı fiziksel olarak ağ topolojisiyle sınırlandırılmıştır.

SD-Access, yönlendirilen bir underlay (routed underlay) üzerinde sanal ağlar oluşturmak için VXLAN kullanır. Sonuç: herhangi bir uç nokta (endpoint), fiziksel konumundan bağımsız olarak herhangi bir sanal ağda yer alabilir, VLAN'ların fiziksel ağ boyunca taşınmasına gerek kalmaz ve makro segmentasyon firewall yerine fabric kenarında (fabric edge) uygulanır.

Farklı departmanlar, IoT cihazları, misafir ağları gibi hepsi izolasyon gerektiren karmaşık segmentasyon ihtiyaçlarına sahip büyük kampüsler için fabric modeli, taşınan VLAN'ları ve VLAN'lar arası yönlendirmeyi manuel olarak yönetmeye kıyasla mimariyi ciddi şekilde sadeleştirir.

---

## ISE Entegrasyonu: Platformun Olağanüstü Hale Geldiği Yer

Tek başına kurulan bir DNA Center güçlüyse, Cisco ISE ile entegre edilmiş bir DNA Center bambaşka bir yetenek seviyesidir.

ISE kimlik ve politika motorunu sağlar. DNA Center ise ağ yönetimi ve uygulama (enforcement) platformunu sağlar. Birlikte:

- Bir kullanıcı kampüs ağına bağlanır (kablolu veya kablosuz)
- ISE, 802.1X aracılığıyla kullanıcıyı Active Directory üzerinden doğrular
- ISE; kimlik, cihaz türü ve durum bilgisinden (posture) yola çıkarak güvenlik grubunu (SGT) belirler
- DNA Center, bu güvenlik grubuyla ilişkili politikayı tüm fabric genelinde uygular
- Politika; A binası, B binası, kablolu veya kablosuz olması fark etmeksizin, bağlandığı her yerde kullanıcıyı takip eder

Bu, kimlik tabanlı ağ yönetiminin (identity-based networking) en eksiksiz halidir. Erişim politikası, kullanıcının hangi fiziksel portta veya IP alt ağında (subnet) olduğuna değil, kim olduğuna ve hangi cihazı kullandığına bağlıdır. Bir finans çalışanı; masasında, toplantı odasında veya uzak bir ofiste kabloyla bağlansa bile finans seviyesinde erişim alır.

Operasyonel sonucu şudur: **ağ segmentasyonu fiziksel bir problem olmaktan çıkar** (bu port hangi VLAN'da?) ve bir politika problemine dönüşür (bu kullanıcının neye erişmesine izin verilmeli?). Bu sadeleşme, karmaşık erişim gereksinimleri olan ortamlarda gerçek bir değer yaratır.

Bunu sözünü ettiğim üretim ortamında uyguladığımda; DNA Center, ISE, Umbrella, Stealthwatch ve Firepower kombinasyonu tamamen entegre bir güvenlik ve ağ fabric yapısı oluşturdu. ISE'de yapılan politika değişiklikleri DNA Center üzerinden tüm ağa otomatik olarak yayıldı. Stealthwatch'tan gelen görünürlük, otomatik yanıtları tetikleyen anomali tespitini besledi. Yüzlerce cihazın bulunduğu bir kampüste bu düzeyde bir entegrasyonu manuel olarak sürdürmek imkansız olurdu.

---

## Bulut Entegrasyonu: AWS ve Ötesi

DNA Center, kapsamını kurum içi (on-premise) kampüsün ötesine genişleten bulut entegrasyon yetenekleri ekledi.

**AWS entegrasyonu**, DNA Center'ın ağ politikalarını ve görünürlüğünü bulut iş yüklerine genişletmesine olanak tanır. Transit Gateway entegrasyonu, VPC bağlantı yönetimi, kurum içi ve AWS ortamları arasında tutarlı politika uygulanması platformun yöneldiği hedefler arasındadır.

Cisco'nun daha geniş vizyonu — ve platformun ilerlediği yön — kurum içi kampüs, şube ağları ve bulut ortamlarında tek bir yönetim düzleminden tutarlı politika ve görünürlük sağlamaktır. Azure ve diğer bulut sağlayıcıları da yol haritasında (roadmap) yer almaktadır.

Bu yetenekler halen gelişmektedir. Kurum içi kampüs yönetimi olgundur; çoklu bulut (multi-cloud) entegrasyonu ise daha yenidir ve gelişmeye devam etmektedir. Ancak ciddi bir bulut varlığına sahip olan ve aynı zamanda Cisco kampüs altyapısı çalıştıran organizasyonlar için bu yakınlaşma takip edilmeye değerdir — Cisco'nun yatırım yaptığı yön burasıdır.

---

## DNA Center mi, Geleneksel Kampüs mü: Mimari Karar

Geleneksel kampüs yönetimi ne zaman DNA Center'dan daha mantıklıdır?

**Geleneksel kampüs (yönetilen switch'ler, ayrı araçlar) şu durumlarda uygundur:**
- Cihaz sayısı, otomasyonun net bir ROI (yatırım getirisi) sunduğu ölçek eşiğinin altındaysa
- Organizasyon, DNA Center'ı düzgün bir şekilde kuracak ve işletecek mühendislik kaynaklarına sahip değilse
- Bütçe kısıtlamaları donanım ve lisanslama yatırımını haklı çıkarmayı zorlaştırıyorsa
- Ağ stabil ve standartlaştırılmışsa — değişiklik sıklığı düşükse
- Cisco'nun baskın olmadığı çoklu üreticili (multi-vendor) bir ortam varsa

**DNA Center şu durumlarda mantıklıdır:**
- Yüksek cihaz sayısı (yüzlerce switch, birden fazla lokasyon)
- Yeni lokasyonların veya cihazların sık sık yapılandırılması (provisioning) gerekiyorsa
- Fabric mimarisinden faydalanan karmaşık segmentasyon gereksinimleri varsa
- ISE halihazırda kurulmuşsa veya planlanıyorsa — entegrasyon değeri katlar
- Mühendislik ekibinin platformu düzgün şekilde işletecek kapasitesi varsa
- Organizasyon uzun vadede Cisco ekosistemine bağlı kalmayı hedefliyorsa

En kötü senaryo, ölçeğin haklı çıkarmadığı bir ortama DNA Center kurup, orantılı bir değer sunmayan karmaşık bir platformun operasyonel yüküyle boğuşmaktır. İkinci en kötü senaryo ise DNA Center'dan faydalanacak kadar büyük bir ağa sahip olup, bunu düzgün işletecek mühendislik kaynaklarını ayırmamaktır.

---

## Sahadan Pratik Gözlemler

Dokümantasyonda görünmeyen ancak pratikte önem taşıyan birkaç husus:

**Ağ standartlaştırması ile başlayın.** DNA Center'ı kurmadan önce mevcut ağ yapılandırmanızı denetleyin. Tutarsız hostname kuralları, standart dışı VLAN yapıları ve eski yapılandırmalar cihaz onboarding sürecini ciddi şekilde yavaşlatır. DNA Center, temiz ve standartlaştırılmış ağları ödüllendirir.

**Asıl iş şablon tasarımıdır.** İyi yapılandırma şablonları oluşturmak için yapılan zaman yatırımı yıllarca karşılığını verir. Aceleye getirilmiş şablonlar, otomasyon değerini zayıflatan manuel müdahalelere ve istisnalara yol açar. Başlangıçta şablonları düzgün bir şekilde tasarlamaya zaman ayırın.

**Canlı sistemler için cluster isteğe bağlı değildir.** Tek nodlu bir kurulum canlı (production) ortamlar için uygun değildir — ağ yönetim platformunuz için tek bir arıza noktası (single point of failure) oluşturur. Başlangıçtan itibaren üç nodlu cluster için bütçe ayırın.

**ISE entegrasyonu ISE uzmanlığı gerektirir.** DNA Center'ı ISE ile entegre etmek platformun tüm potansiyelini ortaya çıkarır, ancak ISE'nin kendisi karmaşıktır. Entegrasyon projesi, ekipte çalışan bir ISE bilgisi olduğunu varsayar. ISE, DNA Center ile birlikte ilk kez canlıya alınacaksa, birleşik öğrenme eğrisini hesaba katın.

**Güncelleme planlaması önemlidir.** DNA Center güncellemeleri (upgrades) bakım pencereleri ve dikkatli bir planlama gerektirir. Appliance'ı eski bir yazılım sürümünde çalıştırmak, güvenlik borcu ve özellik eksikliği biriktirir. Düzenli güncelleme döngülerini operasyonel takviminize dahil edin.

---

## Önemli Çıkarımlar

- **DNA Center pahalıdır** — canlı sistem yüksek erişilebilirliği (HA) için gereken üç nodlu cluster, yazılım lisanslamasından önce bile ciddi bir donanım yatırımıdır. Bu maliyet yalnızca ölçek büyüdüğünde anlamlı hale gelir.
- **İlk kurulum karmaşık ve zaman alıcıdır** — günler değil haftalar sürecek bir süreç ve ağ standartlaştırması için ön çalışma planlayın.
- **Stabilize edildikten sonra operasyonel değeri gerçektir** — birleşik görünürlük, yerleşik loglama, otomasyon ve fabric yönetimi, büyük ağların işletilme şeklini gerçekten değiştirir.
- **Platform, ISE entegrasyonu ile olağanüstü hale gelir** — bağlantı noktasından bağımsız olarak kullanıcıları takip eden ve tüm kampüste uygulanan kimlik tabanlı politika.
- **Yerleşik loglama, üçüncü taraf araç bağımlılığını azaltır** — DNA Center ağ telemetrisini saklayarak ağ cihazı verileri için ayrı bir loglama altyapısı ihtiyacını azaltır.
- **Bulut entegrasyonu büyüyor** — AWS bağlantısı mevcuttur ve daha geniş çoklu bulut desteği geliştirilmektedir.
- **Küçük ve orta ölçekli organizasyonlar için: başka çözümlere bakın.** Düşük cihaz sayılarında yatırım, elde edilecek faydayla orantısızdır. İyi izleme araçlarına sahip geleneksel kampüs yönetimi doğru cevaptır.
- **Ürün gelişmeye devam ediyor** — Cisco platforma aktif olarak yatırım yapıyor. İlk canlıya alındığında sınırlı olan yetenekler her sürümle birlikte daha olgun hale geliyor.

---

## İlgili Makaleler

- 🔐 [Sahadan 802.1X Kimlik Tabanlı Mimari](/tr/technology/identity-based-microsegmentation-8021x/) — DNA Center + ISE kombinasyonunu güçlü kılan kimlik altyapısı
- 🔐 [Zero Trust Yaklaşımı: Güvenliği Ürün Değil Mimari Olarak Tasarlamak](/en/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — SD-Access politika modelinin arkasındaki mimari felsefe
- 🏗️ [Switch, Firewall, AP — Doğru Ürünleri Seçmek Neden Yetmez?](/tr/architecture/core-network-is-not-a-product-list/) — Kampüs mimarisi bağlamı
- 📊 [Doğru İzleme (Monitoring)](/tr/architecture/monitoring-not-just-seeing/) — DNA Center assurance yeteneğinin genel izleme stratejisine uyumu
- 🌐 [Kurumsal WiFi Controller Mimarisi](/en/technology/enterprise-wifi-controller-architecture-cisco-aruba/) — DNA Center ile kablosuz ağ entegrasyonu
