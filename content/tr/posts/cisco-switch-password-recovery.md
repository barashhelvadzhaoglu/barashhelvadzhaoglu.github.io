---
title: "Cisco Switch ve Router Şifre Kurtarma: Catalyst 9000, 2960, 3560 ve ISR"
description: "Cisco cihazlarda unutulan enable ya da konsol şifresini konfigürasyonu kaybetmeden kurtarma — klasik Catalyst (2960, 3560, 3750), SWITCH_IGNORE_STARTUP_CFG ile Catalyst 9000 ve 3850, confreg 0x2142 ile ISR router'lar ve şifre kurtarma kapalıysa yapılacaklar."
date: 2026-10-22
draft: false
aliases:
  - "/tr/posts/catalyst-3560-password-recovery/"

tags: ["Cisco", "Password Recovery", "ROMMON", "IOS", "IOS-XE", "Catalyst 9300", "Catalyst 9200", "Catalyst 2960", "Catalyst 3560", "ISR 4000"]
categories: ["Network Operasyonları"]
keywords: ["Cisco şifre kurtarma", "Cisco switch şifre sıfırlama", "Catalyst 9300 şifre kurtarma", "SWITCH_IGNORE_STARTUP_CFG", "no system ignore startupconfig switch all", "flash_init config.text", "confreg 0x2142", "no service password-recovery", "Cisco 2960 şifre kurtarma", "ISR 4331 şifre kurtarma"]
showToc: true
TocOpen: true
---

Dokümantasyonu olmayan bir cihazı devralıyorsunuz ya da depodan çıkan bir lab switch'i kimsenin bilmediği bir şifre soruyor. Cisco switch ve router'larda, fiziksel erişiminiz ve bir konsol kablonuz varsa bu durumdan konfigürasyonu kaybetmeden çıkabilirsiniz.

Prensip her yerde aynı: açılışı kesin, IOS'u startup konfigürasyonunu **yüklemeden** başlatın, sonra konfigürasyonu geri getirip yeni şifreleri tanımlayın. Değişen tek şey, cihaza konfigürasyonu atlamasını nasıl söylediğiniz:

| Platform | Tipik modeller | Konfigürasyon nasıl atlanır |
| --- | --- | --- |
| Klasik Catalyst | 2960, 2960-X, 3560, 3750 | Boot loader'da `config.text`'in adını değiştirmek |
| IOS-XE Catalyst | 3650, 3850, 9200, 9300, 9400, 9500 | `SWITCH_IGNORE_STARTUP_CFG=1` |
| Router'lar | ISR 4000, ISR 1100, Catalyst 8000, ISR G2 | Configuration register `0x2142` |

## Gerekenler

- Cihaza fiziksel erişim ya da bir konsol sunucusu. Şifre kurtarma ağ üzerinden bilinçli olarak mümkün değil. Bkz. [Yeni Nesil Konsol Sunucu Mimarisi](/tr/posts/next-gen-console-server-architecture/).
- Bir konsol kablosu ve terminal programı. Ayarlar: **9600 baud, 8 data bit, parity yok, 1 stop bit, flow control yok**.
- Bir bakım penceresi. Cihaz yeniden başlar ve bu sırada trafik iletmez.

## Switch'ler: switch: Prompt'una Ulaşmak

Catalyst switch'lerde açılışı **Mode** butonuyla kesersiniz:

1. Konsolu bağlayın ve terminal oturumunu açın.
2. Gücü kesin.
3. Ön paneldeki **Mode** butonuna basılı tutarak gücü yeniden bağlayın.
4. Konsolda açılışın kesildiği mesajı görünene kadar, yaklaşık 10-15 saniye basılı tutun, sonra bırakın.

Artık `switch:` prompt'undasınız.

Çift supervisor'lı bir Catalyst 9400'de Cisco, başlamadan önce ikincil supervisor'ın çıkarılmasını öneriyor.

## Klasik Catalyst (2960, 3560, 3750): config.text'in Adını Değiştirmek

```
switch: flash_init
switch: dir flash:
switch: rename flash:config.text flash:config.text.old
switch: boot
```

Bazı eski boot loader'larda `flash_init`'ten sonra ayrıca `load_helper` gerekir. `config.text`'i **silmeyin**. Adını değiştirmek yeterli ve içeriğine daha sonra ihtiyacınız olacak.

Switch konfigürasyonsuz açılır. Initial configuration dialog'a **no** deyin, ardından:

```
Switch> enable
Switch# rename flash:config.text.old flash:config.text
Switch# copy flash:config.text system:running-config
```

Aşağıdaki "Yeni Şifreleri Tanımlayın ve Kaydedin" bölümüyle devam edin.

## Catalyst 9000 ve 3850: SWITCH_IGNORE_STARTUP_CFG

IOS-XE switch'lerde dosya adını değiştirmek gerekmez. Bir boot loader değişkeni IOS'a startup konfigürasyonunu yok saymasını söyler:

```
switch: SWITCH_IGNORE_STARTUP_CFG=1
switch: boot flash:packages.conf
```

Switch bundle mode'daysa `boot flash:<imaj>.bin` kullanın. Açılıştan sonra initial configuration dialog'a **no** deyin ve konfigürasyonu yükleyin:

```
Switch> enable
Switch# copy startup-config running-config
```

**Önemli:** Değişkeni IOS'tan geri alın. Yoksa switch her reload'da konfigürasyonunu yok sayar:

```
Switch# configure terminal
Switch(config)# no system ignore startupconfig switch all
Switch(config)# end
```

Sonraki bölümle devam edin, ardından kaydedin.

## Router'lar (ISR 4000, ISR 1100, Catalyst 8000): confreg 0x2142

Router'larda Mode butonu yok. Açılışı, gücü verdikten sonraki ilk saniyelerde terminal programından bir **Break** göndererek kesersiniz. `rommon 1 >` prompt'una düşersiniz.

```
rommon 1 > confreg 0x2142
rommon 2 > reset
```

`0x2142` değeri router'a startup konfigürasyonunu yok saymasını söyler. Açılıştan sonra initial configuration dialog'a **no** deyin:

```
Router> enable
Router# copy startup-config running-config
Router# configure terminal
Router(config)# config-register 0x2102
```

Register'ı `0x2102`'ye geri almak şart. Yoksa router her reload'da konfigürasyonunu yok sayar.

## Yeni Şifreleri Tanımlayın ve Kaydedin

Artık privileged moddasınız ve orijinal konfigürasyon yüklü. Yeni bilgileri önceki kimlik doğrulama yapısına uygun şekilde tanımlayın:

```
configure terminal
enable secret <yeni-enable-secret>
username admin privilege 15 secret <yeni-sifre>
line con 0
 login local
line vty 0 15
 login local
end
```

Cihaz TACACS+ ya da RADIUS kullanıyorsa yerel yedek hesabın çalıştığını kontrol edin.

Bir konfigürasyonu running-config'e kopyalamak onu birleştirir. Interface'ler, özellikle switch'lerdeki VLAN interface'leri (SVI), administratively down kalabilir. Kontrol edip düzeltin:

```
show ip interface brief
```

Açık olması gereken interface'leri `no shutdown` ile açın. Sonra kaydedip test edin:

```
write memory
reload
```

Konfigürasyonun ve şifrelerin reload'dan sonra da geçerli olduğundan emin olmak için yeni bilgilerle giriş yapın.

## Şifre Kurtarma Kapatılmışsa

`no service password-recovery` tanımlıysa süreç farklı işler. Cihaz konfigürasyonu atlamanıza izin vermez. Bunun yerine şifre kurtarmanın kapalı olduğunu söyler ve fabrika ayarlarına dönmek isteyip istemediğinizi sorar.

- **Yes:** Konfigürasyon (switch'lerde VLAN veritabanı da) silinir. Cihaz varsayılan ayarlarla açılır. IOS imajı kalır.
- **No:** Cihaz mevcut konfigürasyonla normal açılır ve yine şifre ekranına dönersiniz.

Bu özelliğin amacı bu. Fiziksel erişimi olan biri konfigürasyonu okuyamaz, ama siz de onu kaybedersiniz. Yes demeden önce başka bir kaynakta güncel bir konfigürasyon yedeğiniz olduğundan emin olun. Sıfırlamadan sonra konfigürasyonu geri yükleyin, yedekte yoksa VLAN'ları yeniden oluşturun.

`no service password-recovery`, herkese açık ya da kilitsiz yerlerdeki cihazlar için mantıklı, yeter ki konfigürasyon başka bir yerde yedekli olsun.

## Sık Yapılan Hatalar

- **`config.text`'in adını değiştirmek yerine silmek.** O zaman tek çare yedek.
- **`no system ignore startupconfig switch all` ya da `config-register 0x2102`'yi unutmak.** Cihaz bir sonraki reload'da konfigürasyonsuz açılır.
- **Şifreleri tanımladıktan sonra kaydetmemek.** Bir sonraki reload'da eski şifreler geri gelir.
- **Birleştirmeden sonra kapalı kalan SVI'lar.** Konfigürasyon doğru görünse de ağ üzerinden yönetim erişimi çalışmaz.

## İlgili Yazılar

- [Cisco ROMMON Kurtarma: Flash, TFTP ya da USB'den Açılış](/tr/posts/cisco-rommon-recovery/)
- [Cisco IOS ve IOS-XE Güncelleme Rehberi](/tr/posts/cisco-ios-xe-upgrade-guide/)
- [Yeni Nesil Konsol Sunucu Mimarisi](/tr/posts/next-gen-console-server-architecture/)

Kaynak: [Cisco: Troubleshoot Bootloader and Password Recovery on Catalyst 9000](https://cisco.com/c/en/us/support/docs/switches/catalyst-9300-series-switches/216944-troubleshoot-bootloader-rommon-and-pas.html)
