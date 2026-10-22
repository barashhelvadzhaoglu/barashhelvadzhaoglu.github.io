---
title: "Cisco IOS ve IOS-XE Güncelleme Rehberi: Catalyst Switch'ler ve ISR Router'lar"
description: "Catalyst switch'ler (2960, 3560, 3850, 9200, 9300, 9500) ve router'lar (ISR 4000, ISR 1100, Catalyst 8000) için adım adım Cisco IOS ve IOS-XE yazılım güncelleme — flash kontrolü, ROMMON, install mode, bundle mode, MD5 ve rollback."
date: 2026-10-22
draft: false
aliases:
  - "/tr/posts/catalyst-3560-ios-upgrade/"

tags: ["Cisco", "IOS", "IOS-XE", "Upgrade", "Catalyst 9300", "Catalyst 9200", "Catalyst 9500", "Catalyst 3850", "Catalyst 2960", "Catalyst 3560", "ISR 4000", "ISR 1100", "Catalyst 8000"]
categories: ["Network Operasyonları"]
keywords: ["Cisco IOS güncelleme", "Cisco IOS XE upgrade", "install add file activate commit", "Catalyst 9300 güncelleme", "ISR 4331 güncelleme", "Cisco ROMMON güncelleme", "upgrade rom-monitor filename", "bundle mode install mode geçiş", "Cisco verify md5", "archive download-sw", "packages.conf", "install remove inactive"]
showToc: true
TocOpen: true
---

Cisco güncellemelerinin çoğu daha ilk komut yazılmadan başarısız olur: platforma uymayan imaj, flash'ta yetersiz alan, hedef sürüm için fazla eski bir ROMMON ya da hiçbir yeri göstermeyen bir boot değişkeni. Bu rehber önce kontrolleri, sonra komutları anlatıyor.

Sahada karşılaşılan iki aileyi de kapsıyor:

| Aile | Tipik modeller | Yazılım | Dosya sistemi | Güncelleme yöntemi |
| --- | --- | --- | --- | --- |
| Klasik Catalyst switch'ler | 2960, 2960-X, 3560, 3750 | IOS | `flash:` | `archive download-sw` ya da `.bin` + `boot system` |
| IOS-XE Catalyst switch'ler | 3650, 3850, 9200, 9300, 9400, 9500 | IOS-XE | `flash:` (bazı modellerde `bootflash:`) | Install mode (`packages.conf`) |
| IOS-XE router'lar | ISR 4000, ISR 1100, Catalyst 8200/8300, Catalyst 8000V | IOS-XE | `bootflash:` | Install mode ya da bundle mode |
| Klasik IOS router'lar | ISR G2, C900 | IOS | `flash:` | `.bin` + `boot system` |

Komutlar sahada Catalyst switch'lerde ve ISR router'larda kullandıklarım. Örneklerdeki IP adresleri ve dizinler yer tutucudur.

## 1. Önce Platformu Kontrol Edin

### Dosya Sistemi: flash: mı bootflash: mı?

Tahmin etmeyin, cihaza sorun:

```
show file systems
dir
```

Klasik Catalyst switch'ler ve Catalyst 9200/9300 `flash:` kullanır. ISR ve Catalyst 8000 router'lar `bootflash:` kullanır. Birçok IOS-XE platformunda isimlerden biri diğerinin takma adıdır. Cihaz ne gösteriyorsa onu kullanın. Bu rehberdeki her komut iki isimle de çalışır.

### Model, Sürüm ve Boot Modu

```
show version
show inventory
show boot            ! switch'ler
show bootvar         ! router'lar
show install summary ! yalnızca IOS-XE
```

Şunları not edin:

- **Tam model ve platform ailesi.** ISR 4300 imajı ISR 4400'de açılmaz. Platform ailesi dosya adında yazar, örneğin `isr4300-universalk9`, `c1100-universalk9`, `cat9k_iosxe`.
- **Mevcut sürüm.**
- **IOS-XE'de boot modu.** Boot değişkeni `packages.conf`'u gösteriyorsa cihaz **install mode**'da çalışıyordur. Bir `.bin` dosyasını gösteriyorsa **bundle mode**'dadır.

### Boş Alan

`dir` en altta boş alanı gösterir. IOS-XE imajları büyüktür ve install mode paketleri açmak için ek alan ister. Yer azsa önce temizlik yapın:

```
install remove inactive   ! IOS-XE install mode: kullanılmayan paketleri siler
delete flash:<eski-imaj>.bin
```

## 2. Release Notes'u Okuyun: Güncelleme Yolu ve ROMMON

Release notes'taki iki bilgi güncellemenin çalışıp çalışmayacağını belirler:

- **Güncelleme yolu.** Bazı geçişler doğrudan desteklenmez. Örneğin Cisco, bundle mode'daki Catalyst 9500 switch'lerin 16.x'ten 17.x'e bir ara sürüm üzerinden geçmesi gerektiğini, install mode'un ise doğrudan geçişi desteklediğini belirtiyor.
- **Minimum ROMMON sürümü.** Her IOS-XE sürümü minimum bir ROMMON (boot loader) sürümü ister. Cihazdaki ROMMON daha eskiyse yeni imaj açılmayabilir ve cihaz `rommon` prompt'unda kalır.

Mevcut ROMMON sürümünü kontrol edin:

```
show rom-monitor r0          ! ISR 4000 ve benzeri router'lar
show version | include ROM   ! çoğu platform
```

### ROMMON'u Ayrıca Güncellemek Gerekir mi?

- **Catalyst 9000:** Genelde elle gerekmez. Yeni sürümün içinde daha yeni bir ROMMON varsa switch ilk açılışta primary ROMMON'u otomatik günceller. Golden (yedek) ROMMON ise `upgrade rom-monitor capsule golden` komutuyla elle güncellenir. Tam argümanlar modele göre değişir, kendi platformunuzun güncelleme rehberine bakın.
- **ISR 4000 ve benzeri router'lar:** Her seferinde kontrol edin. Bilinen bir örnek: ISR 4000 router'lar 17.x sürümleriyle açılabilmek için ROMMON 16.12(2r) ister.

### ISR 4000'de ROMMON Güncelleme

ROMMON, ROMMON prompt'undan değil, çalışan IOS-XE'den güncellenir. ROMMON paketini kopyalayın, doğrulayın, sonra:

```
copy ftp://192.0.2.10/images/isr4200_4300_rommon_1612_2r_SPA.pkg bootflash:
verify /md5 bootflash:isr4200_4300_rommon_1612_2r_SPA.pkg
upgrade rom-monitor filename bootflash:isr4200_4300_rommon_1612_2r_SPA.pkg R0
reload
show rom-monitor r0
```

ROMMON güncellemesini yazılım güncellemesinden **önce** yapın. Bir şey ters gider de cihaz açılmazsa [Cisco ROMMON Kurtarma](/tr/posts/cisco-rommon-recovery/) yazısına bakın.

### Secure Boot ve İmzalı İmajlar

IOS-XE imajları imzalıdır. Dosya adındaki `.SPA` imzalı production imajı anlamına gelir. Cihaz açılışta imzayı doğrular. Yanlış platforma ait ya da bozuk bir imaj bu kontrolden geçemez ve açılmaz. Yalnızca Cisco Software Download'dan alınan imajları kullanın ve checksum'ı her zaman doğrulayın.

## 3. İmajı Kopyalayın ve Doğrulayın

Büyük IOS-XE imajlarında FTP, TFTP'den daha hızlı ve güvenilirdir:

```
copy ftp://192.0.2.10/images/isr4300-universalk9.17.12.08.SPA.bin bootflash:
copy ftp://192.0.2.10/images/c1100-universalk9.17.12.08.SPA.bin bootflash:
copy tftp://192.0.2.10/cat9k_iosxe.<surum>.SPA.bin flash:
```

Sunucu kurulumu, kullanıcı bilgileri, FTP yollarındaki çift slash ve management VRF konuları [Cisco Güncellemeleri için TFTP, FTP ve SCP Sunucusu](/tr/posts/tftp-ftp-server-cisco-upgrades/) yazısında.

MD5 checksum'ı Cisco indirme sayfasındaki değerle karşılaştırın:

```
verify /md5 bootflash:c1100-universalk9.17.12.08.SPA.bin
```

Değerler farklıysa dosyayı silip yeniden kopyalayın. Doğrulamadan geçmeyen bir imajı asla kurmayın.

## 4. Install Mode'da Güncelleme (IOS-XE)

Catalyst 9000 switch'ler ile güncel ISR ve Catalyst 8000 router'lar için önerilen mod install mode. Tek komut yeni yazılımı ekler, aktif eder ve kalıcı hale getirir:

```
install add file bootflash:isr4300-universalk9.17.12.08.SPA.bin activate commit
```

Cihaz reload için onay ister, `y` deyin. Reload'dan sonra:

```
show version
show install summary
install remove inactive
```

`show install summary` yeni sürümü `Committed` olarak göstermeli. `install remove inactive` eski paketleri siler ve yer açar.

Catalyst 9000 switch'lerde komut aynı, sadece switch'in dosya sistemiyle:

```
install add file flash:cat9k_iosxe.<surum>.SPA.bin activate commit
```

### Arka Arkaya Birkaç Geçiş

