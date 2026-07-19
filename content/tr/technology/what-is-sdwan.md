---
title: "SD-WAN Nedir? Ağ Mühendisleri İçin Pratik Bir Kılavuz"
seoTitle: "SD-WAN Nedir? Nasıl Çalışır, Kullanım Alanları ve Mimari Açıklaması"
description: "SD-WAN için kapsamlı bir teknik kılavuz: nasıl çalışır, temel bileşenler, trafik yönlendirme ve işletmelerin neden MPLS'i Software-Defined WAN ile değiştirdiği."
date: 2026-06-12
keywords:
  - SD-WAN nedir
  - SD-WAN açıklaması
  - SD-WAN mimarisi
  - SD-WAN vs MPLS
  - Yazılım Tanımlı WAN
  - SD-WAN kullanım alanları
  - SD-WAN trafik yönlendirme
  - WAN optimizasyonu
tags:
  - SD-WAN
  - Ağ Teknolojileri
  - WAN
draft: false
---

# SD-WAN Nedir? Ağ Mühendisleri İçin Pratik Bir Kılavuz

Kurumsal WAN'ın bir sorunu var. On yıllardır şirketler, şubeler, veri merkezleri ve genel merkezler arasındaki uygulama performansını garanti etmek için MPLS hatları için yüksek primler ödüyor. Bu mimari, tüm trafik dahili olduğunda ve tüm uygulamalar veri merkezinde yaşadığında mantıklıydı. Sonra bulut geldi.

Bugün Münih'teki bir şube, Microsoft 365 trafiğini 200 ms'lik bir MPLS backhaul üzerinden Frankfurt'a, oradan internete, oradan Microsoft'un Avrupa edge'ine gönderiyor — her Teams aramasına ve SharePoint senkronizasyonuna 60 ile 100 ms arasında gereksiz gecikme ekleyerek. Ağ, artık var olmayan bir dünya için inşa edildi.

SD-WAN — Software-Defined Wide Area Network (Yazılım Tanımlı Geniş Alan Ağı) — bu sorunun mimari cevabıdır. Bu makale, SD-WAN'ın ne olduğunu, nasıl çalıştığını ve neden kurumsal ağlar için varsayılan WAN mimarisi haline geldiğini açıklıyor.

---

## Temel Fikir

SD-WAN, WAN bağlantısında **kontrol düzlemini** **veri düzleminden** ayırır. Geleneksel router tabanlı bir WAN'da her cihaz, statik yönlendirme tablolarına veya basit metriklere dayanarak kendi iletim kararlarını verir. Bir SD-WAN overlay, bu zekayı tüm siteler, tüm bağlantılar ve tüm uygulamalar üzerinde eş zamanlı görünürlüğe sahip merkezi bir kontrolöre devreder.

Sonuç, akıllı gerçek zamanlı kararlar verebilen bir WAN'dır: MPLS bağlantısında şu an %2 paket kaybı olduğu için bu video konferansı 4G LTE bağlantısı üzerinden gönder; düşük jitter gerektirdiği için bu SAP işlemini MPLS üzerinden yönlendir; gecikmeye toleranslı olduğu için bu yazılım güncellemesini ucuz genişbant üzerinden gönder.

Bu, SD-WAN'ın tanımlayıcı özelliği olan **uygulama farkındalıklı yönlendirmedir**.

---

## Temel Bileşenler

### Edge Cihazlar (SD-WAN Appliance'lar)
Her siteye dağıtılan fiziksel veya sanal cihazlar. WAN bağlantılarını sonlandırır, diğer sitelere şifreli overlay tünelleri oluşturur ve kontrolör tarafından dağıtılan politikaları yerel olarak uygular. Çoğu üretici donanım appliance'ları, sanal appliance'lar (bulut dağıtımları için) ve yazılım ajanları sunar.

### SD-WAN Kontrolör / Orkestratör
Merkezi beyin. Tüm edge'lerin, tüm bağlantıların ve bunların mevcut performans metriklerinin gerçek zamanlı görünümünü korur. Ağ yöneticileri kontrolör düzeyinde politikalar tanımlar — hangi uygulamaların hangi bağlantıları kullandığı, hangi kalite eşiklerinin failover tetiklediği, güvenlik politikalarının nasıl uygulandığı. Kontrolör bu politikaları otomatik olarak tüm edge'lere dağıtır.

### Merkezi Yönetim Portalı
Tüm siteler genelinde izleme, sorun giderme ve yapılandırma için tek bir gösterge paneli. Bu, SD-WAN'ın birincil operasyonel avantajlarından biridir: bir ağ mühendisi 200 şubenin WAN durumunu tek ekranda görebilir ve dakikalar içinde hepsine yapılandırma değişikliği gönderebilir.

