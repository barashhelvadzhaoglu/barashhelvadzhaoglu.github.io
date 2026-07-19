---
title: "Cisco ISE: Mimari, Lisanslama ve Ne Zaman Kullanılır"
description: "Cisco ISE mimari rehberi — deployment modelleri, node rolleri, lisans katmanları, pxGrid entegrasyonları ve ISE'nin ne zaman doğru seçim olduğu."
date: 2026-04-20
draft: false

cover:
  image: "/img/postimages/cisco-ise-architecture-cover.webp"
  alt: "Cisco ISE Mimari ve Lisanslama Rehberi"
  relative: false

tags: ["Cisco ISE", "NAC", "802.1X", "TACACS", "Ağ Güvenliği", "Zero Trust", "Kimlik", "pxGrid"]
categories: ["Mimari"]
keywords:
  - Cisco ISE mimarisi
  - ISE lisans katmanları
  - ISE vs NPS vs ClearPass
  - Cisco ISE deployment modelleri
  - ISE pxGrid entegrasyonu
  - ISE TACACS cihaz yönetimi
  - ISE uç nokta lisanslama
  - ISE DNA Center entegrasyonu
  - Cisco ISE Base Plus Apex
  - kurumsal ağ erişim kontrolü

showToc: true
TocOpen: false
---

# Cisco ISE: Mimari, Lisanslama ve Ne Zaman Kullanılır

Cisco Identity Services Engine (ISE), kurumsal ağ erişim kontrolünün politika beynidir. Ağa bağlanmaya çalışan her cihaz için şu soruyu yanıtlayan platformdur: *sen kimsin, neysin, sağlıklı mısın ve ne yapabilirsin?*

[802.1X saha rehberini](/tr/technology/identity-based-microsegmentation-8021x/) okuduysanız ISE'yi zaten iş başında gördünüz: dinamik VLAN ataması döndüren RADIUS sunucusu, cihazları tanımlayan NAC platformu, posture uyumunu zorunlu kılan politika motoru. Bu yazı protokol detaylarından bir adım geri çekilerek ISE'ye mimari ve yatırım kararı perspektifinden bakıyor — nasıl yapılandırıldığı, nasıl lisanslandığı ve ne zaman doğru araç olduğu.

---

## ISE Ne Yapar — Tek Paragrafta

ISE merkezi bir politika platformudur. Ağa bağlanan cihazlar ve kullanıcılar — kablolu, kablosuz veya VPN üzerinden — ISE üzerinden kimlik doğrular. ISE kimliklerini Active Directory'ye göre kontrol eder, cihaz türünü ve uyumluluk durumunu değerlendirir ve ağ cihazına bir erişim kararı döndürür: tam erişim ver, karantina VLAN'ına al, düzeltme portalına yönlendir veya tamamen reddet. Bu karar VLAN ataması, indirilebilir ACL'ler ve kullanıcıyı ağ boyunca izleyen Security Group Tag'leri (SGT) içerebilir.

Tek platform, daha önce birden fazla ayrı araç gerektiren şeyleri üstlenir: RADIUS sunucusu, NAC cihazı, misafir portalı, cihaz profiler, posture motoru.

---

## Deployment Mimarisi

### Node Rolleri

ISE tek parça bir uygulama değildir. İşlevlerini belirgin node rollerine ayırır:

**PAN — Policy Administration Node:** Yönetim arayüzü. Tüm konfigürasyon burada yapılır. Dağıtık deployment'ta bir aktif PAN ve bir yedek bulunur.

**PSN — Policy Service Node:** Çalışma zamanı uygulama motoru. Ağ cihazlarının konuştuğu yer burasıdır — RADIUS istekleri, TACACS istekleri, misafir portalı yönlendirmeleri, posture kontrolleri. Büyük ortamlarda birden fazla PSN kimlik doğrulama yükünü dağıtır.

