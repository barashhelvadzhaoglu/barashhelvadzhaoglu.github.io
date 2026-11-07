---
title: "Avrupa'da Süpermarket Buzdolaplarına Siber Saldırı: OT ve IoT Cihazları Nasıl Korunur?"
description: "Ekim ve Kasım 2026'da Avrupa'daki süpermarketlerde soğutucular uzaktan ısıtıldı. Şu ana kadar bilinenler, bir soğutma kontrolörüne neden ağdan erişilebildiği ve perakende ile KOBİ ağlarında OT ve IoT cihazlarını korumak için yedi önlem."
date: 2026-11-06
draft: false

tags: ["OT Güvenliği", "IoT Güvenliği", "Siber Güvenlik", "Ağ Segmentasyonu", "Uzaktan Erişim", "Perakende"]
categories: ["Network Mimarisi", "Siber Güvenlik"]
keywords: ["süpermarket buzdolabı siber saldırı", "buzdolabı hacklendi Avrupa", "Danfoss soğutma siber saldırı", "OT güvenliği perakende", "IoT cihaz güvenliği", "OT güvenli uzaktan erişim", "IoT ağ segmentasyonu", "bina otomasyonu güvenliği"]
showToc: true
TocOpen: true
---

Ekim ve Kasım 2026'da Avrupa'nın dört bir yanındaki süpermarketlerde buzdolapları ve dondurucular, içindeki ürünleri bozacak sıcaklıklara ayarlandı. Cihazlara fiziksel olarak kimse dokunmadı. Bu yazı kamuya açık bilgileri özetliyor, bir soğutma kontrolörünün neden ağ üzerinden saldırıya açık olabildiğini açıklıyor ve böyle bir saldırıyı çok daha zor hale getirecek önlemleri sıralıyor.

> **Durum:** Bu yazı 6 Kasım 2026'ya kadarki haberlere ve şirket açıklamalarına dayanıyor. Soruşturmalar sürüyor. Doğrulanmamış bilgileri ayrıca belirtiyorum.

## Ne Oldu?

- **Fransa, 12 Ekim 2026:** Intermarché, Carrefour, Monoprix ve Coopérative U mağazalarında soğutucular ısıtıldı ve gıdalar bozuldu. Intermarché'nin bağlı olduğu grup birkaç milyon euro zarar bekliyor.
- **2 Kasım 2026:** İkinci dalga Belçika'da yaklaşık 75 mağazayı (Delhaize, Carrefour, Intermarché, Spar ve bir IKEA mağazası dahil), İrlanda'da 13 SuperValu mağazasını, İsveç'te ICA ve Coop mağazalarını, ayrıca Hollanda, Estonya ve Finlandiya'daki şirketleri etkiledi. Stockholm'de bir dondurucunun 50 °C'ye kadar ısıtıldığı bildirildi.
- **Ortak nokta:** Etkilenen sistemlerin bir kısmında Danfoss'un soğutma kontrol yazılımı kullanılıyordu. Danfoss'a göre etkilenen müşteriler yazılımlarını güncellememişti. Claroty'deki güvenlik araştırmacıları Ağustos'ta Danfoss soğutma kontrolörlerinde açıklar bildirmişti. Danfoss bunları bir güncellemeyle kapattığını söylüyor.
- **Yöntem:** Belçikalı soğutma servis firması Sabcobel, cihazların defrost moduna geçirildiğini ve tek başına yazılım güncellemesinin yetmediğini, fiziksel değişiklik de gerektiğini açıkladı.

**Şu ana kadar doğrulanmayanlar:** Saldırganların sistemlere nasıl eriştiği, Ağustos'ta bildirilen açıkların kullanılıp kullanılmadığı ve saldırıların arkasında kimin olduğu. Belçika federal savcılığı soruşturma başlattı. AB Tarım Komiseri saldırıları gıda tedarik zincirini bozmaya yönelik kasıtlı bir girişim olarak nitelendirdi.

## Bir Buzdolabı Neden Ağa Bağlı?

Ticari soğutma, evdeki buzdolabı gibi değil. Bir süpermarket, merkezi olarak yönetilen onlarca soğutma ünitesi çalıştırır: sıcaklıklar, defrost döngüleri, alarmlar ve enerji optimizasyonu. Servis firmasının gece alarmları görmesi ve mağazaya gitmeden ayar değiştirebilmesi gerekir.

Bu meşru bir ihtiyaç. Sorun, bu ihtiyacın çoğu zaman nasıl karşılandığı:

- Kontrolör ya da web arayüzü **doğrudan internetten erişilebilir** durumdadır, bazen yıllar önce yapılmış bir port yönlendirmesiyle.
- Kasalar, ofis bilgisayarları ve misafir Wi-Fi ile **aynı ağdadır**.
- Servis firması, kimsenin izlemediği **kalıcı bir uzaktan erişim** aracı kullanır.
- Yazılım, "çalışıyor" diye kurulumdan beri **hiç güncellenmemiştir**.
- **Varsayılan şifreler** hiç değiştirilmemiştir.

Bunların hiçbiri soğutmaya özgü değil. Aynı tablo bina otomasyonunda, ısıtma ve havalandırmada, geçiş kontrolünde, kameralarda, güneş enerjisi invertörlerinde ve üretim makinelerinde de var. Bu olayın süpermarketlerin ötesinde önemli olmasının sebebi bu.

## OT ve IoT Cihazlarını Korumak için Yedi Önlem

