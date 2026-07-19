---
title: "F5 LTM Deep Dive: Virtual Server'lar, iRule'lar, SSL Offloading ve HA"
description: "F5 BIG-IP LTM teknik inceleme — full-proxy mimari, virtual server, pool yapılandırması, iRule, SSL offloading ve sıfır downtime migrasyon rehberi."
date: 2026-04-08
draft: false

cover:
  image: "/img/postimages/f5-ltm-deep-dive-cover.webp"
  alt: "F5 BIG-IP LTM Deep Dive — Virtual Server'lar, iRule'lar, HA"
  relative: false

tags: ["F5", "LTM", "BIG-IP", "iRule", "SSL Offloading", "Load Balancing", "High Availability", "TMOS"]
categories: ["Teknoloji"]
keywords:
  - F5 LTM virtual server yapılandırması
  - F5 iRule örnekleri
  - F5 SSL offloading
  - F5 BIG-IP pool health monitor
  - F5 session persistence cookie
  - F5 LTM high availability
  - F5 TMOS migrasyonu
  - F5 full proxy mimarisi
  - F5 aktif yedek failover
  - F5 2000 5000 migrasyonu

showToc: true
TocOpen: true
---

# F5 LTM Deep Dive: Virtual Server'lar, iRule'lar, SSL Offloading ve HA

Bu yazı F5 BIG-IP serisinin bir parçasıdır.

> **F5'e yeni misiniz?** Önce platform genel bakışıyla başlayın: [F5 BIG-IP Bir Load Balancer Değil — Uygulama Teslim Platformudur](/tr/technology/f5-bigip-application-delivery-platform-overview/)

Büyük resmi zaten biliyorsanız ve LTM'e derinlemesine inmek istiyorsanız — yapılandırma, iRule'lar, migrasyon saha notları — doğru yerdesiniz.

---

## Full-Proxy Mimarisi: Neden Her Şeyi Değiştirir

LTM hakkında anlaşılması gereken en önemli şey, bunun bir **full-proxy** olduğudur. Bu bir pazarlama terimi değildir — LTM'yi her türlü daha basit load balancer'dan ayıran doğrudan operasyonel sonuçları vardır.

Bir istemci F5 LTM üzerinden bağlandığında, iki tamamen ayrı TCP bağlantısı oluşur:

```
İstemci ──[TCP bağlantı 1]──→ F5 LTM ──[TCP bağlantı 2]──→ Backend Sunucu
          (Virtual Server IP)            (Pool Member IP)
```

F5 istemci bağlantısını tamamen sonlandırır, inceler, tüm yönlendirme ve politika kararlarını verir, ardından backend'e yeni bir bağlantı açar. İstemci ve backend sunucusu hiçbir zaman doğrudan iletişim kurmaz.

Bu, pass-through load balancer'ların sağlayamadığı yetenekler sunar:
- İstek ve yanıtın her baytına tam görünürlük
- Trafiğin herhangi bir bölümünü yeniden yazabilme — başlıklar, URI'ler, çerezler, yanıt gövdeleri
- Backend'ler adına SSL sonlandırma — backend'ler düz HTTP görür
- İstemci taraflı ve sunucu taraflı bağlantılar için bağımsız TCP ayarı
- Bağlantı çoğullaması ve HTTP pipelining optimizasyonları

Pratikte, full-proxy konumu, yukarı akış sorunlarının (istemci tarafı) ve aşağı akış sorunlarının (sunucu tarafı) tamamen izole edildiği anlamına gelir. Bu, üretim olaylarında sorun gidermeyi önemli ölçüde basitleştirir.

---

## Virtual Server'lar: Giriş Noktası

**Virtual Server**, istemcilerin bağlandığı IP adresi ve port kombinasyonudur. LTM'deki birincil nesnedir ve tüm trafik politikasının kapsayıcısıdır:

```
Virtual Server: vs_webapp_443
  Hedef IP:           10.10.1.100
  Port:               443
  Protokol:           TCP
  HTTP Profili:       http_profile_xforward
  SSL İstemci Profili: clientssl_webapp
  SSL Sunucu Profili: serverssl_backend
  Varsayılan Pool:    pool_webapp_8080
  Persistence:        cookie_persistence
  iRule:              /Common/rule_uri_routing
```