**MnT — Monitoring and Troubleshooting Node:** PSN'lerden log toplar ve operasyon panosunu sağlar — kimlik doğrulama raporları, başarısız girişimler, aktif oturumlar, alarmlar. Loglama yükünün kimlik doğrulama performansını etkilememesi için politika node'larından ayrıdır.

**pxGrid Controller:** Entegrasyon veri yolu. Aşağıda daha fazla detay var.

### Deployment Modelleri

**Standalone (tek node):** Tüm roller tek bir VM veya cihazda. Lab, PoC veya çok küçük deployment'lar için uygundur. HA yok. Node çökerse kimlik doğrulama durur. ISE'ye bağımlı ağ erişimine sahip üretim ortamları için uygun değildir.

**Küçük dağıtık (2 node):** Bir node PAN+MnT, bir node PSN. Temel yedeklilik. Orta ölçekli ve ılımlı kimlik doğrulama yüküne sahip ortamlar için uygundur.

**HA ile tam dağıtık:** Her rol için özel node'lar, aktif/yedek PAN, yük dağılımı ve coğrafi yedeklilik için birden fazla PSN. Büyük kurumsal ve düzenlenmiş ortamların ihtiyacı budur. Aynı zamanda önemli ölçüde daha fazla altyapı gerektirir — düzgün yedekli bir deployment için minimum 4–6 VM planlayın.

Pratik sonuç: ISE "boşta duran bir VM'e kur" türünden bir proje değildir. Üretim kalitesinde dağıtık deployment, özel altyapı, doğru boyutlandırma ve süregelen operasyonel dikkat gerektirir.

---

## Lisanslama: Katman Yapısı

ISE lisanslaması yıllar içinde evrildi. Mevcut model, uç nokta başına yıllık abonelik olarak satılan üç katman kullanıyor:

### Essentials (eski adıyla Base)

Giriş seviyesi katman. Temel 802.1X kullanım senaryosunu kapsar:
- RADIUS kimlik doğrulama (802.1X kablolu ve kablosuz)
- Temel misafir erişimi
- MAB (MAC Authentication Bypass)
- Temel VLAN ataması

Port kimlik doğrulaması ve temel misafir erişimine ihtiyaç duyan organizasyonlar için yeterlidir. NPS bunların büyük bölümünü ücretsiz yapabilir — Essentials'ın NPS'e göre değeri öncelikle yönetim arayüzü, ölçeklenebilirlik ve Cisco ekosistemi entegrasyonudur.

### Advantage (eski adıyla Plus)

ISE'yi NPS'ten anlamlı biçimde daha güçlü kılan özellikleri ekler:
- **Cihaz profiling** — DHCP, CDP, LLDP, HTTP imzalarından cihaz türünü tanımlama
- **Misafir yaşam döngüsü yönetimi** — sponsor portalları, kendi kendine kayıt, süreli erişim
- **BYOD onboarding** — kişisel cihazlar için sertifika sağlama
- **TrustSec / Security Group Tags (SGT)** — VLAN atamasının ötesinde politika uygulaması

Advantage, kullanım senaryosu temel port kimlik doğrulamasının ötesine geçtiğinde kurumsal deployment'ların çoğunun tercih ettiği katmandır.

### Premier (eski adıyla Apex)

Posture değerlendirmesi ve gelişmiş tehdit yanıtı ekler:
- **Posture** — erişim vermeden önce cihaz sağlığını kontrol etme (AV durumu, işletim sistemi yama seviyesi, disk şifreleme, belirli registry değerleri)
- **Threat-centric NAC** — bir cihaz tehlikeye girdiğinde erişim politikasını otomatik olarak değiştirmek için tehdit istihbaratı beslemeleriyle entegrasyon
- **Passive Identity** — her port'ta 802.1X gerektirmeksizin AD olay loglarından kimlik bilgisi toplama

Premier, uyumluluk pozisyonunun yasal gereklilik olduğu veya otomatik tehdit yanıtına ihtiyaç duyulan yüksek güvenlik ortamları için uygundur.