Release notes bir ara sürüm istiyorsa her adımda aynı sırayı tekrarlayın: kopyala, doğrula, `install add ... activate commit`, kontrol et, `install remove inactive`. Örneğin önce 17.9, sonra 17.12. Bir sonraki imaja yer kalması için adımlar arasında temizlik yapın.

### Bundle Mode'dan Install Mode'a Geçiş

Bundle mode'daki bir cihaz doğrudan bir `.bin` dosyasıyla açılır. Install mode'a geçmek için:

1. Yukarıdaki gibi `install add file <imaj>.bin activate commit` çalıştırın. Bu, paketleri açar ve `packages.conf` dosyasını oluşturur.
2. Boot değişkeninin `packages.conf`'u gösterdiğinden emin olun:

```
configure terminal
no boot system
boot system flash:packages.conf
end
write memory
show boot
```

Router'larda `bootflash:packages.conf` kullanın.

## 5. Bundle Mode ve Klasik IOS

### Bundle Mode'da IOS-XE, ISR G2, C900

```
configure terminal
no boot system
boot system bootflash:<imaj>.bin
end
write memory
show bootvar
reload
```

C900 serisi gibi klasik IOS router'larda dosya sistemi `flash:` ve imaj adı eski formattadır, örneğin `c900-universalk9-mz.SPA.<surum>.bin`.

### Klasik Catalyst Switch'ler (2960, 3560, 3750)

Bu switch'lerde `archive download-sw` var. Komut bir `.tar` dosyasını aktarır, açar, boot değişkenini ayarlar ve isterseniz reload eder:

```
archive download-sw /overwrite /reload tftp://192.0.2.10/c3560-ipservicesk9-tar.<surum>.tar
```

- `/overwrite`: flash'ta yalnızca bir imajlık yer varsa mevcut imajın yerine yazar.
- `/leave-old-sw`: iki imaja yer varsa eski imajı tutar. Rollback o zaman yalnızca boot değişkenini değiştirmekten ibaret olur.

Alternatif olarak `.bin` dosyasını kopyalayıp doğrulayın ve yukarıdaki gibi `boot system flash:<imaj>.bin` ayarlayın.

## 6. Güncellemeden Sonra

```
show version
show install summary          ! IOS-XE install mode
show interfaces status        ! switch'ler
show ip interface brief
show power inline             ! PoE switch'ler
show logging
```

Stack'lerde ve yedekli sistemlerde her üyeyi kontrol edin: Catalyst stack'lerinde `show switch`, çift supervisor'lı sistemlerde `show redundancy`.

## 7. Rollback

- **Install mode:** `show install rollback` rollback noktalarını listeler.
- **Bundle mode ve klasik IOS:** Eski imaj hâlâ flash'taysa `boot system`'i ona geri çevirip reload edin.
- **Cihaz ROMMON'da ya da `switch:` prompt'unda kalıyorsa:** [Cisco ROMMON Kurtarma](/tr/posts/cisco-rommon-recovery/) yazısına bakın.

## Sık Yapılan Hatalar

- **Yanlış platform ailesine ait imaj.** İmza ya da platform kontrolünden geçemez ve açılmaz.
- **ROMMON'u kontrol etmemek.** Yeni imaj daha yeni bir ROMMON ister, cihaz `rommon` prompt'unda kalır.
- **Install mode için yer olmaması.** Paketlerin açılması yarıda kalır. Önce `install remove inactive` çalıştırın.
- **Install mode'a geçtikten sonra boot değişkeninin hâlâ eski `.bin`'i göstermesi.** Cihaz eski sürümle bundle mode'da açılır.
- **Reload sırasında konsol erişimi olmaması.** Konsol sunucusu bunu uzaktan da mümkün kılar: [Yeni Nesil Konsol Sunucu Mimarisi](/tr/posts/next-gen-console-server-architecture/).

## İlgili Yazılar

- [Cisco ROMMON Kurtarma: Flash, TFTP ya da USB'den Açılış](/tr/posts/cisco-rommon-recovery/)
- [Cisco Güncellemeleri için TFTP, FTP ve SCP Sunucusu](/tr/posts/tftp-ftp-server-cisco-upgrades/)
- [Cisco Switch ve Router Şifre Kurtarma](/tr/posts/cisco-switch-password-recovery/)
- [Cisco Nexus NX-OS Yazılım Güncelleme Rehberi](/tr/posts/cisco-nexus-nxos-upgrade-guide/)

Kaynaklar: [Cisco: Upgrading Catalyst 9500 Switches](https://www.cisco.com/c/en/us/support/docs/switches/catalyst-9500-series-switches/222279-upgrading-catalyst-9500-switches.html) · [Cisco: Upgrading Catalyst 9300 Switches](https://www.cisco.com/c/de_de/support/docs/switches/catalyst-9300-series-switches/222280-upgrading-catalyst-9300-switches.html)
