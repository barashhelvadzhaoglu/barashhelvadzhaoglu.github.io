---
title: "F5 GTM ve GSLB Deep Dive: Global Trafik Yönetimi ve DNS Failover"
description: "F5 GTM (BIG-IP DNS) teknik inceleme — Wide IP, iQuery, topoloji routing, TTL stratejisi, çok DC failover ve aktif-aktif mimari desenleri."
date: 2026-04-15
draft: false

cover:
  image: "/img/postimages/f5-gtm-gslb-cover.webp"
  alt: "F5 GTM GSLB Global Trafik Yönetimi — DNS Failover Mimarisi"
  relative: false

tags: ["F5", "GTM", "GSLB", "BIG-IP DNS", "DNS Failover", "Global Load Balancing", "Çok DC", "Disaster Recovery"]
categories: ["Teknoloji"]
keywords:
  - F5 GTM yapılandırması
  - F5 GSLB global server load balancing
  - F5 Wide IP
  - F5 iQuery
  - F5 topoloji load balancing
  - F5 DNS failover
  - F5 GTM vs LTM
  - global traffic manager BIG-IP
  - çok veri merkezi failover
  - F5 GTM TTL stratejisi

showToc: true
TocOpen: true
---

# F5 GTM ve GSLB Deep Dive: Global Trafik Yönetimi ve DNS Failover

Bu yazı F5 BIG-IP serisinin bir parçasıdır.

> **F5'e yeni misiniz?** Önce platform genel bakışıyla başlayın: [F5 BIG-IP Bir Load Balancer Değil — Uygulama Teslim Platformudur](/tr/technology/f5-bigip-uygulama-teslim-platformu-genel-bakis/)

Büyük resmi zaten anlıyorsanız ve GTM'e derinlemesine inmek istiyorsanız — iQuery, Wide IP'ler, topoloji routing, TTL stratejisi ve çok DC tasarımı — doğru yerdesiniz.

---

## GTM'in Çözdüğü Sorun

LTM, uygulama trafiğini tek bir veri merkezi içinde yönetir. Bağlantıları backend sunucular arasında dağıtır, sağlığı izler ve tek bir sitede HA sağlar. Ancak LTM'nin veri merkezinin dışında ne olduğuna dair görünürlüğü yoktur — siteler arasında trafik yönlendiremez.

GTM'in doldurduğu boşluk tam olarak budur. Bir organizasyonun iki veri merkezi, birincil bir DC ve bir DR sitesi ya da küresel olarak dağıtılmış altyapısı olduğunda soru şudur: *İstemciler hangi veri merkezine bağlanacaklarını nasıl bilir ve biri çevrimdışı olduğunda ne otomatik olarak gerçekleşir?*

GTM olmadan yanıt genellikle manuel DNS değişiklikleridir — yavaş, hatalara açık ve otomatik failover için tamamen uygunsuz. GTM bunu DNS katmanında çözer.

---

## DNS Akışı: GTM Nasıl Karar Verir

GTM, uygulama zone'larınız için **yetkili DNS sunucusu** olarak davranır. Bir istemci `webapp.sirket.com`'u çözümlediğinde, sorgu standart bir DNS sunucusu yerine GTM'e ulaşır:

```
1. İstemci: "webapp.sirket.com için IP nedir?"
2. Sorgu GTM'e ulaşır (sirket.com zone'u için yetkili)
3. GTM gerçek zamanlı olarak değerlendirir:
   → DC-1 LTM sağlıklı mı? (iQuery aracılığıyla)
   → DC-2 LTM sağlıklı mı? (iQuery aracılığıyla)
   → Hangi load balancing politikası geçerli?
   → Bu istemci coğrafi olarak nerede?
4. GTM yanıtlar: "webapp.sirket.com = 10.10.1.100" (DC-1 VIP)
5. İstemci 10.10.1.100'e bağlanır → LTM buradan devralır
```

Zeka 3. adımdadır. GTM statik bir kayıt döndüren pasif bir DNS sunucusu değildir — bir sorguyu her yanıtladığında mevcut altyapı sağlığına ve politikaya dayalı gerçek zamanlı bir karar verir.

---

## GTM Nesne Hiyerarşisi

GTM, DNS yapısını yansıtan dört seviyeli bir hiyerarşi kullanır:

