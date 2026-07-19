---
title: "RAID'siz NAS'ınız Bir Zaman Bombasıdır — Ve Çözüm Ayda €1'a Mal Olur"
description: "RAID olmayan NAS işletmeler için ciddi risktir. AWS S3 otomatik şifreli yedekleme nasıl çalışır ve Glacier neden ayda €1'a kadar düşer?"
date: 2026-03-02
draft: false

cover:
  image: "/img/postimages/nas-backup-cover.webp"
  alt: "NAS Yedekleme AWS S3 ile — KOBİ'ler için Veri Güvenliği"
  relative: false

tags: ["NAS", "Yedekleme", "AWS S3", "Veri Güvenliği", "KOBİ", "Münih"]
categories: ["IT İpuçları"]
keywords: ["NAS yedekleme AWS S3", "RAID olmayan NAS riski", "Hyper Backup Synology", "AWS Glacier KOBİ", "bulut yedekleme GDPR", "NAS sabit disk arızası", "S3 Glacier Deep Archive", "otomatik yedekleme Münih", "NAS veri kaybı önleme", "şifreli bulut yedekleme"]
showToc: true
TocOpen: true
---

Bir doktor muayenehanesi düşünün. Sekiz yıllık hasta kayıtları, faturalar, raporlar. Hepsi ofisteki küçük bir NAS cihazında. Bir sabah cihaz açılmıyor. Sabit disk arızası. Bir veri kurtarma şirketi arıyorsunuz — "deneyeceğiz, €800–2000, garanti yok."

Bu senaryo her gün yaşanıyor. Ve önlemek sadece ayda birkaç euroya mal oluyor.

{{< figure src="/img/postimages/nas-backup-cover.webp" title="NAS Yedekleme AWS S3 ile — KOBİ'ler için Veri Güvenliği" >}}

## Yanılgı: "NAS'ım Var, Yani Yedekleme Yapıyorum"

NAS (Network Attached Storage) mükemmel bir cihazdır — merkezi depolama, ağdaki her bilgisayardan erişilebilir. Ancak küçük işletmelerdeki NAS cihazlarının çoğu tek bir sabit diskle çalışır. RAID yok.

**RAID nedir?**
RAID verileri aynı anda birden fazla diske yazar. En basit haliyle RAID 1, aynı verileri aynı anda iki diske yazar. Biri arızalanırsa diğeri devralır. Veri kaybı olmaz.

RAID olmayan tek diskli bir NAS'ta, disk arızalandığı an her şey gider. Uyarı yok, kurtarma yok.

**"Ama benim NAS'ımda RAID var"** — güzel, ama yeterli değil. RAID disk arızasına karşı korur. Yangın, su hasarı, hırsızlık, fidye yazılımı veya yanlışlıkla silme işlemine karşı korumaz. Harici yedekleme şarttır.

## Çözüm: AWS S3 Bulut Yedekleme

AWS S3 (Simple Storage Service), Amazon'un bulut depolama hizmetidir. Büyük şirketlere ait bir şey gibi geliyor — ama küçük işletmeler bunu ayda sadece birkaç euroya kullanabilir.

**Nasıl çalışır:**

```
NAS cihazı (Synology/QNAP)
        ↓ (otomatik, gecelik)
Hyper Backup yazılımı
        ↓ (şifreli)
AWS S3 — Frankfurt (eu-central-1)
        ↓
Verileriniz: güvenli, şifreli, yedekli
```

Synology NAS cihazlarında yerleşik "Hyper Backup" uygulaması bulunur. Bir kez yapılandırırsınız ve her gece değişen dosyaları otomatik olarak S3'e gönderir. Siz uyurken yedeklemeniz çalışır.

## AWS S3 Depolama Katmanları — Hangisi Size Uygun?

| Katman | En iyi kullanım | Erişim | Maliyet |
|---|---|---|---|
| **S3 Standard** | Sık erişilen veriler | Anında | ~€23/TB/ay |
| **S3 Infrequent Access** | Ayda birkaç kez | Anında | ~€12/TB/ay |
| **S3 Glacier Instant** | Nadiren erişilen arşivler | Milisaniye | ~€4/TB/ay |
| **S3 Glacier Deep Archive** | Uzun süreli arşivleme | 12 saat | ~€1/TB/ay |

