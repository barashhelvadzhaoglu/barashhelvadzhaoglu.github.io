---
title: "SecureCRT ve SuperPutty: Her Ağ Mühendisinin Bilmesi Gereken Terminal Araçları"
description: "SecureCRT ve SuperPutty saha rehberi — oturum loglama, taşınabilirlik, kimlik yönetimi, scripting ve SuperPutty'nin PuTTY'ya göre avantajları."
date: 2026-04-13
draft: false

cover:
  image: "/img/postimages/securecrt-superputty-cover.webp"
  alt: "SecureCRT ve SuperPutty — Ağ Mühendisi Terminal Araçları"
  relative: false

tags: ["SecureCRT", "SuperPutty", "PuTTY", "SSH", "Ağ Araçları", "Terminal İstemcisi", "Ağ Mühendisi", "Otomasyon"]
categories: ["Teknoloji"]
keywords:
  - SecureCRT otomatik loglama
  - SecureCRT oturum yönetimi
  - SecureCRT scripting
  - SuperPutty PuTTY alternatifi
  - SecureCRT vs SuperPutty
  - ağ mühendisi terminal araçları
  - SecureCRT oturum dışa aktarma içe aktarma
  - SuperPutty sekmeli oturumlar
  - SecureCRT kimlik bilgisi depolama
  - SSH terminal istemcisi ağ mühendisi

showToc: true
TocOpen: true
---

# SecureCRT ve SuperPutty: Her Ağ Mühendisinin Bilmesi Gereken Terminal Araçları

Birkaç yıldan fazla ağ mühendisliği yapıyorsanız, muhtemelen terminal istemcisinin içinde binlerce saat geçirmişsinizdir. Bir switch'e SSH, birkaç show komutu, değişiklik yap, sonraki cihaza geç. İşin en tekrar eden iş akışı — ve doğru araç bunu önemli ölçüde daha az acı verici kılar.

Çoğu mühendis PuTTY ile başlar. Çalışır, ücretsizdir ve söylediğini yapar. Ancak terminal iş akışını işlevsel olmaktan gerçekten verimli olmaya taşıyan iki araç vardır: **SecureCRT** (profesyonel standart) ve **SuperPutty** (PuTTY kullanıcılarının ihtiyaç duyduğunu bilmediği ücretsiz yükseltme).

Bu yazı her ikisini de kapsar — gerçekte ne yaptıklarını, günlük ağ çalışmasında önemli olan özellikleri ve her birinin ne zaman mantıklı olduğunu.

---

## Neden Düz PuTTY Sonunda Yetmez

PuTTY sağlam bir araçtır. Ara sıra bağlantılar için mükemmel biçimde yeterlidir. Ancak günlük ağ mühendisliği çalışmasında — düzinelerce cihazı yönetmek, birden fazla oturumda aynı anda sorun gidermek, hangi komutların ne zaman çalıştırıldığının kayıtlarına ihtiyaç duymak — düz PuTTY sürtünme yaratır:

- **Sekme yok:** Her bağlantı ayrı bir penceredir. 15 cihazı aynı anda yönetmek, görev çubuğunda 15 pencere ve sürekli doğru olanı aramak demektir.
- **Otomatik loglama yok:** Bir şeyler ters giderse ve 20 dakika önce hangi komutların çalıştırıldığını bilmeniz gerekiyorsa, oturumdan önce loglama'yı manuel olarak yapılandırmadıysanız PuTTY bu kaydı tutmaz. Olay baskısı altında bu nadiren yapılır.
- **Oturum taşınabilirliği yok:** PuTTY oturumları Windows Registry'de saklanır. Yeni bir dizüstü bilgisayara geçmek, kaydedilmiş her oturumu manuel olarak yeniden oluşturmak veya registry anahtarlarını dışa aktarıp hiçbir şeyin bozulmamasını ummak demektir.
- **Oturum başına kimlik bilgisi depolama yok:** Bir ana bilgisayar adı ve port kaydedebilirsiniz, ancak kimlik bilgilerini değil. Her oturum kullanıcı adı ve şifre yazmayı (veya yapıştırmayı) gerektirir.