### Underlay Transport
SD-WAN transport-agnostiktir. Overlay tüneller herhangi bir kombinasyon üzerinde çalışabilir:
- MPLS
- Genişbant internet (fiber, kablo)
- 4G/5G LTE
- Uydu (LEO seçenekleriyle giderek daha alakalı)

Çoğu dağıtım **hibrit underlay** kullanır — gecikmeye duyarlı uygulamalar için MPLS korunurken genel internet trafiği için daha ucuz genişbant eklenir.

---

## Trafik Yönlendirme Nasıl Çalışır

SD-WAN'ın zekası, trafik yönlendirme motorunda yatar. Tipik bir dağıtımın iletim kararlarını nasıl verdiği:

**1. Uygulama Tanımlama**
Edge cihazı, derin paket inceleme (DPI) kullanarak trafiği sınıflandırır; yalnızca hedef IP'yi değil, gerçek uygulamayı tanımlar. Teams video araması ile Teams dosya indirmesi arasındaki farkı, SAP GUI trafiği ile arka plan SAP senkronizasyonu arasındaki farkı bilir.

**2. Bağlantı Kalitesi İzleme**
Her SD-WAN edge, aktif problar kullanarak her WAN bağlantısının performansını sürekli ölçer: gecikme, jitter, paket kaybı ve kullanılabilir bant genişliği. Bu ölçümler her birkaç saniyede bir gerçekleşir ve sisteme neredeyse gerçek zamanlı görünürlük sağlar.

**3. Politika Eşleştirme**
Bir paket geldiğinde, edge onu politika tablosuyla eşleştirir: "Microsoft Teams Video — < 150 ms gecikme, < %1 paket kaybı, < 30 ms jitter gerektirir. Tercih edilen yol: MPLS. Yedek: genişbant. Son çare: LTE."

**4. Dinamik Yol Seçimi**
Edge, politika gereksinimlerini karşılayan yolu seçer. MPLS bağlantısı eşiğin altına düşerse, genişbanta failover milisaniyeler içinde gerçekleşir — tipik olarak uygulamanın kendi zaman aşımı mekanizmasından daha hızlı, yani kullanıcılar çoğu zaman fark etmez.

**5. Paket Düzeyinde Teknikler**
Gelişmiş SD-WAN uygulamaları performansı daha da artırmak için paket düzeyinde teknikler kullanır:
- **İleri Hata Düzeltme (FEC):** Alıcının yeniden iletim olmadan kayıp verileri yeniden yapılandırabilmesi için yedek paketler gönderir
- **Paket kopyalama:** Kritik paketleri aynı anda birden fazla yol üzerinden gönderir ve en önce geleni iletir
- **WAN optimizasyonu:** Bant genişliği tüketimini azaltmak için tekilleştirme, sıkıştırma ve TCP optimizasyonu

---

## SD-WAN ve MPLS: Gerçekte Ne Değişiyor

MPLS tamamen ortadan kalkmıyor — kritik uygulamalar için internet genişbandının karşılayamadığı deterministik gecikme garantileri sağlamaya devam ediyor. Değişen şey, oynadığı roldür.

Geleneksel bir WAN'da MPLS her şeyi taşırdı. Bir SD-WAN dağıtımında MPLS, yalnızca garantilerini gerçekten gerektiren uygulamaları taşır: gecikmeye duyarlı ses ve video, gerçek zamanlı ERP işlemleri, üretim kontrol sistemleri. Diğer her şey — bulut uygulama trafiği, internet gezintisi, yazılım güncellemeleri, yedeklemeler — daha ucuz genişbant bağlantılara taşınır.

Çoğu işletme için pratik sonuç: WAN maliyetleri önemli ölçüde düşerken bulut iş yükleri için uygulama performansı artar, çünkü trafik artık veri merkezi ağ geçitleri üzerinden gereksiz backhaul yapmaz.

---

## Doğrudan İnternet Erişimi ve Bulut On-Ramp'lar

Modern işletmeler için en değerli SD-WAN özelliklerinden biri, şubede **Doğrudan İnternet Erişimi (DIA)** dir. Tüm internet trafiğini merkezi bir hub üzerinden yönlendirmek yerine, şubeler doğrudan internete bağlanır.

Bu, güvenliğin yerel olarak veya bulutta uygulanmasını gerektirir — SD-WAN'ın giderek daha fazla bulut tabanlı güvenlikle (hizmet olarak güvenlik duvarı, güvenli web ağ geçidi, CASB) entegre olduğu yer burasıdır. SD-WAN ile bulut güvenliğinin kombinasyonu, SASE mimarisinin temelidir; ancak bu ayrı bir konudur.

