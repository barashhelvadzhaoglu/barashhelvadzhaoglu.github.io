---
title: "F5 BIG-IP Bir Load Balancer Değil — Uygulama Teslim Platformudur"
description: "F5 BIG-IP bir load balancer'dan çok daha fazlasıdır. LTM, GTM, WAF, APM, AFM ve BGP routing'i kapsayan master rehber."
date: 2026-03-27
draft: false

cover:
  image: "/img/postimages/f5-bigip-platform-overview-cover.webp"
  alt: "F5 BIG-IP Uygulama Teslim Platformu — Kurumsal Mimari Genel Bakış"
  relative: false

tags: ["F5", "BIG-IP", "LTM", "GTM", "WAF", "APM", "ADC", "Load Balancing", "Uygulama Teslimi", "Ağ Güvenliği"]
categories: ["Teknoloji"]
keywords:
  - F5 BIG-IP genel bakış
  - F5 uygulama teslim controller
  - F5 LTM GTM WAF
  - F5 APM SSL VPN
  - F5 BGP routing
  - F5 AFM firewall
  - F5 vs load balancer
  - F5 BIG-IP modülleri
  - kurumsal ADC
  - F5 TMOS

showToc: true
TocOpen: false
---

# F5 BIG-IP: Bir Uygulama Teslim Platformudur

Kurumsal bir ortamda F5'e en yaygın giriş şöyle gerçekleşir: biri *"load balancer çöktü"* yazan bir ticket açar ve F5'i işaret eder. Sorun zaten o cümlede gizlidir.

F5 BIG-IP bir load balancer değildir. Ona öyle demek, bir veri merkezine sunucu odası demek gibidir — teknik olarak yanlış değil, ama konuyu tamamen kaçırıyor.

F5 BIG-IP bir **Uygulama Teslim Controller'ı (ADC)**'dır: uygulamaları yerel ve global altyapıda yöneten, güvence altına alan, optimize eden ve yüksek erişilebilir kılan full-proxy bir platformdur. Load balancing, yaptığı belki düzine şeyden yalnızca biridir.

---

## Bu Seriyi Nasıl Okuyalım

Bu yazı size **büyük resmi** verir — F5'in ne olduğu, nerede durduğu, her modülün ne yaptığı ve alternatiflere göre ne zaman mantıklı olduğu.

**Ağ veya güvenlik mühendisiyseniz** ve yapılandırma, iRule'lar, migrasyon saha notları ve mimari detaylara derinlemesine inmek istiyorsanız — doğrudan ilgilendiğiniz modüle atlayın:

- 🔧 **[F5 LTM Deep Dive](/tr/technology/f5-ltm-virtual-server-irule-ssl-offloading-ha/)** — Virtual server'lar, pool'lar, iRule'lar, SSL offloading, HA ve 30 cihazlık migrasyon rehberi
- 🌐 **[F5 GTM ve GSLB Deep Dive](/tr/technology/f5-gtm-gslb-global-traffic-management/)** — iQuery, Wide IP'ler, topoloji routing, DNS TTL stratejisi, çok DC failover tasarımı
- 🛡️ **[F5 WAF Deep Dive](/tr/technology/f5-waf-asm-advanced-waf-application-security/)** — ASM ve Advanced WAF, OWASP Top 10, bot savunması, şeffaftan engellemeye deployment stratejisi

**Mimar veya karar vericiyseniz** ve F5'in altyapınıza uyup uymadığını değerlendiriyorsanız — okumaya burada devam edin. Bu yazı, iRule sözdizimini anlamanızı gerektirmeden o soruyu yanıtlıyor.

---

## F5 Kurumsal Mimaride Nerede Durur?

F5 BIG-IP, firewall ile uygulama sunucuları arasında çalışır:

```
İnternet
    │
[DDoS Scrubbing / ISP]
    │
[NGFW — Palo Alto / Fortinet]   ← L3/L4: routing, IP filtreleme, VPN, stateful inspection
    │
[F5 BIG-IP]                     ← L4–L7: uygulama teslimi, SSL, sağlık, routing mantığı
    │
[Backend Sunucular / Uygulama Kümeleri]
```

Firewall, ağ düzeyindeki kararları alır. F5, bunun üzerindeki her şeyi yönetir — SSL sonlandırma, sağlık bilincine sahip load balancing, session persistence, trafik manipülasyonu ve Katman 7 güvenliği.

Bu ayrım önemlidir çünkü bir firewall F5'in yaptığını yapmak üzere tasarlanmamıştır. Saniyede binlerce SSL oturumunu verimli biçimde sonlandıramaz, sağlık izleme için HTTP yanıt gövdelerini inceleyemez, uygulama başlıklarını anında yeniden yazamaz ya da URI yolları, çerezler veya kullanıcı kimliğine dayalı routing kararları veremez.

