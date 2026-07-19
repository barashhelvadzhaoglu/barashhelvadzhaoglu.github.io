---
title: "F5 GTM & GSLB Deep Dive: Globales Traffic-Management und DNS-Failover"
description: "F5 GTM (BIG-IP DNS) Deep Dive — Wide IPs, iQuery, Topologie-Routing, TTL-Strategie, Multi-DC-Failover und Aktiv-Aktiv vs. Aktiv-Standby."
date: 2026-04-15
draft: false

cover:
  image: "/img/postimages/f5-gtm-gslb-cover.webp"
  alt: "F5 GTM GSLB Globales Traffic-Management — DNS-Failover-Architektur"
  relative: false

tags: ["F5", "GTM", "GSLB", "BIG-IP DNS", "DNS-Failover", "Globales Load Balancing", "Multi-DC", "Disaster Recovery"]
categories: ["Technologie"]
keywords:
  - F5 GTM Konfiguration
  - F5 GSLB Global Server Load Balancing
  - F5 Wide IP
  - F5 iQuery
  - F5 Topologie Load Balancing
  - F5 DNS-Failover
  - F5 GTM vs LTM
  - Global Traffic Manager BIG-IP
  - Multi-Datacenter-Failover
  - F5 GTM TTL-Strategie

showToc: true
TocOpen: true
---

# F5 GTM & GSLB Deep Dive: Globales Traffic-Management und DNS-Failover

Dieser Artikel ist Teil der F5 BIG-IP-Serie.

> **Neu bei F5?** Beginnen Sie zuerst mit der Plattformübersicht: [F5 BIG-IP ist kein Load Balancer — Es ist eine Application Delivery Platform](/de/technology/f5-bigip-application-delivery-platform-uebersicht/)

Wenn Sie das Gesamtbild bereits verstehen und tief in GTM eintauchen möchten — iQuery, Wide IPs, Topologie-Routing, TTL-Strategie und Multi-DC-Design — sind Sie hier richtig.

---

## Das Problem, das GTM löst

LTM verwaltet Anwendungsdatenverkehr innerhalb eines einzelnen Rechenzentrums. Es verteilt Verbindungen auf Backend-Server, überwacht die Gesundheit und bietet HA innerhalb eines Standorts. Aber LTM hat keine Sichtbarkeit auf das, was außerhalb seines Rechenzentrums passiert — es kann keinen Datenverkehr zwischen Standorten leiten.

Das ist genau die Lücke, die GTM füllt. Wenn eine Organisation zwei Rechenzentren hat, ein primäres DC und einen DR-Standort oder global verteilte Infrastruktur, lautet die Frage: *Wie wissen Clients, mit welchem Rechenzentrum sie sich verbinden sollen, und was passiert automatisch, wenn eines offline geht?*

Ohne GTM lautet die Antwort meist manuelle DNS-Änderungen — langsam, fehleranfällig und für automatisiertes Failover völlig ungeeignet. GTM löst dies auf der DNS-Ebene.

---

## Der DNS-Fluss: Wie GTM entscheidet

GTM fungiert als **autoritativer DNS-Server** für Ihre Anwendungszonen. Wenn ein Client `webapp.unternehmen.de` auflöst, erreicht die Abfrage GTM statt eines Standard-DNS-Servers:

```
1. Client: "Was ist die IP für webapp.unternehmen.de?"
2. Abfrage erreicht GTM (autoritativ für unternehmen.de-Zone)
3. GTM bewertet in Echtzeit:
   → Ist DC-1 LTM gesund? (via iQuery)
   → Ist DC-2 LTM gesund? (via iQuery)
   → Welche Load-Balancing-Richtlinie gilt?
   → Wo befindet sich dieser Client geografisch?
4. GTM antwortet: "webapp.unternehmen.de = 10.10.1.100" (DC-1 VIP)
5. Client verbindet sich mit 10.10.1.100 → LTM übernimmt von hier
```

Die Intelligenz liegt in Schritt 3. GTM ist kein passiver DNS-Server, der einen statischen Eintrag zurückgibt — es trifft bei jeder Beantwortung einer Abfrage eine Echtzeit-Entscheidung basierend auf dem aktuellen Infrastrukturzustand und der Richtlinie.

---

