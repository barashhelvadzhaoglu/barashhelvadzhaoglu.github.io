---
title: "DDoS-Schutzstrategien: ISP-Scrubbing, On-Premise-Appliances und Cloud-Dienste"
description: "DDoS-Schutz Leitfaden — Angriffstypen, ISP-Scrubbing, On-Premise-Appliances, Cloud-Dienste und die richtige Kombination für Ihre Organisation."
date: 2026-03-30
draft: false

cover:
  image: "/img/postimages/ddos-protection-strategies-cover.webp"
  alt: "DDoS-Schutzstrategien — ISP-Scrubbing, On-Premise, Cloud"
  relative: false

tags: ["DDoS", "Netzwerksicherheit", "Arbor", "Cloudflare", "AWS Shield", "ISP-Scrubbing", "On-Premise", "Cloud-Sicherheit"]
categories: ["Technologie"]
keywords:
  - DDoS-Schutzstrategien
  - ISP DDoS-Scrubbing
  - On-Premise DDoS-Appliance
  - Cloud DDoS-Schutz
  - Cloudflare DDoS
  - AWS Shield
  - Arbor DDoS
  - Radware DefensePro
  - hybride DDoS-Schutz
  - DDoS-Mitigationsvergleich

showToc: true
TocOpen: false
---

# DDoS-Schutzstrategien: ISP-Scrubbing, On-Premise-Appliances und Cloud-Dienste

Ein DDoS-Angriff (Distributed Denial of Service) muss Ihre Systeme nicht kompromittieren. Er muss sie nur unerreichbar machen. Und anders als die meisten Sicherheitsbedrohungen ist der Schaden sofort und vollständig sichtbar — Ihre Anwendung hört auf zu funktionieren, Kunden können Sie nicht erreichen, und der Umsatz stoppt.

Was DDoS besonders schwierig macht, ist, dass der Angriffsdatenverkehr auf Paketebene legitim aussieht. Millionen gültiger TCP-SYN-Pakete, Millionen gültiger DNS-Abfragen, Millionen gültiger HTTP-Anfragen — alle perfekt geformt, alle vollständig absichtlich. Ihr Netzwerk verarbeitet sie genauso wie echten Datenverkehr, und das ist genau das Problem.

Als jemand, der in Banking-Infrastruktur gearbeitet hat, wo DDoS-Schutz eine regulatorische Anforderung war — nicht nur eine Best Practice — möchte ich erläutern, wie Organisationen sich tatsächlich schützen: Was die drei Hauptansätze sind, was jeder kann und nicht kann, und wie sie in der Praxis kombiniert werden.

---

## Die Angriffsfläche verstehen

Bevor Sie eine Schutzstrategie wählen, lohnt es sich, präzise zu sein, wogegen Sie sich schützen. DDoS-Angriffe fallen in drei Kategorien, und jede erfordert grundlegend unterschiedliche Mitigationsansätze.

### Volumetrische Angriffe (Schicht 3/4)

Der sichtbarste Typ. Das Ziel ist einfach: Ihre Internetverbindung mit mehr Datenverkehr sättigen, als sie transportieren kann.

Gängige Techniken:
- **UDP-Flood** — massive Mengen UDP-Pakete an zufällige Ports senden. Das Ziel sendet ICMP-„Port nicht erreichbar"-Antworten, was sowohl eingehende als auch ausgehende Bandbreite verbraucht.
- **ICMP-Flood (Ping-Flood)** — mit Ping-Anfragen überwältigen.
- **Amplifikationsangriffe** — die gefährlichste Variante. Der Angreifer sendet kleine Anfragen an falsch konfigurierte Drittanbieter-Server (DNS-Resolver, NTP-Server, Memcached-Instanzen) mit Ihrer IP als Quelle. Diese Server senden große Antworten an Sie. DNS-Amplifikation kann eine 50–70-fache Amplifikation erreichen; Memcached-Amplifikation hat 51.000-fache erreicht.

