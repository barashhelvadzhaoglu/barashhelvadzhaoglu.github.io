---
title: "Cisco Nexus NX-OS Yazılım Güncelleme Rehberi: Sahada Test Edilmiş Adım Adım"
description: "Cisco Nexus NX-OS güncelleme rehberi — hazırlık, güncelleme yolu, dosya transferi, rollback ve ROMMON kurtarma senaryoları."
date: 2025-12-30
draft: false

cover:
  image: "/img/postimages/nexus-nxos-upgrade-cover.webp"
  alt: "Cisco Nexus NX-OS Yazılım Güncelleme Rehberi"
  relative: false

tags: ["Cisco", "Nexus", "NX-OS", "Network", "Upgrade", "Veri Merkezi"]
categories: ["Network Operasyonları"]
keywords: ["Cisco Nexus güncelleme", "NX-OS güncelleme rehberi", "Nexus yazılım günceleme", "NX-OS ROMMON kurtarma", "Nexus upgrade path", "Cisco Nexus rollback", "NX-OS install all", "Nexus bootflash upgrade", "Cisco veri merkezi upgrade", "NX-OS MD5 doğrulama"]
showToc: true
TocOpen: true
---

Bu rehber, Cisco Nexus switch'lerde yazılım (NX-OS) güncelleme sürecini **sahada uygulanabilir**, **adım adım** ve **geri dönüş senaryoları dahil** olacak şekilde ele alır. Amaç; güncelleme sırasında servis kesintisi riskini azaltmak ve olası bir hatada cihazı hızlıca ayağa kaldırabilmektir.

Yaşanan upgrade problemlerinin büyük bölümü güncellemenin kendisinden değil — hazırlık adımlarının atlanmasından kaynaklanır. Bu rehber hazırlığı, uygulama kadar ciddiye alır.

{{< figure src="/img/postimages/nexus-nxos-upgrade-cover.webp" title="Cisco Nexus NX-OS Upgrade Süreci" >}}

> Upgrade hatalarında out-of-band erişim için: [Ağın Arka Kapısı: Next-Gen Console Server Mimarisi](/tr/posts/next-gen-console-server-architecture/)

## 1. Çalışma Öncesi Kontroller

Yazılım güncelleme işlemine başlamadan önce aşağıdaki hazırlık adımlarını mutlaka tamamlayın. Bu aşama en çok atlanan — ve en çok problem üretendir.

### Konfigürasyon Yedeği

- Cihazınızın **mevcut konfigürasyon yedeğini** her şeyden önce alın.
- Yedeği switch üzerinde değil; kendi bilgisayarınızda veya FTP/SFTP gibi **harici bir konumda** saklayın.
- Upgrade başarısız olursa veya rollback gerekirse bu yedek hayati önem taşır.

### Switch Modeli ve Mevcut Yazılım Sürümü Kontrolü

Switch'in modelini ve çalışan NX-OS sürümünü kontrol etmek için:

```bash
show version
show module
show inventory
```

Bu çıktılar; doğru NX-OS imajını seçmek, upgrade path'i belirlemek ve donanım uyumluluğunu kontrol etmek için gereklidir.

## 2. Yazılım Dosyasını İndirme