İki veri merkezi tasarımında mimari genişler:

```
               [F5 GTM]        ← DNS düzeyi: istemcileri doğru DC'ye yönlendirir
              /         \
         [DC-1]         [DC-2]
       [F5 LTM]       [F5 LTM] ← Yerel: her DC içinde trafiği dağıtır
           │               │
      Uygulama Sunucuları  Uygulama Sunucuları
```

GTM her iki LTM'nin üzerinde oturur ve DNS sorgularını yanıtlar — istemcileri sağlık, yük ve coğrafyaya göre uygun veri merkezine yönlendirir. Bu, çok DC failover'ını manuel yerine otomatik yapan şeydir.

---

## Tam Modül Haritası

TMOS (Traffic Management Operating System) temeldir. Her F5 modülü onun üzerinde çalışır. Hangi modülün hangi sorunu çözdüğünü anlamak, hem mimari tasarım hem de lisanslama görüşmeleri için anahtardır.

### LTM — Local Traffic Manager

Temel modül. Neredeyse her F5 deployment'ı buradan başlar.

LTM, bir **full-proxy ADC**'dir: her istemci bağlantısını sonlandırır, inceler, routing ve politika kararları alır ve backend'e yeni bir bağlantı açar. Bu full-proxy konumu, uygulama trafiği üzerinde tam görünürlük ve kontrol sağlar.

LTM'nin sunduğu özellikler:
- Backend sunucu pool'larında load balancing — yalnızca TCP erişilebilirliğini değil, uygulama yanıtlarını anlayan sağlık izleme ile
- SSL/TLS offloading — backend'ler adına HTTPS sonlandırma, şifreleme yüklerini kaldırma
- Session persistence — kullanıcıları istekler genelinde aynı backend sunucusuna bağlı tutma
- iRule'lar — trafik düzeyinde hat hızında çalışan programlanabilir bir betik katmanı: başlık yeniden yazma, URI'ye göre yönlendirme, içerik ekleme, hız sınırı uygulama
- Yüksek erişilebilirlik — saniye altı failover ile Aktif-Yedek veya Aktif-Aktif kümeleme

→ **[F5 LTM Deep Dive: Virtual Server'lar, iRule'lar, SSL Offloading ve HA](/tr/technology/f5-ltm-virtual-server-irule-ssl-offloading-ha/)**

---

### GTM / DNS — Global Traffic Manager

LTM trafiği tek bir veri merkezi içinde yönetir. GTM trafiği veri merkezleri **arasında** yönetir — DNS düzeyinde.

Bir istemci `webapp.sirket.com`'u çözümlediğinde, GTM DNS sorgusunu yanıtlar. Yanıtı, hangi veri merkezinin sağlıklı olduğuna, mevcut yüke ve istemcinin coğrafi olarak nerede bulunduğuna bağlıdır.

GTM'nin temel özelliği **iQuery**'dir — doğrudan LTM'den gerçek zamanlı uygulama sağlık verisi sağlayan özel bir protokol. Bir backend uygulaması başarısız olduğunda ve LTM pool'unu down olarak işaretlediğinde, GTM bunu anında bilir ve DNS TTL süresinin dolmasını beklemeden yeni istemcileri o veri merkezine yönlendirmeyi durdurur.

GTM'nin sunduğu özellikler:
- Birden fazla veri merkezinde Global Server Load Balancing (GSLB)
- Bir DC çevrimdışı olduğunda otomatik DNS düzeyinde failover
- Topoloji tabanlı routing — Avrupalı kullanıcılar AB veri merkezlerine, Orta Doğulu kullanıcılar bölgesel DC'lere
- Esnek politikalar: her zaman birincil tercih et (Global Availability), eşit dağılım (Round Robin) veya bağlantı bilincine sahip (Least Connections)

→ **[F5 GTM ve GSLB Deep Dive: Global Trafik Yönetimi ve DNS Failover](/tr/technology/f5-gtm-gslb-global-traffic-management/)**

---

### WAF — Web Application Firewall (ASM / Advanced WAF)

Bir ağ firewall'u L3/L4'te çalışır. Bir POST isteği gövdesinin SQL injection payload içerip içermediğini inceleyemez. WAF inceleyebilir.

F5 WAF, SSL sonlandırmasından sonra HTTP/HTTPS uygulama trafiğini inceleyerek LTM virtual server'ında inline çalışır. Bu konumlama, şifresi çözülmüş içeriğe tam görünürlük sağlar.