### Cihaz Yönetimi (TACACS+) — Ayrı Lisans

Bu yaygın bir karışıklık kaynağıdır: **Ağ cihazı yönetimi için TACACS+, yukarıdaki uç nokta erişim lisanslarından ayrı olarak lisanslanır.**

Uç nokta lisansları (Essentials/Advantage/Premier) ağa bağlanan kullanıcıları ve cihazları kapsar. Cihaz Yönetimi ise ağ mühendislerinin switch'lere, router'lara ve firewall'lara giriş yapmasını kapsar — ISE'yi AAA sunucusu olarak kullanarak TACACS+ aracılığıyla kimlik doğrulama, kullanıcı veya grup başına komut yetkilendirmesi.

ISE'nin hem uç nokta erişim kontrolünü hem de ağ cihazı yönetici kimlik doğrulamasını yönetmesini istiyorsanız her iki lisans türüne ihtiyacınız vardır. Pek çok organizasyon ISE'yi öncelikle uç nokta erişimi için kullanır ve cihaz yönetimi için ayrı bir TACACS+ çözümü kullanmaya devam eder.

---

## pxGrid: Entegrasyon Platformu

pxGrid (Platform Exchange Grid), ISE'nin entegrasyon çerçevesidir — dış platformların ISE verilerine abone olmasına ve ISE'ye geri olay yayınlamasına olanak tanır.

Pratikte şu senaryoları mümkün kılar:

**Firewall entegrasyonu:** ISE bir kullanıcının kimliğini doğruladığında ve ona bir Security Group Tag atadığında, firewall (Palo Alto, Cisco Firepower) bu eşlemeyi pxGrid aracılığıyla alabilir. Firewall politikası daha sonra IP adresleri yerine SGT'lere göre yazılabilir — kullanıcılar hareket ettikçe değişen IP tabanlı ACL'leri sürdürmek yerine "Finance SGT'nin Finance sunucularına erişimine izin ver."

**SIEM entegrasyonu:** Güvenlik platformları (Splunk, IBM QRadar) ISE oturum verilerine abone olur — kim kimlik doğruladı, nereden, hangi cihazla, ne zaman. Bu, ham ağ loglarının taşımadığı kimlik bağlamıyla güvenlik olayı korelasyonunu zenginleştirir.

**Tehdit yanıtı:** Bir SIEM veya EDR platformu tehlikeye girmiş bir cihaz tespit eder. pxGrid aracılığıyla ISE'ye bir tehdit olayı yayınlar. ISE, cihazın erişim politikasını otomatik olarak değiştirir — karantina VLAN'ı, düzeltme portalına yönlendirme — insan müdahalesi olmadan.

pxGrid, ISE'yi bir ağ erişim aracından tüm altyapıda bağlamı paylaşan bir güvenlik platformuna dönüştürür. Bu entegrasyon değeri, olgun güvenlik mimarilerinde ISE'nin gerekçesinin önemli bir parçasıdır.

---

## ISE + DNA Center: Entegre Kampüs

ISE, DNA Center (Catalyst Center) ile birlikte çalıştığında entegrasyon yerli ve derindir. DNA Center, SD-Access fabric deployment'ları için ISE'yi politika motoru olarak kullanır:

- DNA Center ağ hiyerarşisini ve fabric altyapısını tanımlar
- ISE kimin neye erişebileceğini tanımlar (Security Group politikaları)
- Bir kullanıcı kimlik doğruladığında ISE SGT'sini atar
- DNA Center SGT tabanlı politikayı fabric genelinde otomatik olarak yayar

Sonuç: ISE'deki bir politika değişikliği — "Finans kullanıcıları artık yeni raporlama sunucusuna erişebilir" — bireysel switch konfigürasyonlarına dokunmadan tüm kampüs fabric'ine otomatik olarak yansır. Politika bir kez tanımlanır, her yerde uygulanır.