**Skalierung:** Moderne volumetrische Angriffe übersteigen routinemäßig 1 Tbps. Eine 10-Gbps-Internetverbindung ist dagegen irrelevant — Sie werden gesättigt, bevor ein einziges Paket Ihre Firewall erreicht.

**Kernerkenntnisse:** Sie können volumetrische Angriffe nicht in Ihren eigenen Räumlichkeiten abmildern, wenn das Angriffsvolumen Ihren ISP-Uplink übersteigt. Der Datenverkehr muss upstream — auf ISP- oder Cloud-Ebene — gefiltert werden, bevor er Ihre Verbindung erreicht.

### Protokollangriffe (Schicht 3/4)

Erschöpfen Netzwerkgeräteressourcen statt Bandbreite.

- **SYN-Flood** — Millionen von TCP-SYN-Paketen senden, ohne den Handshake abzuschließen. Das Ziel reserviert Speicher für jede halboffene Verbindung, bis die Verbindungstabelle voll ist und legitime Verbindungen abgelehnt werden.
- **Fragmentierte Paketangriffe** — fehlerhafte oder überlappende IP-Fragmente senden, die Reassemblierungspuffer überfordern.
- **Smurf-Angriff** — ICMP-Broadcast-Amplifikation mit gefälschten Quell-IPs.

**Skalierung:** In Paketen pro Sekunde (Mpps) gemessen, nicht in Bandbreite. Eine 100-Mbps-SYN-Flood bei kleinen Paketgrößen kann die Verbindungstabellenkapazität einer Mittelklasse-Firewall überschreiten.

**Kernerkenntnisse:** Protokollangriffe können On-Premise durch dedizierte DDoS-Hardware mit FPGA-basierter Paketverarbeitung abgemildert werden — aber nur, wenn das Volumen Ihren Upstream-Link nicht zuerst sättigt.

### Anwendungsschichtangriffe (Schicht 7)

Am schwierigsten zu erkennen und abzumildern. Der Datenverkehr ist legitimes HTTP/HTTPS — die Absicht ist bösartig.

- **HTTP-Flood** — Millionen von HTTP-GET- oder POST-Anfragen an ressourcenintensive Endpunkte (Suche, Login, Berichtgenerierung).
- **Slowloris** — viele Verbindungen öffnen und HTTP-Header sehr langsam senden, Verbindungen offen halten ohne Anfragen abzuschließen. Erschöpft den Verbindungspool des Servers.
- **RUDY (R-U-Dead-Yet)** — ähnlich wie Slowloris, aber für POST-Bodies. Sendet Daten ein Byte auf einmal.
- **SSL-Erschöpfung** — TLS-Handshakes initiieren, aber nie abschließen oder Handshakes abschließen und sofort neu verhandeln. CPU-intensiv für Server ohne Hardware-SSL-Beschleunigung.

**Skalierung:** Kann bei niedrigen Datenverkehrsvolumina verheerend effektiv sein — ein paar tausend Anfragen pro Sekunde, die den richtigen Endpunkt treffen, können einen Webserver zum Absturz bringen, der normalerweise Millionen von Anfragen verarbeitet.

**Kernerkenntnisse:** Schicht-7-Angriffe erfordern anwendungsbewusste Mitigation. Ein volumetrischer Scrubbing-Dienst kann eine bösartige HTTP-Flood nicht von legitimem Datenverkehr unterscheiden.

---

## Die drei Schutzansätze

Kein einzelner Schutzansatz deckt alle Angriffstypen in allen Maßstäben ab. Organisationen mit ernsthafter DDoS-Exposition kombinieren typischerweise zwei oder drei dieser Schichten.

---

## 1. ISP-basierte Scrubbing-Dienste

### Wie es funktioniert