## GTM-Objekthierarchie

GTM verwendet eine vierstufige Hierarchie, die die DNS-Struktur widerspiegelt:

```
Rechenzentrum  →  Server  →  Virtual Server  →  Wide IP (Pool-Member)
```

**Rechenzentrum:** Eine logische Gruppierung für einen physischen Standort (DC-Istanbul, DC-Frankfurt). Enthält alle bei GTM registrierten Server an diesem Standort.

**Server:** Ein bei GTM registriertes BIG-IP-Gerät (typischerweise ein LTM). GTM kommuniziert über iQuery mit ihm für Echtzeit-Gesundheitsdaten.

**Virtual Server:** Ein spezifischer LTM Virtual Server (VIP) auf einem registrierten Server. Der tatsächliche Endpunkt, zu dem GTM Datenverkehr leiten kann.

**GTM-Pool:** Eine Gruppe von Virtual Servern über einem oder mehreren LTMs. GTM verteilt DNS-Antworten auf Pool-Members.

**Wide IP:** Der DNS-Name (`webapp.unternehmen.de`), den Clients auflösen. Eine Wide IP referenziert einen oder mehrere GTM-Pools und definiert die Auflösungsrichtlinie.

---

## iQuery: Warum GTM tatsächlich die Anwendungsgesundheit versteht

**iQuery** ist das proprietäre F5-Protokoll, das GTM echte Anwendungsbewusstheit verleiht. Das ist es, was GTM von externen DNS-Load-Balancern unterscheidet, die einfach eine VIP anpingen oder TCP-Erreichbarkeit prüfen.

Ohne iQuery würde GTM nur wissen, ob eine IP-Adresse auf eine Probe antwortet. Mit iQuery weiß GTM:

- Ob der LTM Virtual Server aktiviert und aktiv ist
- Ob der Pool hinter diesem Virtual Server gesunde, aktive Members hat
- Aktuelle aktive Verbindungsanzahl auf dem LTM
- Aktuelle CPU- und Speicherauslastung

**Die kritische Implikation:** Wenn eine Backend-Anwendung ausfällt und LTM seinen Pool als ausgefallen markiert, propagiert iQuery dies **sofort** an GTM — bevor ein Client die Chance hat, sich mit einem defekten Endpunkt zu verbinden. GTM hört sofort auf, mit dieser VIP des DCs auf DNS-Abfragen zu antworten.

Eine TCP-Gesundheitsprobe von GTM zu einer VIP-IP würde dies niemals erkennen — die VIP-IP bleibt erreichbar, selbst wenn die Anwendung dahinter vollständig defekt ist. iQuery ist das, was den Unterschied macht.

### Registrierung eines LTM bei GTM

```
Server: ltm-dc1
  Produkt:         BIG-IP (aktiviert iQuery)
  Adresse:         10.10.0.1 (LTM-Management-IP)
  Rechenzentrum:   DC-Istanbul
  Virtual Server:  [automatisch via iQuery entdeckt]
    - vs_webapp_443  (10.10.1.100:443)
    - vs_api_443     (10.10.1.101:443)
    - vs_admin_443   (10.10.1.102:443)
```

Nach der Registrierung entdeckt und überwacht GTM automatisch alle Virtual Server auf diesem LTM. Keine manuelle Virtual-Server-Konfiguration in GTM erforderlich — iQuery kümmert sich um die Erkennung.

---

## Wide IPs und GTM-Pools

Eine Wide IP verbindet einen DNS-Namen mit einer Auflösungsrichtlinie:

```
Wide IP: webapp.unternehmen.de (Typ: A)
  Pool: gtm_pool_webapp_primary
    Load-Balancing-Methode: Global Availability
    Members:
      - ltm-dc1 / vs_webapp_443  (Reihenfolge: 1)
      - ltm-dc2 / vs_webapp_443  (Reihenfolge: 2)
  Fallback-Pool:    gtm_pool_webapp_dr
  Last-Resort-Pool: [SERVFAIL zurückgeben, wenn alle Pools erschöpft]
```

Eine Wide IP kann mehrere Pools in Prioritätsreihenfolge haben. Wenn der primäre Pool keine verfügbaren Members hat, versucht GTM automatisch den nächsten Pool. Das ermöglicht gestaffelte Failover-Architekturen ohne manuelle Eingriffe.