Bu entegrasyon, DNA Center zaten çalışan ortamlarda ISE için en güçlü argümanlardan biridir. Ayrı ayrı her iki platform da yeteneklidir. Birlikte, kimlik bilincine sahip ağ fabric'ini tek başlarına sağlayamadıkları şekilde sunarlar.

---

## ISE vs. NPS vs. ClearPass: Ne Zaman Hangisi

Çoğu organizasyonun ISE'ye bağlanmadan önce alması gereken karar budur.

**Windows NPS (Network Policy Server)** Windows Server ile ücretsiz gelir. RADIUS kimlik doğrulama, temel VLAN ataması ve 802.1X'i yönetir. Active Directory'ye karşı temel port kimlik doğrulamasına ihtiyaç duyan organizasyonlar için NPS çalışır. Sınırlılıkları: cihaz profiling yok, misafir portalı yok, posture yok, SGT desteği yok, sınırlı ölçeklenebilirlik ve birden fazla RADIUS sunucusu genelinde merkezi yönetim yok. NPS, basit gereksinimleri ve sınırlı bütçesi olan küçük ortamlar için doğru yanıttır.

**Aruba ClearPass**, ISE'nin birincil rakibidir. Eşdeğer özellikler sunar — 802.1X, profiling, misafir portalı, posture, TACACS. ClearPass satıcıdan bağımsızdır (herhangi bir ağ satıcısının switch ve AP'leriyle çalışır), güçlü misafir ve BYOD iş akışları nedeniyle güçlü bir üne sahiptir ve Aruba kablosuz ortamlarında veya Cisco ekosistemi bağımlılığının endişe konusu olduğu çok satıcılı ağlarda tercih edilir. Lisanslama da uç nokta başına aboneliktir.

**Cisco ISE** şu durumlarda doğru seçimdir:
- Ortam ağırlıklı olarak Cisco'dur (switch'ler, AP'ler, DNA Center, Firepower) — yerli entegrasyonlar en fazla değeri sunar
- Kampüs genelinde SGT tabanlı politika uygulaması bir gereksinimdir
- Güvenlik platformlarıyla pxGrid entegrasyonları planlanmaktadır
- Ölçek, dağıtık ve HA yetenekli bir platform gerektiriyor
- Posture uygulaması bir uyumluluk gereksinimidir

Dürüst özet:

| | NPS | ClearPass | Cisco ISE |
|---|---|---|---|
| Maliyet | Ücretsiz | Uç nokta başına abonelik | Uç nokta başına abonelik |
| 802.1X / RADIUS | ✅ | ✅ | ✅ |
| Cihaz profiling | ❌ | ✅ | ✅ |
| Misafir portalı | Temel | ✅ | ✅ |
| Posture | ❌ | ✅ | ✅ (Premier) |
| SGT / TrustSec | ❌ | ❌ | ✅ |
| DNA Center entegrasyonu | ❌ | ❌ | ✅ (yerli) |
| pxGrid ekosistemi | ❌ | Sınırlı | ✅ |
| Satıcı bağımsızlığı | ✅ | ✅ | Cisco optimize |
| Operasyonel karmaşıklık | Düşük | Orta | Yüksek |

---

## Saha Notları: Boyutlandırma ve Operasyonel Gerçeklik

Üretim deployment'larından birkaç gözlem:

**PSN boyutlandırması çoğu ekibin planladığından daha önemlidir.** Kimlik doğrulama istekleri vardiya değişimlerinde, sabah giriş yoğunluklarında ve ağ olaylarında ani artış gösterir. Ortalama yük için doğru boyutlandırılmış PSN'ler, zirve anında yetersiz kalabilir. Zirve için boyutlandırın, yeterli boşluk bırakın.