Bu sınırlamalar beş cihaz yönetirken yönetilebilirdir. Yüzlerce cihaz yönetirken, gerçek ek yüke dönüşürler.

---

## SecureCRT: Profesyonel Standart

SecureCRT, VanDyke Software tarafından yapılan ticari bir terminal istemcisidir. On yıllardır profesyonel ağ mühendisliği ortamlarında tercih edilen araç olmuştur. Bunun nedeni arayüz değildir — gerçek mühendislik çalışmasında önemli olan operasyonel özelliklerdir.

### Otomatik Oturum Loglama

Bu, günlük iş akışını en çok değiştiren özelliktir.

SecureCRT, her oturum için otomatik olarak bir log dosyası oluşturacak şekilde yapılandırılabilir — cihaza göre adlandırılmış, zaman damgalı, seçtiğiniz bir klasör yapısında saklanmış. Bunu düşünmenize gerek yok. Bir cihaza bağlanırsınız ve SecureCRT her şeyi zaten diske yazıyordur:

```
Logs/
  2026-03/
    core-sw-01_20260314_143022.log
    fw-dc1_20260314_151437.log
    router-edge-01_20260314_162005.log
```

**Pratikte neden önemlidir:**

Bir ağ olayı sırasında, tam olarak hangi komutların çalıştırıldığını, hangi sırayla ve cihazın ne yanıt verdiğini bilmeniz gerekir. Baskı altında manuel bellek güvenilmezdir. Otomatik loglar, ekstra adım gerektirmeden her oturumun eksiksiz, zaman damgalı kaydını verir.

Düzenlenmiş ortamlarda (bankacılık, sağlık hizmetleri) değişiklik yönetimi için, oturum logları çoğunlukla bir uyumluluk gereksinimidir. SecureCRT bunu mühendislerin logulamayı etkinleştirmeyi hatırlamasına güvenmek yerine otomatik olarak yönetir.

"Geçen Perşembe bu cihazda ne değişti" sorunun yanıtı için — log klasörünüzde grep yapın.

**SecureCRT'de otomatik loglamayı yapılandırma:**

`Options → Global Options → Log File` — değişkenler kullanarak log dosya adı deseni ayarlayın:

```
%D\%H_%Y%M%D_%h%m%s.log
```

`%H` ana bilgisayar adı, `%Y%M%D` tarih, `%h%m%s` saattir. SecureCRT dizinler mevcut değilse otomatik olarak oluşturur.

Loglama'yı oturum başına veya oturum grubu başına da yapılandırabilirsiniz — farklı müşteri ortamları için farklı log konumları istiyorsanız kullanışlıdır.

---

### Oturum Yönetimi ve Taşınabilirlik

SecureCRT tüm oturumları, Windows Registry değil, taşınabilir dosya tabanlı bir formatta saklar. Bu, PuTTY'den temel bir farktır.

**Oturum klasörleri ve organizasyonu:**

Oturumlar bir ağaç yapısında düzenlenir — tıpkı dosya gezgini gibi. Birden fazla müşteri veya ortam yöneten bir ağ mühendisi için tipik organizasyon:

```
Oturumlar/
  Müşteri-A/
    Çekirdek/
      core-sw-01
      core-sw-02
    Dağıtım/
      dist-sw-zemin1
      dist-sw-zemin2
    Firewall'lar/
      fw-birincil
      fw-ikincil
  Müşteri-B/
    ...
  Lab/
    ...
```

Her oturum şunları saklar: ana bilgisayar adı/IP, port, protokol, kullanıcı adı, bağlantı ayarları ve isteğe bağlı olarak şifre (şifreli). Bir oturum klasörü açtığınızda, tüm cihazlarınızı ağınızın yapılandırıldığı gibi organize edilmiş görürsünüz.

**Taşınabilirlik — yeni makineye geçiş:**