Ihr ISP (oder ein spezialisierter Scrubbing-Anbieter mit Upstream-Netzwerkvereinbarungen) leitet Ihren Datenverkehr während eines Angriffs an ein **Scrubbing-Center** um. Im Scrubbing-Center wird Angriffsdatenverkehr gefiltert und nur sauberer Datenverkehr an Ihr Netzwerk weitergeleitet:

```
Normaler Betrieb:
  Internet → ISP → Ihr Netzwerk

Während eines Angriffs:
  Internet → ISP → Scrubbing-Center → Sauberer Datenverkehr → Ihr Netzwerk
                          │
                   Angriffsdatenverkehr verworfen
```

Die Datenverkehrsumleitung wird typischerweise auf zwei Arten ausgelöst:
- **On-Demand:** Sie kontaktieren den ISP, wenn ein Angriff erkannt wird. Manueller Prozess, Reaktionszeit hängt vom Anbieter ab.
- **Always-On:** Datenverkehr wird kontinuierlich durch Scrubbing geleitet. Keine Erkennungsverzögerung, fügt aber Latenz hinzu.

### Was ISP-Scrubbing schützt

ISP-Scrubbing ist speziell für **volumetrische Angriffe** konzipiert. Es arbeitet auf Netzwerkebene, upstream Ihrer Infrastruktur. Ein Angriff, der Ihren 10-Gbps-Link sättigen würde, wird durch die 10-Tbps+-Kapazität des Anbieters absorbiert, bevor er Sie erreicht.

### Was ISP-Scrubbing nicht tut

- **Schicht-7-Schutz:** ISP-Scrubbing arbeitet auf L3/L4. Es kann HTTP-Anfrageinhalte nicht analysieren.
- **Low-and-Slow-Angriffe:** Slowloris, RUDY und SSL-Erschöpfung sind nicht volumetrisch.
- **Sofortige Reaktion:** On-Demand-Scrubbing hat eine Aktivierungsverzögerung — typischerweise 15–30 Minuten, während Datenverkehr umgeleitet wird.

### Wann ISP-Scrubbing sinnvoll ist

- Ihre primäre Bedrohung sind volumetrische Angriffe
- Ihr ISP-Link beträgt 10 Gbps oder weniger
- Sie haben regulatorische Anforderungen für DDoS-Schutz, können aber Hardware-Kosten nicht rechtfertigen
- Sie möchten eine kostengünstige Basis-Schutzschicht

---

## 2. On-Premise DDoS-Appliances

### Wie es funktioniert

Ein dediziertes Hardwaregerät (oder virtuelle Appliance) sitzt inline in Ihrem Netzwerk, upstream Ihrer Firewall:

```
Internet → [ISP-Router] → [DDoS-Appliance] → [NGFW] → Internes Netzwerk
```

Die Appliance analysiert den gesamten Datenverkehr in Echtzeit und verwirft Angriffspakete, bevor sie Ihre Firewall oder Server erreichen. Im Gegensatz zu softwarebasierten Lösungen verwenden zweckgebundene DDoS-Appliances **FPGA-Hardware** (Field Programmable Gate Array) für die Paketverarbeitung — was Line-Rate-Analyse bei 40–100 Gbps ermöglicht.

### Führende On-Premise-Lösungen

**NETSCOUT Arbor (Peakflow / Sightline / TMS)**
Die dominante Enterprise-Lösung, besonders im Banking- und Telekommunikationsbereich. Arbor gilt weithin als Industriestandard für On-Premise-DDoS-Schutz. Die Plattform kombiniert:
- **Sightline:** Datenverkehrsanalyse und Angriffserkennung mittels Flow-Daten (NetFlow, sFlow, IPFIX) und BGP
- **Threat Mitigation System (TMS):** Hardwarebasierte Scrubbing-Appliance, inline oder out-of-band deployt
- Integration mit Arbors globalem Bedrohungsintelligenznetzwerk (ATLAS)

