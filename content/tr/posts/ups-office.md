---
title: "Elektrik Kesilince Ne Olur? Bir UPS Yalnızca Bilgisayarınızı Değil — Tüm Ofisinizi Korur"
description: "Elektrik kesintisi tüm ofis cihazlarını tehdit eder. NAS, switch, modem ve kameralarınızı doğru UPS seçimiyle koruyun."
date: 2026-03-23
draft: false

cover:
  image: "/img/postimages/ups-office-cover.webp"
  alt: "UPS Ofis Koruması — Elektrik Kesintisinde NAS, Switch ve Kameraları Güvence Altına Alma"
  relative: false

tags: ["UPS", "Güç Koruması", "NAS", "Ofis IT", "KOBİ", "Münih"]
categories: ["IT İpuçları"]
keywords: ["UPS ofis KOBİ", "elektrik kesintisi NAS koruması", "UPS NAS entegrasyonu", "APC UPS Münih", "PoE switch UPS", "ofis güç koruması", "NAS dosya sistemi bozulmasını önleme", "UPS türleri karşılaştırma", "Synology UPS", "kesintisiz güç kaynağı ofis"]
showToc: true
TocOpen: true
---

"UPS mu? Evet var — bilgisayarın yanında duruyor."

Bunu sürekli duyuyorum. Ve her seferinde sormak istiyorum: Peki NAS'ınız? Switch'iniz? Modeminiz? Ödeme terminaliniz?

Çoğu işletme UPS'i yalnızca bilgisayarın aniden kapanmaması için bir önlem olarak görür. Oysa bir elektrik kesintisinde ofisinizdeki düzinelerce cihaz risk altındadır — ve bilgisayar bunların en az kritik olanıdır.

{{< figure src="/img/postimages/ups-office-cover.webp" title="Tüm Ofis için UPS Koruması — NAS, Switch, Kameralar" >}}

> Tam veri koruması için UPS'i bulut yedeklemeyle tamamlayın: [RAID'siz NAS'ınız Bir Zaman Bombasıdır](/tr/posts/nas-backup/)

## Elektrik Kesilince Gerçekte Ne Olur?

Bir muayenehane veya küçük bir ofis düşünün. Elektrik aniden kesildiğinde aşağıdaki tüm cihazlar aynı anda kapanır:

- **NAS cihazı** — bir yazma işlemi ortasında kesiliyor, disk hasar görebilir
- **Ağ switch'i** — tüm ağ bağlantıları düşüyor
- **Modem/router** — internet yok
- **IP telefon santrali** — telefon hatları kesiliyor
- **Ödeme terminali** — devam eden işlem iptal oluyor
- **Güvenlik kameraları** — kayıt duruyor
- **Bilgisayarlar** — kaydedilmemiş çalışma kayboluyor

Her şey aynı anda kapanıyor. Elektrik geldiğinde tüm cihazlar aynı anda açılmaya çalışır — bu ani yük, zayıf elektrik tesisatında ek sorunlara yol açabilir.

## En Büyük Risk: NAS'ınız

Bu cihazlar arasında ani elektrik kesintisinden en çok etkilenen NAS'tır. NAS sürekli veri yazar. Bir kopyalama işlemi veya zamanlanmış yedekleme sırasında elektrik kesilirse yazma işlemi yarıda kalır. Bu dosya sistemi bozulmasına yol açabilir.

Synology ve QNAP NAS cihazları doğrudan bir UPS ile çalışabilir. USB kablosuyla bağlandığında NAS, elektrik kesilme anını algılar ve güvenli bir kapanma sırası başlatır:

```
Elektrik kesildi
      ↓
UPS anında devreye giriyor (batarya)
      ↓
NAS, UPS'ten sinyal alıyor
      ↓
Açık dosyalar kaydediliyor
      ↓
2 dakikada güvenli kapanma
      ↓
Veri kaybı yok, disk bozulması yok
      ↓
Elektrik gelince otomatik yeniden başlatma
```