Büyük bulut sağlayıcıları da **SD-WAN cloud on-ramp** özellikleri geliştirdi: AWS, Azure ve Google Cloud'a optimized giriş noktaları, SD-WAN kontrolörlerinin bulut hedefli trafiği otomatik olarak yönlendirebileceği noktalar. Bu, bulut trafiğinin internete çıkmadan önce bir veri merkezi üzerinden backhaul yapılmasının performans cezasını ortadan kaldırır.

---

## Dağıtım Modelleri

**Yönetilen SD-WAN**
SD-WAN altyapısı bir hizmet sağlayıcı tarafından dağıtılır ve işletilir. İşletme, SLA'larla yönetilen bir hizmet alır. SD-WAN'ı bağımsız olarak işletecek dahili ağ mühendisliği kapasitesine sahip olmayan kuruluşlar için yaygındır.

**Kendin Yönet / Kurumsal Yönetimli SD-WAN**
İşletme, SD-WAN appliance'larını ve lisanslarını doğrudan üreticiden satın alır ve altyapıyı dahili olarak işletir. Maksimum kontrol ve esneklik sağlar. Nitelikli ağ mühendisliği personeli gerektirir.

**Bulut Barındırılan Kontrolör**
Çoğu üretici artık kontrolörünü SaaS hizmeti olarak sunuyor; bu da kontrolör altyapısını dahili olarak işletme ihtiyacını ortadan kaldırıyor. Edge'ler on-premises'tedir; kontrol düzlemi bulut barındırmalıdır.

---

## SD-WAN'ın En Çok Anlam İfade Ettiği Yerler

SD-WAN belirli senaryolarda açık değer sunar:

- **Dağıtık perakende veya konaklama:** POS sistemleri, dijital tabela ve misafir WiFi için güvenilir bağlantı gerektiren, minimal yerinde IT personeli olan düzinelerden yüzlerce siteye kadar
- **Birden fazla fabrikaya sahip üretim:** Standart kurumsal trafik ile birlikte gerçek zamanlı OT/IT yakınsama gereksinimleri
- **Finansal hizmetler şubeleri:** MPLS ayak izini azaltma maliyet baskısıyla birlikte temel bankacılık uygulamaları için katı uygulama performansı gereksinimleri
- **Sağlık ağları:** GDPR/HIPAA uyumluluk gereksinimleri ve ağ kesintilerine yüksek duyarlılıkla klinik-klinik bağlantısı

---

## SD-WAN'ın Çözmediği Şeyler

Sınırlamaları açıkça ele almakta fayda var:

SD-WAN, nitelikli ağ mühendisliği ihtiyacını ortadan kaldırmaz. Uygulama farkındalıklı yönlendirmeyi yönlendiren politikaların doğru tanımlanması gerekir. Yanlış yapılandırılmış bir SD-WAN, gecikmeye duyarlı trafiği güvenilmez bağlantılar üzerinden, doğru yapılandırılmış bir SD-WAN'ın onu optimal şekilde yönlendirdiği kadar kolayca yönlendirebilir.

SD-WAN aynı zamanda doğası gereği güvenlik sağlamaz. Bir SD-WAN overlay, siteler arasında şifreli bir tüneldir, ancak tehditlere karşı trafik inceleme yapmaz. Güvenlik üzerine katmanlanmalıdır — ya SD-WAN appliance'ındaki entegre güvenlik işlevleri (Fortinet'in FortiOS ile yaptığı gibi) aracılığıyla ya da bulut tabanlı güvenlik hizmetleriyle entegrasyon yoluyla.

Son olarak, SD-WAN işleyen bir underlay gerektirir. Bir şubedeki internet devreleri güvenilmez ise SD-WAN aralarında geçiş yapabilir, ancak temelden kötü bir bağlantı ortamını telafi edemez.

---

## Özet

SD-WAN, kurumsal WAN için olgun, kanıtlanmış bir mimaridir. Bulut iş yükleri için uygulama performansında ölçülebilir iyileştirmeler sunar, daha ucuz genişbandla hibrit underlay sağlayarak WAN maliyetlerini düşürür ve merkezi yönetim sayesinde WAN operasyonlarını önemli ölçüde basitleştirir.

Önde gelen üreticiler — Fortinet, Cisco, HPE Aruba ve Palo Alto — mimariye anlamlı şekilde farklı yaklaşımlar benimsemektedir. Bu farklılıkları anlamak, platform seçiminde kritik öneme sahiptir — bu serinin aşağıdaki makaleleri tam da bunu ayrıntılı olarak incelemektedir.

---

*Bu makale SD-WAN mimarileri üzerine bir serinin parçasıdır. Sıradaki: [Fortinet SD-WAN — Pratikte Güvenlik Odaklı Ağ](/tr/posts/fortinet-sd-wan/)*