**Bir VIP, birden fazla uygulama:** Tek bir virtual server IP'si, HTTP Host başlığına veya URI yoluna göre yönlendirme yapmak için iRule'lar kullanarak birden fazla uygulamaya hizmet verebilir. Bu, IP tüketimini azaltır ve yukarı akış firewall kurallarını basitleştirir.

**Virtual server durumu pool sağlığından bağımsızdır:** Bir virtual server devre dışı bırakılırsa, pool member'ların sağlıklı olup olmadığına bakılmaksızın hiçbir trafik pool'a ulaşmaz. Virtual server kullanılabilirliğini, pool member kullanılabilirliğinden ayrı olarak her zaman izleyin.

**Üç virtual server türü:**
- **Standard** — full proxy, en yaygın tür
- **Performance Layer 4** — L7 incelemesinin gerekmediği yüksek verimli senaryolar için proxy'yi atlar
- **Forwarding** — proxy davranışı olmadan pass-through yönlendirme, şeffaf deployment'larda kullanılır

---

## Pool'lar ve Load Balancing Yöntemleri

**Pool**, virtual server'ın trafiği dağıttığı backend sunucuları grubudur:

```
Pool: pool_webapp_8080
  Load Balancing Yöntemi: Least Connections (member)
  Slow Ramp Time:         30 saniye
  Monitor:                http_monitor_webapp
  Member'lar:
    192.168.10.11:8080   Öncelik Grubu: 1
    192.168.10.12:8080   Öncelik Grubu: 1
    192.168.10.13:8080   Öncelik Grubu: 2  ← yedek, yalnızca grup 1 başarısız olursa etkinleşir
```

**Load balancing yöntemleri karşılaştırması:**

- **Round Robin** — sıralı dağılım. Durumsuz, tekdüze iş yükleri için çalışır. Bağlantı süreleri önemli ölçüde farklılaştığında kötü seçimdir.
- **Least Connections (member)** — en az aktif bağlantıya sahip member'a gönderir. Değişken oturum süreleri olan uygulamalar için en iyisi. Çoğu üretim ortamında standart seçim.
- **Least Connections (node)** — yalnızca bu pool değil, bir sunucu IP'sine tüm pool'lardaki bağlantıları sayar. Bir sunucu birden fazla pool'a katıldığında kullanın.
- **Ratio** — ağırlıklı dağılım. A member'ı, B member'ından 3× daha fazla bağlantı alır. Farklı kapasitelere sahip sunucular için.
- **Fastest** — en son yanıt veren member'a gönderir. Sıcak nokta oluşturabilir; daha fazla kararlılık için bunun yerine Observed kullanın.

