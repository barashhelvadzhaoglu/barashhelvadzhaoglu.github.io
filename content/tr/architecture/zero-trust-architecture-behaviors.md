---
title: "Zero Trust Zihniyeti: Güvenliği Bir Ürün Değil, Bir Mimari Olarak Mühendislemek"
description: "Zero Trust bir ürün değil mimari yaklaşımdır. Kullanıcı doğrulama, sürekli erişim kontrolü ve VPN ötesinde modern güvenlik nasıl çalışır."
date: 2026-01-03
draft: false
author: "Barash Helvadzhaoglu"
language: "tr"

cover:
  image: "/img/postimages/zero-trust-not-product.webp"
  alt: "Zero Trust Zihniyeti: Güvenliği Bir Mimari Olarak Mühendislemek"
  relative: false

categories:
  - Siber Güvenlik
  - IT Mimarisi
  - Ağ Güvenliği

tags:
  - zero trust
  - siber güvenlik
  - MFA
  - ağ güvenliği
  - erişim kontrolü
  - VPN
  - 802.1X
  - NAC
  - kimlik doğrulama
  - mimari

keywords:
  - zero trust mimarisi
  - sürekli doğrulama
  - ağ güvenliği en iyi uygulamaları
  - MFA zero trust
  - cihaz uyumluluğu
  - kimlik ve erişim yönetimi
  - firewall ve erişim kontrolü
  - 802.1X zero trust
  - NAC kurumsal
  - sıfır güven mimarisi
  - never trust always verify
  - mikro segmentasyon

toc: true
tocopen: true
---

# Zero Trust Zihniyeti: Güvenliği Bir Ürün Değil, Bir Mimari Olarak Mühendislemek

Zero Trust bugün neredeyse her güvenlik sunumunda geçen bir kavram. Ancak sahada karşılığına baktığımızda, çoğu zaman yanlış yerde, yanlış beklentiyle ve yanlış araçlarla ele alındığını görüyoruz. Bunun temel sebebi, Zero Trust'ın bir teknoloji ya da satın alınabilir bir ürün gibi konumlandırılması. Oysa Zero Trust; lisanslanan, kutulanan ya da tek bir vendor'dan alınan bir çözüm değildir. Zero Trust, bir mimari bakış açısıdır ve daha da önemlisi, bir davranış biçimidir.

Zero Trust'ın özü son derece nettir: **Never trust, always verify.** Hiçbir kullanıcıya, hiçbir cihaza, hiçbir bağlantıya varsayılan olarak güvenme. Güven, sürekli olarak yeniden kazanılan bir durumdur. Bu yaklaşım, klasik "içerisi güvenlidir, dışarısı tehlikelidir" varsayımını tamamen ortadan kaldırır. Çünkü modern IT dünyasında içerisi ve dışarısı artık net sınırlarla ayrılmış değildir.

{{< figure src="/img/postimages/zero-trust-layered-architecture.webp" title="Zero Trust: Katmanlı Bir Mimari" >}}

**Özetle:**
* Zero Trust bir ürün değil, mimari yaklaşımdır
* Varsayılan güven kavramını reddeder
* Sürekli doğrulama esasına dayanır

> Bu yazı, IT altyapısını sistem olarak ele alan serinin bir parçasıdır. Başlangıç noktası için: [IT Altyapısı Bir Ürün Koleksiyonu Değildir](/tr/architecture/it-infrastructure-not-a-collection-of-products/)

## Zero Trust Hiçbir Üreticinin Malı Değildir

Zero Trust kavramı pratikte ilk olarak güvenlik üreticilerinin vizyonlarıyla şekillenmeye başladı. Ancak burada önemli bir ayrım yapmak gerekir: Zero Trust herhangi bir üreticinin "sahip olduğu" bir konsept değildir. Tek bir teknolojiyle temsil edilemez.

Bunun sebebi şudur: Zero Trust, aynı anda birden fazla katmanın birlikte ve tutarlı şekilde çalışmasını zorunlu kılar. Network, güvenlik, kimlik, kullanıcı, cihaz ve uygulama katmanları birbirinden kopuk çalışıyorsa, Zero Trust yalnızca bir söylem olarak kalır. Mimari olarak karşılığı yoktur.

**Bu bölümün özü:**
* Zero Trust vendor'a ait değildir
* Tek bir teknolojiyle kurulamaz
* Katmanlar arası tutarlılık gerektirir

## Kullanıcı ve Cihaz Doğrulaması: Mimarinin Başladığı Yer