**KOBİ'ler için öneri:**
Aktif iş verileri: **S3 Infrequent Access** — uygun fiyat, gerektiğinde anında erişim.
Eski kayıtlar ve arşiv dosyaları: **S3 Glacier Instant** — çok düşük maliyet, yine de anında erişilebilir.

Bir muayenehane için tipik senaryo: aktif hasta verileri S3 IA'da (~€5–8/ay), eski arşiv yılları Glacier'da (~€1–2/ay). **Aylık toplam: €6–10.**

## GDPR ve Hukuki Boyut

Hasta, müvekkil veya müşteri verisi işliyorsanız GDPR'a tabissiniz. Bulut yedekleme için iki şey kritik:

**1. Frankfurt bölgesi (eu-central-1) zorunludur** — verileriniz AB sınırları içinde kalmalıdır.

**2. Şifreleme zorunludur** — Hyper Backup, verilerinizi S3'e göndermeden önce şifreler. Şifreleme anahtarı sizde kalır — AWS bile içeriği göremez.

**3. Hesap sizin adınıza açılır** — Her müşteri için ayrı bir AWS hesabı açıyorum, sizin adınıza. Veriler ve hesap tamamen size aittir.

Muayenehaneler ve hukuk büroları için ayrıca **Veri İşleme Sözleşmesi (DPA)** hazırlıyorum — GDPR kapsamında zorunludur.

## Kurulum Nasıl İşler?

1. AWS hesabı sizin adınıza açılır
2. Doğru katman ve yaşam döngüsü politikalarıyla S3 bucket oluşturulur
3. NAS'ınıza Hyper Backup kurulur
4. İlk tam yedekleme oluşturulur
5. Ertesi günden itibaren yalnızca değişen dosyalar gönderilir
6. Aylık durum raporu e-posta ile iletilir

**Kurulumdan sonra yapmanız gereken:** Hiçbir şey. Her şey otomatik çalışır.

## NAS'ım Yoksa Ne Olur?

S3 yedekleme NAS olmadan da mümkündür. PC'lerinize küçük bir yedekleme ajanı kuruyoruz (Duplicati — ücretsiz) ve seçilen klasörler otomatik olarak S3'e gönderilir.

## Sonuç

Tek diskli bir NAS uyarısız herhangi bir anda arızalanabilir. RAID'li bir NAS bile fidye yazılımına veya fiziksel hasara karşı korumaz. AWS S3 ile verileriniz ayda sadece birkaç euro karşılığında şifreli, yedekli ve güvende olur.

Hesap sizin, veriler sizin, şifreleme anahtarı sizin.

**📱 WhatsApp:** [wa.me/4916098665971](https://wa.me/4916098665971)

---

## İlgili Yazılar

**Koruma & Güvenlik**
- 🔋 [Elektrik Kesilirse Ne Olur? Ofisiniz için UPS Koruması](/tr/posts/ups-office/) — NAS ve ağ cihazlarını elektrik kesintisinden koruma
- 🔒 [SSL Sertifikası — "Güvenli Değil" Uyarısı Müşteri Kaybettirir](/tr/posts/ssl-websecurity/) — KOBİ'ler için web sitesi güvenliği
- 📶 [Wi-Fi Sorunları? Kablo Gerektirmeyen Kalıcı Mesh Çözümü](/tr/posts/wifi-mesh-solution/) — Ofis ve villalar için profesyonel Wi-Fi

**Mimari & Altyapı**
- 📐 [IT Altyapısı Bir Ürün Koleksiyonu Değildir](/tr/architecture/it-infrastructure-not-a-collection-of-products/) — Dayanıklı altyapı için sistem düşüncesi
- 📊 [Monitoring Zihniyeti: Sadece Görmek Değil, Anlamak](/tr/architecture/monitoring-not-just-seeing/) — IT sorunlarını tırmanmadan önce yakalamak