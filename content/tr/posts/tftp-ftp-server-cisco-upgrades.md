---
title: "Cisco Güncellemeleri için TFTP, FTP ve SCP Sunucusu: Kurulum ve Sorun Giderme"
description: "Cisco IOS ve IOS-XE imaj aktarımı için Windows, macOS ve Linux'ta TFTP, FTP ya da SCP sunucusu kurulumu — cihaz tarafı komutlar, management VRF, FTP yolundaki çift slash, boyut sınırları ve firewall sorunları."
date: 2026-10-22
draft: false

tags: ["Cisco", "TFTP", "FTP", "SCP", "IOS", "IOS-XE", "Upgrade"]
categories: ["Network Operasyonları"]
keywords: ["Cisco TFTP sunucu kurulumu", "copy tftp flash", "copy ftp bootflash", "ip ftp username", "ip tftp source-interface", "Tftpd64", "tftpd-hpa", "macOS TFTP sunucusu", "Cisco SCP kopyalama", "TFTP 32MB sınırı", "Mgmt-vrf copy"]
showToc: true
TocOpen: true
---

Her Cisco güncellemesi bir dosyayı cihaza getirmekle başlar. 20 MB'lık klasik bir IOS imajı için neredeyse her yöntem iş görür. WAN üzerinden 1 GB'lık bir IOS-XE imajında ise protokol seçimi, kopyalamanın beş dakika mı süreceğini yoksa bir saat sonra mı yarıda kalacağını belirler.

Bu rehber hangi protokolün ne zaman kullanılacağını, sunucunun Windows, macOS ve Linux'ta nasıl kurulacağını ve cihaz tarafındaki komutları ve tuzakları anlatıyor.

## Hangi Protokol?

| Protokol | Port | Kimlik doğrulama | Güçlü yanları | Zayıf yanları |
| --- | --- | --- | --- | --- |
| TFTP | UDP 69 | Yok | Basit, her yerde destekleniyor, ROMMON'dan çalışır | Yavaş, WAN'da güvenilmez, eski sunucularda boyut sınırı |
| FTP | TCP 21 (+ veri) | Kullanıcı ve şifre | Büyük imajlar için hızlı ve güvenilir | Açık metin, veri kanalı için firewall ayarı gerekir |
| SCP | TCP 22 | SSH | Şifreli, mevcut SSH erişimini kullanır | Bazı platformlarda FTP'den yavaş |
| HTTP(S) | TCP 80/443 | İsteğe bağlı | Hızlı, sunması kolay | Eski IOS sürümlerinde yok |

Sahadaki kuralım:

- Ağ üzerinden normal güncellemeler için **FTP**. Büyük IOS-XE imajlarında hızlı ve güvenilir.
- Cihaz ROMMON'daysa **TFTP**. ROMMON yalnızca TFTP biliyor. Bkz. [Cisco ROMMON Kurtarma](/tr/posts/cisco-rommon-recovery/).
- Güvenlik politikası açık metin protokollere izin vermiyorsa **SCP**.

## Sunucu Kurulumu

### Windows: Tftpd64

Tftpd64; TFTP sunucusu, DHCP sunucusu ve syslog sunucusunu bir arada sunan ücretsiz bir araç.

1. Tftpd64'ü kurun ve başlatın.
2. **Current Directory**'yi imajların bulunduğu klasör yapın.
3. **Server interface** olarak cihazlara bakan ağ adaptörünün IP adresini seçin.
4. Windows firewall'da Tftpd64'e izin verin. Zaman aşımlarının en sık sebebi bu.

Windows'ta FTP için yaygın ücretsiz seçenek FileZilla Server.

### macOS: Yerleşik TFTP Sunucusu

macOS'ta hazır bir TFTP sunucusu var. Dosyaları `/private/tftpboot` dizininden sunar:

```
sudo mkdir -p /private/tftpboot
sudo cp <imaj>.bin /private/tftpboot/
sudo chmod 644 /private/tftpboot/<imaj>.bin
sudo launchctl load -F /System/Library/LaunchDaemons/tftp.plist
```

Durdurmak için `sudo launchctl unload -F /System/Library/LaunchDaemons/tftp.plist`. macOS firewall'u açıksa gelen bağlantılara izin verin.

### Linux: tftpd-hpa ve vsftpd

Debian ve Ubuntu'da:

```
sudo apt install tftpd-hpa
```

Konfigürasyon `/etc/default/tftpd-hpa` dosyasında. Varsayılan dizin `/srv/tftp`:

```
TFTP_DIRECTORY="/srv/tftp"
TFTP_OPTIONS="--secure"
```

`TFTP_OPTIONS`'a `--create` seçeneğini yalnızca cihazların dosya yüklemesi gerekiyorsa ekleyin, örneğin konfigürasyon yedekleri için.

FTP için yerel bir kullanıcıyla `vsftpd` yeterli:

```
sudo apt install vsftpd
sudo adduser netops
```

İmajları kullanıcının home dizinine ya da `/tftpboot/images` gibi ortak bir dizine koyun.

