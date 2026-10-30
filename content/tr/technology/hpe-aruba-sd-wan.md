---
title: "HPE Aruba SD-WAN: EdgeConnect ve WAN Optimization Mirası"
seoTitle: "HPE Aruba SD-WAN İncelemesi | EdgeConnect, Silver Peak Mimarisi ve SASE"
description: "HPE Aruba'nın SD-WAN platformuna derinlemesine bir bakış: Silver Peak satın alması, EdgeConnect mimarisi, application-defined WAN ve Aruba'nın kurumsal pazardaki ayrışma noktaları."
date: 2026-10-30T06:41:11+01:00
keywords:
  - HPE Aruba SD-WAN
  - Aruba EdgeConnect
  - Silver Peak SD-WAN
  - Aruba SD-WAN SASE
  - application-defined WAN
  - Aruba Orchestrator
  - HPE Aruba SSE
  - EdgeConnect Ultra
tags:
  - SD-WAN
  - Aruba
  - HPE
  - Ağ Teknolojileri
draft: false
---

# HPE Aruba SD-WAN: EdgeConnect ve WAN Optimization Mirası

HPE Aruba'nın SD-WAN hikayesi bir ağ deviyle değil, bir WAN optimization uzmanıyla başlıyor. Silver Peak Systems, pazarı yeni bir mimariye hazır hale getiren teknoloji dönüşümüyle birlikte SD-WAN'a yönelmeden önce, kurumsal WAN performansının zorlu problemlerini (deduplication, sıkıştırma, TCP optimization, uygulama hızlandırma) çözmek için yıllarını harcadı. HPE, Silver Peak'i 2020 yılında yaklaşık 925 milyon dolara satın alarak bu teknolojiyi **Aruba EdgeConnect SD-WAN** adıyla Aruba portföyüne entegre etti.

Silver Peak mirası önemlidir; çünkü Aruba'nın SD-WAN çözümünü rakiplerinden neyin ayırdığını açıklar: Çoğu safkan (pure-play) SD-WAN üreticisinin daha sonra geliştirdiği veya hiç geliştirmediği güçlü bir WAN optimization temeli ve uçtan uca görünürlük sağlayan Aruba kampüs ve kablosuz altyapı entegrasyonu.

---

## EdgeConnect Mimarisi

Aruba EdgeConnect, her lokasyonda SD-WAN data plane'ini oluşturan fiziksel ve sanal cihazdır (appliance). Mimari, yönetim ve veri fonksiyonlarını birbirinden ayırır:

**Aruba Orchestrator** (eski adıyla Silver Peak Unity Orchestrator) — merkezi yönetim ve policy platformudur. Bulut ortamında (cloud-hosted) veya on-premises olarak konumlandırılabilen Orchestrator; intent-based policy tanımlama, zero-touch provisioning ve gerçek zamanlı topoloji görselleştirmesi sağlar. Ağ mühendisleri iş hedeflerini (business intent) tanımlar — örneğin "Microsoft 365 trafiği düşük gecikme ve yüksek güvenilirlik gerektirir" — ve Orchestrator bu hedefi tüm EdgeConnect cihazlarına dağıtılan SD-WAN konfigürasyonuna dönüştürür.

**Aruba EdgeConnect Appliances** — her lokasyondaki uç cihazlardır. Farklı throughput gereksinimleri için donanım cihazları (EC-US, EC-S, EC-M, EC-L, EC-XL katmanları), sanal cihazlar (AWS, Azure, Google Cloud için) ve standart x86 donanımlar üzerinde yalnızca yazılım (software-only) dağıtımları şeklinde sunulur.