Zero Trust mimarisi pratikte çok temel bir soruyla başlar:
> "Bu kullanıcı ve bu cihaz, şu anda erişmek istediği kaynağa gerçekten erişmeli mi?"

Bu soruya anlamlı bir cevap verebilmek için ilk adım, network'e dahil olan kullanıcıların ve cihazların doğrulanmasıdır. Active Directory, LDAP veya modern identity provider'lar bu yapının merkezinde yer alır. Kullanıcıya hangi kaynaklara erişebileceği sadece kimliğine değil, rolüne ve risk durumuna göre belirlenir.

Ancak Zero Trust açısından önemli olan yalnızca kullanıcının kim olduğu değildir; cihazın durumu, kurumsal envantere ait olup olmadığı ve güvenlik politikalarına uygunluğu da bu kararın bir parçasıdır.

**Hatırlanması gerekenler:**
* Kullanıcı doğrulaması tek başına yeterli değildir
* Cihaz kimliği ve durumu da değerlendirilir
* Erişim kararı bağlama göre verilir

## VPN ≠ Zero Trust: Uzaktan Erişimin Doğru Çerçevesi

Uzaktan çalışma artık istisna değil, standarttır. Ancak birçok organizasyonda hâlâ klasik VPN mantığıyla hareket edilir: kullanıcı VPN'e bağlanır ve bir anda tüm lokal network'ün parçası haline gelir. **Bu yaklaşım Zero Trust değildir.** Bu yalnızca uzaktan erişimdir.

Zero Trust mimarisinde uzaktan erişim, "her yere erişim" anlamına gelmez. Kullanıcı yalnızca yetkili olduğu uygulamalara veya kaynaklara erişir. Amaç her zaman aynıdır: erişimi minimumda tutmak ve sürekli kontrol etmek.

**Bu bölümün kilidi:**
* VPN ≠ Zero Trust
* Erişim tüm network'e değil, kaynağa olmalıdır
* Yetki sürekli kontrol edilir

## Sürekli Doğrulama ve MFA

Zero Trust'ı klasik güvenlik yaklaşımlarından ayıran en önemli nokta, doğrulamanın tek seferlik kabul edilmemesidir. Kullanıcı ve cihaz davranışı değiştikçe, erişim sürekli olarak yeniden değerlendirilir.

Bu noktada **çok faktörlü kimlik doğrulama (MFA)** devreye girer. SMS, mobil uygulama bildirimi, donanımsal token veya biyometrik doğrulama gibi ek katmanlar kullanılır. Özellikle mail server, finans sistemleri veya ERP gibi kritik uygulamalara erişimde, kullanıcıdan belirli aralıklarla kendini yeniden doğrulaması istenir.

**Özetle:**
* Doğrulama süreklidir
* MFA Zero Trust'ın temel bileşenidir
* Kritik kaynaklarda periyotlar kısaltılır

## Firewall: Politika Karar Noktası

Firewall katmanı, Zero Trust mimarisinde merkezi bir rol oynar. Ancak bu rol, klasik anlamda "internet çıkışını kontrol eden cihaz" olmaktan çok daha fazlasıdır. Zero Trust yaklaşımında firewall, kimlik ve bağlam farkındalığı olan bir karar noktasıdır.

Firewall üzerinde tanımlanan kurallar yalnızca IP veya port bazlı olmamalıdır. Kullanıcı, grup ve uygulama bazlı kurallar yazılabildiğinde Zero Trust gerçek anlamda uygulanabilir hale gelir.

> Switch, firewall ve AP'nin birlikte nasıl çalıştığını anlamak için: [Switch, Firewall, AP — Doğru Ürünleri Seçmek Neden Yeterli Değildir](/tr/architecture/core-network-is-not-a-product-list/)

**Bu katmanın özeti:**
* Firewall politika karar noktasıdır
* Kimlik ve uygulama farkındalığı şarttır
* Port bazlı kurallar yeterli değildir

## Access Katmanı: Zero Trust Buradan Başlar

Zero Trust yalnızca firewall ve VPN katmanında uygulanmaz. Mimarinin başladığı yer access katmanıdır. 802.1X ve NAC çözümleri bu noktada devreye girer. Tüm switch portları ve wireless erişimler merkezi bir sistem tarafından kontrol edilir. Kullanıcı veya cihaz network'e bağlanmadan önce doğrulanır ve bu doğrulama sonucuna göre dinamik olarak VLAN atanır veya politika uygulanır.

{{< figure src="/img/postimages/zero-trust-access-layer-802-1x.webp" title="802.1X Erişim Kontrolü: Ağ Kenarında Zero Trust" >}}

