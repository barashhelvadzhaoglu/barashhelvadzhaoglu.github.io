---
title: "Web Sitenizde 'Güvenli Değil' mi Yazıyor? Müşteriler Anında Ayrılıyor — Ve SSL Sertifikaları Çok Daha Kısa Olacak"
seoTitle: "SSL Sertifikası Süresi Doldu mu? Müşteriler Ayrılıyor — 47 Güne Düşüyor"
description: "Süresi dolmuş SSL müşteri kaybettirir ve Google sıralamasına zarar verir. Sertifikalar 47 güne düşüyor — otomatik yönetim zorunlu hale geliyor."
date: 2026-03-20
draft: false

cover:
  image: "/img/postimages/ssl-websecurity-cover.webp"
  alt: "SSL Sertifikası ve Web Sitesi Güvenliği — KOBİ'ler için Cloudflare WAF"
  relative: false

tags: ["SSL", "Web Sitesi Güvenliği", "Cloudflare", "WAF", "Web Sitesi", "Münih"]
categories: ["IT İpuçları"]
keywords: ["SSL sertifikası süresi doldu", "web sitesi güvenli değil uyarısı", "Cloudflare WAF KOBİ", "SSL 47 gün", "otomatik SSL yönetimi", "DDoS koruması Münih", "HTTPS web sitesi güvenliği", "Google sıralaması SSL", "Cloudflare DNS Münih", "Web Uygulama Güvenlik Duvarı"]
showToc: true
TocOpen: true
---

Tarayıcıda bir web sitesi açıyorsunuz ve adres çubuğunda bunu görüyorsunuz: 🔴 **"Bağlantınız özel değil"**

Ne yaparsınız? Büyük ihtimalle geri tuşuna basarsınız.

Müşterileriniz de tam olarak bunu yapıyor. Ve bunu fark etmiyor bile olabilirsiniz — çünkü süresi dolmuş bir SSL sertifikası genellikle web sitesi sahibine bildirim göndermez.

{{< figure src="/img/postimages/ssl-websecurity-cover.webp" title="SSL Sertifikası ve Web Sitesi Güvenliği — Cloudflare ile" >}}

## SSL Sertifikası Nedir ve Neden Önemlidir?

SSL sertifikası (Secure Sockets Layer), web siteniz ile ziyaretçiler arasındaki bağlantıyı şifreleyen dijital bir belgedir. Adres çubuğundaki kilit simgesi ve "https://" varlığını onaylar.

SSL'in iki temel işlevi vardır:

**1. Güvenlik:** Ziyaretçinin tarayıcısı ile sunucunuz arasında akan verileri şifreler. İletişim formu dolduran bir hasta, ödeme bilgisi giren bir müşteri — bu veriler şifreli iletilir.

**2. Güven:** Ziyaretçi kilit simgesini gördüğünde sitenin meşru olduğunu bilir. "Güvenli değil" uyarısı tam tersini yapar.

## Süresi Dolmuş SSL Sertifikasının Gerçek Maliyeti

Pek çok işletme SSL sertifikalarını "bir kez kur unut" mantığıyla ele alır. Bir ya da iki yıllık sertifika satın alır, süresi dolar, fark etmez — bazen haftalarca.

Bu sürede neler olur:

**Müşteri kaybı:** "Güvenli değil" uyarısıyla karşılaşan ziyaretçilerin büyük çoğunluğu anında sayfadan ayrılır. İletişim formları, randevu talepleri, online siparişler — hiçbiri tamamlanmaz.

**Google sıralamasında düşüş:** Google, SSL olmayan veya süresi dolmuş sertifikalı siteleri arama sonuçlarında aşağı iter.

**İtibar hasarı:** "Güvenli değil" gören bir müşteri o işletme hakkında kalıcı olumsuz bir izlenim taşır.

## Büyük Değişiklik Geliyor: SSL Sertifikaları 47 Güne Düşüyor

Şu anda SSL sertifikaları 90 gün veya bir yıl geçerlidir. Bu değişiyor.