F5 iki WAF katmanı sunar:
- **ASM** — bilinen saldırılara karşı imza tabanlı koruma, OWASP Top 10 kapsamı, parametre ve çerez zorunluluğu
- **Advanced WAF** — davranışsal bot savunması, credential stuffing koruması, JavaScript challenge'ları ve L7 DoS azaltmayı ekler

WAF'ın koruduğu şeyler: SQL injection, XSS, CSRF, parametre tampering, çerez zehirlenmesi, zorla gezinme, bot trafiği ve uygulama katmanı DoS.

→ **[F5 WAF Deep Dive: ASM ve Advanced WAF ile Uygulama Güvenliği](/tr/technology/f5-waf-asm-advanced-waf-application-security/)**

---

### APM — Access Policy Manager

APM, F5'in kimlik ve erişim modülüdür — F5'in trafik tesliminin ötesine geçerek **erişim kontrolüne** girdiği yer.

- **SSL VPN** — BIG-IP Edge Client aracılığıyla tam ağ düzeyinde uzak erişim, Cisco AnyConnect veya Fortinet SSL VPN ile karşılaştırılabilir
- **Zero Trust Network Access (ZTNA)** — tam ağı açığa çıkarmadan kimlik bilincine sahip, uygulama başına erişim
- **SSO** — uygulamalar genelinde sorunsuz kimlik doğrulama için Kerberos, SAML, OAuth entegrasyonu
- **MFA entegrasyonu** — RADIUS, LDAP, Active Directory, RSA SecurID
- **Endpoint inspection** — erişim vermeden önce cihaz sağlığını doğrulama (AV durumu, yama seviyesi, domain üyeliği)

APM'nin bağımsız VPN çözümlerine göre avantajı: LTM ile aynı donanım ve yönetim düzlemini paylaşır. Hem uygulama teslimi hem de uzak erişim için tek platform.

---

### AFM — Advanced Firewall Manager

AFM, F5 platformuna ağ düzeyinde firewall özellikleri ekler:

- L3/L4 stateful paket incelemesi — ADC üzerinde inline çalışan geleneksel bir ağ firewall'una benzer
- **DoS ve DDoS koruması** — donanım hızlarında hız sınırlama, protokol anomali tespiti, TCP SYN flood azaltma
- **IP intelligence** — F5'in tehdit istihbaratı beslemeleri aracılığıyla bilinen kötü IP'leri, Tor çıkış node'larını, botnet C2 adreslerini engelleme
- Ağ Adresi Çevirisi (NAT) politikaları

AFM, organizasyonların firewall ve ADC işlevlerini tek bir platformda birleştirmek istediğinde veya ADC'nin kendisine özel bir koruma katmanı ihtiyaç duyulduğunda kullanılır.

---

### BGP ve Dinamik Routing

F5'in en az bilinen özelliklerinden biri: **BIG-IP tam bir routing yığını çalıştırır**.

TMOS, BGP, OSPF, route domain'li statik rotalar (VRF eşdeğeri) ve ECMP destekler. Pratikte BGP en ilgili olanıdır:

- F5, BGP routing'e katılabilir ve Virtual IP adreslerini BGP rotaları olarak duyurabilir
- Büyük kurumsal ve servis sağlayıcı ortamlarında, BGP aracılığıyla **anycast VIP duyurusu**, aynı VIP IP'nin birden fazla veri merkezinden duyurulmasına olanak tanır — routing doğal olarak istemcileri en yakın sağlıklı siteye yönlendirir
- Planlı bakım pencerelerinde BGP çekilmesi, manuel DNS değişikliklerine gerek kalmadan trafiği otomatik olarak DR sitelerine kaydırır

Çalıştığım bankacılık ortamında, planlı bakım sırasında VIP duyurularını dinamik olarak çekmek için F5 ile çekirdek routing katmanı arasında BGP kullandık — temiz, otomatik, DNS değişikliği gerektirmiyor.

---

### Link Controller

Link Controller, birden fazla ISP bağlantısında giden internet bağlantısını yönetir:

- Birden fazla upstream ISP bağlantısında load balancing
- Maliyet tabanlı routing — daha ucuz bağlantıları tercih et, gerektiğinde premium bağlantılara geç
- Bağlantı arızasında otomatik yeniden yönlendirme ile ISP sağlık izleme

Basit aktif-yedek yerine akıllı dağılım isteyen çok ISP bağlantısı olan organizasyonlar için en ilgili modüldür.

---

### iRule'lar ve iRules LX

iRule'lar, F5'in programlanabilir trafik katmanıdır — TMOS veri düzleminde hat hızında çalışan Tcl tabanlı betikler. Modüller genelinde uygulanır ve trafiğin herhangi bir yönünü manipüle edebilir: başlıklar, URI'ler, çerezler, routing kararları, SSL özellikleri.

