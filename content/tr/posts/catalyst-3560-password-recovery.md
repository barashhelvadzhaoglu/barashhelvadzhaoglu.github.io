---
title: "Cisco Catalyst 3560 Şifre Kurtarma: İki Yöntem, Adım Adım"
description: "Cisco Catalyst 3560'ta unutulan enable veya konsol şifresini kurtarma — boot loader ile konfigürasyonu koruyarak ya da şifre kurtarma kapalıysa fabrika ayarlarına dönerek."
date: 2026-10-16
draft: false

tags: ["Cisco", "Catalyst", "Switch", "Password Recovery", "Boot Loader", "IOS"]
categories: ["Network Operasyonları"]
keywords: ["Catalyst 3560 şifre kurtarma", "Cisco switch şifre sıfırlama", "flash_init", "config.text yeniden adlandırma", "no service password-recovery", "Cisco boot loader", "Cisco 3560 mode butonu", "enable secret sıfırlama"]
showToc: true
TocOpen: true
---

Bir switch'i devralıyorsunuz, dokümantasyon yok ve enable şifresini kimse bilmiyor. Ya da depodan çıkan bir lab switch'i, hiç koymadığınız bir şifreyi soruyor. Cisco Catalyst 3560'ta fiziksel erişiminiz ve bir konsol kablonuz varsa iki durumdan da konfigürasyonu kaybetmeden çıkabilirsiniz.

Bu rehber sahada karşılaşılan iki durumu anlatıyor:

- **Yöntem 1: Konfigürasyonu koruyarak.** Switch startup konfigürasyonunu yüklemeden açılır, şifreleri değiştirirsiniz ve eski konfigürasyonu geri yüklersiniz.
- **Yöntem 2: Şifre kurtarma kapatılmışsa.** Birisi `no service password-recovery` komutunu girmiş. Switch'i yine geri alabilirsiniz ama yalnızca fabrika ayarlarına döndürerek.

> **Lab notu:** Bu adımları kendi 8 portlu PoE Catalyst 3560 switch'imde uyguluyorum. Lab'dan alınan konsol çıktıları bu rehbere eklenecek.

## Gerekenler

- Switch'e fiziksel erişim. Uzaktan şifre kurtarma bilinçli olarak mümkün değil.
- Bir konsol kablosu (RJ-45 rollover ya da USB-seri) ve SecureCRT, PuTTY veya `screen` gibi bir terminal programı.
- Terminal ayarları: **9600 baud, 8 data bit, parity yok, 1 stop bit, flow control yok**.
- Bir bakım penceresi. Switch iki kez yeniden başlar ve bu sırada trafik iletmez.

Uzaktan konsol erişimi için profesyonel çözüm bir konsol sunucusu. Bkz. [Yeni Nesil Konsol Sunucu Mimarisi](/tr/posts/next-gen-console-server-architecture/).

## Kurtarma Nasıl Çalışıyor?

Catalyst 3560, startup konfigürasyonunu flash'ta `config.text` adlı bir dosyada tutar. Normal açılışta IOS bu dosyayı yükler. Şifre kurtarmada açılış IOS başlamadan önce kesilir ve **boot loader**'a düşersiniz. Bu, `switch:` prompt'u olan küçük bir ortamdır.

Boot loader'da flash dosya sistemine erişebilirsiniz. `config.text` yeniden adlandırılırsa IOS konfigürasyonsuz, yani şifresiz açılır. Ardından giriş yapar, konfigürasyonu elle geri yükler ve yeni şifreleri tanımlarsınız.

## Yöntem 1: Şifreyi Kurtar, Konfigürasyonu Koru

### Adım 1: Açılışı Kesin

1. Konsol kablosunu bağlayın ve terminal oturumunu açın.
2. Güç kablosunu çıkarın.
3. Ön paneldeki **Mode** butonuna basılı tutun.
4. Butonu bırakmadan gücü yeniden bağlayın.
5. Yaklaşık 15 saniye sonra, konsolda sistemin flash dosya sistemi başlatılmadan önce kesildiği mesajı görününce butonu bırakın.

Artık `switch:` prompt'unu görmelisiniz. Switch normal açılırsa gücü kesip butona biraz daha uzun basarak tekrar deneyin.

### Adım 2: Flash'ı Başlatın

Flash dosya sistemi henüz bağlanmadı. Başlatın:

```
switch: flash_init
```

Bazı eski boot loader sürümlerinde ayrıca yardımcı dosyaları yüklemek gerekir:

```
switch: load_helper
```

Ardından flash içeriğini listeleyin:

```
switch: dir flash:
```

IOS imajını (ya da imajı içeren bir dizini), `config.text`, `vlan.dat` ve varsa `private-config.text` dosyalarını görmelisiniz.

### Adım 3: Konfigürasyon Dosyasının Adını Değiştirin

```
switch: rename flash:config.text flash:config.text.old
```

`config.text` dosyasını **silmeyin**. Adını değiştirmek IOS'un onu yüklememesi için yeterli, içeriğine de birazdan ihtiyacınız olacak.

### Adım 4: IOS'u Konfigürasyonsuz Açın

```
switch: boot
```

Switch boş konfigürasyonla açılır. Initial configuration dialog'a girmek isteyip istemediğinizi sorduğunda **no** deyin.

