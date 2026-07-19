---
title: "Proje Portföyü — Seçilmiş Kurumsal Projeler"
description: "Barash Helvadzhaoglu'nun ağ güvenliği projeleri. Bankacılık, üretim ve hizmet sektörlerinde kurumsal dağıtımlar — NDA uyumlu."
date: 2026-01-01
draft: false
showToc: false
hidemeta: false
keywords:
  - ağ güvenliği projeleri
  - kurumsal ağ mühendisi portföyü
  - zero trust deployment
  - veri merkezi modernizasyonu
  - Cisco NDFC VXLAN
  - Fortinet firewall kurulumu
  - Palo Alto VPN migrasyonu
  - ağ otomasyonu Python
  - F5 load balancer migrasyonu
  - Aruba ClearPass 802.1X
---

# Proje Portföyü

11 yılı aşkın kurumsal ölçekli dağıtım deneyimi: **bankacılık**, **üretim**, **otelcilik**, **eğitim** ve **hizmet** sektörlerinde. NDA yükümlülükleri nedeniyle müşteri isimleri paylaşılmamaktadır — ancak sektör, teknoloji yığını ve ölçülebilir sonuçlar aşağıda yer almaktadır.

> **Üst yönetim kademesinden profesyonel bir referans mektubu talep üzerine sunulabilir.**

---

## 1. Kurumsal Ağ Mimarisi & Veri Merkezi

![Veri Merkezi VXLAN](/img/postimages/project-dc-fabric-vxlan.webp)

### Veri Merkezi Fabric Modernizasyonu — Bankacılık Sektörü
**Rol:** Kıdemli Ağ Güvenliği Mühendisi | İstanbul, 2022–2025

- **Cisco NDFC** ile active-active tasarımlı çift veri merkezi fabric mimarisi kuruldu
- **100+ switch**, **sıfır kesinti** ile **VXLAN/BGP-EVPN** mimarisine taşındı
- Verim **%25** artırıldı, merkezi otomasyon ve görünürlük sağlandı

`Cisco NDFC` `Nexus 9000` `VXLAN` `BGP-EVPN`

---

![Fabrika Ağı](/img/postimages/project-packaging-factory.webp)

### Ağ Altyapısı Yenileme — Global Ambalaj Üreticisi
**Rol:** Ağ Güvenliği Lideri | Çoklu site, 2018–2022

- Birden fazla fabrika lokasyonunda uçtan uca altyapı yenileme
- **Cisco ISE**, AnyConnect ve E-posta Güvenliği ile uç nokta koruma entegrasyonu
- Gelişmiş segmentasyon sayesinde güvenlik olayları **%25** azaltıldı

`Cisco Catalyst 9000` `ISE` `Fortinet FGT` `AMP`

---

![Otel Ağı](/img/postimages/project-hotel-network.webp)

### Otel Ağ Altyapısı Kurulumu — Otelcilik Sektörü
**Rol:** Ağ Güvenliği Lideri | İstanbul

- Eksiksiz kablolu ve kablosuz altyapı tasarlandı ve hayata geçirildi
- **200+ Aruba AP** ve **50+ switch** kuruldu, HA tasarımı ile **%99,9 uptime** sağlandı
- Misafir/personel segmentasyonu için Fortinet firewall yapılandırıldı

`Aruba AP` `Fortinet Firewall` `VLAN Segmentasyonu` `Misafir Wi-Fi`

---

![F5 Migrasyon](/img/postimages/project-f5-migration.webp)

### Yük Dengeleyici Migrasyonu — Bankacılık Sektörü
**Rol:** Kıdemli Ağ Güvenliği Mühendisi | İstanbul, 2022–2025

- **30+ F5 LTM/GTM cihazı** 2000'den 5000 serisine taşındı (TMOS 13.x → 15.x)
- Performans **6 kat** artırıldı, sıfır kesintili HA migrasyonu gerçekleştirildi
- Otomatik yapılandırma ile manuel operasyon yükü **%50** azaltıldı

`F5 LTM` `F5 GTM` `TMOS 15.x` `HA Clustering` `SSL Offloading`

---

## 2. Siber Güvenlik & Zero Trust Dağıtımları

![Zero Trust VPN](/img/postimages/project-zero-trust-vpn.webp)

### SSL VPN & Zero Trust Uygulaması — Bankacılık Sektörü
**Rol:** Kıdemli Ağ Güvenliği Mühendisi | İstanbul, 2022–2025

- **10+ şirkette, 500+ kullanıcı** için **Fortinet SSL VPN** altyapısı kuruldu
- **FortiClient, FortiEMS ve MFA** ile kimlik tabanlı erişim kontrolü entegre edildi
- Merkezi Zero Trust izleme ile **%99,9 uptime** elde edildi

`Fortinet NGFW` `FortiClient` `FortiEMS` `MFA` `Zero Trust`

---

### Palo Alto GlobalProtect VPN Migrasyonu — Bankacılık Sektörü
**Rol:** Kıdemli Ağ Güvenliği Mühendisi | İstanbul, 2022–2025