**Radware DefensePro**
Stark im Finanzdienstleistungsbereich. Verhaltensbasierte Erkennung, die eine dynamische Basislinie des normalen Datenverkehrs erstellt und Anomalien erkennt — effektiv gegen Zero-Day-DDoS-Angriffe, die keinen bekannten Signaturen entsprechen.

**Fortinet FortiDDoS**
In das Fortinet-Ökosystem integriert. Geeignet für Organisationen, die bereits FortiGate-Firewalls betreiben und konsistentes Management wünschen.

**F5 BIG-IP AFM (Advanced Firewall Manager)**
Wie in der F5-Serie besprochen — AFM bietet DDoS-Mitigationsfähigkeiten als Teil der BIG-IP-Plattform. Am besten geeignet für Umgebungen, die bereits F5 für Application Delivery betreiben.

### Was On-Premise-Appliances schützen

- **Protokollangriffe:** SYN-Floods, fragmentierte Pakete, fehlerhafte Header — mit Hardware-Geschwindigkeit behandelt, bevor sie die Firewall erreichen
- **Anwendungsschichtangriffe:** Fortgeschrittene Appliances mit Verhaltensanalyse können HTTP-Floods, Slowloris und SSL-Erschöpfung erkennen und abmildern
- **Zero-Day-Verhaltensangriffe:** Raten- und verhaltensbasierte Erkennung identifiziert Angriffsmuster ohne bekannte Signaturen

### Was On-Premise nicht kann

**Volumetrische Angriffe, die Ihren ISP-Link übersteigen:** Eine On-Premise-Appliance in Ihrem Rechenzentrum kann nicht helfen, wenn 500 Gbps Angriffsdatenverkehr Ihre 10-Gbps-Internetverbindung füllt. Das ist die grundlegende Einschränkung.

Deshalb sind On-Premise-Appliances und ISP-Scrubbing **komplementär, nicht konkurrierend**.

---

## 3. Cloud-DDoS-Schutzdienste

### Wie es funktioniert

Cloud-DDoS-Schutz leitet Ihren gesamten Datenverkehr durch das global verteilte Netzwerk des Anbieters. Sauberer Datenverkehr wird an Ihre Ursprungsserver geliefert; Angriffsdatenverkehr wird am Edge verworfen:

```
Ohne Cloud-Schutz:
  Benutzer → Internet → Ihr Server

Mit Cloud-Schutz:
  Benutzer → [Cloudflare / Akamai / AWS Edge] → Ihr Server
                          │
                   Angriffsdatenverkehr am Netzwerk-Edge verworfen
```

### Führende Cloud-Lösungen

**Cloudflare**
Der bekannteste Cloud-DDoS-Anbieter. Cloudflare betreibt eines der weltweit größten Anycast-Netzwerke — 300+ PoPs global, mit einer Gesamtkapazität von über 230 Tbps. Kernfähigkeiten:
- Automatische DDoS-Mitigation ohne manuelle Eingriffe
- Schicht 3, 4 und 7 Schutz in einer einzigen Plattform
- WAF-Integration — Anwendungssicherheit und DDoS-Mitigation vom selben Anbieter
- Magic Transit für Infrastruktur-Level-Schutz (BGP-basiert, nicht nur HTTP)
- Unbegrenzte DDoS-Mitigation — keine GB-Gebühren während Angriffen

**AWS Shield**
- **Shield Standard:** Automatisch für alle AWS-Ressourcen enthalten. Schützt vor gängigen L3/L4-Angriffen.
- **Shield Advanced:** Bezahlte Stufe mit L7-Schutz, 24/7 DDoS Response Team-Zugang und Integration mit AWS WAF.
- Am besten geeignet für Organisationen mit erheblicher AWS-Infrastruktur.

**Akamai Prolexic**
Enterprise-fokussierte Cloud-Scrubbing-Plattform. Betreibt 20+ global verteilte Scrubbing-Center. Starke Erfolgsbilanz in Finanzdienstleistungen und Medien.

