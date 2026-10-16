---
title: "Catalyst 3560 Açılmıyorsa: Boot Loader ile Kurtarma"
description: "switch: prompt'unda kalan bir Cisco Catalyst 3560'ı kurtarma — boot loader değişkenleri, başka bir imajla açılış ve Xmodem ile konsol üzerinden yeni IOS imajı aktarma."
date: 2026-10-16
draft: false

tags: ["Cisco", "Catalyst", "Switch", "Boot Loader", "IOS", "Recovery"]
categories: ["Network Operasyonları"]
keywords: ["Catalyst 3560 boot loader", "Cisco switch prompt kurtarma", "copy xmodem flash", "Cisco switch boot döngüsü", "BOOT değişkeni Cisco", "MANUAL_BOOT", "Cisco 3560 IOS imajı yok", "Cisco switch xmodem baud rate"]
showToc: true
TocOpen: true
---

Her network mühendisi er ya da geç bunu yaşar: reload'dan sonra switch geri gelmez. Konsolda sadece `switch:` prompt'u vardır. IOS imajı yoktur, bozuktur ya da boot değişkeni var olmayan bir dosyayı gösteriyordur.

Bu, switch'i değiştirmek için bir sebep değil. Catalyst 3560'ın boot loader'ında, flash'taki imaj tamamen silinmiş olsa bile IOS'u yeniden çalıştırmak için gereken her şey var. Bu rehberde şunlar anlatılıyor:

- Boot loader ortamını nasıl okuyacağınız ve switch'in neden orada durduğu
- Flash'ta zaten olan bir imajla nasıl açılış yapacağınız
- Flash boşsa **Xmodem** ile konsol üzerinden yeni imajı nasıl aktaracağınız
- Çözümü nasıl kalıcı hale getireceğiniz

> **Lab notu:** Bu senaryoları kendi 8 portlu PoE Catalyst 3560 switch'imde test ediyorum. Lab'dan alınan konsol çıktıları ve aktarım süreleri bu rehbere eklenecek.

## Switch Neden Boot Loader'da Kalıyor?

Boot loader, IOS'u `BOOT` değişkeninde yazan imajdan başlatır. Bu başarısız olursa ya da `BOOT` değişkeni tanımlı değilse ve boot loader kendisi açılabilir bir imaj bulamazsa, switch `switch:` prompt'unda kalır. Tipik sebepler:

- Güncelleme ters gitmiştir: `boot system`'de bir yazım hatası vardır ya da yenisi hazır olmadan eski imaj silinmiştir.
- İmaj dosyası bozuktur, örneğin yarıda kesilmiş bir kopyalama yüzünden.
- `MANUAL_BOOT` değişkeni `yes` olarak ayarlıdır, switch her seferinde prompt'ta bekler.
- Flash dosya sistemi bozulmuştur.

Bir diğer belirti **boot döngüsü**: switch IOS'u yüklemeye başlar, çöker ve tekrar tekrar yeniden başlar. Döngüyü kırmak için açılışı Mode butonuyla kesin. Adımlar [şifre kurtarma rehberinde](/tr/posts/catalyst-3560-password-recovery/) anlatılıyor.

## Adım 1: Durumu İnceleyin

Flash'ı başlatın ve içeriğe bakın:

```
switch: flash_init
switch: dir flash:
```

Ardından boot loader ortam değişkenlerini görüntüleyin:

```
switch: set
```

En önemli değişkenler:

| Değişken | Anlamı |
| --- | --- |
| `BOOT` | Switch'in açmaya çalıştığı imaj(lar), noktalı virgülle ayrılır |
| `MANUAL_BOOT` | `yes` = her zaman boot loader prompt'unda dur |
| `BAUD` | Konsol hızı. Değişken tanımlı değilse varsayılan 9600 |
| `CONFIG_FILE` | Konfigürasyon dosyasının adı, varsayılan `config.text` |

Boot loader sürümünüzün hangi komutları desteklediğini `help` ile görebilirsiniz.

## Adım 2: Flash'taki Bir İmajla Açın

`dir flash:` geçerli bir IOS imajı gösteriyorsa doğrudan onunla açabilirsiniz. `archive download-sw` ile kurulan imajlar bir alt dizinde durur, bu yüzden tam yolu kontrol edin:

```
switch: dir flash:c3560-ipservicesk9-mz.<surum>
switch: boot flash:c3560-ipservicesk9-mz.<surum>/c3560-ipservicesk9-mz.<surum>.bin
```

Sorun `MANUAL_BOOT` ise düzeltin:

```
switch: set MANUAL_BOOT no
```