Oturumlar dosya tabanlı olduğundan, yeni bir dizüstü bilgisayara geçmek basittir:

1. SecureCRT oturumlar klasörünü yeni makineye kopyalayın (veya bulut depolama / ağ paylaşımı aracılığıyla senkronize edin)
2. SecureCRT'yi klasöre yönlendirin
3. Tüm oturumlar, organizasyon ve ayarlar hemen kullanılabilir

Birden fazla mühendisli ortamlarda, ortak bir ağ sürücüsü ortak bir oturum veritabanını tutabilir — herkes aynı cihaz listesine erişir ve bir mühendis tarafından yapılan eklemeler hemen diğerlerine görünür.

**Dışa aktarma ve yedekleme:**

`File → Export Settings` tüm oturum veritabanını tek bir dosyaya dışa aktarır. Dizüstü bilgisayar yenilemesinden önce kişisel yedek isteyen mühendisler için bu 30 saniye alır.

---

### Kimlik Bilgisi Depolama ve Otomatik Giriş

SecureCRT, oturum başına kullanıcı adları ve şifreler depolamayı, şifreleri seçtiğiniz algoritmayla (AES-256) şifrelenmiş olarak destekler.

**Otomatik giriş dizisi:**

Kimlik bilgileri saklamanın ötesinde, SecureCRT **giriş scriptleri** veya **otomatik giriş** desenleri kullanarak giriş otomasyonunu destekler. Standart giriş dizisi olan cihazlar için (kullanıcı adı istemi → şifre istemi → isteğe bağlı etkinleştirme şifresi istemi), şunları yapılandırırsınız:

```
Oturum Özellikleri → Bağlantı → SSH2:
  Kullanıcı Adı: admin
  Şifre: [saklanmış, şifreli]

Oturum Özellikleri → Terminal → Emülasyon → Expect Scriptleri:
  "Username:" isteminde kullanıcı adı gönder
  "Password:" isteminde şifre gönder
  ">" isteminde etkinleştirme şifresi gönder
```

Yapılandırıldıktan sonra, bir oturum açmak otomatik olarak bağlanır ve giriş yapar. Yüzlerce cihaz yöneten bir ağ mühendisi için, kimlik bilgilerini tekrar tekrar yazmaktan kurtarılan zaman önemlidir — ancak daha da önemlisi, yanlış pencereye kimlik bilgisi yazma riskini ortadan kaldırır.

**Kimlik bilgisi güvenliği hakkında bir not:**

SecureCRT'nin şifre depolama özelliği, saklanan şifreleri şifrelemek için bir ana şifre (veya Windows kimlik bilgisi deposu entegrasyonu) kullanır. Şifreli şifre dosyası, ana şifre olmadan bir saldırgan için kullanışlı değildir. Katı kimlik bilgisi yönetimi politikalarına sahip ortamlar için SecureCRT, SSH anahtar tabanlı kimlik doğrulamayla da entegre olur — bu, yüksek güvenlikli ortamlarda saklanan şifrelerden tercih edilir.

---

### Sekmeli Arayüz ve Çok Oturum Yönetimi

SecureCRT birden fazla oturumu tek bir pencere içinde sekmeler olarak görüntüler. Ağ geçişi sırasında 20 eş zamanlı oturumu yönetene kadar bu küçük bir şeymiş gibi görünür:

```
[core-sw-01] [core-sw-02] [dist-sw-01] [fw-birincil] [router-edge] [+]
```

Çok oturumlu çalışma için önemli özellikler:

**Oturum döşemesi:** Pencereyi birden fazla oturumu aynı anda görüntülemek için bölün. Bir yük devretme testi sırasında, biri aktif cihazı ve diğeri yedeği gösteren iki bölme isteyebilirsiniz — ikisini aynı anda izlemek.

**Sekmede bağlan:** Kaydedilmiş herhangi bir oturuma sağ tıklayın → "Sekmede Bağlan." Yeni pencereler olmadan ihtiyaç duyduğunuz kadar oturum açın.