**Azure DDoS Protection**
Microsofts Angebot für Azure-gehostete Ressourcen. Am relevantesten für Organisationen, die erhebliche Workloads in Azure betreiben.

### Was Cloud-Schutz zusätzlich bedeutet

- **Latenz:** Gesamter Datenverkehr läuft durch das Netzwerk des Anbieters. Für die meisten Webanwendungen ist die durch Edge-PoPs hinzugefügte Latenz vernachlässigbar oder negativ. Für latenzempfindliche Anwendungen sorgfältig bewerten.
- **Datenschutz/Compliance:** Gesamter Datenverkehr, einschließlich SSL-entschlüsselter Inhalte, läuft durch die Infrastruktur des Anbieters. In regulierten Branchen sorgfältige Prüfung erforderlich.
- **DNS-Abhängigkeit:** DNS-basierter Cloud-Schutz kann umgangen werden, wenn Angreifer Ihre Ursprungs-IP entdecken. Ursprungs-IPs sorgfältig schützen — Zugang auf Firewall-Ebene auf IP-Bereiche des Cloud-Anbieters beschränken.

---

## Vergleich der drei Ansätze

| | ISP-Scrubbing | On-Premise-Appliance | Cloud-Dienst |
|---|---|---|---|
| Volumetrischer Schutz | ✅ | ❌ (durch Link begrenzt) | ✅✅ |
| Protokollangriff-Schutz | ✅ | ✅✅ | ✅ |
| Anwendungsschicht (L7) | ❌ | ✅ (fortgeschrittene Modelle) | ✅✅ |
| Aktivierungszeit | Minuten (On-Demand) | Sofort | Sofort |
| Datenverkehrssichtbarkeit | Begrenzt | Vollständig | Anbieterabhängig |
| Compliance / Datenresidenz | ✅ | ✅✅ | Prüfung erforderlich |
| CapEx | Niedrig | Hoch | Keine |
| OpEx | Mittel | Mittel | Mittel–Hoch |
| Skalierbarkeit | ISP-Kapazität | Feste Hardware | Nahezu unbegrenzt |

---

## Das hybride Modell: Wie ernsthafte Organisationen alle drei kombinieren

In Hochrisikoumgebungen — Banking, Zahlungsabwickler, Regierungsinfrastruktur, großer E-Commerce — reicht eine einzelne Schutzschicht nie aus. Die Standardarchitektur kombiniert alle drei:

```
Angriffsdatenverkehr
      │
      ▼
[Cloud / ISP-Scrubbing]      ← Absorbiert volumetrische Fluten bevor sie Sie erreichen
      │
  Gereinigter Datenverkehr
      │
      ▼
[On-Premise-Appliance]       ← Fängt Protokollangriffe und L7-Anomalien ab
      │
      ▼
[NGFW + WAF]                 ← Anwendungssicherheit und Richtliniendurchsetzung
      │
      ▼
[Anwendungsserver]
```

Jede Schicht behandelt, was die anderen nicht können. Die Kombination schafft Defense-in-Depth, das gegen das gesamte Spektrum der DDoS-Angriffstypen widerstandsfähig ist.

### Praxisbeispiel: Bankensektor

In der Banking-Umgebung, in der ich gearbeitet habe, sah der DDoS-Schutz-Stack so aus:

- **Arbor TMS** On-Premise — Inline-Scrubbing für Protokollangriffe, Echtzeit-Flow-Analyse für Anomalieerkennung, BGP-Integration für automatisierte Datenverkehrsumleitung
- **ISP-Scrubbing-Vertrag** — aktiviert, wenn Arbor volumetrische Angriffssignaturen erkannte, die den Uplink sättigen würden
- **Cloudflare Magic Transit** — für öffentlich zugängliche Webanwendungen, mit Always-On-Cloud-Level-Schutz und WAF-Integration
- **F5 AFM** — zusätzlicher L4-Schutz auf der Application-Delivery-Ebene