Bu entegrasyon olmadan bir UPS size yalnızca birkaç dakika daha satın alır — NAS yine de aniden kapanabilir.

## UPS Türleri — Hangisi Size Uygun?

**Standby (Offline) UPS**
En uygun fiyatlı seçenek. Ev kullanımı ve basit bilgisayarlar için yeterli. Voltaj dalgalanmalarına karşı sınırlı koruma.

**Line-Interactive UPS**
KOBİ'ler için ideal seçim. Voltaj dalgalanmalarını sürekli düzenler ve arızada anında bataryaya geçer. NAS cihazları, switch'ler ve kritik ofis ekipmanları için önerilen tür.

**Online Double Conversion UPS**
En yüksek koruma sınıfı. Kritik sunucular, tıbbi cihazlar ve hiçbir kesintiye toleransı olmayan sistemler için.

## PoE Switch: Kameralarınız da Korunuyor

PoE switch (Power over Ethernet) kullanıyorsanız kameralarınız switch üzerinden güç alır. Switch UPS'e bağlıysa kameralar da korunur:

```
UPS
  ↓
PoE Switch
  ├── Kamera 1 (switch üzerinden güç)
  ├── Kamera 2 (switch üzerinden güç)
  └── NAS (switch üzerinden bağlı)
```

Elektrik kesildiğinde UPS devreye girer, switch çalışmaya devam eder, kameralar kayıt yapmaya devam eder — NAS güvenli kapanma işlemini tamamlarken.

## Kaç Dakika Yeterli?

Tipik bir ofis kurulumu için 10–15 dakika yeterlidir. Bu sürede NAS güvenli kapanma işlemini tamamlar, açık belgeler kaydedilir ve sunucular düzgün şekilde kapatılır.

Çoğu KOBİ için **650VA–1500VA** doğru aralıktır.

## UPS Bakımı Hakkında Bir Not

UPS bataryaları genellikle her 3–5 yılda bir değiştirilmelidir. APC ve Eaton gibi markalarda batarya modülerdir — vidasını açın, değiştirin, bitti. Beş dakika.

Müşterilerim için yıllık UPS kontrolü yapıyorum: batarya kapasitesi test edildi, yazılım güncellemeleri kontrol edildi, NAS entegrasyonu çalışıyor mu doğrulandı.

## Nereden Başlamalı: Önceliklendirme

1. **NAS + switch** — en kritik, buradan başlayın
2. **Sunucu, varsa**
3. **Modem/router** — internet sürekliliği için
4. **Bilgisayarlar** — en az kritik

## Sonuç

Doğru UPS, doğru yapılandırılmış ve yıllık olarak bakımı yapılmış şekilde, elektrik kesintisinden kaynaklanan veri kaybı riskini neredeyse sıfıra indirir. Ücretsiz değerlendirme için WhatsApp'tan yazın.

**📱 WhatsApp:** [wa.me/4916098665971](https://wa.me/4916098665971)

---

## İlgili Yazılar

**Koruma & Güvenlik**
- 💾 [RAID'siz NAS'ınız Bir Zaman Bombasıdır](/tr/posts/nas-backup/) — AWS S3 ile veri yedekleme
- 🔒 [SSL Sertifikası — "Güvenli Değil" Uyarısı Müşteri Kaybettirir](/tr/posts/ssl-websecurity/) — KOBİ'ler için web sitesi güvenliği
- 📶 [Wi-Fi Sorunları? Kablo Gerektirmeyen Kalıcı Mesh Çözümü](/tr/posts/wifi-mesh-solution/) — Ofis ve villalar için profesyonel Wi-Fi

**Mimari & Altyapı**
- 🛠️ [Ağın Arka Kapısı: Next-Gen Console Server](/tr/posts/next-gen-console-server-architecture/) — Her şey çöktüğünde out-of-band erişim
- 📐 [IT Altyapısı Bir Ürün Koleksiyonu Değildir](/tr/architecture/it-infrastructure-not-a-collection-of-products/) — Dayanıklı IT için sistem düşüncesi