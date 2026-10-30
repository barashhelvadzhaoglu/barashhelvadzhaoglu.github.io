---
title: "Cisco SD-WAN: Catalyst SD-WAN ve Kurumsal Mimari Yaklaşımı"
seoTitle: "Cisco SD-WAN İncelemesi | Catalyst SD-WAN, Viptela Mimarisi ve Kurumsal Kullanım Senaryoları"
description: "Cisco'nun SD-WAN platformuna kapsamlı bir bakış: Viptela satın alması, Catalyst SD-WAN mimarisi, vManage ve kurumsal ortamlarda Cisco yaklaşımının rakiplerle karşılaştırması."
date: 2026-10-30T06:35:00+01:00
keywords:
  - Cisco SD-WAN
  - Catalyst SD-WAN
  - Cisco Viptela
  - vManage SD-WAN
  - Cisco SASE
  - Cisco SD-WAN mimarisi
  - Cisco ThousandEyes SD-WAN
  - kurumsal SD-WAN
tags:
  - SD-WAN
  - Cisco
  - Ağ Teknolojileri
draft: false
---

# Cisco SD-WAN: Catalyst SD-WAN ve Kurumsal Mimari Yaklaşımı

Cisco'nun SD-WAN yolculuğu, son on yılın en önemli kurumsal ağ satın alımlarından birinden geçiyor. 2017 yılında Cisco, doğrudan amaca yönelik bir SD-WAN girişimi olan Viptela'yı yaklaşık 610 milyon dolara satın aldı. Bu satın alma, Cisco'nun bugün **Catalyst SD-WAN** (eski adıyla Cisco SD-WAN ve öncesinde Viptela SD-WAN) olarak adlandırdığı çözümün temelini oluşturdu. Viptela mirasını anlamak, Cisco'nun platformunu bugün niteleyen hem mimari güçleri hem de operasyonel karmaşıklığı açıklamaya yardımcı olur.

---

## Viptela Mimarisi

Viptela, sıfırdan dağıtık ve ölçeklenebilir bir SD-WAN fabric yapısı olarak inşa edildi. Temel tasarımı, WAN mimarisini dört fonksiyonel katmana (plane) ayırdı:

**vManage** — merkezi yönetim ve orkestrasyon katmanı. Tüm SD-WAN lokasyonlarında konfigürasyon, izleme ve policy yönetimi için tek bir gösterge paneli (dashboard). vManage, ağ yöneticilerinin birincil arayüzüdür.

**vSmart Controller** — control plane. Overlay Management Protocol (OMP) kullanarak tüm edge cihazlarına routing bilgilerini ve SD-WAN policy'lerini dağıtır. vSmart veri trafiğini iletmez (forward etmez); yalnızca veri trafiğinin nereye gideceğini kontrol eder.

**vBond** — orkestrasyon katmanı. NAT traversal ve kimlik doğrulama süreçlerini yöneterek edge cihazları ile SD-WAN fabric'inin geri kalanı arasındaki ilk bağlantıyı sağlar. Edge cihazları sisteme dahil edildikten (onboard edildikten) sonra vBond'un rolü minimuma iner.

**vEdge / Catalyst SD-WAN Router** — her lokasyondaki data plane. Cisco artık SD-WAN işlevselliğini Catalyst 8000 serisi router'larda ve ISR router'larda (SD-WAN yazılımı aracılığıyla) sunmanın yanı sıra, bulut dağıtımları için sanal appliance'lar da sağlamaktadır.

Bu dört bileşenli mimari, bazı rakip platformlara kıyasla daha karmaşıktır; örneğin Fortinet'in FortiOS'i, tüm SD-WAN işlevlerini tek bir işletim sistemi imajına entegre eder. Ancak bu mimari ölçeklenebilirlik için tasarlanmıştır. Binlerce lokasyona sahip çok büyük dağıtımlar, sorumlulukların ayrılmasından (separation of concerns) büyük fayda sağlar: control plane, data plane performansını etkilemeksizin yatayda ölçeklenebilir.

---

## OMP: Fabric Protokolü

OMP (Overlay Management Protocol), Cisco SD-WAN fabric yapısını bir arada tutan protokoldür. vSmart controller'lar ile tüm vEdge/Catalyst router'lar arasında çalışır ve şunları dağıtır:

- Routing bilgileri (BGP route anonslarına benzer)
- SD-WAN policy'leri (application-aware routing kuralları, data policy'leri)
- Güvenlik bilgileri (IPsec tünelleri için security association'lar)

Bu merkezi dağıtım modeli, policy değişikliklerinin tüm lokasyonlara hızlı ve tutarlı bir şekilde yayılmasını sağlar. Bir ağ mühendisi vManage üzerinde bir application-aware routing policy'sini değiştirdiğinde, vSmart güncellenen policy'yi etkilenen tüm edge cihazlarına otomatik olarak iletir (push eder). Cihazlara tek tek müdahale etmeye gerek kalmaz.

Edge'ler arasındaki IPsec tünelleri OMP tarafından dağıtılan bilgilere dayanarak kurulur ve saniye altı (sub-second) hat kalitesi izleme için **BFD (Bidirectional Forwarding Detection)** protokolünü destekler; bu mekanizma, bir WAN hattında bozulma olduğunda hızlı yol failover'ı sağlar.

---

## Catalyst SD-WAN'da Application-Aware Routing

Cisco'nun application-aware routing özelliği kavramsal düzeyde diğer SD-WAN üreticileriyle benzer şekilde çalışır, ancak kendine özgü bazı uygulama karakteristiklerine sahiptir:

**Uygulama tanımlama (Application identification)**, Cisco'nun NBAR2 (Network-Based Application Recognition) motorunu kullanır — sürekli güncellenen binlerce uygulama imzasından oluşan kütüphanesiyle sektördeki en olgun uygulama sınıflandırma teknolojilerinden biridir. NBAR2; dinamik portlar, şifrelenmiş protokoller ve bulut uygulama varyantlarını kullanan uygulamaları tespit edebilir.

**SLA sınıfları (SLA classes)**, her trafik kategorisi için kabul edilebilir performans eşiklerini (latency, jitter, packet loss) tanımlar. Bir WAN tünelinin ölçülen performansı SLA eşiğinin altına düşerse, etkilenen trafik gereksinimleri karşılayan başka bir tünele otomatik olarak failover yapar.

**Data policy'leri**, basit SLA eşleştirmesinin ötesinde ayrıntılı trafik yönlendirmesi (traffic steering) sağlar; trafiği kaynak/hedef, uygulama, DSCP değeri veya bunların bir kombinasyonuna göre yönlendirebilir ve doğrudan internet erişimi (direct internet access), güvenlik appliance'ları üzerinden service chaining veya bir merkez üzerinden backhaul zorunluluğu getirebilir.

---

## ThousandEyes Entegrasyonu: WAN'ın Ötesinde Görünürlük

Cisco'nun SD-WAN platformundaki ayırt edici yeteneklerden biri, Cisco'nun 2020 yılında satın aldığı internet ve bulut zekası platformu olan **ThousandEyes** ile entegrasyondur.

ThousandEyes, yalnızca kurumsal WAN genelinde değil, internet ve bulut sağlayıcı ağları üzerinde de uçtan uca görünürlük sunar. SD-WAN bağlamında bu, Cisco müşterilerinin yalnızca Frankfurt'a giden MPLS hatlarında %5 paket kaybı olduğunu görmekle kalmayıp, aynı zamanda Frankfurt'taki Azure ExpressRoute peering noktasında tıkanıklık (congestion) yaşandığını ve bunun bir lokasyondaki tüm kullanıcıların Microsoft 365 performansını etkilediğini — henüz helpdesk'e ticket gelmeye başlamadan önce — tespit edebilmeleri anlamına gelir.

Bu görünürlük katmanı, uygulama performans izlemesini herhangi bir şirket içi (on-premises) SD-WAN platformunun tek başına görebileceğinin ötesine taşır. Karmaşık bulut bağımlılıkları olan büyük kurumlar için ThousandEyes entegrasyonu, rakip SD-WAN üreticilerinin yerel araçlarıyla boy ölçüşemeyeceği bir sorun giderme (troubleshooting) bağlamı sunar.

---

## Catalyst 8000 Serisi: Donanım Platformu

Cisco'nun SD-WAN edge dağıtımları için birincil donanım platformu, Cisco'nun şube portföyünde ISR 4000 serisinin yerini alan **Catalyst 8000 serisidir**. Catalyst 8000, tanıdık Cisco IOS routing özellik setini SD-WAN overlay yetenekleriyle birleştiren SD-WAN yazılım yığını ile IOS XE çalıştırır.

SD-WAN'ı Catalyst 8000 üzerinde çalıştırmanın başlıca avantajları:
- SD-WAN'ın yanı sıra eksiksiz IOS XE özellik seti: Underlay routing için OSPF, BGP, EIGRP; LAN yedekliliği için HSRP/VRRP; MQC ile QoS
- Cisco'nun QuantumFlow işlemcileriyle donanım tabanlı paket iletimi (hardware-based forwarding)
- Daha küçük lokasyonlarda aynı cihazın WAN router, SD-WAN edge ve LAN dağıtım (distribution) router'ı olarak görev yapabilmesi
- Mevcut Cisco IOS uzmanlığına sahip organizasyonlar için tanıdık operasyonel model

Cisco ayrıca AWS, Azure ve Google Cloud dağıtımları için **Catalyst SD-WAN Virtual** (eski adıyla vEdge Cloud) çözümünü sunarak SD-WAN fabric yapısının yerel olarak bulut ortamlarına genişletilmesine olanak tanır.

---

## Cisco SASE: Umbrella ve Meraki Entegrasyonu

Cisco'nun SASE stratejisi, WAN edge tarafındaki Catalyst SD-WAN ile buluttan sunulan güvenlik (DNS güvenliği, secure web gateway, CASB, ZTNA) için **Cisco Umbrella**'nın bir araya getirilmesine dayanır. Bu entegrasyon, SD-WAN policy'lerinin şube lokasyonlarındaki internete giden trafiği merkezi bir veri merkezine backhaul etmeye gerek kalmadan denetim için en yakın Umbrella PoP noktasına yönlendirmesini sağlar.

Daha basit dağıtımlar için Cisco Meraki, Catalyst SD-WAN'a göre daha az gelişmiş özelliğe sahip olmakla birlikte çok daha yalın bir operasyonel modele sahip bulut yönetimli bir SD-WAN alternatifi sunar. Meraki, operasyonel sadeliğin özellik derinliğinden daha ağır bastığı orta ölçekli pazar (mid-market) ile dağıtık perakende/konaklama sektörünü hedefler.

---

## Cisco SD-WAN'ın Öne Çıktığı Alanlar

**Mevcut Cisco altyapısına sahip büyük kurumsal ortamlar**
Cisco Catalyst switch'leri, Cisco kablosuz ağ çözümlerini (DNA Center), NAC için Cisco ISE'ı ve Cisco firewall'larını çalıştıran organizasyonlar Catalyst SD-WAN'dan en yüksek değeri elde eder. SD-WAN ile Cisco DNA Center arasındaki entegrasyon, kampüs ve WAN genelinde eşzamanlı olarak intent-based networking yaklaşımını mümkün kılar. DNA Center'da bir kez tanımlanan policy, erişim (access) katmanından WAN edge'e kadar tutarlı bir şekilde uygulanır.

**Karmaşık routing gereksinimleri**
Catalyst SD-WAN, eksiksiz IOS XE routing yığınını korur. Karmaşık underlay routing gereksinimleri olan şube lokasyonları — birden fazla ISP ile BGP peering, karmaşık policy-based routing, MPLS VPN entegrasyonu — SD-WAN dışı routing yetenekleri kısıtlı olan üreticilere kıyasla Cisco'nun platformundan çok daha iyi verim alır.

**Geniş ölçekte görünürlük ve sorun giderme**
vManage analitiği ile ThousandEyes kombinasyonu, Cisco SD-WAN'a rekabet edilmesi zor bir sorun giderme (troubleshooting) yeteneği kazandırır. Binlerce kullanıcı için WAN performansını yöneten ağ operasyon ekipleri (NOC) için bu görünürlük araçları, platforma yapılan yüksek yatırımı haklı çıkarır.

**Uyumluluk gereksinimleri olan regüle sektörler**
Cisco'nun kurumsal pazardaki konumu, vManage'deki denetim izi (audit trail) yetenekleri ve kapsamlı uyumluluk dokümantasyonu, Catalyst SD-WAN'ı katı satın alma ve uyumluluk gereksinimlerine sahip finansal hizmetler, sağlık ve kamu sektörü organizasyonları için güvenilir bir seçenek haline getirir.

---

## Cisco SD-WAN'ın Kısıtları

**Operasyonel karmaşıklık**
Dört bileşenli mimari (vManage, vSmart, vBond, edge'ler), daha yalın platformlara göre daha fazla operasyonel iş yükü (overhead) gerektirir. vSmart yedekliliğinin yönetimi, sertifika yaşam döngüleri ve controller yazılım güncellemeleri, daha küçük organizasyonların veya sınırlı ağ mühendisliği personeline sahip yapıların yükünü artırabilecek karmaşıklıklar getirir.

**Maliyet**
Cisco SD-WAN lisanslaması ucuz değildir. Platform lisanslama modeli (DNA Software abonelik katmanları) donanım maliyetleriyle birleştiğinde Catalyst SD-WAN'ı pazarın üst segmentine konumlandırır. Küçük ve orta ölçekli organizasyonlar genellikle diğer çözümlerde daha iyi bir fiyat/performans değeri bulur.

**Güvenlik entegrasyonu**
SD-WAN ve NGFW'ün tek bir işletim sisteminde birleştiği Fortinet'in aksine, Cisco'nun SD-WAN ve güvenlik çözümleri API'ler ve policy koordinasyonu yoluyla entegre olan ayrı ürünlerdir. Entegrasyon çalışır, ancak Fortinet'in bütünleşik yaklaşımı kadar kesintisiz ve pürüzsüz değildir. Her şubede derinlemesine güvenlik denetimine (deep security inspection) ihtiyaç duyan kurumların ayrı güvenlik appliance'ları veya buluttan sunulan güvenlik çözümleri kurup yönetmesi gerekir; bu da maliyeti ve karmaşıklığı artırır.

---

## Tipik Dağıtım Mimarisi

Standart bir Cisco Catalyst SD-WAN dağıtımı:

- **vManage / vSmart / vBond:** Bulut hizmeti olarak barındırılır (Cisco tarafından barındırılan veya şirket içinde/bulutta self-hosted)
- **Hub lokasyonları:** Birden fazla WAN hattına sahip Catalyst 8300 veya 8500 serisi; spoke lokasyonlar için bölgesel hub görevi görür
- **Şube (branch) lokasyonları:** Çift WAN (MPLS + geniş bant) bağlantılı Catalyst 8200 veya 8300 serisi; vManage üzerinden zero-touch provisioning ile devreye alınır
- **Bulut lokasyonları:** AWS/Azure ortamlarında Catalyst SD-WAN Virtual; şirket içi ve bulut iş yükleri genelinde tutarlı policy uygulanmasını sağlar
- **Uzak kullanıcılar (Remote users):** Buluttan sağlanan güvenlik için Umbrella ile entegre Cisco AnyConnect veya Cisco Secure Client

---

## Özet

Cisco Catalyst SD-WAN, hem Viptela mirasını hem de Cisco'nun bu mimariye yaptığı sürekli yatırımı yansıtan derinlikli yeteneklere sahip kurumsal düzeyde bir platformdur. Gelişmiş routing gereksinimlerinin, uçtan uca görünürlüğün ve daha geniş bir Cisco altyapısıyla entegrasyonun kritik olduğu büyük ve karmaşık ortamlarda öne çıkar.

Bunun karşılığındaki ödünleşim (trade-off) ise maliyet ve karmaşıklıktır. Daha sade bir operasyonel modele, daha sıkı bir güvenlik entegrasyonuna veya lokasyon başına daha düşük maliyete ihtiyaç duyan organizasyonlar için Fortinet, HPE Aruba veya Palo Alto kendi özel gereksinimlerine daha uygun olabilir.

Halihazırda Cisco ekosistemine yoğun yatırım yapmış olan kurumlar için — DNA Center, ISE, Umbrella, Catalyst switch altyapısı — Catalyst SD-WAN, farklı bir WAN üreticisiyle yakalanması oldukça zor olan bir mimari uyum ve tutarlılık sunar.

---

*Bu serinin bir sonraki yazısı: [HPE Aruba SD-WAN — EdgeConnect ve WAN Optimizasyonu Mirası](/en/posts/hpe-aruba-sd-wan/)*