- Switch modelinize uygun NX-OS imajını Cisco'nun resmi portalından indirin:
  [https://software.cisco.com/download/home](https://software.cisco.com/download/home)
- İndirme için geçerli bir **Cisco hesabı ve gerekli yetkiler** gerekmektedir.
- İndirme tamamlandıktan sonra **MD5 hash değerini mutlaka not alın** — transfer sonrası doğrulama için kullanacaksınız.

> MD5 doğrulaması, dosyanın indirme sırasında bozulmadığını doğrular. Bu adım isteğe bağlı değildir.

## 3. Upgrade Path Kontrolü

Mevcut NX-OS sürümünüzden hedef sürüme **doğrudan geçiş her zaman desteklenmeyebilir**. Bazı sürüm kombinasyonları ara adımlar gerektirir.

Cisco'nun resmi araçlarını kullanarak kontrol edin:

- **Nexus Upgrade Matrix Tools**
- Nexus 9000 / 3000 Series
- Nexus 7000 Series

> Birden fazla geçiş adımı gerekiyorsa, işleme başlamadan **tüm ara sürüm imajlarını** önceden indirin.

## 4. Yazılım Dosyasını Switch'e Kopyalama

### Seçenek A: FTP ile Transfer

FTP en yaygın kullanılan yöntemlerden biridir. NX-OS imajları 2 GB'a yaklaşabileceğinden transfer süresi ağ hızına bağlıdır.

```bash
copy ftp://user1:Qazwsx@10.10.10.5/nxos.9.3.10.bin bootflash:
```

Nexus'ta birden fazla VRF tanımı varsa transfer için hangi VRF kullanılacağı sorulur. Management interface genellikle management VRF kullandığından bu örnekte management VRF seçilir.

### Seçenek B: USB ile Transfer (Önerilen)

USB transfer benim tercih ettiğim yöntemdir:

- FTP server hazır değilse
- Zaman kısıtı varsa
- Network üzerinden transfer riski almak istemiyorsanız

```bash
copy usb1:nxos.9.3.10.bin bootflash:
```

Devam etmeden önce USB dosya sisteminin Nexus tarafından desteklendiğinden emin olun.

### MD5 Hash Doğrulaması

Transfer tamamlandıktan sonra dosya bütünlüğünü doğrulayın:

```bash
show file bootflash:nxos.9.3.10.bin md5sum
```

Çıktı, Cisco indirme portalındaki MD5 hash değeriyle birebir aynı olmalıdır.

## 5. Güncelleme İşlemi

Tüm kontroller tamamlandıktan sonra güncellemeyi başlatın:

```bash
install all nxos bootflash:nxos.9.3.10.bin
```

- Switch, yükleme öncesinde mevcut konfigürasyonu otomatik olarak kaydeder.
- Reboot öncesinde onay ister.
- Onay verildikten sonra cihaz yeniden başlar ve upgrade işlemi başlar.

Upgrade süresi cihaz modeline ve yazılım boyutuna göre değişir.

## 6. Rollback ve Kurtarma Senaryoları

{{< figure src="/img/postimages/nexus-upgrade-rollback.webp" title="Nexus Upgrade Rollback ve Kurtarma Yolu" >}}

### ROMMON Moduna Geçiş

Yükleme başarısız olursa veya cihaz açılmazsa:

- Cihaz açılışı sırasında console bağlantısı üzerinden **CTRL + L** veya **CTRL + C** tuşlarına basarak **ROMMON moduna** geçin.

### ROMMON'dan TFTP ile Boot

```bash
set ip 10.10.10.2 255.255.255.0
set gw 10.10.10.1
cmdline recoverymode=1
boot tftp://10.10.10.2/tftpboot/nxos.9.3.10.bin
init system
reload-nxos
```

### ROMMON'dan USB ile Boot

```bash
boot usb1:nxos.9.3.10.bin bootflash:
set ip 10.10.10.2 255.255.255.0
set gw 10.10.10.1
cmdline recoverymode=1
boot usb1:nxos.9.3.10.bin
init system
reload-nxos
```

TFTP veya USB ile boot ettikten sonra boot ayarlarını doğrulayın ve düzeltin:

```bash
show boot
```

```bash
configure terminal
  boot nxos bootflash:/nxos.9.3.10.bin
```

## Kritik Uyarı

Yazılım güncellemesi sırasında:

- **Ağ bağlantısını kesmeyin**
- **Güç kaynağını kesmeyin**

Her iki durum da cihazı fiziksel müdahale olmaksızın kurtarılamaz hale getirebilir.

---

## İlgili Yazılar

**Mimari & Operasyonlar**
- 🛠️ [Ağın Arka Kapısı: Next-Gen Console Server Mimarisi](/tr/posts/next-gen-console-server-architecture/) — IP yönetimi kesildiğinde out-of-band erişim
- 📊 [Monitoring Zihniyeti: Sadece Görmek Değil, Anlamak](/tr/architecture/monitoring-not-just-seeing/) — Sorunları tırmanmadan önce yakalamak
- 🏗️ [Switch, Firewall, AP — Doğru Ürünleri Seçmek Neden Yeterli Değildir](/tr/architecture/core-network-is-not-a-product-list/) — Mimari öncelikli core network tasarımı
- 🎯 [Ağ Altyapısında Ürün Seçimi: Stratejik Kriterler](/tr/architecture/network-product-selection-strategy/) — Üreticileri stratejik değerlendirme

**Pratik Mühendislik**
- 🛡️ [Network Packet Broker (NPB) Masterclass](/tr/posts/network-packet-broker-masterclass/) — Trafik görünürlüğü ve güvenlik stratejisi
- 🔐 [802.1X Saha Deployment Rehberi](/tr/technology/identity-based-microsegmentation-8021x/) — Kimlik tabanlı ağ erişim kontrolü