iRules LX, daha karmaşık mantık ve harici API entegrasyonları için bunu bir Node.js çalışma zamanıyla genişletir.

iRule'lar, standart dışı uygulama gereksinimleri olan organizasyonlar için F5'i benzersiz biçimde esnek kılan şeydir — hiçbir profil veya politika kullanım senaryosunu karşılamadığında, bir iRule genellikle karşılar.

---

## F5 Ne Zaman Mantıklıdır — Ne Zaman Değil?

F5 BIG-IP güçlü, operasyonel açıdan olgun ve pahalıdır. Onu kullanma kararı yalnızca itibara değil, belirli gereksinimlere dayanmalıdır.

**F5 doğru seçimdir:**
- SSL/TLS sonlandırma hacmi yüksek olduğunda — fiziksel cihazlardaki donanım hızlandırması, yazılım çözümlerinin ekonomik olarak karşılayamadığı saniyede binlerce oturumu yönetir
- Uygulamalar, daha basit proxy'lerin uygulama kodu değişiklikleri olmadan ifade edemeyeceği karmaşık trafik mantığı (iRule'lar) gerektirdiğinde
- Birden fazla veri merkezi otomatik DNS düzeyinde failover (GTM) gerektirdiğinde
- Düzenleyici gereklilikler ayrıntılı denetim loguyla WAF zorunlu kıldığında
- Uygulama teslimi, VPN ve L7 güvenliği için tek bir platforma ihtiyaç duyulduğunda — operasyonel karmaşıklığı azaltmak
- Görev-kritik uygulamalar bağlantı durumu yansıtma ile saniye altı HA failover gerektirdiğinde

**Alternatifleri değerlendirin:**
- Altyapınız tamamen cloud-native olduğunda — AWS ALB, Azure Load Balancer veya GCP Load Balancing çoğu kullanım senaryosunu şirket içi donanım gerektirmeden karşılar
- Trafik hacimleri ılımlı ve Nginx Plus veya HAProxy gereksinimlerinizi çok daha düşük maliyetle karşıladığında
- Uygulamalar durumsuz ve session persistence gerekli olmadığında
- TCO birincil kısıt ve açık kaynak çözümler ekibiniz için operasyonel olarak uygulanabilir olduğunda

Dürüst özet: şirket içi altyapıya ve görev-kritik uygulama gereksinimlerine sahip bankacılık, telekom ve büyük kurumlarda F5 baskın platform olmayı sürdürüyor. Cloud-native veya maliyet kısıtlı ortamlarda, F5 lisanslamaya bağlanmadan önce alternatifleri ciddiye alın.

---

## Bu Seri

Bu yazı başlangıç noktasıdır. Her modülün özel bir deep dive'ı vardır:

- 🔧 **[F5 LTM Deep Dive: Virtual Server'lar, iRule'lar, SSL Offloading ve HA](/tr/technology/f5-ltm-virtual-server-irule-ssl-offloading-ha/)** — Full-proxy mimarisi, pool yapılandırması, health monitor'lar, iRule örnekleri, session persistence, HA kümeleme ve sıfır downtime 30 cihaz migrasyon rehberi
- 🌐 **[F5 GTM ve GSLB Deep Dive: Global Trafik Yönetimi ve DNS Failover](/tr/technology/f5-gtm-gslb-global-traffic-management/)** — Wide IP'ler, iQuery, topoloji routing, TTL stratejisi, aktif-aktif ve aktif-yedek DC desenleri
- 🛡️ **[F5 WAF Deep Dive: ASM ve Advanced WAF ile Uygulama Güvenliği](/tr/technology/f5-waf-asm-advanced-waf-application-security/)** — Güvenlik politikası modelleri, OWASP Top 10 kapsamı, bot savunması, L7 DoS koruması ve şeffaftan engellemeye deployment stratejisi

---

## İlgili Yazılar

- 🛡️ [Network Packet Broker (NPB) Masterclass](/tr/posts/network-packet-broker-masterclass/) — Tam yığın genelinde trafik görünürlüğü
- 🔐 [Zero Trust Zihniyeti: Güvenliği Bir Mimari Olarak Mühendislemek](/tr/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — APM ve WAF'ın Zero Trust'ta yeri
- 🏗️ [IT Altyapısı Ürünler Koleksiyonu Değildir](/tr/architecture/it-infrastructure-not-a-collection-of-products/) — ADC yerleşiminin arkasındaki sistem düşüncesi
- 🎯 [Ağ Altyapısı Ürün Seçimi: Stratejik Kriterler](/tr/architecture/network-product-selection-strategy/) — ADC satıcılarını nesnel olarak nasıl değerlendirirsiniz