```
Veri Merkezi  →  Sunucu  →  Virtual Server  →  Wide IP (Pool Member)
```

**Veri Merkezi:** Fiziksel bir site için mantıksal gruplama (DC-Istanbul, DC-Frankfurt). O konumdaki tüm GTM kayıtlı sunucuları içerir.

**Sunucu:** GTM'e kayıtlı bir BIG-IP cihazı (genellikle bir LTM). GTM, gerçek zamanlı sağlık verileri için iQuery aracılığıyla onunla iletişim kurar.

**Virtual Server:** Kayıtlı bir sunucudaki belirli bir LTM virtual server'ı (VIP). GTM'in trafiği yönlendirebileceği gerçek endpoint.

**GTM Pool'u:** Bir veya birden fazla LTM genelinde virtual server'lardan oluşan bir grup. GTM, DNS yanıtlarını pool member'lar arasında dağıtır.

**Wide IP:** İstemcilerin çözümlediği DNS adı (`webapp.sirket.com`). Bir Wide IP, bir veya daha fazla GTM pool'una referans verir ve çözümleme politikasını tanımlar.

---

## iQuery: GTM'in Gerçekte Uygulama Sağlığını Neden Anladığı

**iQuery**, GTM'e gerçek uygulama farkındalığı veren özel F5 protokolüdür. Bu, GTM'i yalnızca bir VIP'e ping atan veya TCP erişilebilirliğini kontrol eden harici DNS load balancer'lardan ayıran şeydir.

iQuery olmadan GTM yalnızca bir IP adresinin probe'a yanıt verip vermediğini bilir. iQuery ile GTM şunları bilir:

- LTM virtual server'ının etkin ve aktif olup olmadığı
- O virtual server'ın arkasındaki pool'un sağlıklı, aktif member'lara sahip olup olmadığı
- LTM'deki mevcut aktif bağlantı sayısı
- Mevcut CPU ve bellek kullanımı

**Kritik sonuç:** Bir backend uygulaması başarısız olduğunda ve LTM pool'unu down olarak işaretlediğinde, iQuery bunu GTM'e **anında** iletir — herhangi bir istemcinin bozuk bir endpoint'e bağlanma şansı olmadan. GTM, o DC'nin VIP'ini hemen DNS sorgularına yanıt olarak vermeyi durdurur.

GTM'den bir VIP IP'sine TCP sağlık probe'u bu durumu hiçbir zaman tespit edemezdi — VIP IP'si, arkasındaki uygulama tamamen bozuk olsa bile erişilebilir kalmaya devam eder. Farkı yaratan iQuery'dir.

### GTM'e LTM Kaydetme

```
Sunucu: ltm-dc1
  Ürün:          BIG-IP (iQuery'yi etkinleştirir)
  Adres:         10.10.0.1 (LTM yönetim IP'si)
  Veri Merkezi:  DC-Istanbul
  Virtual Server'lar: [iQuery aracılığıyla otomatik keşfedilir]
    - vs_webapp_443  (10.10.1.100:443)
    - vs_api_443     (10.10.1.101:443)
    - vs_admin_443   (10.10.1.102:443)
```

Kaydedildikten sonra GTM, o LTM'deki tüm virtual server'ları otomatik olarak keşfeder ve izler. GTM'de manuel virtual server yapılandırması gerekmez — iQuery keşfi yönetir.

---

## Wide IP'ler ve GTM Pool'ları

Bir Wide IP, bir DNS adını bir çözümleme politikasına bağlar:

```
Wide IP: webapp.sirket.com (tür: A)
  Pool: gtm_pool_webapp_primary
    Load Balancing Yöntemi: Global Availability
    Member'lar:
      - ltm-dc1 / vs_webapp_443  (Sıra: 1)
      - ltm-dc2 / vs_webapp_443  (Sıra: 2)
  Fallback Pool:    gtm_pool_webapp_dr
  Last Resort Pool: [tüm pool'lar tükenirse SERVFAIL döndür]
```

Bir Wide IP'nin öncelik sırasına göre birden fazla pool'u olabilir. Birincil pool'un kullanılabilir member'ı yoksa GTM otomatik olarak bir sonraki pool'u dener. Bu, manuel müdahale olmadan kademeli failover mimarisi sağlar.

---

## Load Balancing Yöntemleri

