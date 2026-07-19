---
title: "OT Ağları: Bir IT Mühendisinin Fabrika Zemininde Gerçekte Karşılaştıkları"
description: "IT mühendisi için OT güvenlik rehberi — Purdue modeli, Katman 2 firewall, OT imzaları, yama yapılamayan sistemler ve endüstriyel 802.1X."
date: 2026-04-03
draft: false

cover:
  image: "/img/postimages/ot-network-security-cover.webp"
  alt: "OT Ağ Güvenliği — IT Mühendisinin Endüstriyel Ağ Rehberi"
  relative: false

tags: ["OT Güvenliği", "Endüstriyel Ağ", "Purdue Modeli", "SCADA", "ICS", "Firewall", "Ağ Güvenliği", "Modbus", "PROFINET"]
categories: ["Teknoloji"]
keywords:
  - OT ağ güvenliği IT mühendisi
  - Purdue modeli endüstriyel ağ
  - OT firewall Katman 2 deployment
  - OT odaklı firewall imzaları
  - Modbus PROFINET endüstriyel protokoller
  - IT OT ağ segmentasyonu
  - eski PLC Windows XP güvenliği
  - 802.1X OT ağ zorlukları
  - endüstriyel ağ DMZ
  - Fortinet OT firewall

showToc: true
TocOpen: true
---

# OT Ağları: Bir IT Mühendisinin Fabrika Zemininde Gerçekte Karşılaştıkları

Çoğu ağ mühendisi kariyerini IT altyapısında geçirir — kurumsal LAN'lar, veri merkezleri, kampüs ağları, bulut bağlantısı. Sonra bir gün masanıza fabrika, depo otomasyon sistemi veya bir tesis içeren bir proje düşer. Ve birden tanıdık kurallar tam olarak geçerli olmaz.

OT (Operational Technology — Operasyonel Teknoloji) ağları IT ağları değildir. Cihazlar farklıdır, protokoller farklıdır, öncelikler farklıdır ve — kritik olarak — bir şeyi yanlış yapmanın sonuçları farklıdır. IT'de yanlış yapılandırılmış bir switch ağ kesintisine neden olur. OT'de yanlış yapılandırılmış bir ağ değişikliği üretim hattını durdurabilir, pahalı ekipmanı hasar görebilir veya kritik altyapı senaryolarında fiziksel güvenlik riskleri yaratabilir.

Bu yazı IT mühendisinin perspektifinden yazılmıştır — bir firewall eklemek, bir ağı segmente etmek veya endüstriyel bir sistemi kurumsal ağa bağlamak için çağrılan kişi. Derin bir SCADA mühendisliği rehberi değil, karşılaşacaklarınız ve herhangi bir şeye dokunmadan önce düşünmeniz gerekenler için pratik bir yönlendirme.

---

## Temel Fark: Gizlilik Yerine Erişilebilirlik

IT güvenliğinde klasik öncelik sırası **CIA: Gizlilik, Bütünlük, Erişilebilirlik**'tir. Gizlilik önce gelir — verileri yetkisiz erişimden korumak birincil endişedir.

OT'de öncelik sırası esasen **AIC: Erişilebilirlik, Bütünlük, Gizlilik**'tir. Üretim hattı çalışmaya devam etmelidir. IT ortamında 30 saniyelik ağ kesintisi bir rahatsızlıktır. Bir üretim tesisinde 30 saniyelik ağ kesintisi, ıskarta ürün, hasar görmüş makineler veya bir güvenlik olayı anlamına gelebilir.

Bu tersine çevirme, OT ortamındaki her ağ kararı için doğrudan sonuçlar doğurur:

- **OT cihazlarını kapsamlı planlama olmadan yeniden başlatmazsınız.** IT ortamında bir Cisco switch dramaya gerek kalmadan 3 dakikada yeniden başlatılabilir. Üretim hattına gömülü bir switch, planlanmış bakım penceresi, üretim durdurma ve tesis operasyon ekibiyle koordinasyon gerektirebilir.
- **Yama yönetimi basit değildir.** IT'de sistemleri düzenli olarak yamarsınız. OT'de birçok sistem yamalanamamaktadır — satıcı yazılım sürümünü sertifikalandırır ve herhangi bir değişiklik sertifikayı geçersiz kılar veya pahalı yeniden doğrulama gerektirir.
- **Ağ değişiklikleri koordinasyon gerektirir.** IT'de VLAN eklemek rutindir. OT'de aynı değişiklik üretim yöneticilerinden, güvenlik mühendislerinden ve ekipman satıcılarından onay gerektirebilir.