**Aruba Central** — görünürlüğü SD-WAN'ın ötesine taşıyarak Aruba'nın kablosuz (AP'ler), kablolu switching (CX serisi) ve güvenlik altyapısına genişleten birleşik yönetim portalıdır. Kampüs, şube ve WAN genelinde Aruba kullanan kurumlar için Central, tek bir operasyonel görünüm sunar.

---

## Application-Defined WAN: Temel Ayrışma Noktası

Aruba'nın SD-WAN yaklaşımı için kullandığı pazarlama terimi **application-defined WAN (AD-WAN)**'dır. Bu kavram, özünde diğer üreticilerdeki application-aware routing ile aynıdır — trafik uygulamaya göre tanımlanır ve gerçek zamanlı hat kalitesine göre yönlendirilir — ancak uygulama biçimi Silver Peak'in WAN optimization köklerini yansıtır.

**Deep packet inspection ve uygulama sınıflandırma**
EdgeConnect, binlerce uygulama imzasını sınıflandırmak için DPI kullanır. Öncelikli olarak hedef IP'ye veya temel port eşleştirmesine dayanan bazı SD-WAN platformlarının aksine, EdgeConnect'in sınıflandırma motoru yalnızca açık metin (cleartext) başlıkların paket incelemesine dayanmaz; istatistiksel analiz ve flow metadata kullanarak şifrelenmiş akışlar içindeki uygulamaları da tanımlayabilir.

**Mikrosaniye hassasiyetinde sürekli hat kalitesi izleme**
EdgeConnect, her bir WAN tünelini saniyenin altındaki ölçüm aralıklarıyla sürekli olarak probe eder. Sistem; her aktif tünel için latency, jitter ve paket kaybına dair kayan bir görünüm (rolling view) tutar ve periyodik yoklama ortalamaları yerine neredeyse gerçek zamanlı verilere dayalı yol seçim kararları alınmasını sağlar. Bu, Silver Peak'in WAN optimization alanındaki çalışmalarının doğrudan bir mirasıdır; zira gecikme ölçümünün hassasiyeti doğrudan TCP optimization kararlarını etkiler.

**İlk pakette uygulama tanımlama (First-packet application identification)**
Bazı SD-WAN platformlarının pratik bir kısıtlaması, yol seçiminin ancak uygulama tanımlandıktan sonra devreye girmesidir; bu da birden fazla paket gerektirebilir. Aruba EdgeConnect, bilinen uygulamalar için hedef ve porta dayalı olarak ilk pakette yol seçimi kararı verebilir ve DPI sonraki trafik için sınıflandırmayı netleştirir. VoIP gibi gecikmeye duyarlı uygulamalar için bu durum oldukça kritiktir: Sistem akışı tanımlayana kadar bir çağrının ilk birkaç paketi suboptimal bir yoldan iletilmez.

---

## WAN Optimization: Silver Peak'in Kattıkları

Aruba'nın SD-WAN çözümünü çoğu rakibinden teknik olarak en çok ayrıştıran yetenek, Silver Peak'ten miras kalan **WAN optimization yığınıdır**.

**Veri azaltma (Deduplication ve sıkıştırma)**
EdgeConnect, tünel uç noktaları arasında paylaşılan bir veri deposu (data store) tutar. Aynı veri bloğu daha önce görüldüğünde — ki dosya transferleri, yedekleme trafiği ve paylaşılan nesnelere sıkça başvuran uygulama verilerinde bu yaygındır — verinin tamamı yerine yalnızca bir hash referansı iletilir. Bu, uygun iş yükleri için WAN bant genişliği tüketimini %50 ila %90 oranında azaltabilir.

**TCP optimization**
Standart TCP, düşük gecikme ve düşük paket kaybına sahip yerel alan ağları (LAN) için tasarlanmıştır. Yüksek gecikmeli WAN hatlarında veya anlık paket kayıpları yaşanan linklerde, TCP'nin congestion control mekanizmaları verimlilikte (throughput) ciddi düşüşe neden olur. EdgeConnect'in TCP optimization motoru bir TCP proxy gibi davranarak WAN linkinin her iki tarafındaki uygulamaya yerel bir TCP uç noktası sunarken, EdgeConnect cihazları arasında optimize edilmiş bir taşıma protokolü kullanır. Uygulamalar, gerçek WAN koşullarından bağımsız olarak LAN'a yakın bir TCP performansı görür.

**Uygulama hızlandırma (Application acceleration)**
Belirli uygulamalar için (CIFS/SMB dosya transferleri, on-premises Exchange için MAPI, Oracle Forms ve diğerleri), EdgeConnect genel TCP optimization'ın ötesine geçen protokole özel hızlandırma modülleri içerir. Bu modüller uygulama katmanı protokollerini anlar; verileri akıllıca önceden çeker (prefetch) veya önbelleğe (cache) alır.

Daha fazla kurumsal uygulama yerleşik CDN hızlandırması ve bulut için optimize edilmiş protokollerle cloud-native mimarilere geçtikçe, geleneksel WAN optimization değerinin dönüştüğünü belirtmek gerekir. Microsoft 365 gibi SaaS uygulamaları zaten internet üzerinden iletim için optimize edilmiştir. WAN optimization yığını, en çok WAN'a duyarlı eski protokollere sahip uygulamalar ve lokasyonlar arası veri replikasyon iş yükleri için değerini korumaktadır.

---

## Boost: Paket Düzeyinde Güvenilirlik Artırımı

Aruba'nın **Boost** yeteneği, WAN güvenilirliğini uygulama seviyesinden ziyade paket seviyesinde ele alır. Şunları içerir:

**Forward Error Correction (FEC):** Akışa yedek parite paketleri ekler, böylece alıcı düşen paketleri yeniden iletime (retransmission) gerek kalmadan yeniden oluşturabilir. Orta düzeyde paket kaybı (%1-3) olan hatlarda FEC, TCP retransmission'ın getirdiği gidiş-dönüş gecikmesi (round-trip delay) olmadan etkin kaybı neredeyse sıfıra indirebilir.

**Packet Order Correction:** Sırası bozulan paketleri uygulamaya teslim etmeden önce alıcı tarafında yeniden sıralar. Zaman zaman paketleri sıra dışı ileten geniş bant (broadband) bağlantılar için oldukça kullanışlıdır.

**High Availability (HA) tunneling:** Gecikmeye duyarlı paketlerin kopyalarını aynı anda iki farklı WAN yolundan iletir ve ilk ulaşan kopyayı teslim eder. Efektif paket kaybı sıfıra yaklaşır; gecikme ise iki yoldan daha iyi olanıyla sınırlandırılır.

Bu yetenekler, paket kaybının ve jitter'ın öngörülemez olduğu internet broadband bağlantıları üzerindeki ses ve video uygulamaları için kritik önem taşır.

---

## Aruba SSE ve SASE Entegrasyonu

HPE Aruba'nın SASE stratejisi, şu hizmetleri sunan bulut tabanlı bir güvenlik platformu olan **Aruba SSE** (Security Service Edge) etrafında şekillenmiştir:
- Secure Web Gateway (SWG)
- Cloud Access Security Broker (CASB)
- Zero Trust Network Access (ZTNA)
- Digital Experience Monitoring (DEM)

EdgeConnect SD-WAN, şubelerdeki internet çıkışlı trafiği denetim amacıyla en yakın SSE PoP noktasına yönlendirmek üzere Aruba SSE ile entegre çalışır; böylece trafiği merkezi bir veri merkezi firewall'una geri taşımaya (backhaul) gerek kalmadan doğrudan internet çıkışı (direct internet breakout) sağlar.

Aruba Central; hem WAN yönlendirmesi hem de bulut güvenliği için tek bir policy modeli sunarak EdgeConnect SD-WAN ve Aruba SSE genelinde birleşik bir yönetim sağlar. Bu, Aruba'nın ayrı ürünlerden inşa edilen çoğu SASE mimarisini etkileyen yönetim parçalanmışlığı (management fragmentation) sorununa verdiği yanıttır.

---

## HPE Aruba SD-WAN'ın Güçlü Olduğu Alanlar

**WAN optimization gereksinimleri**
Lokasyonlar arasında yoğun veri replikasyonu yapan, WAN performansına duyarlı eski uygulama trafiği bulunan veya şubeler arasında sıkça büyük dosya transferleri gerçekleştiren kurumlar; çoğu rakip SD-WAN platformunun sağlayamadığı ölçülebilir bir değeri EdgeConnect'in WAN optimization yığınından elde eder.

**Broadband bağımlı lokasyonlar için yüksek güvenilirlik gereksinimleri**
Boost FEC, paket sırası düzeltme ve HA tunneling kombinasyonu; internet broadband bağlantısının birincil veya tek WAN taşıyıcısı olduğu, paket kaybı ya da jitter endişesi bulunan lokasyonlar için EdgeConnect'i ideal hale getirir — perakende mağazaları, dağıtık konaklama sektörü ve internet servis sağlayıcı (ISP) altyapısının zayıf olduğu bölgelerdeki şubeler gibi.

**Birleşik Aruba kampüs ve WAN yönetimi**
Aruba CX switching ve Aruba wireless altyapısını (Aruba Central üzerinden yönetilen) kullanan kurumlar, EdgeConnect'i WAN'a genişleterek operasyonel tutarlılık kazanır. Kampüs switching ve kablosuz ağlarını yöneten aynı Aruba Central portalı WAN görünürlüğü de sağlayarak ağ operasyon ekibinin izlemek zorunda olduğu yönetim düzlemi (management plane) sayısını azaltır.

**Intent-based yönetim modeli**
Orchestrator'ın intent-based policy modeli, SD-WAN pazarındaki en sezgisel modellerden biridir. İş hedeflerini belirleyip — "birleşik iletişim trafiğine öncelik ver, SaaS için bulut yolunu kullan, ERP'yi MPLS üzerinden koru" — sistemin bunu cihaz konfigürasyonuna dönüştürmesini sağlamak, cihaz başına manuel yapılandırma karmaşıklığının büyük bölümünü ortadan kaldırır. Sınırlı SD-WAN deneyimine sahip ekipler, daha ayrıntılı teknik policy tanımlaması gerektiren platformlara kıyasla çalışan bir kuruluma çok daha hızlı ulaşabilir.

---

## HPE Aruba SD-WAN'ın Limitleri ve Zayıf Yönleri

**Güvenlik entegrasyonu**
Fortinet'in entegre NGFW+SD-WAN modelinin aksine, EdgeConnect tam teşekküllü bir NGFW içermez. Şube güvenliği ya Aruba SSE (bulut üzerinden sağlanan) ya da üçüncü taraf bir firewall entegrasyonu gerektirir. Her şubede yerel olarak stateful firewall ve IPS'e ihtiyaç duyan kurumlar için bu durum, Fortinet'in yerel olarak çözdüğü mimariye ek bir bileşen getirmektedir.

**Pazar payı ve ekosistem**
SD-WAN pazarında Fortinet ve Cisco, Aruba'ya kıyasla daha büyük bir kurulu tabana (installed base) ve daha geniş bir iş ortağı ekosistemine sahiptir. Aruba'nın SD-WAN çözümü teknik olarak güçlü olsa da, Avrupa kurumsal ortamlarında Cisco veya Fortinet kurulumlarına kıyasla daha az karşımıza çıkar; bu da deneyimli entegratör ve iş ortağı bulma imkanını etkileyebilir.

**Küçük ölçekte karmaşıklık**
Çok küçük ölçekli kurulumlar için (20 lokasyon altı), Orchestrator lisanslama maliyeti ve operasyonel yük gereksiz kalabilir. Platform binlerce lokasyona ölçeklenecek şekilde tasarlanmıştır; küçük ölçekte daha yalın platformlar daha iyi bir operasyonel deneyim sunabilir.

---

## Tipik Dağıtım Mimarisi

Standart bir HPE Aruba EdgeConnect SD-WAN mimarisi:

- **Orchestrator:** Cloud-hosted (Aruba tarafından yönetilen) veya on-premises sanal cihaz (virtual appliance)
- **Hub lokasyonları:** Spoke tünellerini sonlandıran ve bölgesel internet çıkışı sağlayan, veri merkezi lokasyonlarındaki EdgeConnect XL veya EC-L cihazları
- **Şube lokasyonları:** Dual WAN bağlantısına sahip, Orchestrator üzerinden zero-touch provision edilmiş EdgeConnect EC-S veya EC-M cihazları; broadband üzerindeki ses/video trafiği için Boost etkinleştirilmiş
- **Bulut bağlantısı:** Bulut ortamlarında tutarlı policy uygulamak için AWS/Azure üzerinde çalışan EdgeConnect Virtual
- **İnternet güvenliği:** EdgeConnect uç cihazlarından yerel yönlendirme (local steering) ile Aruba SSE entegrasyonu

---

## Özet

HPE Aruba EdgeConnect SD-WAN, pazardaki en olgun WAN optimization yeteneğini modern bir SD-WAN mimarisine taşır. WAN optimization'ın önemini koruduğu senaryolarda — lokasyonlar arası replikasyon, gecikmeye duyarlı eski uygulamalar, broadband üzerinde yüksek güvenilirlik gereksinimleri — Silver Peak mirası gerçek bir teknik ayrışma sunar.

Aruba entegrasyonu; kampüs ve şube altyapısına sahip kurumlara kablosuz, kablolu ve WAN altyapısında operasyonel olarak son derece cazip bir birleşik yönetim yolu sağlar. Mevcut bir Aruba altyapısı bulunmayan ve belirgin bir WAN optimization ihtiyacı olmayan ortamlardaki saf SD-WAN kurulumlarında ise Cisco veya Fortinet'e kıyasla ayrışan noktalar daralmaktadır.

---

*Bu serideki bir sonraki yazı: [Palo Alto SD-WAN — Prisma SD-WAN ve Güvenlik Öncelikli Yaklaşım](/en/posts/palo-alto-sd-wan/)*