**Birden fazla oturuma komut gönder:** SecureCRT'nin "Sohbet Penceresi" ve "Tüm Sekmelere Gönder" özelliği, birden fazla oturuma aynı anda aynı komutu göndermeyi sağlar. Bir grup switch genelinde tutarlı bir değişiklik uygulamak için aynı komutu 10 kez yeniden yazmaya gerek yoktur.

---

### Scripting ve Otomasyon

SecureCRT, VBScript, JScript ve Python destekli yerleşik bir scripting motoru içerir. Scriptler, terminal oturumuyla programatik olarak etkileşime girer — komutlar gönderir, çıktı okur, yanıtlara dayalı kararlar verir.

**Scripting'in sağladıkları:**

- Otomatik konfigürasyon yedekleme: cihaz listesine bağlanın, `show running-config` çalıştırın, çıktıyı cihaz başına bir dosyaya kaydedin
- Toplu konfigürasyon değişiklikleri: bir grup cihaz genelinde aynı değişikliği uygulayın, her birinin çıktısını loglayın
- Veri toplama: birden fazla cihazdan arayüz istatistikleri, yönlendirme tablosu girdileri veya VLAN bilgisi toplayın ve bir raporda derleyin
- Etkileşimli otomasyon: bir sonraki komutu göndermeden önce belirli çıktıyı bekleyen scriptler

**Basit Python örneği — cihaz listesinden show version toplama:**

```python
# SecureCRT Python scripti
import time

def main():
    tab = crt.GetScriptTab()
    devices = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]

    for device in devices:
        crt.Session.Connect("/SSH2 /L admin /PASSWORD pass " + device)
        tab.Screen.WaitForString("#")
        tab.Screen.Send("terminal length 0\n")
        tab.Screen.WaitForString("#")
        tab.Screen.Send("show version\n")
        tab.Screen.WaitForString("#")
        output = tab.Screen.ReadString("#")

        with open(f"C:\\logs\\{device}_version.txt", "w") as f:
            f.write(output)

        crt.Session.Disconnect()
        time.sleep(1)

main()
```

Daha karmaşık otomasyon için (tam ağ envanteri, konfigürasyon uyumluluk kontrolü, toplu VLAN değişiklikleri), Python ile birleştirilmiş SecureCRT scripting, tam bir Ansible veya Netmiko kurulumuna gerek kalmadan yetenekli bir otomasyon platformu sunar.

---

### SecureFX Entegrasyonu

SecureFX, VanDyke'ın SFTP/FTP istemcisidir — ayrı satılır ancak SecureCRT ile sıkıca entegre edilmiştir. Entegrasyon şunlar için kullanışlıdır:

- Ağ cihazlarından yerel sunucuya konfigürasyon yedekleri aktarma
- Cihazlara yazılım yükleme
- Ağ cihazlarından merkezi bir depoya log dosyaları taşıma

SecureCRT içinden, aynı oturum kimlik bilgilerini kullanarak SecureFX'i başlatabilirsiniz — ayrı giriş gerekmez. Cisco IOS cihazları için, SecureCRT (CLI etkileşimi için) ve SecureFX (dosya aktarımı için) kombinasyonu tam operasyonel iş akışını kapsar.

---

### Protokol Desteği

SecureCRT, bir ağ mühendisinin düzenli olarak kullandığı tüm protokolleri destekler:

- **SSH1 / SSH2** — modern ağ cihazları için birincil protokol
- **Telnet** — eski cihazlar, lab ortamları
- **Seri (COM portu)** — ilk cihaz kurulumu veya kurtarma için konsol kablosu bağlantıları
- **RDP** — Uzak Masaüstü bağlantıları, Windows sunucularını aynı oturum yöneticisinde ağ cihazlarıyla birlikte yönetmek için kullanışlı
- **SFTP / FTP** (SecureFX entegrasyonu aracılığıyla)