Bunu çalışmaya başlamadan önce anlamak yalnızca mesleki nezaket değildir — gerçek operasyonel olayları önler.

---

## Purdue Modeli: OT Ağ Mimarisinin Haritası

Purdue Modeli (ISA-95), endüstriyel ağ mimarisini anlamak için standart çerçevedir. En alttaki fiziksel süreçlerden en üstteki kurumsal IT'ye kadar seviyeleri tanımlar:

```
Seviye 4/5  — Kurumsal IT Ağı (ERP, e-posta, kurumsal LAN)
─────────────────────────────────────────────────────────────
              IT/OT DMZ  ← IT mühendislerinin çalıştığı sınır
─────────────────────────────────────────────────────────────
Seviye 3    — Operasyonlar / Saha Yönetimi
              (Tarihçi sunucular, mühendislik iş istasyonları,
               HMI sunucuları, toplu yönetim)

Seviye 2    — Denetimsel Kontrol
              (SCADA sunucuları, HMI istemcileri, DCS iş istasyonları)

Seviye 1    — Temel Kontrol
              (PLC'ler, DCS kontrolörleri, RTU'lar)

Seviye 0    — Fiziksel Süreç
              (Sensörler, aktüatörler, motorlar, valfler)
```

**IT mühendislerinin tipik olarak çalıştığı yer:** IT/OT DMZ ve Seviye 3. Kurumsal IT ağı ile OT ortamı arasındaki bağlantının yönetildiği yer burasıdır. Firewall projeleri, tarihçi bağlantısı, uzak erişim çözümleri ve ağ segmentasyonu çalışmalarının yapıldığı yer.

**IT mühendislerinin nadiren doğrudan dokunduğu şeyler:** Seviye 0, 1 ve 2 — gerçek kontrol sistemleri, PLC'ler ve SCADA bileşenleri. Bunlar OT/otomasyon mühendisleri ve ekipman satıcılarının alanıdır.

IT ile OT arasındaki DMZ, endüstriyel ağ mimarisindeki en kritik sınırdır. Var olmalıdır. Trafik kurumsal ağ ile OT ortamı arasında serbestçe akmamalıdır.

---

## OT Protokolleri: Bu Ağlarda Neler Çalışıyor

Bir OT ağına ilk kez ağ analizörü bağladığınızda, hiçbir IT ağında görünmeyen protokoller göreceksiniz. Bunların ne olduğunu — yüzey düzeyinde bile olsa — anlamak, makul firewall ve segmentasyon kararları vermenize yardımcı olur.

### Modbus

1979'da geliştirilen en eski endüstriyel protokol. Üretim, kamu hizmetleri ve bina otomasyonunda hâlâ yaygın biçimde kullanılmaktadır.

- **Modbus RTU:** Seri tabanlı (RS-232, RS-485). Ethernet değil, fiziksel seri bağlantılar üzerinden çalışır.
- **Modbus TCP:** TCP/IP içinde kapsüllenmiş Modbus. Port 502 üzerinde çalışır.

Modbus'ta **kimlik doğrulama yoktur, şifreleme yoktur, yetkilendirme yoktur**. Modbus etkin bir kontrolörün port 502'sine ulaşabilen ağdaki herhangi bir cihaz sensör değerlerini okuyabilir veya kontrol komutları yazabilir. Bu tarihsel bir ihmal değildir — Modbus, fiziksel erişimin güvenlik kontrolü olduğu izole seri ağlar için tasarlanmıştır.

Modbus TCP, OT segmentinin dışından erişilebilen bir Ethernet ağında olduğunda, kimlik doğrulamanın yokluğu önemli bir risktir. Firewall politikası, Modbus etkin kontrolörlere hangi cihazların ulaşabileceğini kısıtlamalıdır.

### DNP3 (Distributed Network Protocol)

Kamu hizmetlerinde yaygın — enerji üretimi, su arıtma, petrol ve gaz. Başlangıçta kontrol merkezleri ile uzak saha cihazları (trafo merkezleri, pompa istasyonları) arasındaki SCADA iletişimi için tasarlanmıştır.