---

## Load-Balancing-Methoden

GTM Load Balancing arbeitet auf DNS-Antwortebene — jede Methode bestimmt, welche IP des Pool-Members für eine gegebene Abfrage zurückgegeben wird.

### Global Availability

Gibt immer die IP des ersten verfügbaren Members zurück. Wechselt zum nächsten Member nur, wenn das aktuelle nicht verfügbar ist:

```
Members (in Prioritätsreihenfolge):
  1. ltm-dc1 / vs_webapp_443  ← gesamter Datenverkehr wenn gesund
  2. ltm-dc2 / vs_webapp_443  ← Datenverkehr nur wenn DC-1 ausfällt
```

**Geeignet für:** Primär/DR-Architekturen. Der gesamte Datenverkehr läuft am primären Standort; DR aktiviert sich nur bei echten Ausfällen. Das war die Standardmethode in der Banking-Umgebung — kosteneffizient, einfach zu verstehen und vorhersehbar bei Ausfällen.

### Round Robin

Wechselt DNS-Antworten zwischen Pool-Members ab:

```
Abfrage 1 → DC-1 VIP
Abfrage 2 → DC-2 VIP
Abfrage 3 → DC-1 VIP
```

**Geeignet für:** Aktiv-Aktiv-Multi-DC-Architekturen mit gleicher Kapazität an jedem Standort. Verbreitet in groß angelegten Webanwendungen, wo beide Standorte kontinuierlich Last teilen sollen.

### Ratio

Gewichtete Verteilung:

```
ltm-dc1 / vs_webapp_443  Ratio: 7  ← 70% der DNS-Antworten
ltm-dc2 / vs_webapp_443  Ratio: 3  ← 30% der DNS-Antworten
```

**Geeignet für:** Aktiv-Aktiv wenn Rechenzentren unterschiedliche Kapazitäten haben. Ermöglicht kapazitätsproportionale Lastverteilung.

### Topology

Routet DNS-Antworten basierend auf dem geografischen Standort der Client-DNS-Resolver-IP:

```
Topologie-Einträge (von oben nach unten bewertet, erste Übereinstimmung gewinnt):
  Subnetz 10.0.0.0/8        → DC-Istanbul   (alle internen Benutzer)
  ISP: Turk Telekom          → DC-Istanbul
  Region: Europa             → DC-Frankfurt
  Region: Naher Osten        → DC-Istanbul
  Standard                   → DC-Frankfurt
```

**Geeignet für:** Globale Anwendungen mit Benutzern in mehreren Regionen. Reduziert die Latenz, indem Benutzer zum nächsten DC geleitet werden. Ermöglicht auch Datenresidenz-Compliance — sicherstellt, dass Anfragen von EU-Benutzern in EU-Rechenzentren verarbeitet werden.

GTM verwendet eine IP-Geolokalisierungsdatenbank, um Resolver-IPs auf Regionen abzubilden. Halten Sie diese Datenbank aktuell — ISPs vergeben IP-Bereiche regelmäßig neu, und veraltete Geolokalisierungsdaten senden Benutzer in falsche Regionen.

### Least Connections

Leitet zum Pool-Member mit den wenigsten aktiven Verbindungen, die in Echtzeit über iQuery erhalten werden:

```
Aktueller Status via iQuery:
  ltm-dc1: 4.521 aktive Verbindungen
  ltm-dc2: 3.102 aktive Verbindungen
  → GTM gibt DC-2 VIP für nächste Abfrage zurück
```

**Geeignet für:** Aktiv-Aktiv-Architekturen, wo dynamisches Load Balancing basierend auf tatsächlichen Verbindungsanzahlen gegenüber statischen Gewichtungen bevorzugt wird.

---

## DNS-TTL-Strategie: Der am meisten missverstandene Aspekt

TTL bestimmt, wie lange DNS-Resolver die Antwort von GTM zwischenspeichern. Das wird weithin missverstanden:

**TTL steuert nicht die Failover-Geschwindigkeit für Clients, die den Namen bereits aufgelöst haben.** Ein Client, der `webapp.unternehmen.de` vor 10 Sekunden aufgelöst hat, verwendet weiterhin die zwischengespeicherte IP bis TTL abläuft — unabhängig davon, was GTM derzeit antwortet.