**Bu bölümün özü:**
* Zero Trust access katmanında başlar
* 802.1X merkezi kontrol sağlar
* Statik VLAN / SSID yapıları ölçeklenmez

## Cihaz Profilleme ve IoT

Modern Zero Trust mimarilerinde yalnızca kullanıcı cihazları değil, network'e bağlanan tüm uçlar kontrol altına alınır. Yazıcılar, kameralar, IP telefonlar, kart okuyucular gibi cihazlar da doğrulama sürecine dahil edilir.

Yeni nesil NAC çözümleri DHCP fingerprint, CDP/LLDP bilgileri ve cihaz üretici bilgileri gibi birçok parametreyi birleştirerek cihaz profillemesi yapar. Cihazın güncel olup olmadığı, güvenlik durumu veya kurumsal standartlara uygunluğu da değerlendirilir.

**Kilit noktalar:**
* Cihaz profilleme kritik önemdedir
* MAC adresi tek başına yeterli değildir
* Envanter entegrasyonu şarttır

## Misafir Erişimi: Güven Varsayılmaz

Zero Trust mimarisinde misafir erişimleri bile kontrol altındadır. Guest portal'lar aracılığıyla misafir kullanıcılar doğrulamadan geçirilir ve yalnızca belirli süre ve yetkilerle erişim sağlanır. Misafirler genellikle sadece internete çıkabilir; şirket kaynaklarına erişimleri sınırlıdır.

**Bu bölümün özeti:**
* Misafir erişimi sınırsız değildir
* Süre ve yetki bazlı kontrol uygulanır
* Güven varsayılmaz

## Sürekli İzleme: Mimarinin En Kritik Parçası

Her katmanda erişim ve davranışlar izlenir ve kaydedilir. Anormal bir durum veya riskli hareket tespit edilirse, sistem otomatik olarak erişimi sınırlar veya ek doğrulama ister.

> Altyapıda gerçek görünürlük nasıl kurulur: [İzleme Zihniyeti: Sadece Görmek Değil, Anlamak ve Proaktif Hareket Etmek](/tr/architecture/monitoring-mindset-not-just-seeing-but-understanding-and-acting-proactively/)

## Sonuç

Zero Trust bir ürün değildir.
Tek bir cihazla kurulmaz.
"Kurduk, bitti" denilemez.

Zero Trust; firewall, switch ve wireless altyapılarının; kullanıcı ve cihaz bilgilerini merkezi bir noktadan alarak birlikte çalıştığı, erişimin her aşamada yeniden sorgulandığı yaşayan bir mimaridir. Bu yüzden Zero Trust'ı satın alınacak bir teknoloji değil, tasarlanacak ve işletilecek bir yetkinlik olarak görmek gerekir.

## Not

Bu makale ilk olarak **Substack**'te daha kısa, anlatısal bir biçimde yayınlanmıştı.
Bu versiyon, serinin mimari temelini genişletiyor.

👉 **Makaleyi Substack'te okuyun:** [Burayı Tıklayın](https://substack.com/home/post/p-183954997)

---

## İlgili Yazılar

**Mimari & Güvenlik Tasarımı**
- 📐 [IT Altyapısı Bir Ürün Koleksiyonu Değildir](/tr/architecture/it-infrastructure-not-a-collection-of-products/) — Bu serinin temel yazısı
- 🏗️ [Switch, Firewall, AP — Doğru Ürünleri Seçmek Neden Yeterli Değildir](/tr/architecture/core-network-is-not-a-product-list/) — Core network tasarımında sistem düşüncesi
- 📊 [İzleme Zihniyeti: Sadece Görmek Değil, Anlamak ve Proaktif Hareket Etmek](/tr/architecture/monitoring-mindset-not-just-seeing-but-understanding-and-acting-proactively/) — Altyapıda gerçek görünürlük

**Teknik Mühendislik**
- 🔐 [802.1X Projelerinde Başarı: Saha Deneyimleri](/tr/posts/unlocking-success-in-802-1x-projects-field-insights/) — Kimlik tabanlı erişimin sahada uygulanması
- 🛡️ [Network Packet Broker (NPB) Masterclass](/tr/posts/network-packet-broker-npb-masterclass/) — Gelişmiş trafik görünürlüğü ve güvenlik stratejisi
- 🛠️ [Ağın Arka Kapısı: Next-Gen Console Server Mimarisi](/tr/posts/next-gen-console-server-terminal-server-architecture/) — Her şey kesildiğinde out-of-band erişim