**MnT node'u çoğunlukla küçük boyutlandırılır.** Yüzlerce ağ cihazından gelen loglama önemli veri hacmi üretir. Küçük boyutlandırılmış bir MnT node'u, sorun giderme görünürlüğü için dar boğaz haline gelir — tam ihtiyaç duyduğunuz anda. Yeterli disk ve bellek sağlayın.

**ISE yükseltmeleri önemli bakım olaylarıdır.** CUCM gibi, ISE yükseltmeleri de belirli bir sırayı izler — önce PAN, sonra MnT, sonra PSN'ler — ve bakım pencereleri gerektirir. Eski bir ISE sürümü çalıştırmak güvenlik borcu biriktirir. Operasyon takvimine düzenli yükseltme döngüleri ekleyin.

**İzleme moduyla başlayın.** ISE'yi mevcut bir ağda kullanıma alırken, izleme modunda başlayın — ISE kimlik doğrulama isteklerini işler ve ne olacağını loglar, ancak politikayı uygulamaz. Bu, zorunlu kılınmadan önce kimlik doğrulamada başarısız olacak cihazları ortaya koyar. Düşük etkili moda, ardından tam uygulamaya kademeli olarak geçin.

**Uç nokta sayısı insanları şaşırtır.** ISE, eş zamanlı aktif uç noktaların sayısını lisanslar. Her biri dizüstü bilgisayar ve telefon taşıyan 2.000 çalışana sahip bir kampüste bu minimum 4.000 uç nokta demektir — artı yazıcılar, IP telefonlar, kameralar ve IoT cihazları. Lisansı boyutlandırmadan önce doğru bir cihaz sayımı alın.

---

## Temel Çıkarımlar

- **ISE bir platform, ürün değildir** — birden fazla nokta çözümünün (RADIUS sunucusu, NAC, misafir portalı, posture motoru) yerini tek entegre platformla alır.
- **Lisanslama uç nokta başına, katmanlıdır** — temel 802.1X için Essentials, profiling ve misafir için Advantage, posture için Premier. Cihaz Yönetimi (TACACS) ayrıdır.
- **Üretim için dağıtık HA deployment zorunludur** — özel altyapı ve doğru node boyutlandırması için planlayın.
- **pxGrid entegrasyonları ISE'nin değerini çarpar** — kimliğe dayalı firewall politikası, oturum bağlamıyla zenginleştirilmiş SIEM, otomatik tehdit yanıtı.
- **ISE + DNA Center, eksiksiz kampüs fabric hikayesidir** — SGT tabanlı politika bir kez tanımlanır, her yerde otomatik olarak uygulanır.
- **NPS, basit ortamlar için doğru yanıttır** — küçük deployment'ları aşırı mühendislik etmeyin.
- **ClearPass, çok satıcılı ortamlar için doğru yanıttır** veya Cisco ekosistemi bağlılığının sınırlı olduğu durumlarda.
- **İzleme moduyla başlayın** — kimlik doğrulamanın mevcut ortamınıza ne yapacağını doğruladıktan sonra uygulayın.

---

## İlgili Yazılar

- 🔐 [802.1X Projeleri: Kimlik Tabanlı Mimariyi Sahada Kullanıma Almak](/tr/technology/identity-based-microsegmentation-8021x/) — ISE'nin etkinleştirdiği saha deployment rehberi
- 🏛️ [Cisco DNA Center / Catalyst Center: Ne Zaman Mantıklıdır](/tr/architecture/cisco-dna-center-catalyst-center-architecture-guide/) — ISE'nin entegre olduğu kampüs yönetim platformu
- 🔐 [Zero Trust Zihniyeti: Güvenliği Bir Mimari Olarak Mühendislemek](/tr/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — Kimlik tabanlı erişim kontrolünün arkasındaki felsefe
- 🛡️ [F5 WAF Deep Dive](/tr/technology/f5-waf-asm-advanced-waf-application-security/) — ISE'nin L2/L3 uygulamasının yanında tamamlayıcı L7 güvenliği