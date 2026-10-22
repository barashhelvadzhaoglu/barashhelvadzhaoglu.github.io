---
title: "Cisco ROMMON Kurtarma: Switch ya da Router'ı Flash, TFTP veya USB'den Açmak"
description: "Cisco switch ya da router switch: veya rommon prompt'unda mı kaldı? Catalyst 9300, 9200, 3850, 2960, 3560 ve ISR 4000 için kurtarma senaryoları — flash'tan açılış, ROMMON ağ değişkenleri, TFTP ya da USB'den açılış ve eski ROMMON sorunu."
date: 2026-10-22
draft: false
aliases:
  - "/tr/posts/catalyst-3560-boot-loader-recovery/"

tags: ["Cisco", "ROMMON", "Boot Loader", "Recovery", "IOS-XE", "Catalyst 9300", "Catalyst 9200", "Catalyst 3850", "Catalyst 2960", "Catalyst 3560", "ISR 4000"]
categories: ["Network Operasyonları"]
keywords: ["Cisco ROMMON kurtarma", "Cisco switch rommon'da kaldı", "switch: prompt", "rommon boot tftp", "IP_ADDRESS DEFAULT_GATEWAY rommon", "boot usbflash0", "emergency-install", "Cisco rommon eski", "Catalyst 9300 bootloader", "ISR 4331 rommon"]
showToc: true
TocOpen: true
---

Reload'dan sonra cihaz geri gelmiyor. Konsolda yalnızca `switch:` (Catalyst switch'ler) ya da `rommon 1 >` (router'lar) var. Bu ROMMON, diğer adıyla boot loader: IOS'u başlatan küçük program. Geçerli bir imaj bulamadığı ya da başlatamadığı için durmuş.

Çoğu durumda bu bir donanım arızası değil ve cihazı değiştirmeniz gerekmiyor. Hangi yoldan çıkacağınız tek bir soruya bağlı: **Flash'ta hâlâ sağlam bir imaj var mı?**

| Senaryo | Durum | Çıkış yolu |
| --- | --- | --- |
| 1 | Doğru imaj flash'ta | Onunla açın, boot değişkenini düzeltin |
| 2 | İmaj yok ya da bozuk | TFTP ya da USB'den açın, sonra imajı flash'a kopyalayın |
| 3 | İmaj var ama ROMMON onun için çok eski | Eski bir imajla açın, ROMMON'u güncelleyin, sonra yükseltin |

## Başlamadan Önce: Konsol Erişimi

ROMMON'a yalnızca konsoldan ulaşılır. Bir şubede bu bir laptop ve konsol kablosu demek. Rack'in yanında nadiren bulunduğunuz bir data center'da ise kurtarmayı mümkün kılan şey konsol sunucusu: [Yeni Nesil Konsol Sunucu Mimarisi](/tr/posts/next-gen-console-server-architecture/).

Önce ortama bakın:

```
switch: dir flash:
switch: set
```

Router'larda:

```
rommon 1 > dir bootflash:
rommon 2 > set
```

`set`, boot loader değişkenlerini gösterir. Önemli olanlar `BOOT` (hangi imajın açılacağı) ve bazı switch'lerde `MANUAL_BOOT` (`yes` ise switch her seferinde prompt'ta durur). Router'larda ayrıca `confreg` ile configuration register'a bakın. `0x2100` değeri router'ı ROMMON'da tutar. Normal değer `0x2102`.

`help` ya da `?`, ROMMON sürümünüzün desteklediği komutları listeler.

## Senaryo 1: Doğru İmaj Flash'ta

İmaj orada ama boot değişkeni yanlış: güncellemeden sonra bir yazım hatası, silinmiş bir dosya adı ya da `MANUAL_BOOT=yes`.

### Elle Açın

Install mode'daki Catalyst 9000 ve diğer IOS-XE switch'ler:

```
switch: boot flash:packages.conf
```

Bundle mode'da ya da klasik Catalyst switch'lerde:

```
switch: boot flash:<imaj>.bin
```

Klasik Catalyst switch'lerde `archive download-sw` ile kurulan imajlar bir alt dizinde durur. Tam yolu `dir flash:<dizin>` ile kontrol edin.

Router'lar:

```
rommon 1 > boot bootflash:<imaj>.bin
```

Router configuration register yüzünden ROMMON'da kaldıysa:

```
rommon 1 > confreg 0x2102
rommon 2 > reset
```

### Boot Değişkenini IOS'tan Düzeltin

IOS çalışınca düzeltmeyi kalıcı hale getirin, yoksa sorun bir sonraki reload'da tekrar çıkar:

```
configure terminal
no boot system
boot system flash:packages.conf
end
write memory
show boot
```

Bundle mode'da `packages.conf` yerine `.bin` dosyasının adını, router'larda `bootflash:` kullanın.

## Senaryo 2: İmaj Yok ya da Bozuk

İmaj yanlışlıkla silinmiş, kopyalama yarıda kesilmiş ya da flash boş. İmajı dışarıdan cihaza getirmeniz gerekiyor. Bunun iki pratik yolu var.

| | ROMMON'dan TFTP | USB |
| --- | --- | --- |
| Sahada birinin olması gerekir mi | Hayır | Evet |
| Konsol sunucusu üzerinden çalışır mı | Evet | Yalnızca biri USB'yi takarsa |
| Hız | Ağa bağlı | Hızlı |
| Tipik kullanım | Data center, uzak lokasyonlar | Şube, lab |

### Seçenek A: ROMMON'dan TFTP ile Açılış

Bir konsol sunucusu üzerinden uzaktan bağlıysanız ve cihazın etrafındaki ağ çalışıyorsa en pratik yol TFTP. İşin zor kısmı ROMMON'daki ağ ayarları, çünkü ROMMON'da IOS, routing ya da DHCP yok. Her şeyi elle girersiniz.

**Gereksinimler:**

- **Management portu** bağlı ve erişilebilir olmalı. Catalyst 9000 switch'lerde bu, ayrı management portu (Gi0/0). ROMMON ön paneldeki portları kullanmaz.
- İmajın bulunduğu TFTP sunucusu management ağından erişilebilir olmalı. Kurulum ve firewall kuralları: [Cisco Güncellemeleri için TFTP, FTP ve SCP Sunucusu](/tr/posts/tftp-ftp-server-cisco-upgrades/).

**Catalyst 9000 switch'ler:**

```
switch: set IP_ADDRESS 192.0.2.50
switch: set IP_SUBNET_MASK 255.255.255.0
switch: set DEFAULT_GATEWAY 192.0.2.1
switch: ping 192.0.2.10
switch: boot tftp://192.0.2.10/cat9k_iosxe.<surum>.SPA.bin
```

Önce `ping` ile test edin. Ping başarısızsa açılışı denemenin anlamı yok. Management portundaki kabloyu, gateway'i ve TFTP sunucusundaki firewall'u kontrol edin.

Cisco'ya göre iki kısıt var:

- TFTP'den açılan switch **bundle mode'da** açılır.
- İmaj **flash'a kopyalanmaz**, yalnızca bellekten çalışır. Bir sonraki reload'da yine prompt'a dönersiniz.

**ISR 4000 ve diğer IOS-XE router'lar:**

```
rommon 1 > IP_ADDRESS=192.0.2.50
rommon 2 > IP_SUBNET_MASK=255.255.255.0
rommon 3 > DEFAULT_GATEWAY=192.0.2.1
rommon 4 > TFTP_SERVER=192.0.2.10
rommon 5 > TFTP_FILE=isr4300-universalk9.<surum>.SPA.bin
rommon 6 > set
rommon 7 > boot tftp://192.0.2.10/isr4300-universalk9.<surum>.SPA.bin
```

Değişken adları ve tam boot sözdizimi ROMMON sürümüne göre değişir. `set` ve `help` ile kontrol edin. Eski router'lar (ISR G2) bunun yerine imajı doğrudan flash'a yazan `tftpdnld` komutunu kullanır.

**Cihaz TFTP'den açıldıktan sonra:** İmajı flash'a kopyalayın, doğrulayın ve [güncelleme rehberindeki](/tr/posts/cisco-ios-xe-upgrade-guide/) gibi düzgünce kurun:

```
copy tftp://192.0.2.10/<imaj>.bin flash:
verify /md5 flash:<imaj>.bin
install add file flash:<imaj>.bin activate commit
```

Bundle mode'daki ya da klasik IOS'lu cihazlarda `install add` yerine `boot system`'i kopyalanan dosyaya ayarlayın.

### Seçenek B: USB'den Açılış

Biri USB bellek takabiliyorsa en kolay ve en hızlı yol bu. Belleği FAT32 ile biçimlendirin ve imajı kopyalayın.

```
switch: dir usbflash0:
switch: boot usbflash0:<imaj>.bin
```

ISR router'larda USB aygıtının adı genelde `usb0:` (bazı modellerde `usb1:`):

```
rommon 1 > dir usb0:
rommon 2 > boot usb0:<imaj>.bin
```

Cihaz ayağa kalkınca imajı USB'den flash'a kopyalayın ve boot değişkenini düzeltin:

```
copy usbflash0:<imaj>.bin flash:
verify /md5 flash:<imaj>.bin
```

Ardından Senaryo 1'deki gibi kurun ya da `boot system`'i ayarlayın.

### Seçenek C: emergency-install (Catalyst 9000)

Catalyst 9000 switch'lerde (9200 serisi hariç) ROMMON'da `emergency-install` komutu var. Bir imajı TFTP'den doğrudan flash'a kurar:

```
switch: emergency-install tftp://192.0.2.10/cat9k_iosxe.<surum>.SPA.bin
switch: boot flash:packages.conf
```

Dikkat: Bu komut konfigürasyon dahil **tüm flash dosya sistemini siler**. Yalnızca A ve B seçenekleri mümkün değilse ve konfigürasyon yedeğiniz varsa kullanın.

### Seçenek D: Konsol Üzerinden Xmodem (Klasik Catalyst)

2960 ve 3560 gibi klasik Catalyst switch'lerin boot loader'ında network yığını yok, çoğunda USB portu da yok. Son çare konsol üzerinden Xmodem ile aktarım:

```
switch: flash_init
switch: set BAUD 115200
switch: copy xmodem: flash:<imaj>.bin
```

`set BAUD` komutundan sonra terminal programınızı 115200 baud'a çevirin. Bu hızda bile aktarım uzun sürer. Sonra hızı `set BAUD 9600` ile geri alın, yoksa 9600 baud ile bağlanan bir sonraki kişi sadece anlamsız karakterler görür.

## Senaryo 3: ROMMON Yeni İmaj için Çok Eski

İmaj flash'ta ve doğru, ama cihaz yine de onunla açılmıyor. ISR 4000 router'larda bu, hedef sürüm cihazdakinden daha yeni bir ROMMON istediğinde olur. Örneğin ROMMON 16.12(2r) gerektiren 17.x sürümleri.

Bildiğim kadarıyla bu platformlarda ROMMON, ROMMON prompt'undan güncellenemiyor. Güncelleme IOS-XE'den yapılıyor. Çıkış yolu:

1. Mevcut ROMMON'la çalışan **daha eski bir imajla** açın. Sakladıysanız flash'tan, yoksa Senaryo 2'deki gibi TFTP ya da USB'den.
2. IOS-XE'de ROMMON'u güncelleyin: `upgrade rom-monitor filename bootflash:<rommon>.pkg R0`, ardından reload.
3. `show rom-monitor r0` ile kontrol edin.
4. Şimdi yeni imajı kurun.

[Güncelleme rehberinde](/tr/posts/cisco-ios-xe-upgrade-guide/) ROMMON kontrolünün güncellemeden önce gelmesinin sebebi bu.

Benzer bir durum: boot değişkeni başka bir platform ailesine ait bir imajı gösteriyor, örneğin ISR 4400'de bir ISR 4300 imajı. Cihaz ROMMON'da kalır. Doğru imajı elle açın ve boot değişkenini düzeltin.

## Önlem

- Mevcut ve bir önceki imajı management ağından erişilebilen bir sunucuda tutun.
- Planlı her reload'dan önce `show boot` (ya da `show bootvar`) ve ROMMON gereksinimini kontrol edin.
- Management portunu ihtiyacınız olmadan önce bağlayın ve test edin.
- Her güncellemede konsol erişimini hazır tutun: [Yeni Nesil Konsol Sunucu Mimarisi](/tr/posts/next-gen-console-server-architecture/).

## İlgili Yazılar

- [Cisco IOS ve IOS-XE Güncelleme Rehberi](/tr/posts/cisco-ios-xe-upgrade-guide/)
- [Cisco Güncellemeleri için TFTP, FTP ve SCP Sunucusu](/tr/posts/tftp-ftp-server-cisco-upgrades/)
- [Cisco Switch ve Router Şifre Kurtarma](/tr/posts/cisco-switch-password-recovery/)
- [Cisco Nexus NX-OS Güncelleme Rehberi (ROMMON kurtarma dahil)](/tr/posts/cisco-nexus-nxos-upgrade-guide/)

Kaynaklar: [Cisco: Troubleshoot Bootloader and Password Recovery on Catalyst 9000](https://cisco.com/c/en/us/support/docs/switches/catalyst-9300-series-switches/216944-troubleshoot-bootloader-rommon-and-pas.html) · [Cisco: ISR 4000 Stuck in ROMMON](https://www.cisco.com/c/en/us/support/docs/routers/4000-series-integrated-services-routers/200678-Troubleshoot-Cisco-4000-Series-ISR-Stuck.html)