GTM load balancing, DNS yanıt seviyesinde çalışır — her yöntem, belirli bir sorgu için hangi pool member'ın IP'sinin döndürüleceğini belirler.

### Global Availability

Her zaman ilk kullanılabilir member'ın IP'sini döndürür. Yalnızca mevcut kullanılamadığında bir sonraki member'a geçer:

```
Member'lar (öncelik sırasına göre):
  1. ltm-dc1 / vs_webapp_443  ← sağlıklıyken tüm trafik
  2. ltm-dc2 / vs_webapp_443  ← yalnızca DC-1 başarısız olduğunda trafik
```

**En iyisi:** Birincil/DR mimarileri. Tüm trafik birincil sitede çalışır; DR yalnızca gerçek kesintiler sırasında etkinleşir. Bankacılık ortamındaki standart yöntem buydu — uygun maliyetli, hakkında düşünmesi basit ve arıza altında öngörülebilir.

### Round Robin

DNS yanıtlarını pool member'lar arasında dönüşümlü olarak verir:

```
Sorgu 1 → DC-1 VIP
Sorgu 2 → DC-2 VIP
Sorgu 3 → DC-1 VIP
```

**En iyisi:** Her sitede eşit kapasiteli aktif-aktif çok DC mimarileri. Her iki sitenin de sürekli olarak yükü paylaşması gereken büyük ölçekli web uygulamalarında yaygın.

### Ratio

Ağırlıklı dağılım:

```
ltm-dc1 / vs_webapp_443  Ratio: 7  ← DNS yanıtlarının %70'i
ltm-dc2 / vs_webapp_443  Ratio: 3  ← DNS yanıtlarının %30'u
```

**En iyisi:** Veri merkezlerinin farklı kapasitelere sahip olduğu aktif-aktif. Kapasiteyle orantılı yük dağılımı sağlar.

### Topology

DNS yanıtlarını istemcinin DNS çözümleyici IP'sinin coğrafi konumuna göre yönlendirir:

```
Topoloji Kayıtları (yukarıdan aşağıya değerlendirilir, ilk eşleşme kazanır):
  alt ağ 10.0.0.0/8         → DC-Istanbul   (tüm dahili kullanıcılar)
  ISP: Turk Telekom         → DC-Istanbul
  bölge: Avrupa             → DC-Frankfurt
  bölge: Orta Doğu          → DC-Istanbul
  varsayılan               → DC-Frankfurt
```

**En iyisi:** Birden fazla bölgedeki kullanıcılara sahip global uygulamalar. Kullanıcıları en yakın DC'ye yönlendirerek gecikmeyi azaltır. Ayrıca veri yerleşimi uyumluluğunu sağlar — AB kullanıcılarının isteklerinin AB veri merkezlerinde işlenmesini garanti eder.

GTM, çözümleyici IP'lerini bölgelere eşleştirmek için bir IP coğrafi konum veritabanı kullanır. Bu veritabanını güncel tutun — ISP'ler IP aralıklarını düzenli olarak yeniden tahsis eder ve güncel olmayan coğrafi konum verileri kullanıcıları yanlış bölgelere gönderir.

### Least Connections

iQuery aracılığıyla gerçek zamanlı olarak elde edilen en az aktif bağlantıya sahip pool member'a yönlendirir:

```
iQuery aracılığıyla mevcut durum:
  ltm-dc1: 4.521 aktif bağlantı
  ltm-dc2: 3.102 aktif bağlantı
  → GTM bir sonraki sorgu için DC-2 VIP'ini döndürür
```

**En iyisi:** Statik ağırlıklar yerine gerçek bağlantı sayılarına dayalı dinamik load balancing'in tercih edildiği aktif-aktif mimariler.

---

## DNS TTL Stratejisi: En Çok Yanlış Anlaşılan Konu

TTL, DNS çözümleyicilerin GTM'nin yanıtını ne kadar süre önbelleğe alacağını belirler. Bu yaygın biçimde yanlış anlaşılır:

**TTL, adı zaten çözümlemiş istemciler için failover hızını kontrol etmez.** 10 saniye önce `webapp.sirket.com`'u çözümleyen bir istemci, TTL sona erene kadar önbelleğe alınan IP'yi kullanmaya devam eder — GTM'nin şu anda neye yanıt verdiğinden bağımsız olarak.

