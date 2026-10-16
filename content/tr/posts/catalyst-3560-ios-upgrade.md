---
title: "Cisco Catalyst 3560 IOS Güncelleme: İki Yöntem ve Doğrulama"
description: "Cisco Catalyst 3560'ta IOS güncelleme — archive download-sw ile manuel kopyalama ve boot system karşılaştırması, flash alanı, MD5 doğrulama ve rollback."
date: 2026-10-16
draft: false

tags: ["Cisco", "Catalyst", "Switch", "IOS", "Upgrade"]
categories: ["Network Operasyonları"]
keywords: ["Catalyst 3560 IOS güncelleme", "archive download-sw", "Cisco switch yazılım güncelleme", "boot system flash", "verify md5 Cisco", "Cisco 3560 TFTP güncelleme", "Cisco switch flash alanı", "Cisco IOS rollback"]
showToc: true
TocOpen: true
---

Catalyst 3560'ta IOS güncellemek karmaşık değil ama ayrıntılar önemli: hangi dosya formatını indirdiğiniz, flash'ta ne kadar yer kaldığı ve boot değişkeninin doğru imajı gösterip göstermediği. Bunlardan birinde yapılan hata, switch'in IOS yerine boot loader'da açılmasıyla sonuçlanır.

İki yol var:

- **Yöntem A: `.tar` dosyasıyla `archive download-sw`.** Switch imajı ve web device manager dosyalarını kendisi açar, boot değişkenini de kendisi ayarlar.
- **Yöntem B: `.bin` dosyasıyla manuel güncelleme.** İmajı kopyalar, doğrular, `boot system`'i ayarlar ve reload edersiniz.

> **Lab notu:** Kendi 8 portlu PoE Catalyst 3560 switch'imi iki yöntemle de güncelliyorum. Lab'dan alınan konsol çıktıları ve süreler bu rehbere eklenecek.

## 1. Başlamadan Önce

### Konfigürasyonu Yedekleyin

```
Switch# copy running-config startup-config
Switch# copy startup-config tftp:
```

Yedeği switch'in dışında tutun: laptopunuzda, bir TFTP ya da SCP sunucusunda veya konfigürasyon yönetim aracınızda.

### Modeli, Sürümü ve Feature Set'i Belirleyin

```
Switch# show version
Switch# show inventory
```

Üç şeyi not edin:

- **Tam model**, örneğin `WS-C3560-8PC-S`. İmaj platformla uyumlu olmalı.
- **Mevcut IOS sürümü**.
- **Feature set**, örneğin IP Base (`ipbasek9`) ya da IP Services (`ipservicesk9`). Bilinçli olarak değiştirmiyorsanız yeni imaj için aynı feature set'i seçin.

### Boot Ayarlarını ve Flash Alanını Kontrol Edin

```
Switch# show boot
Switch# dir flash:
```

`show boot`, switch'in bir sonraki reload'da hangi imajı yükleyeceğini gösterir. `dir flash:` dosyaları ve en altta boş alanı gösterir. 8 portlu 3560 gibi kompakt switch'lerde flash az. Çoğu zaman iki imajı aynı anda tutacak yer olmaz.

### İmajı İndirin

İmajı Cisco Software Download'dan indirin. Bunun için servis sözleşmesi gerekiyor. İki dosya tipi göreceksiniz:

| Dosya | İçerik | Kullanım |
| --- | --- | --- |
| `.tar` | IOS imajı ve web device manager dosyaları | `archive download-sw` (Yöntem A) |
| `.bin` | Yalnızca IOS imajı | Manuel kopyalama ve `boot system` (Yöntem B) |

İndirme sayfasındaki **MD5 checksum** değerini not edin. Switch üzerinde bununla karşılaştıracaksınız.

Klasik Catalyst 3560 end of life oldu. İndirme sayfasındaki en yeni sürüm bu platform için son sürüm.

## 2. Yöntem A: archive download-sw

Cisco'nun bu switch ailesi için önerdiği yöntem bu. Tek komut `.tar` dosyasını aktarır, flash'ta yeni bir dizine açar, boot değişkenini günceller ve isterseniz reload eder.

```
Switch# archive download-sw /overwrite /reload tftp://192.0.2.10/c3560-ipservicesk9-tar.<surum>.tar
```

En kullanışlı seçenekler:

| Seçenek | Etkisi |
| --- | --- |
| `/overwrite` | İki imaja yer yoksa mevcut imajın yerine yazar |
| `/leave-old-sw` | Eski imajı tutar (yalnızca flash ikisine de yetiyorsa) |
| `/reload` | Başarılı indirmeden sonra switch'i reload eder |
| `/imageonly` | Web device manager dosyaları olmadan yalnızca IOS imajını kurar |

İki imaja yer varsa `/overwrite` yerine `/leave-old-sw` kullanın. Rollback o zaman sadece boot değişkenini değiştirmekten ibaret olur.

`/reload` kullanmadıysanız reload'dan önce sonucu kontrol edin:

```
Switch# show boot
Switch# dir flash:
Switch# reload
```

## 3. Yöntem B: .bin Dosyasıyla Manuel Güncelleme

Manuel yöntem her adımda tam kontrol sağlar. Elinizde yalnızca `.bin` dosyası varsa ya da boot değişkenine dokunmadan önce imajı doğrulamak istiyorsanız işe yarar.

### İmajı Kopyalayın

```
Switch# copy tftp://192.0.2.10/c3560-ipservicesk9-mz.<surum>.bin flash:
```

Yer yetmiyorsa önce eski imajı silmeniz gerekir. Bu, switch üzerindeki rollback seçeneğinizi ortadan kaldırır. Eski imajın TFTP sunucunuzda olduğundan ve konsol bağlantısının hazır olduğundan emin olun.

TFTP küçük dosyalar için iş görür ama yavaştır ve uzak mesafelerde güvenilir değildir. IOS sürümünüz destekliyorsa SCP ya da FTP daha hızlı.

### Checksum'ı Doğrulayın

```
Switch# verify /md5 flash:c3560-ipservicesk9-mz.<surum>.bin
```

Sonucu Cisco indirme sayfasındaki MD5 değeriyle karşılaştırın. Farklıysa dosyayı silip yeniden kopyalayın. Doğrulamadan geçmeyen bir imajla asla açılış yapmayın.

### Boot Değişkenini Ayarlayın ve Reload Edin

```
Switch# configure terminal
Switch(config)# boot system flash:c3560-ipservicesk9-mz.<surum>.bin
Switch(config)# end
Switch# copy running-config startup-config
Switch# show boot
Switch# reload
```

Reload'dan önce `show boot`'u kontrol edin. `BOOT path-list` doğru dosya adı ve yolla yeni imajı göstermeli.

## 4. Güncellemeden Sonra

```
Switch# show version
Switch# show interfaces status
Switch# show power inline
Switch# show logging
```

- `show version`: Yeni IOS sürümü çalışıyor.
- `show interfaces status`: Beklenen tüm portlar açık.
- `show power inline`: PoE cihazları yeniden besleniyor.
- `show logging`: Açılışta hata yok.

Yeni sürümün sorunsuz çalıştığından emin olduğunuzda, rollback için tutmak istemiyorsanız eski imajı silerek yer açın.

## 5. Rollback

- **Eski imaj hâlâ flash'ta:** Boot değişkenini `boot system flash:<eski-imaj>` ile geri alın, kaydedin ve reload edin.
- **Eski imaj silindi:** TFTP sunucusundan geri kopyalayın, MD5'i doğrulayın ve boot değişkenini ayarlayın.
- **Switch IOS'u hiç açamıyor:** `switch:` prompt'unda kalır. Bu durum [Catalyst 3560 Açılmıyorsa: Boot Loader ile Kurtarma](/tr/posts/catalyst-3560-boot-loader-recovery/) yazısında anlatılıyor.

## Sık Yapılan Hatalar

- **Yanlış platform ya da feature set.** Başka bir modelin imajı açılmaz.
- **Yeni imaj doğrulanmadan eskisini silmek.** Kopya bozuksa açılacak hiçbir şey kalmaz.
- **`boot system`'de yazım hatası.** Switch imajı bulamaz ve boot loader'da kalır.
- **Reload sırasında konsol bağlantısı olmaması.** Bir şey ters giderse bunu yalnızca konsoldan görebilirsiniz.

## İlgili Yazılar

- [Cisco Catalyst 3560 Şifre Kurtarma: İki Yöntem](/tr/posts/catalyst-3560-password-recovery/)
- [Catalyst 3560 Açılmıyorsa: Boot Loader ile Kurtarma](/tr/posts/catalyst-3560-boot-loader-recovery/)
- [Cisco Nexus NX-OS Yazılım Güncelleme Rehberi](/tr/posts/cisco-nexus-nxos-upgrade-guide/)
- [Network Mühendisleri için SecureCRT ve SuperPuTTY](/tr/technology/securecrt-superputty/)