Seri bağlantı desteği, ağ mühendisleri için özellikle değerlidir. Konsol kablosuyla bir cihaza bağlanmak, SSH ile aynı oturum yöneticisi arayüzünü kullanır — bir konsol oturumunu ve aynı cihaza birden fazla SSH oturumunu aynı anda açabilirsiniz, hepsi aynı pencerede.

---

## SuperPutty: PuTTY Kullanıcılarının Bilmediği Ücretsiz Yükseltme

PuTTY'yi günlük kullanıyorsanız, SuperPutty'yi hiç duymamış olma ihtimaliniz yüksektir. Yeterince pazarlanmaz, arkasında büyük bir şirket yoktur ve ilk bakışta — başka bir PuTTY penceresi gibi görünür. Ancak PuTTY'nin kendisini değiştirmeden PuTTY'nin en büyük günlük kullanım sınırlılıklarını çözer.

### SuperPutty Gerçekte Nedir

SuperPutty, **PuTTY için bir oturum yöneticisi ve sekmeli arayüz sarmalayıcısıdır**. PuTTY'nin yerini almaz — SuperPutty'nin çalışması için PuTTY kurulu olmalıdır. SuperPutty'nin eklediği şey, PuTTY'nin ciddi çok oturumlu çalışma için eksik olan her şeydir:

- Tek pencerede birden fazla PuTTY oturumuyla sekmeli arayüz
- Klasör organizasyonuyla kalıcı oturum kitaplığı
- Mevcut PuTTY oturumlarının içe aktarılması — mevcut yapılandırmanız kaybolmaz
- Döşenmiş düzen — birden fazla oturum aynı anda görünür
- Hızlı bağlantı çubuğu
- Oturum arama

**Tamamen ücretsiz ve açık kaynaklıdır.**

---

### PuTTY Oturumlarınızı İçe Aktarma

SuperPutty kurulduktan sonra yapılacak ilk şey: mevcut PuTTY oturumlarınızı içe aktarın.

`Tools → Import Sessions → From PuTTY Settings`

SuperPutty, Windows Registry'den PuTTY oturum verilerini okur ve kendi oturum veritabanında ilgili oturumları oluşturur. Kaydedilmiş tüm ana bilgisayar adları, port ayarları ve bağlantı tercihleri otomatik olarak içe aktarılır. Sıfırdan başlamazsınız.

İçe aktarmadan sonra PuTTY oturumlarınız SuperPutty'nin oturum ağacında görünür — hemen kullanıma hazır. PuTTY kendisi normal şekilde çalışmaya devam eder; SuperPutty ve PuTTY bir arada bulunur.

---

### Sekmeli Arayüz ve Oturum Organizasyonu