TTL, **yeni DNS sorgularının** mevcut altyapı durumunu ne kadar hızlı yansıtacağını kontrol eder.

### TTL Takas Değerlendirmeleri

| TTL | Failover görünürlüğü | DNS sorgu yükü | Kullanım alanı |
|---|---|---|---|
| 30 sn | Hızlı | Yüksek | Kritik ödeme sistemleri, kimlik doğrulama servisleri |
| 60 sn | İyi | Orta | Çoğu üretim uygulaması |
| 300 sn | Orta | Düşük | Dahili araçlar, izleme |
| 3600 sn | Yavaş | Çok düşük | Statik içerik, nadiren değişen kayıtlar |

Bankacılık ortamında:
- Ödeme işleme ve kimlik doğrulama servisleri için **30 saniye**
- Genel bankacılık uygulamaları için **60 saniye**
- Dahili panolar ve izleme araçları için **300 saniye**

### Minimum Etkin Failover Süresini Hesaplama

```
En kötü durum failover süresi ≈ Sağlık kontrolü aralığı + TTL
```

5 saniyelik iQuery kontrol aralığı ve 30 saniyelik TTL ile: en kötü durum ~35 saniyedir. Bazı istemciler arıza tespitinden sonra saniyeler içinde yeni DC'ye geçer; diğerleri TTL süresinin dolmasını bekler.

Katı RTO gereksinimleri olan uygulamalar için geçiş penceresini zarif biçimde yönetmek için düşük TTL'yi uygulama düzeyinde yeniden deneme mantığıyla birleştirin.

---

## Çok DC Mimari Desenleri

### Aktif-Yedek (Birincil / DR)

```
Normal:
  GTM → DC-1 LTM → Uygulama Sunucuları (DC-1)
  DC-2 sıcak yedektir — çalışıyor, senkronize, trafik yok

DC-1 arızası:
  iQuery: DC-1 LTM virtual server'ı down olarak işaretlendi
  GTM: DC-1 VIP'ini hemen yanıt olarak vermeyi durdurur
  Yeni DNS sorguları: DC-2 VIP'ini alır
  Trafik kayması: TTL penceresi içinde
```

Gereksinimler:
- Her iki DC'de özdeş uygulama deployment'ı
- Veritabanı replikasyonu (sıfır RPO için senkron, daha düşük RPO için asenkron)
- GTM yöntemi: **Global Availability**

### Aktif-Aktif (Yük Paylaşımı)

```
Normal:
  GTM → DC-1 (DNS yanıtlarının %50'si)
  GTM → DC-2 (DNS yanıtlarının %50'si)

DC-1 arızası:
  GTM, %100'ünü DC-2'ye yönlendirir
```

Gereksinimler:
- DC'ler arasında paylaşılan oturum durumu veya durumsuz uygulama tasarımı
- Her DC'nin bağımsız olarak %100 trafiği karşılayabilmesi gerekir (bu kapasite için plan yapın)
- Her iki DC'den aynı anda yazılabilir veritabanı
- GTM yöntemi: **Round Robin**, **Ratio** veya **Least Connections**

Aktif-aktif, daha iyi kaynak kullanımı ve daha hızlı etkin failover sağlar (soğuk başlatma DR sitesi yok). Mimari karmaşıklık daha yüksektir — özellikle veritabanı yazma çakışmaları ve oturum durumu yönetimi konusunda.

### Topoloji Tabanlı Coğrafi Dağılım

```
AB kullanıcıları    → Avrupa'daki çözümleyici IP   → DC-Frankfurt
MENA kullanıcıları  → Orta Doğu'daki çözümleyici IP → DC-Istanbul
Dahili             → RFC1918 kaynak                → DC-Istanbul (en yakın)
Varsayılan         → DC-Frankfurt
```

Her DC, normal koşullarda kendi bölgesinin trafiğini yönetir. Fallback topoloji kayıtları, kesinti sırasında tüm bölgeleri hayatta kalan DC'ye yönlendirir.

Bu desen performans avantajlarını (daha düşük gecikme) uyumluluk gereksinimleriyle (veri yerleşimi) ve kapasite optimizasyonuyla (her DC kendi bölgesi için boyutlandırılmış) birleştirir.

---

## GTM Monitor'ları ile iQuery: Her Biri Ne Zaman Kullanılır