**Slow Ramp Time** az kullanılır ama önemlidir. Bir pool member başarısızlıktan kurtulduğunda hemen kullanılabilir hale gelir — ancak tam olarak hazır olmayabilir (JVM, cache'ler, veritabanı bağlantı havuzları). Slow Ramp Time, yeni kullanılabilir bir member'ın ağırlığını belirtilen saniyeler boyunca kademeli olarak artırır ve soğuk bir sunucunun anında aşırı yüklenmesini önler.

**Öncelik Grupları**, tek bir pool içinde aktif ve yedek member setlerine olanak tanır. Grup 1 member'ları, minimum aktif member eşiğinin üzerindeyken tüm trafiği alır. Grup 2 member'ları, Grup 1 eşiğin altına düştüğünde otomatik olarak etkinleşir.

---

## Health Monitor'lar: Load Balancing Yönteminden Daha Önemli

Bir pool member, TCP erişilebilir ve uygulama düzeyinde tamamen bozuk olabilir. Her istekte HTTP 500 döndüren bir ödeme işleme sunucusu hâlâ TCP erişilebilirdir — temel bir TCP monitor sorunu hiçbir zaman tespit etmez.

Bu, üretim ortamlarında gördüğüm en yaygın başarısızlık senaryosudur ve ekiplerin en sık yetersiz yatırım yaptığı yerdir.

### TCP Monitor: Gerekli ama Yetersiz

```
Monitor: tcp_monitor_basic
  Tür:      TCP
  Interval:  5 saniye
  Timeout:   16 saniye
```

Tespit eder: ağ bağlantı kaybı, sunucu çöküşleri, port dinlenmiyor.

Tespit etmez: uygulama hataları, veritabanı bağlantı başarısızlıkları, bellek tükenmesi, kısmen başlatılmış uygulama durumları.

### HTTP Monitor: Üretim Standardı

```
Monitor: http_monitor_webapp
  Tür:            HTTP
  Send String:    GET /health HTTP/1.1\r\nHost: webapp.internal\r\nConnection: close\r\n\r\n
  Receive String: "status":"healthy"
  Interval:       5 saniye
  Timeout:        16 saniye
```

LTM, yalnızca yanıt gövdesi tam olarak beklenen dizeyi içerdiğinde member'ı UP olarak işaretler. Uygulama, yalnızca portun açık olduğunu değil, sağlıklı olduğunu aktif olarak onaylamalıdır.

İyi bir `/health` endpoint'i şunları kontrol eder: veritabanı bağlantısı, cache kullanılabilirliği, kilit bağımlılık durumu ve ilgiliyse disk alanı. `{"status":"degraded"}` ile HTTP 200 döndüren bir uygulama, monitor kontrolünü başarısız kılmalıdır.

### Şifreli Backend'ler için HTTPS Monitor

```
Monitor: https_monitor_webapp
  Tür:         HTTPS
  SSL Profili:  serverssl_monitor (dahili olarak öz imzalı sertifikaları kabul edecek şekilde yapılandırın)
  Send String:  GET /health HTTP/1.1\r\nHost: webapp.internal\r\n\r\n
  Receive String: "status":"healthy"
```

### Timeout Formülü

Sık yapılan bir yanlış yapılandırma: timeout değerini interval'e eşit veya daha küçük ayarlamak. Doğru formül:

```
Timeout = (Interval × yeniden deneme sayısı) + 1
```

Interval=5 ve 3 yeniden denemeyle: Timeout = 16. Bu, geçici ağ dalgalanmalarından kaynaklanan yanlış pozitifleri önlemek için LTM'ye member'ı düşürmeden önce yeniden deneme zamanı verir.

---

## SSL Offloading ve SSL Bridging

### SSL Offload (Yalnızca İstemci SSL)

```
İstemci ──(HTTPS/TLS 1.3)──→ F5 LTM ──(HTTP)──→ Backend
```

F5, istemciden TLS'yi sonlandırır ve şifrelenmemiş HTTP'yi backend'lere iletir. Maksimum backend CPU tasarrufu. Virtual server'da bir **İstemci SSL Profili** gerektirir:

```
İstemci SSL Profili: clientssl_webapp
  Sertifika:   /Common/webapp_cert
  Anahtar:     /Common/webapp_key
  Zincir:      /Common/intermediate_ca
  Şifreler:    TLSv1.2:TLSv1.3
  Seçenekler:  TLSv1 Yok, TLSv1.1 Yok
```

### SSL Bridging (İstemci + Sunucu SSL)

```
İstemci ──(HTTPS/TLS 1.3)──→ F5 LTM ──(HTTPS/TLS)──→ Backend
```

F5 şifresini çözer, inceler, ardından backend için yeniden şifreler. Uyumluluk gereksinimlerinin uçtan uca şifrelemeyi zorunlu kıldığı düzenlenmiş ortamlarda (bankacılık, sağlık) gereklidir. Bağlantı başına iki TLS el sıkışması nedeniyle biraz gecikme ekler — ancak tam uyumluluk ve görünürlük sağlar.

Bankacılık ortamında, tüm üretim virtual server'ları SSL bridging çalıştırıyordu. Her bağlantı şifresi çözülüyor, WAF tarafından inceleniyor ve backend'e yeniden şifreleniyordu.

### Sertifika Yönetimi

Temel operasyonel noktalar:
- F5, sertifikalar sona erme tarihine yaklaştığında varsayılan olarak uyarı vermez. Virtual server'lardaki sertifika süresini kontrol etmek için harici izleme (SolarWinds, Zabbix) kurun.
- Sertifika değiştirme sıfır downtime ile yapılır: sertifika nesnesini güncelleyin, profil buna otomatik olarak referans verir.
- **SNI**, tek bir VIP'nin farklı sertifikalara sahip birden fazla uygulamaya hizmet vermesine olanak tanır.

---

## Session Persistence

### Cookie Persistence (Önerilen)

F5, HTTP yanıtına pool member'ı tanımlayan bir çerez ekler:

```
Persistence Profili: cookie_persistence
  Yöntem:      Insert
  Çerez Adı:   BIGipServer_webapp
  Son Kullanma: Session
  Şifrele:     Etkin
```

Sonraki isteklerde, tarayıcı bu çerezi gönderir. F5, mevcut yük dağılımından bağımsız olarak doğru member'a yönlendirir. Uygulamaya şeffaf, NAT üzerinden çalışır, istemci IP değişikliklerine dayanır.

### Kaynak Adres Persistence

Aynı istemci IP'sinden gelen tüm trafiği aynı member'a yönlendirir:

```
Persistence Profili: source_addr_persistence
  Timeout: 3600 saniye
```

Basit, ancak birçok kullanıcı bir NAT IP'yi paylaştığında sorunlu — aynı NAT arkasındaki tüm kullanıcılar aynı backend sunucusuna gider, yük dağılımını bozar.

### iRule Tabanlı Evrensel Persistence

Özel oturum tanımlayıcıları için (standart dışı çerezler, URL parametreleri, özel başlıklar):

```tcl
when HTTP_REQUEST {
  persist uie [HTTP::header "X-Session-Token"]
}
```

Özel bir başlık değerine göre kalıcı hale getirir — hiçbir standart profilin desteklemediği bir şey.

---

## iRule'lar: Programlanabilir Trafik Katmanı

iRule'lar, TMOS veri düzleminde hat hızında çalışan Tcl tabanlı betiklerdir. En güçlü LTM farklılaştırıcısıdır — aksi takdirde uygulama kodu değişikliği gerektiren trafik mantığı.

### Olay Modeli

iRule'lar, trafik yaşam döngüsündeki olaylarda çalışır:
- `HTTP_REQUEST` — istemciden tam HTTP isteği alındı
- `HTTP_RESPONSE` — backend'den yanıt alındı
- `CLIENT_ACCEPTED` — istemciden TCP bağlantısı kuruldu
- `SERVER_CONNECTED` — F5 backend'e bağlandı
- `SSL_HANDSHAKE_START` — TLS müzakeresi sırasında

### Üretim iRule Örnekleri

**Backend'e istemci IP iletimi:**
```tcl
when HTTP_REQUEST {
  HTTP::header insert "X-Forwarded-For"   [IP::client_addr]
  HTTP::header insert "X-Real-IP"         [IP::client_addr]
  HTTP::header insert "X-Forwarded-Proto" "https"
}
```

**URI tabanlı pool yönlendirmesi:**
```tcl
when HTTP_REQUEST {
  if { [HTTP::uri] starts_with "/api/v2/" } {
    pool pool_api_v2_servers
  } elseif { [HTTP::uri] starts_with "/api/" } {
    pool pool_api_v1_servers
  } elseif { [HTTP::uri] starts_with "/admin/" } {
    pool pool_admin_servers
  } else {
    pool pool_web_servers
  }
}
```

**Pool boşken bakım yönlendirmesi:**
```tcl
when HTTP_REQUEST {
  if { [active_members pool_webapp_8080] < 1 } {
    HTTP::redirect "https://status.sirket.com/bakim"
  }
}
```

**Host başlığı tabanlı yönlendirme — bir VIP'de birden fazla uygulama:**
```tcl
when HTTP_REQUEST {
  switch [HTTP::host] {
    "uygulama1.sirket.com" { pool pool_app1 }
    "uygulama2.sirket.com" { pool pool_app2 }
    "api.sirket.com"       { pool pool_api  }
    default                { pool pool_default }
  }
}
```

**İstemci IP'ye göre bağlantı hızı sınırlaması:**
```tcl
when CLIENT_ACCEPTED {
  set conn_limit 50
  if { [table lookup -notouch [IP::client_addr]] > $conn_limit } {
    reject
  } else {
    table incr [IP::client_addr]
    table timeout [IP::client_addr] 60
  }
}
```

### iRule Performans Notları

iRule'lar, virtual server üzerinden her bağlantı veya istek için çalışır. Yönergeler:
- Yüksek trafikli iRule'larda karmaşık dize işlemlerinden kaçının — hesaplanan değerleri önbelleğe almak için `table` kullanın
- Sözdizimi hatası tüm iRule'u sessizce devre dışı bırakır — önce staging ortamında test edin
- Üretimde `log local0.debug` kullanımını sınırlayın — aşırı loglama performansı etkiler
- `RULE_INIT` olayı başlangıçta bir kez çalışır ve paylaşılan veri yapılarını başlatmak için idealdir

---

## High Availability: Üretimde Aktif-Yedek

### Cihaz Grupları ve Trafik Grupları

F5 HA, **Cihaz Güveni** (eşler arasında karşılıklı kimlik doğrulama) ve **Cihaz Grupları** (sync-failover yapılandırması) kullanır:

```
Cihaz Grubu: dg_production
  Tür:     sync-failover
  Member'lar: bigip-01 (Aktif), bigip-02 (Yedek)

Trafik Grubu: traffic-group-1
  Floating IP'ler: 10.10.1.100 (VIP), 10.10.1.1 (self IP)
  Aktif on:        bigip-01
```

Trafik Grupları, failover sırasında cihazlar arasında geçiş yapan floating IP'leri içerir. bigip-01 başarısız olduğunda, bigip-02 traffic-group-1'in sahipliğini alır ve gratuitous ARP aracılığıyla VIP'yi duyurur.

### Özel Heartbeat VLAN: Zorunlu

F5 HA, ağ failover kullanır — cihazlar arasındaki heartbeat paketleri eş başarısızlığını tespit eder. Kritik kural:

**Üretim ve yönetim ağlarından ayrı, her zaman özel bir failover VLAN kullanın.**

Heartbeat için üretim arayüzünü paylaşmak, ağ tıkanıklığı sırasında yanlış failover olayları oluşturur. Her iki cihaz da diğerinin başarısız olduğuna inanır ve her ikisi de aynı anda aktif hale gelir — split-brain. Trafik çoğaltılır, oturumlar bozulur ve olaydan kurtulmak zahmetlidir.

```
Failover VLAN: vlan_ha_heartbeat
  Arayüz:            1.3 (özel)
  bigip-01 self IP:  192.168.100.1/24
  bigip-02 self IP:  192.168.100.2/24
```

### Config Sync: Manuel - Otomatik

**Otomatik sync** — aktif cihazda yapılan değişiklikler anında yedek cihaza yayılır. Risk: kısmi veya yanlış bir yapılandırma değişikliği inceleyemeden önce yayılır.

**Manuel sync** — yönetici değişiklikleri doğruladıktan sonra sync'i açıkça tetikler. Üretim için daha güvenli. Düzenlenmiş ortamlarda standart seçim.

### Bağlantı Yansıtma

Varsayılan olarak, failover tüm mevcut bağlantıları düşürür — istemcilerin yeniden bağlanması gerekir. Çoğu web uygulaması için bu kabul edilebilirdir.

Uzun süreli bağlantılar için (kalıcı WebSocket'ler, büyük dosya transferleri, veritabanı bağlantıları), **bağlantı yansıtma** yedek cihazda oturum durumunu korur. Failover bu bağlantıları minimum kesinti ile sürdürür.

Bağlantı yansıtmayı seçici olarak etkinleştirin — her iki cihazda da bellek ve CPU tüketir. Her virtual server buna ihtiyaç duymaz.

---

## Saha Notları: 2000 → 5000 Migrasyonu

### Neden Migrasyon Yaptık

BIG-IP 2000 serisi, bankacılık yoğun saatlerinde SSL offloading tavanına ulaşmıştı. TMOS 13.x destek sonuna yaklaşıyordu. 5000 serisi, donanım SSL hızlandırması, 6× verim iyileştirmesi ve TMOS 15.x aracılığıyla TLS 1.3 desteği sunuyordu.

### Sıfır Downtime Yaklaşımı: 30+ Cihaz, 0 Kesinti

**Faz 1 — Paralel deployment**
5000 serisi donanımı mevcut 2000 serisi yanına kurun. Yeni cihazlarda özdeş virtual server'lar, pool'lar, profiller ve iRule'lar yapılandırın. Henüz sıfır trafik.

**Faz 2 — Kritik olmayan virtual server üzerinde doğrulama**
Tek bir dahili uygulamayı yeni cihaza yönlendirin. 72 saat izleyin: bağlantı oranları, SSL el sıkışma gecikmesi, health monitor davranışı, iRule yürütme logları, sentetik yük altında HA failover testi.

**Faz 3 — İş riski bazında kademeli migrasyon**
Virtual server'ları gruplara göre taşıyın — önce dahili araçlar, sonra genel uygulamalar, en son ödeme işleme. Her grup için:
- Yeni cihaza işaret etmek üzere yukarı akış yönlendirme / SNAT'ı güncelleyin
- 48 saat izleyin
- Grup başına 72 saat eski cihazı geri alma seçeneği olarak tutun

**Faz 4 — HA çifti tamamlama**
Yeni aktif cihazda tüm virtual server'lar doğrulandıktan sonra:
1. Önce yedek (eski cihaz) değiştirin
2. Yeni yedeğin aktiften yapılandırmayı senkronize ettiğini doğrulayın
3. Zorla failover yapın — yeni yediği üretim yükü altında test edin
4. Eski aktifi devre dışı bırakın

**İşe yaratan kural: her iki HA cihazını aynı anda hiçbir zaman değiştirmeyin.** Trafiği üstlenen her zaman tam doğrulanmış, üretimde test edilmiş bir cihaz olmalıdır.

### TMOS Uyumluluk Denetimi: Başlamadan Önce Yapın

TMOS 13.x için yazılmış iRule'lar her zaman 15.x'te aynı şekilde davranmaz. Migrasyondan önce tüm iRule'ları şunlar için denetleyin:

- `HTTP::` komutları — HTTP/2 senaryolarında davranış değişiklikleri
- `SSL::` olayları — TLS 1.3'te yeni olaylar ve değişen zamanlama
- `RULE_INIT` yürütmesi — başlangıçta zamanlama farklılıkları

Cutover öncesinde değişiklik gerektiren 3 iRule bulduk. Bunları staging ortamında bulmak, üretim olay yanıtında saatler kurtardı.

---

## Temel Çıkarımlar

- LTM bir **full-proxy**'dir — pass-through değil. Bu ayrım tüm yeteneklerini ve sorun giderme yaklaşımlarını yönlendirir.
- **Health monitor'lar**, load balancing yönteminden daha önemlidir. Uygulama yanıtlarını kontrol eden HTTP monitor'lar her zaman TCP monitor'lardan daha iyidir.
- **iRule'lar**, uygulama kodu değişiklikleri olmadan hat hızında trafik mantığı sağlar — en güçlü LTM farklılaştırıcısı.
- **SSL offloading**, şifreleme yükünü backend'lerden kaldırır. Düzenlenmiş ortamlarda SSL bridging gereklidir.
- HA için her zaman **özel bir heartbeat VLAN** kullanın. Paylaşılan arayüzler split-brain'e neden olur.
- Migrasyonlarda: **önce yedek, sonra aktif**. Aynı anda asla.

---

## Bu Seri

- 📖 [F5 BIG-IP Platform Genel Bakış — Tüm Modüller](/tr/technology/f5-bigip-application-delivery-platform-overview/) ← F5'e yeniyseniz buradan başlayın
- 🌐 [F5 GTM ve GSLB Deep Dive](/tr/technology/f5-gtm-gslb-global-traffic-management/)
- 🛡️ [F5 WAF Deep Dive](/tr/technology/f5-waf-asm-advanced-waf-application-security/)

## İlgili Yazılar

- 🛠️ [Ağın Arka Kapısı: Yeni Nesil Console Server Mimarisi](/tr/posts/next-gen-console-server-architecture/) — F5 bakım pencereleri sırasında out-of-band erişim
- 🛡️ [Network Packet Broker (NPB) Masterclass](/tr/posts/network-packet-broker-masterclass/) — ADC ile birlikte trafik görünürlüğü
- 🔐 [Zero Trust Zihniyeti](/tr/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — LTM'nin Zero Trust mimarisindeki yeri