IOS çalışınca boot değişkenini kalıcı olarak ayarlayın:

```
Switch# configure terminal
Switch(config)# boot system flash:<yol>/<imaj>.bin
Switch(config)# end
Switch# copy running-config startup-config
Switch# show boot
```

## Adım 3: Flash Boş: Xmodem ile İmaj Aktarın

Flash'ta kullanılabilir bir imaj yoksa bir tane getirmeniz gerekir. Klasik Catalyst 3560'ta boot loader'ın network yığını yok, switch'in de USB depolama portu yok. Yani tek yol konsol. Kullanılan protokol **Xmodem** ve ciddi her terminal programı bunu destekler.

### İmajı Hazırlayın

`.tar` değil `.bin` dosyasını kullanın. Xmodem tek bir dosya aktarır ve boot loader arşiv açamaz. Aktarım uzun sürdüğü ve tekrarlamak istemeyeceğiniz için MD5 checksum'ı önceden bilgisayarınızda kontrol edin.

### Konsol Hızını Artırın

9600 baud'da bu boyutta bir IOS imajını aktarmak birkaç saat sürer. Önce hızı artırın:

```
switch: set BAUD 115200
```

Konsol çıktısı hemen okunmaz hale gelir. Terminal programınızı 115200 baud'a çevirin ve `switch:` prompt'u geri gelene kadar Enter'a basın.

### Aktarımı Başlatın

```
switch: copy xmodem: flash:c3560-ipservicesk9-mz.<surum>.bin
```

Switch dosyayı bekler. Terminal programınızda bir Xmodem gönderimi başlatın:

- **SecureCRT:** Transfer > Send Xmodem
- **Tera Term:** File > Transfer > XMODEM > Send
- **minicom / screen:** `lrzsz` paketindeki `sx`

115200 baud'da imaj boyutuna ve terminal programına bağlı olarak yarım saat ile bir saat arası bir süre bekleyin. Aktarım sırasında konsol oturumuna dokunmayın.

### Yeni İmajla Açın

```
switch: dir flash:
switch: boot flash:c3560-ipservicesk9-mz.<surum>.bin
```

## Adım 4: Toparlayın

IOS çalışınca:

1. İmajı doğrulayın: `verify /md5 flash:<imaj>.bin`
2. Adım 2'deki gibi `boot system`'i yeni imaja ayarlayın ve kaydedin.
3. **Konsol hızını geri alın.** Boot loader'daki `BAUD` 115200'de kalırsa konsol da bu hızda kalır. Daha sonra varsayılan 9600 baud ile bağlanan herkes sadece anlamsız karakterler görür. Değeri boot loader'da geri alın (`set BAUD 9600`) ya da IOS'taki konsol hızının ekibinizin beklediği değer olduğundan emin olun.
4. Switch'in yardımsız açıldığını görmek için bir kez reload edin.

## Peki TFTP ve USB?

Yeni Catalyst platformlarında boot loader daha fazlasını yapabiliyor. Bazı modellerde USB depolama portu (`usbflash0:`) var ya da management portundan ağ üzerinden imajla açılabiliyorlar. Bu, Xmodem'den çok daha hızlı. Klasik 3560'ta bu seçenekler yok, yani flash boşsa tek yol Xmodem. Platformunuzun neleri desteklediğini `switch:` prompt'unda `help` yazarak görebilirsiniz.

Cihaz açılmadığında TFTP ya da USB'den açılış fikri, data center switch'leri için [Nexus NX-OS güncelleme rehberinde](/tr/posts/cisco-nexus-nxos-upgrade-guide/) anlatılıyor.

## Önlem

- Mevcut ve bir önceki imajı erişebildiğiniz bir TFTP sunucusunda tutun.
- Her güncellemeden sonraki reload'dan önce MD5 checksum'ı doğrulayın.
- Planlı her reload'dan önce `show boot`'u kontrol edin.
- Her güncellemede konsol erişimini hazır tutun. Konsol sunucusu bunu uzaktan da mümkün kılar: [Yeni Nesil Konsol Sunucu Mimarisi](/tr/posts/next-gen-console-server-architecture/).

## İlgili Yazılar

- [Cisco Catalyst 3560 Şifre Kurtarma: İki Yöntem](/tr/posts/catalyst-3560-password-recovery/)
- [Catalyst 3560 IOS Güncelleme: İki Yöntem ve Doğrulama](/tr/posts/catalyst-3560-ios-upgrade/)
- [Cisco Nexus NX-OS Yazılım Güncelleme Rehberi](/tr/posts/cisco-nexus-nxos-upgrade-guide/)