- **1.000+ kullanıcı** VPN altyapısı **Palo Alto NGFW ve GlobalProtect**'e taşındı
- MFA ile ayrıntılı rol tabanlı erişim kontrolü uygulandı
- VPN kaynaklı olaylar **%35** azaltıldı

`Palo Alto NGFW` `GlobalProtect` `MFA` `Rol Tabanlı Erişim`

---

![DNA Center](/img/postimages/project-dna-center-sdaccess.webp)

### Kurumsal Ağ Modernizasyonu & Otomasyon — Üretim (TR/EG)
**Rol:** Ağ Güvenliği Lideri | Türkiye & Mısır, 2018–2022

- ISE, Umbrella, Stealthwatch ve Firepower entegrasyonuyla **Cisco DNA Center** mimarisi kuruldu
- Policy tabanlı VLAN sağlama, 802.1X otomasyonu ve yapay zeka destekli analitik etkinleştirildi
- Otomatik iş akışları ile operasyonel yük **~%60** azaltıldı
- **Cisco Success Story olarak yayınlandı** — Türkiye'deki ilk büyük ölçekli DNA Center & Stealthwatch entegrasyonlarından biri

`Cisco DNA Center` `ISE` `Umbrella` `Stealthwatch` `Firepower` `Catalyst 9000`

---

![Firewall Policy](/img/postimages/project-firewall-policy.webp)

### Firewall Policy Optimizasyonu & SOC Entegrasyonu — Bankacılık Sektörü
**Rol:** Kıdemli Ağ Güvenliği Mühendisi | İstanbul, 2022–2025

- **30+ firewall kural seti** denetlendi ve optimize edildi
- **FortiManager** ve **FortiAnalyzer** ile otomatik alarm ve uyumluluk raporlaması
- Yanlış alarm oranı **%40** azaltıldı

`FortiManager` `FortiAnalyzer` `Uyumluluk Otomasyonu` `SOC`

---

## 3. Ağ Otomasyonu & Gözlemlenebilirlik

![SOC Splunk](/img/postimages/project-splunk-soc.webp)

### SOC Tehdit Görünürlüğü & Splunk Dashboard — Bankacılık Sektörü
**Rol:** Kıdemli Ağ Güvenliği Mühendisi | İstanbul, 2022–2025

- Firewall ve IPS logları **birleşik Splunk dashboard**'larına entegre edildi
- DDoS, iç ve dış saldırı görünürlüğü için çok katmanlı dashboard tasarlandı
- Olay müdahale süresi **%40** kısaltıldı

`Splunk SIEM` `Fortinet IPS` `Check Point` `Dashboard Otomasyonu`

---

![Python Otomasyon](/img/postimages/project-python-automation.webp)

### Python Tabanlı Ağ Otomasyonu — Bankacılık Sektörü
**Rol:** Kıdemli Ağ Güvenliği Mühendisi | İstanbul, 2022–2025

- **Cisco Nexus** switch'lerinden envanter verisi toplayan **Python script'leri** geliştirildi
- Policy/nesne işlem süresi **2–3 saatten 5–10 dakikaya** indirildi

`Python` `Cisco Nexus` `DevOps Entegrasyonu` `Kapasite Planlaması`

---

### SLA İzleme & Raporlama — Çoklu Müşteri
**Rol:** Ağ Güvenliği Lideri | 2018–2022

- SLA tabanlı müşteriler için **Zabbix** izleme ve **Grafana** dashboard'ları kuruldu
- Uptime SLA **%97'den %99,9'a** yükseltildi

`Zabbix` `Grafana` `SolarWinds` `SLA Raporlama`

---

## 4. Unified Communications

### Cisco CUCM Kurulumu — Petrokimya & Havacılık
**Rol:** Ağ Güvenliği Mühendisi / Lideri | 2014–2022

- 5+ şirketin IP telefon altyapısı tek bir CUCM cluster'ında konsolide edildi
- **3.000+ çalışan** için **Cisco Jabber** devreye alındı
- VPN gerektirmeyen dış erişim için **Expressway Edge/Core** uygulandı

`Cisco CUCM` `Jabber` `Expressway` `SIP Trunk`

---

## Teknolojiler & Üreticiler

| Kategori | Teknolojiler |
|---|---|
| Firewall | Cisco Firepower, Fortinet FortiGate, Palo Alto NGFW, Check Point |
| Switching | Cisco Catalyst 9K, Nexus 9K, HP Comware, Aruba |
| Güvenlik & NAC | Cisco ISE, Aruba ClearPass, 802.1X, FortiEMS |
| VPN & Uzaktan Erişim | GlobalProtect, FortiClient, AnyConnect, ZTNA |
| Otomasyon | Python, Bash, Cisco DNA Center, FortiManager |
| İzleme | SolarWinds, Splunk, Zabbix, Grafana, FortiAnalyzer |
| Yük Dengeleme | F5 LTM, F5 GTM |
| Kablosuz | Aruba, Cisco Meraki, Cisco WLC |

---

*Üst yönetim kademesinden profesyonel bir referans mektubu talep üzerine sunulabilir.*  
*Proje detayları veya danışmanlık sorguları için [iletişime geçin](/tr/iletisim/).*