Oturumlar içe aktarıldıktan (veya doğrudan SuperPutty'de oluşturulduktan) sonra, bir cihaza bağlanmak onu sekme olarak açar:

```
[core-sw-01] [fw-birincil] [router-edge] [dist-sw-02] [+]
```

Oturumlar klasörlerde düzenlenebilir — SecureCRT'de kullandığınız aynı yapı, yalnızca ticari lisans maliyeti olmadan.

**Döşenmiş düzen:** SuperPutty pencereyi bir oturum bölmesi ızgarasına bölmeyi destekler. Birden fazla cihazı aynı anda izlediğiniz bakım pencereleri sırasında kullanışlıdır.

**Otomatik yeniden bağlanma:** SuperPutty, düşen oturumları otomatik olarak yeniden bağlayabilir — bağlantı zaman aşımlarının yaygın olduğu uzun süreli izleme oturumları için kullanışlıdır.

---

### SuperPutty'nin Sahip Olmadığı Şeyler

Sınırlılıklar hakkında doğrudan olmak için:

- **Otomatik loglama yok:** SuperPutty oturumları otomatik olarak loglamaz. Her oturum için PuTTY'nin yerleşik loglamasını yapılandırabilirsiniz, ancak SecureCRT'nin özelliğine eşdeğer küresel "her şeyi otomatik logla" yoktur.
- **Yerleşik scripting motoru yok:** SuperPutty'nin SecureCRT'nin VBScript/Python scripting'ine eşdeğeri yoktur. Otomasyon için ayrı araçlar kullanırsınız (Netmiko, Paramiko, Ansible).
- **Kimlik bilgisi şifrelemesi yok:** SuperPutty, şifreleri SecureCRT'nin sağladığı şifreleme seçenekleri olmadan oturum veritabanında saklar. Katı kimlik bilgisi yönetimine sahip üretim ortamları için bu bir değerlendirmedir.
- **Daha az cilalı:** SuperPutty, gönüllüler tarafından sürdürülen bir açık kaynak projesidir. İyi çalışır, ancak ticari bir ürünün cilasından ve aktif geliştirmesinden yoksundur.

---

## SecureCRT vs. SuperPutty: Ne Zaman Hangisi

| | SecureCRT | SuperPutty |
|---|---|---|
| Maliyet | Ticari lisans (~99–150 $/koltuk) | Ücretsiz |
| Otomatik oturum loglama | ✅ Yerleşik, küresel | ❌ Yalnızca oturum başına PuTTY loglaması |
| Oturum taşınabilirliği | ✅ Dosya tabanlı, kolay dışa aktarma | ✅ XML tabanlı, içe aktarılabilir |
| PuTTY oturum içe aktarma | ❌ Geçerli değil | ✅ Registry'den doğrudan içe aktarma |
| Sekmeli arayüz | ✅ | ✅ |
| Döşenmiş oturumlar | ✅ | ✅ |
| Scripting (Python/VBScript) | ✅ Yerleşik motor | ❌ |
| Kimlik bilgisi depolama (şifreli) | ✅ AES-256 | ⚠️ Yalnızca temel |
| Seri/konsol desteği | ✅ | ✅ (PuTTY aracılığıyla) |
| RDP desteği | ✅ | ✅ (PuTTY/mRemoteNG aracılığıyla) |
| SecureFX entegrasyonu | ✅ | ❌ |
| Aktif ticari destek | ✅ | Yalnızca topluluk |

**SecureCRT kullanın:**
- Otomatik oturum loglaması gerektiğinde (uyumluluk, olay müdahalesi)
- Otomasyon veya toplu işlemler için script çalıştırdığınızda
- Yüzlerce cihaz yönetiyor ve sağlam, güvenilir bir oturum yöneticisine ihtiyaç duyuyorsanız
- Organizasyonunuz şifreli kimlik bilgisi depolama gerektirdiğinde
- Oturum kayıtlarının zorunlu olduğu düzenlenmiş ortamlarda çalışıyorsanız

**SuperPutty kullanın:**
- Zaten PuTTY kullanıcısıysanız ve araçları değiştirmeden sekmeli oturumlar istiyorsanız
- Maliyet bir kısıtsa (bireysel kullanım, küçük ekip)
- Otomasyon ihtiyaçlarınız ayrı araçlar (Ansible, Netmiko) tarafından karşılanıyorsa
- Ticari bir araça bağlanmadan önce oturum yöneticisinin iş akışınızı iyileştirip iyileştirmediğini değerlendirmek istiyorsanız

**Dürüst değerlendirme:** Günlük üretim altyapısını yöneten çalışan bir ağ mühendisiyseniz, SecureCRT'nin otomatik loglaması tek başına lisans maliyetini haklı kılar. Oturum loglarının bir olay veya değişiklik sonrası inceleme sırasında tam olarak ihtiyaç duyulan kaydı sağladığı zamanların sayısı küçük değildir. SuperPutty, düz PuTTY üzerinde gerçek bir yükseltmedir ve hiçbir şeye mal olmaz — ancak loglama ve scripting'e güvenen mühendisler için SecureCRT'nin yerini tutmaz.

---

## Pratik Kurulum: Günlük Kullanım için SecureCRT Yapılandırması

Günlük kullanımdan birkaç yapılandırma önerisi:

**Küresel loglama kurulumu:**
`Options → Global Options → Log File`
```
Log dosya adı: C:\NetworkLogs\%H_%Y%M%D_%h%m%s.log
Bağlantıda:    Logu başlat
Log verisi:    Zaman damgaları dahil tüm oturum verisi
```

**Oturum klasörü yapısı:**
En üst düzeyde müşteri veya ortama göre düzenleyin, ardından cihaz rolüne göre. Tutarlı adlandırma (çekirdek, dağıtım, erişim, firewall, router), yüzlerce oturum olsa bile gezinmeyi hızlı kılar.

**Oturum grubu başına renk şemaları:**
SecureCRT, oturum veya klasör başına farklı terminal renk şemalarını destekler. Üretim ve lab ortamları için farklı bir renk kullanmak, yanlış pencere hatasını önler — lab'da olduğunuzu sanırken yanlışlıkla üretim cihazında komut çalıştırmak.

**SSH anahtar kimlik doğrulaması:**
Üretim ortamları için, saklanan şifreler yerine SSH anahtar kimlik doğrulamasını yapılandırın:
`Oturum Özellikleri → Bağlantı → SSH2 → PublicKey`
Özel anahtar dosyanıza işaret edin. Anahtar bağlantıda otomatik olarak kullanılır — şifre istemi yok, saklanan şifre yok.

**Anahtar sözcük vurgulama:**
`Options → Global Options → Advanced → Keyword Sets`
`%Error`, `down`, `FAIL`, `alarm` gibi anahtar sözcükleri kırmızı görünecek şekilde yapılandırın. Kritik hata mesajları yoğun bir çıktı akışında hemen göze çarpar.

---

## Temel Çıkarımlar

- **Düz PuTTY işlevseldir ancak gerçek sınırlılıkları vardır** — sekme yok, otomatik loglama yok, oturum taşınabilirliği yok.
- **SecureCRT'nin otomatik loglaması**, en operasyonel açıdan değerli özelliğidir — her oturum, her komut, her yanıt, ekstra adım gerektirmeden otomatik olarak zaman damgalı ve saklanmış.
- **SecureCRT'de oturum taşınabilirliği**, yeni bir dizüstü bilgisayara geçişin yeniden yapılandırma değil kopyalama işlemi olduğu anlamına gelir. Paylaşılan oturum veritabanları ekip tutarlılığı sağlar.
- **Otomatik girişle kimlik bilgisi depolama**, tekrarlayan yazmayı ortadan kaldırır ancak hassas ortamlarda ana şifre veya anahtar tabanlı kimlik doğrulamayla birleştirilmelidir.
- **SecureCRT scripting'i**, aksi takdirde ayrı bir araç gerektiren otomasyona olanak tanır — toplu işlemler ve konfigürasyon toplama için kullanışlı.
- **SuperPutty doğru yanıttır** — PuTTY'yi bilen ve sekmeli oturumlar, oturum organizasyonu ve PuTTY oturum içe aktarma isteyen mühendisler için — sıfır maliyetle.
- Şu an düz PuTTY kullanıyorsanız ve SuperPutty'yi hiç denemediyseniz: bugün kurun. Mevcut oturumlarınızı iki dakikada içe aktarın. Sekme arayüzü tek başına iş akışınızı değiştirecek.

---

## İlgili Yazılar

- 🛠️ [Ağın Arka Kapısı: Yeni Nesil Console Server Mimarisi](/tr/posts/next-gen-console-server-architecture/) — SSH başarısız olduğunda bant dışı erişim
- 🔐 [802.1X Kimlik Tabanlı Mimari Sahada](/tr/technology/identity-based-microsegmentation-8021x/) — SSH erişim kontrolünün arkasındaki kimlik doğrulama çerçevesi
- 📊 [İzleme Doğru Yapıldığında](/tr/architecture/monitoring-not-just-seeing/) — Manuel CLI çalışmasını proaktif izlemeyle tamamlamak