CA/Browser Forum — sertifika kuruluşlarını ve büyük tarayıcıları bir araya getiren kurul — yeni bir gereklilik kabul etti: Önümüzdeki yıllarda SSL sertifikası geçerlilik süresi **47 güne** düşecek. Apple, Google ve Mozilla bu kararı destekliyor.

**Bu ne anlama geliyor?**
Şu anda yılda bir kez yeniliyorsanız, yakında **yılda 7–8 kez** yenilemeniz gerekecek. Manuel takip neredeyse imkânsız hale gelir.

**Bu karar neden alındı?**
Daha kısa geçerlilik süreleri, ele geçirilmiş sertifikaların etkisini sınırlar ve sektörü otomasyona yönlendirir — bu aslında olumlu bir gelişmedir.

## Çözüm: Cloudflare ile Otomatik SSL Yönetimi

Cloudflare web sitenizin DNS'ini devraldığında SSL sertifikanızı otomatik olarak yönetir. Siz hiçbir şeyi takip etmeden süresi dolmadan yeniler. Geçerlilik 47 güne düştüğünde hiçbir fark yaratmaz — her şey arka planda otomatik halledilir.

Bu özellik ücretsiz Cloudflare planında bile mevcuttur.

## SSL'in Ötesinde: WAF ve DDoS Koruması

SSL sadece başlangıçtır. Cloudflare'e geçtiğinizde ayrıca şunları alırsınız:

**WAF (Web Uygulama Güvenlik Duvarı):** Web sitenizi SQL injection, XSS saldırıları ve bot trafiğinden korur.

**DDoS Koruması:** Sitenizi çökertmeye yönelik saldırı trafiği otomatik olarak tespit edilip filtrelenir.

**Analitik:** Kaç ziyaretçi geldi, nereden, kaç saldırı engellendi — aylık rapor.

## Hosting Taşıması Gerekmiyor

En sık duyduğum soru: "Web sitemi taşımam mı gerekiyor?"

Hayır. Cloudflare yalnızca DNS düzeyinde çalışır. Web siteniz olduğu yerde kalır — Ionos, Strato, neredeyse. Kurulum 1–2 saat sürer ve ziyaretçileriniz hiçbir şey fark etmez.

## Aylık Güvenlik Raporu

Her ay size şuna benzer bir rapor gönderirim:

```
Web Sitesi Raporunuz — Mart 2026
──────────────────────────────────
✅ SSL Sertifikası: Geçerli (otomatik yönetiliyor)
✅ Çalışma Süresi: %99,98
🛡️ Engellenen Saldırılar: 94
⚡ Savuşturulan DDoS Girişimleri: 2
👥 Toplam Ziyaretçi: 1.203
⚡ Ortalama Yükleme Süresi: 0,8 sn
```

## Sonuç

SSL sertifikası artık bir seçenek değil — temel bir gereklilik. 47 güne düşürülmesiyle birlikte manuel yönetim sürdürülebilir olmaktan çıkıyor.

Web sitenizin SSL durumunu ücretsiz kontrol ediyorum. WhatsApp'tan yazmanız yeterli.

**📱 WhatsApp:** [wa.me/4916098665971](https://wa.me/4916098665971)

---

## İlgili Yazılar

**Koruma & Güvenlik**
- 💾 [RAID'siz NAS'ınız Bir Zaman Bombasıdır](/tr/posts/nas-backup/) — AWS S3 ile veri yedekleme
- 🔋 [Elektrik Kesilirse Ne Olur?](/tr/posts/ups-office/) — Ofis ve muayenehane için UPS koruması
- 📶 [Wi-Fi Sorunları? Kablo Gerektirmeyen Kalıcı Mesh Çözümü](/tr/posts/wifi-mesh-solution/) — Ofis ve villalar için profesyonel Wi-Fi

**Mimari & Altyapı**
- 🛡️ [Zero Trust Zihniyeti: Güvenlik Bir Mimari Olarak](/tr/architecture/zero-trust-architecture-behaviors/) — Güvenlik ürün değil kültür olarak
- 📐 [IT Altyapısı Bir Ürün Koleksiyonu Değildir](/tr/architecture/it-infrastructure-not-a-collection-of-products/) — Dayanıklı IT için sistem düşüncesi