TTL steuert, wie schnell **neue DNS-Lookups** den aktuellen Infrastrukturzustand widerspiegeln.

### TTL-Kompromisse

| TTL | Failover-Sichtbarkeit | DNS-Abfragelast | Anwendungsfall |
|---|---|---|---|
| 30 Sek | Schnell | Hoch | Kritische Zahlungssysteme, Auth-Dienste |
| 60 Sek | Gut | Moderat | Die meisten Produktionsanwendungen |
| 300 Sek | Moderat | Niedrig | Interne Tools, Monitoring |
| 3600 Sek | Langsam | Sehr niedrig | Statische Inhalte, selten ändernde Einträge |

In der Banking-Umgebung:
- **30 Sekunden** für Zahlungsabwicklung und Authentifizierungsdienste
- **60 Sekunden** für allgemeine Banking-Anwendungen
- **300 Sekunden** für interne Dashboards und Monitoring-Tools

### Berechnung der minimalen effektiven Failover-Zeit

```
Worst-Case-Failover-Zeit ≈ Gesundheitsprüfungsintervall + TTL
```

Mit einem 5-Sekunden-iQuery-Prüfintervall und 30-Sekunden-TTL: Worst Case ist ~35 Sekunden. Einige Clients wechseln innerhalb von Sekunden nach der Fehlererkennung zum neuen DC; andere warten auf TTL-Ablauf.

Für Anwendungen mit strengen RTO-Anforderungen kombinieren Sie niedrige TTL mit Wiederholungslogik auf Anwendungsebene, um das Übergangsfenster reibungslos zu handhaben.

---

## Multi-DC-Architekturmuster

### Aktiv-Standby (Primär / DR)

```
Normal:
  GTM → DC-1 LTM → App-Server (DC-1)
  DC-2 ist Hot-Standby — läuft, synchronisiert, kein Datenverkehr

DC-1-Ausfall:
  iQuery: DC-1 LTM Virtual Server als ausgefallen markiert
  GTM: hört sofort auf, mit DC-1 VIP zu antworten
  Neue DNS-Abfragen: erhalten DC-2 VIP
  Datenverkehrsverschiebung: innerhalb des TTL-Fensters
```

Anforderungen:
- Identisches Anwendungs-Deployment auf beiden DCs
- Datenbankreplikation (synchron für null RPO, asynchron für niedrigeres RPO)
- GTM-Methode: **Global Availability**

### Aktiv-Aktiv (Lastverteilung)

```
Normal:
  GTM → DC-1 (50% der DNS-Antworten)
  GTM → DC-2 (50% der DNS-Antworten)

DC-1-Ausfall:
  GTM leitet 100% zu DC-2
```

Anforderungen:
- Zwischen DCs geteilter Sitzungszustand oder zustandsloses Anwendungsdesign
- Jedes DC muss 100% des Datenverkehrs unabhängig bewältigen (für diese Kapazität planen)
- Gleichzeitig von beiden DCs beschreibbare Datenbank
- GTM-Methode: **Round Robin**, **Ratio** oder **Least Connections**

Aktiv-Aktiv liefert bessere Ressourcennutzung und schnelleres effektives Failover (kein Kaltstart-DR-Standort). Die Architekturkomplexität ist höher — besonders rund um Datenbankschreibkonflikte und Sitzungszustandsverwaltung.

### Topologiebasierte geografische Verteilung

```
EU-Benutzer    → Resolver-IP in Europa    → DC-Frankfurt
MENA-Benutzer  → Resolver-IP im Nahen Osten → DC-Istanbul
Intern         → RFC1918-Quelle            → DC-Istanbul (nächster)
Standard       → DC-Frankfurt
```

Jedes DC verarbeitet unter normalen Bedingungen den Datenverkehr seiner Region. Fallback-Topologie-Einträge leiten alle Regionen während eines Ausfalls zum überlebenden DC.

Dieses Muster kombiniert Leistungsvorteile (geringere Latenz) mit Compliance-Anforderungen (Datenresidenz) und Kapazitätsoptimierung (jedes DC für seine Region dimensioniert).

---

## GTM-Monitore vs. iQuery: Wann was verwenden