### 1. Neyin Olduğunu Bilin

Bilmediğiniz cihazları koruyamazsınız. Ağa bağlı her kontrolörün, gateway'in ve sensörün envanterini tutun: üretici, model, yazılım sürümü, IP adresi, kimin yönettiği ve uzaktan nasıl erişildiği.

### 2. İnternete Doğrudan Açık Olmasın

Bir OT cihazının yönetim arayüzü asla internetten erişilebilir olmamalı. Firewall'unuzdaki port yönlendirmelerini kontrol edin. Dışarıdan neyin göründüğünü anlamak için public IP adreslerinizi Shodan gibi servislerde aratın.

### 3. Ağı Segmentlere Ayırın

OT ve IoT cihazları kendi VLAN'ında ya da ağ segmentinde olmalı. Segmentler arasındaki firewall kimin kiminle konuşabileceğine karar verir:

- Soğutma kontrolörü yalnızca kendi yönetim sunucusuyla ve kullanılıyorsa üreticinin bulut servisiyle konuşur.
- Kasalar, ofis bilgisayarları ve misafir Wi-Fi kontrolöre hiç erişemez.

Endüstriyel ağlarda segmentasyon hakkında daha fazlası: [OT Ağları: Bir IT Mühendisinin Fabrika Zemininde Gerçekte Karşılaştıkları](/tr/technology/ot-network-security/).

### 4. Dışarı Giden Trafiği Kısıtlayın

Birçok cihazın yalnızca birkaç hedefe ulaşması gerekir. Tam olarak bu adreslere ve portlara izin verin, gerisini engelleyin. Cihaz ele geçirilse bile ek araç indiremez ve saldırganın sunucusuna bağlanamaz.

### 5. Servis Firmalarının Uzaktan Erişimini Güvenli Hale Getirin

Servis firmasının erişime ihtiyacı var, ama sizin koşullarınızla:

- Erişim **IPsec VPN ya da ZTNA (Zero Trust Network Access)** üzerinden ve **çok faktörlü kimlik doğrulama** ile olmalı, asla açık bir port üzerinden değil.
- Erişim yalnızca firmanın baktığı sistemlerle sınırlı olmalı, tüm ağa değil.
- Erişim **yalnızca gerektiğinde açılmalı**, sonra kapatılmalı ve kimin ne zaman bağlandığı kayıt altına alınmalı.

### 6. Güncellemeler ve Şifreler

OT cihazlarının yazılım güncellemelerini, sunucularda olduğu gibi üreticiyle koordineli şekilde planlayın. Tüm varsayılan şifreleri değiştirin ve ortak tek bir kullanıcı yerine kişisel hesaplar kullanın.

### 7. Yazılımın Aşamayacağı Güvenlik Sınırları

Bu, bu olaya en özgü ders. Ele geçirilmiş bir kontrolör bir dondurucuyu 50 °C'ye kadar ısıtabiliyorsa, sistemde bağımsız bir güvenlik sınırı yok demektir. Fiziksel ya da donanım tabanlı sınırlar ve ağdan bağımsız çalışan yerel alarmlar, ele geçirilmiş bir kontrolörün fiziksel zarar vermesini engeller. İzleme de önemli: Gece saat 3'te yapılan olağandışı sıcaklık ya da konfigürasyon değişiklikleri anında alarm üretmeli.

## Küçük İşletmeler için Hızlı Kontrol Listesi

- Mağazamızda hangi cihazların ağa bağlı olduğunu biliyor muyuz?
- Bunlardan herhangi birine internetten erişilebiliyor mu?
- Kasalardan ve misafir Wi-Fi'dan ayrı bir ağdalar mı?
- Servis firmamız nasıl bağlanıyor ve ne zaman bağlandığını görebiliyor muyuz?
- Yazılım en son ne zaman güncellendi? Varsayılan şifreler değiştirildi mi?
- Ağ ya da kontrolör çökse bile çalışan bir alarm var mı?

Bu sorulardan birine cevap veremiyorsanız, işe oradan başlayın.

## İlgili Yazılar

- [OT Ağları: Bir IT Mühendisinin Fabrika Zemininde Gerçekte Karşılaştıkları](/tr/technology/ot-network-security/)
- [Zero Trust Zihniyeti: Güvenliği Bir Ürün Değil, Bir Mimari Olarak Mühendislemek](/tr/architecture/zero-trust-architecture-behaviors/)
- [802.1X Projeleri: Kimliği Ağa Taşıyan Mimariyi Sahada Kurmak](/tr/technology/identity-based-microsegmentation-8021x/)
- [Firewall Seçimi ve Kapasite Planlaması](/tr/technology/firewall-selection-capacity/)

## Kaynaklar

- [Euronews: Cyberattacks hit supermarket fridges and freezers in Europe](https://www.euronews.com/2026/11/02/cyberattack-hits-belgian-supermarket-fridges-and-freezers)
- [Forbes: New wave of refrigerator cyberattacks roils European supermarkets](https://www.forbes.com/sites/conormurray/2026/11/02/new-wave-of-refrigerator-cyberattacks-roils-european-supermarkets-everything-is-destroyed/)
- [Al Jazeera: Suspected cyberattacks trigger supermarket fridge failures across Europe](https://www.aljazeera.com/news/2026/11/2/freezers-in-sweden-belgium-overheat-following-possible-cyberattacks)
- [Axios: Europe's fridges are getting hacked](https://www.axios.com/2026/11/02/europe-supermarket-fridges-attacks-food)