## Cihaz Tarafı: İmajı Kopyalamak

### TFTP

```
copy tftp://192.0.2.10/<imaj>.bin flash:
```

### FTP

Kullanıcı bilgileri URL'nin içinde olabilir ya da bir kez tanımlanabilir:

```
configure terminal
ip ftp username netops
ip ftp password <sifre>
end
copy ftp://192.0.2.10/images/<imaj>.bin bootflash:
```

**Çift slash.** IOS, FTP URL'sindeki yolu FTP kullanıcısının home dizinine göre değerlendirir. İmajlar home dizini dışında mutlak bir yoldaysa sunucu adresinden sonra iki slash kullanın:

```
copy ftp://192.0.2.10//tftpboot/images/<imaj>.bin bootflash:
```

`ftp://sunucu/images/dosya`, `<home>/images/dosya` anlamına gelir. `ftp://sunucu//tftpboot/images/dosya` ise `/tftpboot/images/dosya` demektir. Pek çok "file not found" hatasının sebebi bu ayrıntı.

### SCP

Bir SCP sunucusundan dosya çekmek:

```
copy scp://netops@192.0.2.10/images/<imaj>.bin flash:
```

Laptoptan cihaza dosya göndermek için cihazda SCP sunucusunun açık olması gerekir:

```
configure terminal
ip scp server enable
end
```

Sonra laptoptan:

```
scp <imaj>.bin admin@<cihaz-ip>:flash:<imaj>.bin
```

Politikanız gerektiriyorsa aktarımdan sonra `ip scp server enable`'ı tekrar kapatın.

### Her Zaman Doğrulayın

```
verify /md5 flash:<imaj>.bin
```

Değeri Cisco indirme sayfasındaki MD5 checksum ile karşılaştırın. Hatasız kopyalanmış bir dosya bile eksik olabilir.

## Management Portu ve VRF

Catalyst 9000 switch'lerde ayrı management portu (GigabitEthernet0/0), `Mgmt-vrf` adlı kendi VRF'inde durur. ISR 4000 ve Catalyst 8000 router'larda management portu `Mgmt-intf` VRF'inde. VRF belirtilmeyen bir kopyalama global routing tablosunu kullanır ve sunucuya yalnızca management ağından ulaşılabiliyorsa başarısız olur.

Cihaza kaynak olarak hangi interface'i kullanacağını söyleyin:

```
configure terminal
ip tftp source-interface GigabitEthernet0/0
ip ftp source-interface GigabitEthernet0/0
end
```

ISR 4000 router'larda management portunun adı `GigabitEthernet0`. Adı `show ip interface brief` ile kontrol edin.

## Sorun Giderme

### Zaman Aşımı ya da "Connection refused"

- Doğru kaynak interface ya da VRF ile cihazdan sunucuya `ping` atın.
- Sunucudaki firewall'u kontrol edin. Windows ve macOS gelen bağlantıları varsayılan olarak engeller.
- FTP'de veri kanalı ek portlar kullanır. Cihaz ile sunucu arasında bir firewall varsa passive mode sorunları sık görülür.

### "File not found"

- Yolu sunucunun kök dizinine (TFTP) ya da kullanıcının home dizinine (FTP) göre kontrol edin. Çift slash'ı unutmayın.
- Büyük-küçük harfe dikkat edin. Linux ve macOS sunucularda dosya adları büyük-küçük harfe duyarlı.
- Sunucu kullanıcısının dosyayı okuyabildiğini kontrol edin.

### Kopyalama 32 MB'da Duruyor (TFTP)

Klasik TFTP 512 byte'lık bloklar ve 16 bit'lik bir blok sayacı kullanır. İki taraf da daha büyük blokları ya da blok numarasının başa dönmesini desteklemiyorsa bu, bir aktarımı yaklaşık 32 MB ile sınırlar. Eski ya da minimal TFTP sunucularında bu sınır hâlâ var. IOS-XE imajları ise çok daha büyük.

- Büyük imajlarda FTP ya da SCP kullanın.
- TFTP şartsa güncel bir sunucu kullanın ve cihazda blok boyutunu artırın:

```
configure terminal
ip tftp blocksize 8192
end
```

### Aktarım Çok Yavaş

TFTP her bloktan sonra bir onay bekler. Gecikmesi yüksek bir WAN hattında bu onu son derece yavaşlatır. Uzak mesafelerde FTP ya da SCP kullanın ya da cihaza yakın bir sunucu konumlandırın.

## İlgili Yazılar

- [Cisco IOS ve IOS-XE Güncelleme Rehberi](/tr/posts/cisco-ios-xe-upgrade-guide/)
- [Cisco ROMMON Kurtarma: Flash, TFTP ya da USB'den Açılış](/tr/posts/cisco-rommon-recovery/)
- [Cisco Nexus NX-OS Yazılım Güncelleme Rehberi](/tr/posts/cisco-nexus-nxos-upgrade-guide/)
- [Network Mühendisleri için SecureCRT ve SuperPuTTY](/tr/technology/securecrt-superputty/)