DNP3'ün temel kimlik doğrulama uzantıları vardır (Güvenli Kimlik Doğrulama Sürüm 5), ancak dağıtılmış uygulamaların çoğu hâlâ orijinal kimlik doğrulamasız sürümü kullanmaktadır. Modbus gibi, izole ağlar için tasarlanmış ve çoğunlukla kağıt üzerinde mevcut olan güvenlik özellikleri olmadan dağıtılmıştır.

### OPC-UA (OPC Unified Architecture)

Eski protokollerdeki güvenlik açıklarını gidermek için özel olarak tasarlanmış modern endüstriyel iletişim standardı. OPC-UA şunları destekler:
- Sertifika tabanlı kimlik doğrulama
- Şifreli iletişim
- İnce taneli yetkilendirme (hangi istemcilerin hangi veri noktalarını okuyabileceği)

OPC-UA, yeni kurulumlarda ve Tarihçi sunucu bağlantısında karşılaşacağınız protokoldür — Seviye 3 sistemlerin bir güvenlik sınırını korurken Seviye 2 kontrolörlerden veri topladığı yöntem.

### PROFINET

Siemens'in endüstriyel Ethernet protokolü, Avrupa üretiminde (otomotiv, gıda işleme, ilaç) baskındır. PROFINET standart Ethernet üzerinde çalışır ancak belirli EtherType değerleri kullanır ve gerçek zamanlı açıdan hassastır — milisaniyelik gecikmeler önemlidir.

PROFINET'in neredeyse hiç yerleşik güvenliği yoktur. Fiziksel olarak izole edilmiş bir ağı varsayar. PROFINET kontrolörlü ortamlarda, ağ segmentasyonu katı olmalıdır — PROFINET trafiği asla kendi özel VLAN'ının dışına çıkmamalıdır.

### EtherNet/IP

Rockwell Automation / Allen-Bradley'nin endüstriyel Ethernet protokolü. Kuzey Amerika üretiminde yaygın. PROFINET'e benzer güvenlik özellikleri — izole ağlar için tasarlanmış, sınırlı kimlik doğrulama.

---

## IT Mühendisinin Gerçekte Yapması İstenenler

Pratikte, IT/ağ mühendisleri OT projelerine dahil olduğunda, talep genellikle şu kategorilerden birine girer:

### Senaryo 1: "PC ile Makine Arasına Firewall Ekle"

En yaygın senaryo. Bir Windows PC (SCADA yazılımı veya HMI çalıştıran), aralarında hiçbir ağ cihazı olmadan Ethernet aracılığıyla doğrudan bir PLC veya üretim makinesine bağlıdır. Talep, bir güvenlik katmanı eklemektir.

```
Önce:
  [Windows HMI PC] ──────────────── [PLC / Makine Kontrolörü]

Sonra (tipik yaklaşım):
  [Windows HMI PC] ── [Firewall] ── [PLC / Makine Kontrolörü]
```

**Katman 2 şeffaf firewall deployment'ı:**

Bu yola firewall eklemenin operasyonel açıdan en güvenli yolu, **Katman 2 şeffaf mod**dur ("bump in the wire" veya köprü modu olarak da adlandırılır). Firewall trafiği şeffaf olarak geçirir — ne cihaz onun varlığından haberdar olur, ne IP adresleri değişir ne de routing değişiklikleri yapılır. Firewall arızalanırsa, trafik kaldırılıp doğrudan yeniden bağlanarak geri yüklenebilir.

Bu önemlidir çünkü PLC veya endüstriyel kontrolör üzerindeki IP adreslerini değiştirmek, onunla konuşan uygulama yazılımını yeniden yapılandırmayı gerektirir — bu, satıcı desteği, yeniden sertifikalama ve üretim kesintisi içerebilecek bir süreçtir.

Şeffaf modda:
- PLC mevcut IP adresini korur
- HMI PC mevcut IP adresini korur
- Firewall, yönlendirilmiş bir atlama olmadan trafiği inceler ve politikayı uygular

Bu senaryoda firewall politikası tipik olarak şunları içerir:
- HMI'dan kontrolöre belirli OT protokolü trafiğine izin ver (Modbus port 502, PROFINET, EtherNet/IP)
- Yalnızca gerekli yönetim protokollerine izin ver
- Geri kalanını engelle
- Görünürlük için tüm trafiği logla

### Senaryo 2: "OT Ağını Kurumsal IT'ye Bağla"

Üretim ekibi, fabrika zemininden kurumsal sistemlere veri almak ister — ERP'ye üretim istatistikleri, raporlama veritabanına sensör verileri, uzak izleme yeteneği.