Das war keine Redundanz um ihrer selbst willen — jede Schicht behandelte Angriffstypen, die die anderen nicht konnten.

---

## DDoS-Reaktionsplanung: Der nicht-technische Teil

Technologie ist nur ein Teil der DDoS-Bereitschaft. Der andere Teil ist organisatorisch:

**Runbooks:** Dokumentieren Sie genau, was zu tun ist, wenn ein Angriff beginnt. Wer wird benachrichtigt? Wer aktiviert ISP-Scrubbing? Was ist der Eskalationspfad? Unter einem Angriff ist der falsche Zeitpunkt, das herauszufinden.

**Kontaktlisten:** ISP-Scrubbing-Aktivierung, Cloud-Anbieter-Support, Upstream-Router-Zugang, Netzwerkingenieure im Bereitschaftsdienst. Alle aktuell, alle getestet.

**Schwellenwerte und Automatisierung:** Definieren Sie, wann automatisierte Mitigation aktiviert wird gegenüber wann menschliche Überprüfung erforderlich ist. Vollständig manuelle Reaktionen sind für moderne Angriffsraten zu langsam.

**Regelmäßiges Testen:** Ein DDoS-Schutz-Stack, der nie getestet wurde, ist ein DDoS-Schutz-Stack, dem Sie nicht wirklich vertrauen. Planen Sie periodische Tests mit Ihrem ISP und Cloud-Anbieter.

**Post-Incident-Review:** Überprüfen Sie nach jedem bedeutenden Angriff, was funktioniert hat, was nicht, und wie der Angriffsdatenverkehr aussah. DDoS-Taktiken entwickeln sich — Ihre Schutzstrategie sollte das auch tun.

---

## Wichtigste Erkenntnisse

- DDoS-Angriffe kommen in drei grundlegend verschiedenen Typen — volumetrisch, Protokoll und Anwendungsschicht — und jeder erfordert unterschiedliche Mitigation.
- **Keine einzelne Schutzschicht deckt alle Angriffstypen ab.** Volumetrische Angriffe erfordern Upstream-Scrubbing-Kapazität; Protokollangriffe benötigen hardwaregeschwindige Paketverarbeitung; L7-Angriffe erfordern anwendungsbewusste Analyse.
- **ISP-Scrubbing** ist die einzige Option für sehr große volumetrische Angriffe — der Angriff muss absorbiert werden, bevor er Ihren Link erreicht.
- **On-Premise-Appliances** (Arbor, Radware, F5 AFM) bieten granulare Sichtbarkeit, compliance-freundliche On-Site-Verarbeitung und effektiven Protokoll/L7-Schutz — können aber keine Angriffe handhaben, die Ihre ISP-Link-Kapazität übersteigen.
- **Cloud-Dienste** (Cloudflare, AWS Shield, Akamai) bieten massive Skalierung, globale Verteilung und Always-On-Schutz ohne Hardwareinvestition — leiten aber Datenverkehr durch Drittanbieter-Infrastruktur.
- In Hochrisikoumgebungen arbeiten alle drei Schichten zusammen. Das ist kein Over-Engineering — es ist die Architektur, die ernsthafte Organisationen in der Praxis verwenden.

---

## Verwandte Artikel

- 🛡️ [F5 BIG-IP Plattformübersicht](/de/technology/f5-bigip-application-delivery-platform-overview/) — F5 AFM als Teil der DDoS-Defense-in-Depth
- 🔐 [Die Zero-Trust-Mentalität: Sicherheit als Architektur entwickeln](/de/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — DDoS-Schutz im Zero-Trust-Framework
- 🛡️ [Network Packet Broker (NPB) Masterclass](/de/posts/network-packet-broker-masterclass/) — Datenverkehrssichtbarkeit für DDoS-Forensik
- 📊 [Monitoring richtig gemacht](/de/architecture/monitoring-not-just-seeing/) — DDoS früh durch proaktives Monitoring erkennen