**iQuery (BIG-IP LTM'ler için):**
- LTM'den gerçek zamanlı uygulama sağlık verileri
- Ek izleme trafiği yok
- Yalnızca IP erişilebilirliğini değil uygulama sağlığını bilir
- Otomatik virtual server keşfi
- Tüm BIG-IP LTM endpoint'leri için kullanın

**GTM yerel monitor'ları (BIG-IP olmayan endpoint'ler için):**
- GTM kendi sağlık probe'larını doğrudan endpoint'lere gönderir
- TCP, HTTP, HTTPS, ICMP destekler
- Hibrit ortamlarda üçüncü taraf load balancer'lar, bulut endpoint'leri, kaynak sunucular için kullanın

Çoğu kurumsal deployment'ta iQuery, tüm BIG-IP'ten BIG-IP'e izlemeyi yönetir. GTM yerel monitor'ları, bazı endpoint'lerin F5 cihazı olmadığı hibrit mimariler için ayrılmıştır.

---

## GTM'de DNS Persistence

GTM TCP durumunu korumaz — yalnızca DNS yanıtlarını etkiler. Ancak, aynı çözümleyiciden tekrarlanan sorguların yapılandırılabilir bir süre boyunca aynı IP'yi döndürmesini sağlamak için **DNS persistence** destekler:

```
Wide IP Persistence:
  Etkin: Evet
  TTL:   300 saniye
  Tür:   Kaynak IP'ye göre (çözümleyici IP)
```

Persistence etkinleştirildiğinde GTM, load balancing yönteminden bağımsız olarak 300 saniye boyunca aynı çözümleyiciye aynı VIP'i döndürür. Bu, istemciler sık sık yeniden çözümlediğinde oturum kesintisini azaltır.

**Önemli uyarı:** DNS persistence, son istemci IP'sine değil **çözümleyici IP'sine** dayanır. Birçok son kullanıcı tek bir ISP özyinelemeli çözümleyiciyi paylaştığında, hepsi GTM için aynı "istemci" olarak görünür. Persistence, bu durumlarda orantısız trafiği bir DC'ye yoğunlaştırabilir. Etkinleştirmeden önce persistence'ın gerçekten yardımcı olup olmadığını değerlendirin.

---

## Temel Çıkarımlar

- GTM, **çok DC DNS failover'ını** çözer — LTM'nin tek başına ele alamayacağı sorun.
- **iQuery**, GTM'nin en önemli özelliğidir: yalnızca IP erişilebilirliği değil, gerçek uygulama sağlık farkındalığı. LTM bir uygulama pool'unu down olarak işaretlediğinde GTM anında tepki verir.
- **Global Availability**, birincil/DR için doğru yöntemdir. Aktif-aktif için **Round Robin** veya **Ratio**.
- **Topology** routing, global deployment'lar için gecikmeyi azaltır ve veri yerleşimi uyumluluğunu sağlar.
- **TTL yalnızca yeni aramaları kontrol eder** — mevcut bağlantıları değil. Minimum etkin failover = sağlık kontrolü aralığı + TTL.
- **BIG-IP LTM'ler için iQuery** kullanın; üçüncü taraf endpoint'ler için GTM yerel monitor'larını kullanın.

---

## Bu Seri

- 📖 [F5 BIG-IP Platform Genel Bakış — Tüm Modüller](/tr/technology/f5-bigip-uygulama-teslim-platformu-genel-bakis/) ← F5'e yeniyseniz buradan başlayın
- 🔧 [F5 LTM Deep Dive](/tr/technology/f5-ltm-virtual-server-irule-ssl-offloading-ha/)
- 🛡️ [F5 WAF Deep Dive](/tr/technology/f5-waf-asm-advanced-waf-uygulama-guvenligi/)

## İlgili Yazılar

- 🏗️ [IT Altyapısı Ürünler Koleksiyonu Değildir](/tr/architecture/it-infrastructure-not-a-collection-of-products/) — Çok DC tasarımı için sistem düşüncesi
- 🔐 [Zero Trust Zihniyeti](/tr/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — Dağıtık altyapıda kimlik bilincine sahip erişim
- 📊 [İzleme Doğru Yapıldığında](/tr/architecture/monitoring-not-just-seeing/) — GTM ve LTM sağlığını proaktif olarak izleme