### Adım 5: Eski Konfigürasyonu Geri Yükleyin

```
Switch> enable
Switch# rename flash:config.text.old flash:config.text
Switch# copy flash:config.text system:running-config
```

Switch artık hostname, VLAN'lar, interface'ler ve eski şifreler dahil orijinal konfigürasyonla çalışıyor. Privileged moda konfigürasyon yüklenmeden önce girdiğiniz için hâlâ bu moddasınız.

### Adım 6: Yeni Şifreleri Tanımlayın

```
Switch# configure terminal
Switch(config)# enable secret <yeni-enable-secret>
Switch(config)# username admin privilege 15 secret <yeni-sifre>
Switch(config)# line con 0
Switch(config-line)# login local
Switch(config-line)# line vty 0 15
Switch(config-line)# login local
Switch(config-line)# end
```

Bunu daha önceki kimlik doğrulama yapısına göre uyarlayın. Switch TACACS+ ya da RADIUS kullanıyorsa yerel yedek hesabın çalıştığını kontrol edin.

### Adım 7: Interface'leri Kontrol Edin ve Kaydedin

Bir konfigürasyonu running-config'e kopyalamak onu birleştirir, her interface'in durumunu birebir geri getirmez. Özellikle VLAN interface'lerinin (SVI) administratively down olup olmadığına bakın:

```
Switch# show ip interface brief
```

Açık olması gereken interface'leri `no shutdown` ile açın. Sonra kaydedin:

```
Switch# copy running-config startup-config
```

Her şeyin yeniden başlatmadan sonra da çalıştığından emin olmak için bir kez reload edip yeni bilgilerle giriş yapın.

## Yöntem 2: Şifre Kurtarma Kapatılmışsa

Switch'te `no service password-recovery` tanımlıysa Mode butonu farklı davranır. Boot loader'dan flash dosya sistemine erişemezsiniz. Bunun yerine switch şifre kurtarmanın kapalı olduğunu söyler ve sistemi varsayılan konfigürasyona döndürmek isteyip istemediğinizi sorar.

- **yes** derseniz switch konfigürasyon dosyasını ve VLAN veritabanını siler, fabrika ayarlarıyla açılır. IOS imajı flash'ta kalır.
- **no** derseniz switch mevcut konfigürasyonla normal açılır ve yine şifre ekranına dönersiniz.

Bu özelliğin bilinçli bir bedeli var. Fiziksel erişimi olan bir saldırgan konfigürasyonu okuyamaz, ama siz de onu kaybedersiniz.

Sıfırlamadan önce konfigürasyonun başka bir kaynakta güncel bir yedeği olduğundan emin olun: bir konfigürasyon yönetim aracı, bir TFTP sunucusu ya da arşivlenmiş bir `show running-config` çıktısı. Sıfırlamadan sonra:

1. Şifresiz giriş yapın ve yeni bilgileri tanımlayın.
2. Konfigürasyonu yedekten geri yükleyin.
3. Yedekte yoksa VLAN'ları yeniden oluşturun. VLAN veritabanı (`vlan.dat`) da silinir.
4. `no service password-recovery`'nin tekrar açılıp açılmayacağına karar verin. Herkese açık ya da kilitsiz yerlerdeki switch'ler için mantıklı, yeter ki konfigürasyon başka bir yerde yedekli olsun.

## Yeni Boot Loader'lar: Startup Konfigürasyonunu Yok Saymak

Yeni Catalyst modelleri ve boot loader sürümleri `config.text`'i yeniden adlandırmaktan daha temiz bir yol sunuyor: IOS'a bir açılış için startup konfigürasyonunu yok saymasını söyleyen bir boot loader değişkeni. Switch'inizin bunu destekleyip desteklemediği model ve boot loader sürümüne bağlı. `switch:` prompt'unda `set` yazarak boot loader'ınızın tanıdığı değişkenleri görebilirsiniz.

3560'ın boot loader'ının burada ne sunduğunu lab çıktıları gelince ekleyeceğim.

## Sık Yapılan Hatalar

- **`config.text`'i yeniden adlandırmak yerine silmek.** Konfigürasyon gider, tek çare yedek.
- **Dosyanın adını geri değiştirmeyi unutmak.** Bir sonraki reload'da switch konfigürasyonsuz açılır.
- **Adı geri değiştirmeden `copy startup-config running-config` kullanmak.** O anda startup konfigürasyonu normal adıyla mevcut değil.
- **Şifreleri değiştirdikten sonra kaydetmemek.** Bir sonraki reload'da eski şifreler geri gelir.
- **Birleştirmeden sonra kapalı kalan SVI'lar.** Konfigürasyon doğru görünse de ağ üzerinden yönetim erişimi çalışmaz.

## İlgili Yazılar

- [Catalyst 3560 IOS Güncelleme: İki Yöntem ve Doğrulama](/tr/posts/catalyst-3560-ios-upgrade/)
- [Catalyst 3560 Açılmıyorsa: Boot Loader ile Kurtarma](/tr/posts/catalyst-3560-boot-loader-recovery/)
- [Cisco Nexus NX-OS Yazılım Güncelleme Rehberi](/tr/posts/cisco-nexus-nxos-upgrade-guide/)
- [Yeni Nesil Konsol Sunucu Mimarisi](/tr/posts/next-gen-console-server-architecture/)