**iQuery (für BIG-IP LTMs):**
- Echtzeit-Anwendungsgesundheitsdaten vom LTM
- Kein zusätzlicher Monitoring-Datenverkehr
- Kennt Anwendungsgesundheit, nicht nur IP-Erreichbarkeit
- Automatische Virtual-Server-Erkennung
- Für alle BIG-IP LTM-Endpunkte verwenden

**GTM-native Monitore (für Nicht-BIG-IP-Endpunkte):**
- GTM sendet eigene Gesundheitsproben direkt an Endpunkte
- Unterstützt TCP, HTTP, HTTPS, ICMP
- Für Drittanbieter-Load-Balancer, Cloud-Endpunkte, Ursprungsserver in hybriden Umgebungen verwenden

In den meisten Enterprise-Deployments übernimmt iQuery das gesamte BIG-IP-zu-BIG-IP-Monitoring. GTM-native Monitore sind für hybride Architekturen reserviert, wo einige Endpunkte keine F5-Geräte sind.

---

## DNS-Persistenz in GTM

GTM pflegt keinen TCP-Zustand — es beeinflusst nur DNS-Antworten. Es unterstützt jedoch **DNS-Persistenz**, um sicherzustellen, dass wiederholte Abfragen vom gleichen Resolver für einen konfigurierbaren Zeitraum die gleiche IP zurückgeben:

```
Wide IP Persistenz:
  Aktiviert: Ja
  TTL:       300 Sekunden
  Typ:       nach Quell-IP (Resolver-IP)
```

Mit aktivierter Persistenz gibt GTM unabhängig von der Load-Balancing-Methode für 300 Sekunden dieselbe VIP an denselben Resolver zurück. Das reduziert Sitzungsunterbrechungen, wenn Clients häufig neu auflösen.

**Wichtiger Vorbehalt:** DNS-Persistenz basiert auf der **Resolver-IP**, nicht der End-Client-IP. Wenn viele Endbenutzer einen einzelnen rekursiven ISP-Resolver teilen, erscheinen sie GTM alle als derselbe „Client". Persistenz kann in diesen Fällen disproportionalen Datenverkehr zu einem DC konzentrieren. Bewerten Sie, ob Persistenz wirklich hilft, bevor Sie sie aktivieren.

---

## Wichtigste Erkenntnisse

- GTM löst **Multi-DC-DNS-Failover** — das Problem, das LTM allein nicht addressieren kann.
- **iQuery** ist GTMs wichtigste Funktion: echte Anwendungsgesundheitsbewusstheit, nicht nur IP-Erreichbarkeit. Wenn LTM einen Anwendungspool als ausgefallen markiert, reagiert GTM sofort.
- **Global Availability** ist die richtige Methode für Primär/DR. **Round Robin** oder **Ratio** für Aktiv-Aktiv.
- **Topology**-Routing reduziert die Latenz und ermöglicht Datenresidenz-Compliance für globale Deployments.
- **TTL steuert nur neue Lookups** — nicht bestehende Verbindungen. Minimales effektives Failover = Gesundheitsprüfungsintervall + TTL.
- Verwenden Sie **iQuery für BIG-IP LTMs**; verwenden Sie GTM-native Monitore für Drittanbieter-Endpunkte.

---

## Diese Serie

- 📖 [F5 BIG-IP Plattformübersicht — Alle Module](/de/technology/f5-bigip-application-delivery-platform-uebersicht/) ← Beginnen Sie hier, wenn Sie neu bei F5 sind
- 🔧 [F5 LTM Deep Dive](/de/technology/f5-ltm-virtual-server-irules-ssl-offloading-ha/)
- 🛡️ [F5 WAF Deep Dive](/de/technology/f5-waf-asm-advanced-waf-anwendungssicherheit/)

## Verwandte Artikel

- 🏗️ [IT-Infrastruktur ist keine Produktsammlung](/de/architecture/it-infrastructure-not-a-collection-of-products/) — Systemdenken für Multi-DC-Design
- 🔐 [Die Zero-Trust-Mentalität](/de/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — Identitätsbewusster Zugang über verteilte Infrastruktur
- 📊 [Monitoring richtig gemacht](/de/architecture/monitoring-not-just-seeing/) — GTM- und LTM-Gesundheit proaktiv überwachen