Bu bir DMZ mimarisi gerektirir:

```
[Kurumsal IT Ağı]
         │
    [IT/OT Firewall]   ← Katı politika: yalnızca belirli akışlara izin ver
         │
    [OT DMZ]
    [Tarihçi Sunucu]    ← OT'den veri toplar, IT'ye sunar
         │
    [OT Firewall]       ← OT'yi DMZ'den koruyan ayrı firewall
         │
    [OT Ağı — Seviye 2/3]
```

DMZ prensibi: kurumsal ağ, OT cihazlarına doğrudan ulaşamaz. DMZ'deki Tarihçi sunucu, OT sistemlerinden veri toplar (OT firewall tarafından izin verilir) ve kurumsal sistemlerin kullanımına sunar (IT firewall tarafından izin verilir). Kurumsal ağ ne OT ağına, ne de OT ağı kurumsal ağa doğrudan bağlantı başlatabilir.

**Neden iki firewall, bir değil?** DMZ'deki Tarihçi sunucu ele geçirilirse, herhangi bir ağa erişim yolu sağlamamalıdır. DMZ segmentli tek bir firewall, iki ayrı firewall'dan daha az izolasyon sağlar.

### Senaryo 3: "Düz OT Ağına Segmentasyon Ekle"

Birçok eski OT ortamı tamamen düz bir ağa sahiptir — tüm PLC'ler, HMI'lar, mühendislik iş istasyonları ve hatta bazen kurumsal bağlantılı PC'ler aynı Katman 2 yayın etki alanındadır. Her cihaz diğer her cihaza ulaşabilir.

Bu ağı segmente etmek şunları içerir:
- VLAN yetenekli yönetilen switchler eklemek
- Cihaz türü veya işleve göre VLAN'lar tanımlamak (Seviye 2 kontrolörler, Seviye 3 denetimsel, mühendislik iş istasyonları)
- Katı VLAN arası politikayla bir firewall üzerinden VLAN'lar arasında routing yapmak

**Kritik kısıt:** Herhangi bir ağ değişikliği yapmadan önce mevcut iletişim akışlarını kapsamlı biçimde belgeleyin. Hangi cihazlar hangi cihazlarla konuşur? Hangi portlar üzerinde? Bir PLC ile kontrolörü arasındaki belgelenmemiş iletişim yolunu kıran segmentasyon, üretim hattını durdurur.

IT ortamlarında, akışları birkaç gün izleyerek keşfedebilir ve ardından uygulayabilirsiniz. OT'de, bazı iletişim akışları yalnızca belirli üretim aşamalarında gerçekleşir — haftalık bir toplu işlem, vardiya sonu raporu — ve kısa bir izleme penceresi sırasında görünmez. Segmentasyonu uygulamadan önce tüm iletişim gereksinimlerini belgelemek için OT ekibiyle çalışın.

---

## OT Odaklı Firewall'lar: Satıcıların Geliştirdikleri

Standart IT firewall'ları (NGFW'ler bile) OT protokollerine sınırlı görünürlüğe sahiptir. IP başlıklarını ve TCP/UDP portlarını inceleyebilirler, ancak Modbus TCP komutunun içeriğini anlayamazlar — "sensör değeri oku" ile "aktüatöre kontrol komutu yaz" arasındaki farkı ayırt edemezler.

OT odaklı firewall'lar **endüstriyel protokol incelemesi** ekler — OT protokolü payload'larını ayrıştırma ve protokole özgü içeriğe dayalı politika kararları verme yeteneği.

### İmza Farkı

Standart bir NGFW'nin 2.000–5.000 uygulama imzası olabilir — çoğunlukla IT uygulamaları (HTTP, TLS, DNS, SMB, Office 365, vb.). OT yetenekli bir firewall lisansı, endüstriyel protokoller için yüzlerce ek imza ekler:

- **Modbus TCP:** Okuma isteklerini (HMI'dan kabul edilebilir) yazma komutlarından (yalnızca yetkili sistemlerle kısıtla) ayırt et
- **PROFINET:** Belirli PROFINET servislerini tanımla ve kontrol et
- **EtherNet/IP:** CIP (Common Industrial Protocol) komutlarını ayrıştır
- **DNP3:** DNP3 fonksiyon kodlarını ve nesne türlerini incele
- **OPC-DA/UA:** OPC iletişim yönünü ve veri türlerini kontrol et
- **BACnet:** Bina otomasyon protokolü incelemesi
- Düzinelerce endüstriyel ve bina otomasyon protokolü daha

**Neden önemli:** OT protokolü incelemesi olmadan, bir firewall yalnızca "bu IP o IP'ye bu portta ulaşabilir mi" yi kontrol edebilir. OT incelemesiyle, "HMI, PLC'den Modbus holding registerlarını okuyabilir, ancak coillere yazamaz" ı zorunlu kılabilir — IP/port filtrelemeden temel olarak farklı bir kontrol düzeyi.

### Satıcı Ortamı

**OT Bundle'lı Fortinet FortiGate:**
Fortinet, temel NGFW'yi endüstriyel protokol imzaları ve OT'ye özgü tehdit istihbaratıyla genişleten belirli OT/ICS lisansları sunar. FortiGate, şeffaf modda (Katman 2) veya yönlendirilmiş modda dağıtılabilir. IT için zaten FortiGate çalıştıran ortamlarda, aynı platform her ikisini de yönetir.

**ICS/SCADA içeriğiyle Palo Alto Networks:**
Palo Alto'nun App-ID motoru, endüstriyel protokol tanımlamasını içerir. Industrial IoT Security aboneliği OT cihaz görünürlüğü, risk değerlendirmesi ve protokole özgü politikalar ekler. Bölge tabanlı mimari, Purdue modeli segmentasyonuyla iyi uyum sağlar.

**Claroty, Nozomi Networks, Dragos (OT'ye özel):**
Bunlar geleneksel firewall'lar değildir — OT'ye özgü güvenlik izleme platformlarıdır. SPAN portu aracılığıyla OT ağına bağlanırlar (pasif izleme) ve derin görünürlük sağlarlar: varlık keşfi, protokol analizi, davranışsal temel, anomali tespiti. Trafiği engellemezler ancak genel IT araçlarının sağlayamadığı görünürlük sunarlar. Genellikle standart bir firewall ile birlikte kullanılır.

**Cisco Industrial Network Director:**
Cisco'nun OT odaklı yönetim ve güvenlik platformu, OT ağı görünürlüğü için Cisco endüstriyel switchleri ve firewall'larıyla entegre olur.

### Lisanslama Gerçeği

OT firewall yetenekleri, standart IT NGFW özelliklerinden ayrı olarak lisanslanır. OT projesi için bir firewall belirtiyorsanız, standart kurumsal lisans yeterli değildir — OT/ICS bundle veya eşdeğeri gerekir. Bu hem maliyeti hem de müşteriyle satıcı seçim görüşmesini etkiler.

---

## Yama Sorunu: Dokunamadığınız Eski Sistemler

IT'de yama rutin bir işlemdir. Aylık yama döngüleri, otomatik dağıtım, merkezi yönetim. OT'de yama çoğunlukla imkânsızdır.

Sebepler spesifik ve meşrudur:

**Satıcı sertifikasyonu:** Endüstriyel ekipman üreticileri (Siemens, Rockwell, Schneider, ABB, vb.) sistemlerini belirli yazılım sürümleriyle sertifikalandırır. İşletim sistemi sürümünü değiştirmek veya işletim sistemi yaması uygulamak, ekipman sertifikasyonunu geçersiz kılabilir; orijinal ekipmandan daha pahalıya mal olabilecek ve aylarca sürebilecek bir yeniden doğrulama süreci başlatır.

**Üretim bağımlılığı:** Yama, kesinti gerektirir. Sürekli süreç endüstrilerinde (kimya tesisleri, çelik fabrikaları), "kesinti" planlanmış yıllık bakım penceresi anlamına gelebilir — yama uygulamak için yılda bir fırsat.

**Kullanım ömrü dolmuş yazılım:** Kritik endüstriyel yazılım çalıştıran Windows XP, Windows 2003 Server ve daha eski sistemlerle karşılaşacaksınız. Microsoft bu sistemler için yıllardır güvenlik yaması yayınlamamıştır. Üzerlerinde çalışan endüstriyel yazılım daha yeni Windows sürümlerinde doğrulanmadığı için yükseltilemezler.

**Ağ güvenliği için ne anlama gelir:**

Sistemleri yamalayamazsanız, ağ kontrolleriyle telafi etmelisiniz:

- **Katı ağ segmentasyonu:** Yamalanamamış sistemler, internet kaynaklı tehditlere maruz kalabilecekleri herhangi bir ağdan erişilemez olmalıdır
- **Uygulama beyaz listesi:** Yalnızca özellikle yetkili uygulamalar OT uç noktalarında çalışabilir (uç nokta işletim sistemi bunu destekliyorsa)
- **Telafi edici kontroller:** Firewall, yamanın normalde yapacağı işi yapmalıdır — ağ politikası aracılığıyla saldırı yüzeyini kısıtlama
- **Çevrimdışı antivirüs güncellemeleri:** İnternet bağlantısı yerine hava boşluklu ortamlarda USB veya çevrimdışı medya aracılığıyla iletilen AV güncellemeleri

OT'deki güvenlik görüşmesi "sistemlerinizi yama yapın" değildir — "yamayalamadığımız sistemleri ağ mimarisi ve telafi edici kontroller aracılığıyla nasıl koruruz" sorusudur.

---

## OT'de 802.1X ve NAC: Standart IT Yaklaşımlarının Neden Doğrudan Transfer Olmadığı

802.1X port tabanlı ağ erişim kontrolü, kurumsal IT'de standarttır. OT'de belirli zorluklar yaratır:

**PLC'ler ve kontrolörlerin 802.1X supplicant'ları yoktur.** Bir Siemens S7 PLC veya Allen-Bradley ControlLogix kontrolörü, 802.1X istemcisi olan standart bir işletim sistemi çalıştırmaz. Kullanıcı adı/şifre veya sertifika kullanarak bir RADIUS sunucusuna kendini doğrulayamaz. Bir 802.1X etkin switch portuna basitçe bağlanamaz.

**Geçici çözüm olarak MAC Authentication Bypass (MAB):** OT cihazları için standart yaklaşım MAB'dır — cihazın MAC adresi kimlik doğrulama kimlik bilgisi olarak kullanılır. Switch, MAC adresini RADIUS'a gönderir; RADIUS bunu yetkili cihaz veritabanına göre kontrol eder. MAC biliniyorsa erişim verilir.

MAB bir miktar kontrol sağlar — bilinmeyen cihazlar ağ erişimi alamaz — ancak sertifika veya kimlik bilgisi tabanlı kimlik doğrulamadan daha zayıftır. MAC adresleri taklit edilebilir. Değer görünürlükte ve yetkisiz cihazların bağlanmasını önlemede, kriptografik kimlik doğrulamada değildir.

**Katı MAC adresi yönetimi gereksinimi:** OT'de MAB, tüm yetkili cihaz MAC adreslerinin doğru bir veritabanını sürdürmeyi gerektirir. Dinamik IT ortamında bu uygulanamaz. Cihazların nadiren değiştiği ve tüm eklemelerin değişiklik yönetiminden geçtiği OT'de uygulanabilirdir — ancak disiplin gerektirir.

**Alternatif olarak profiling:** OT güvenlik platformları (Claroty, Nozomi, Cisco CyberVision), ağdaki cihazları profilleyebilir — pasif trafik analizinden PLC modellerini, yazılım sürümlerini ve iletişim kalıplarını tanımlar. Bu, cihazların kimlik doğrulaması yapmasını gerektirmeden varlık görünürlüğü sağlar. Profil verileri NAC politikalarına beslenebilir: "bu cihaz profili bir Siemens S7 PLC ile eşleşiyorsa, PLC VLAN'ına yerleştir."

**Ağ değişikliği riski:** Mevcut bir düz OT ağında son derece dikkatli planlama olmadan 802.1X'i etkinleştirmek, üretim hattını durdurabilir. Zorunluluğu etkinleştirmeden önce her cihaz yetkili veritabanında olmalıdır. Doğrulama süreci yalnızca normal operasyonu değil, tüm üretim aşamalarını kapsamalıdır. Hafta sonu toplu çalışması sırasında ağdan düşen kaçırılan bir cihaz Pazartesi sabahı olayına neden olabilir.

---

## Pratik Kontrol Listesi: OT Ağına Dokunmadan Önce

Saha deneyiminden — OT ortamında herhangi bir ağ değişikliği yapmadan önce gerçekleşmesi gereken şeyler:

- **Önce OT ekibiyle konuşun.** Otomasyon mühendisleri ve tesis operasyon personeli, ağ hakkında belgelenmemiş şeyler bilir. Herhangi bir değişiklikten önce onların katkısı gereklidir.
- **Mevcut iletişim akışlarını belgeleyin.** Hangi cihazlar hangileriyle, hangi portlar üzerinde, hangi sıklıkta konuşuyor. Kısa süreli izlemeye güvenmeyin — tüm bilinen iletişim yollarının belgelerini OT ekibinden isteyin.
- **Üretim programını anlayın.** Bakım penceresi ne zaman? Tesiste planlanmış kesinti ne zaman? Değişiklikler bu pencerelerle uyumlu olmalı, üretim üzerine dayatılmamalıdır.
- **Mümkünse lab veya staging ortamında test edin.** Birçok satıcı endüstriyel ekipmanları için lab ortamları veya simülatörler sağlar.
- **Bir geri alma planınız olsun.** Katman 2 firewall eklemesi için geri alma, firewall'u kaldırıp doğrudan yeniden bağlamaktır — bu prosedürü gerektiğinde hızlıca uygulanabilmesi için belgeleyin.
- **Yazılım/konfigürasyon yedeklerini koordine edin.** Herhangi bir ağ değişikliği yapmadan önce OT cihaz konfigürasyonlarının yedeklendiğinden emin olun. Bir PLC'nin güç döngüsüne ihtiyacı varsa, konfigürasyonu kurtarılabilir olmalıdır.
- **Değişiklikten önce ve sonra "çalışıyor" tanımını yapın.** OT ekibiyle kabul kriterlerini belirleyin — hangi sistemlere erişilebilir olmalı, hangi süreçler çalışıyor olmalı — değişikliği başarılı ilan etmeden önce.

---

## Temel Çıkarımlar

- **OT ağları, gizlilik yerine erişilebilirliği önceliklendirir** — bu, birçok IT güvenlik varsayımını tersine çevirir ve her kararı bilgilendirmelidir.
- **Purdue modeli**, IT/OT sınırının nerede oturduğunu tanımlar. Seviye 3 ile kurumsal IT arasındaki DMZ, IT mühendislerinin en sık çalıştığı yerdir.
- **OT protokolleri (Modbus, PROFINET, EtherNet/IP, DNP3)** kimlik doğrulama veya şifrelemeye sahip değildir. Ağ kontrolleri birincil güvenlik mekanizmasıdır.
- **Katman 2 şeffaf firewall deployment'ı**, OT cihazları arasına güvenlik eklemenin en güvenli yoludur — IP adresi değişikliği yok, routing değişikliği yok, konfigürasyon değişiklikleri olmadan geri alınabilir.
- **OT odaklı firewall'lar**, endüstriyel protokolleri anlar ve politikayı protokol düzeyinde zorunlu kılabilir (okumalara izin ver, yazmaları engelle) — IP/port filtrelemeden temel olarak farklı bir yetenek.
- **OT firewall lisanslaması**, IT NGFW lisanslamasından ayrıdır — bunu proje kapsamına dahil edin.
- **Yamalanmamış eski sistemler OT'de normaldir** — telafi edici ağ kontrolleri, IT'de yamanın sağladığının yerini alır.
- **802.1X doğrudan transfer olmaz** — PLC'ler kimlik doğrulayamaz. MAB ve cihaz profiling pratik alternatiflerdir.
- **Herhangi bir şeye dokunmadan önce OT ekipleriyle koordine edin** — üretim ortamlarındaki ağ hatalarının sonuçları IT'dekinden önemli ölçüde daha ciddidir.

---

## İlgili Yazılar

- 🔐 [802.1X Kimlik Tabanlı Mimari Sahada](/tr/technology/identity-based-microsegmentation-8021x/) — 802.1X'in IT ortamlarında nasıl çalıştığı ve OT'nin neden farklı olduğu
- 🔐 [Zero Trust Zihniyeti: Güvenliği Bir Mimari Olarak Mühendislemek](/tr/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — IT/OT sınır tasarımına uygulanan Zero Trust prensipleri
- 🛡️ [DDoS Koruma Stratejileri](/tr/technology/ddos-koruma-stratejileri-isp-scrubbing-on-premise-bulut/) — OT bağlantılı altyapıyı volumetrik saldırılardan korumak
- 🏗️ [IT Altyapısı Ürünler Koleksiyonu Değildir](/tr/architecture/it-infrastructure-not-a-collection-of-products/) — OT ağ tasarımı için de geçerli sistem düşüncesi