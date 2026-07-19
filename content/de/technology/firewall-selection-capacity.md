---
title: "Firewall-Auswahl und Kapazitätsplanung: Was die Datenblätter Ihnen nicht sagen"
description: "Enterprise-Firewall-Auswahl — realer Durchsatz, SSL-Inspection, Stärken und Kompromisse bei Fortinet, Palo Alto, Cisco und Check Point."
date: 2026-04-06
draft: false

cover:
  image: "/img/postimages/firewall-selection-capacity-cover.webp"
  alt: "Enterprise Firewall-Auswahl und Kapazitätsplanung"
  relative: false

tags: ["Firewall", "NGFW", "Fortinet", "Palo Alto", "Cisco Firepower", "Check Point", "Netzwerksicherheit", "Kapazitätsplanung", "SSL-Inspection"]
categories: ["Technologie"]
keywords:
  - Enterprise Firewall Auswahlguide
  - Firewall Kapazitätsplanung
  - Fortinet vs Palo Alto vs Cisco vs Check Point
  - NGFW SSL Inspection Durchsatz
  - Firewall Durchsatz Real World
  - Enterprise Firewall Vergleich
  - Palo Alto App-ID Architektur
  - Fortinet FortiGate hoher Durchsatz
  - Cisco Firepower IPS
  - Check Point Firewall Verwaltung

showToc: true
TocOpen: true
---

# Firewall-Auswahl und Kapazitätsplanung: Was die Datenblätter Ihnen nicht sagen

Gespräche über Firewall-Auswahl verlaufen meist auf eine von zwei Arten. Entweder wird die Entscheidung auf Basis von Markenvertrautheit getroffen — „wir haben immer Anbieter X verwendet" — oder sie basiert auf Durchsatzzahlen aus Datenblättern, ohne zu verstehen, was diese Zahlen in der Produktion wirklich bedeuten. Beide Ansätze führen entweder dazu, für Kapazität zu viel zu bezahlen, die man nicht nutzen wird, oder zu einer Unterdimensionierung für den tatsächlichen Datenverkehr.

Nach dem Deployment von Hunderten von Fortinet-Firewalls in Banking- und Fertigungsumgebungen und umfangreicher Arbeit mit Palo Alto und Cisco in Produktionsinfrastruktur möchte ich zeigen, wie der Auswahlprozess tatsächlich aussieht, wenn man für das Ergebnis verantwortlich ist — nicht nur für die Empfehlung.

Den architektonischen Kontext hinter Firewall-Platzierungsentscheidungen finden Sie unter: [Switch, Firewall, AP — Warum die Auswahl der richtigen Produkte nicht ausreicht](/de/architecture/core-network-is-not-a-product-list/)

---

## Die Zahl, die alle irreführt: Firewall-Durchsatz

Jedes Firewall-Datenblatt beginnt mit einer Durchsatzzahl. 10 Gbps. 40 Gbps. 100 Gbps. Diese Zahlen sind real — unter den spezifischen Bedingungen, unter denen sie gemessen wurden.

Diese Bedingungen sind nicht Ihre Produktionsumgebung.

Datenblatt-Durchsatz wird typischerweise gemessen mit:
- Großen Paketgrößen (1518 Bytes) — realer Datenverkehr enthält viel kleinere Pakete
- Keine Sicherheitsfunktionen aktiviert — kein IPS, keine Anwendungskontrolle, keine SSL-Inspection
- Synthetischem Testdatenverkehr — nicht der gemischte, stoßartige, unregelmäßige Datenverkehr eines echten Netzwerks

Was tatsächlich Firewall-Kapazität in der Produktion verbraucht:

**PPS (Pakete pro Sekunde):** Kleine Pakete sind teurer als große Pakete. Eine Firewall, die 1 Gbps aus 64-Byte-Paketen bewegt, verarbeitet etwa 20× mehr Pakete pro Sekunde als 1 Gbps aus 1500-Byte-Paketen. Umgebungen mit hohen Transaktionsraten (Banking, Handel, Datenbankreplikation) belasten PPS-Grenzen lange vor Bandbreitengrenzen.

**Gleichzeitige Sitzungen:** Jede verfolgte Verbindung belegt Speicher in der Zustandstabelle. Eine Firewall mit 2 Millionen gleichzeitiger Sitzungskapazität bedeutet nicht „2 Millionen Benutzer" — ein einzelner Benutzer kann gleichzeitig Dutzende offener Sitzungen haben. Hochgradig gleichzeitige Umgebungen (Webserver hinter der Firewall, Datenbankcluster, Microservices-Architekturen) erschöpfen Sitzungstabellen schneller als Bandbreite.

**Neue Sitzungsrate:** Wie viele neue Verbindungen pro Sekunde die Firewall herstellen kann. Bei SYN-Flood-Bedingungen oder in Spitzenverkehrsperioden wird die neue Sitzungsrate zur bindenden Einschränkung.

**SSL/TLS-Inspection:** Hier geht die meiste Kapazitätsplanung schief. Wenn SSL-Inspection aktiviert ist — HTTPS-Datenverkehr entschlüsseln, inspizieren, neu verschlüsseln — fällt der Durchsatz auf den meisten Plattformen erheblich. Das Ausmaß der Auswirkungen variiert je nach Anbieter und Modell.

---

## Die SSL-Inspection-Realität

Der Großteil des Enterprise-Datenverkehrs ist heute HTTPS. Wenn Ihre Firewall SSL nicht inspiziert, inspiziert sie den Großteil Ihres Datenverkehrs nicht. Aber die Aktivierung der SSL-Inspection hat direkte, erhebliche Leistungskosten.

Eine Firewall, die mit 10 Gbps Durchsatz vermarktet wird, könnte bei aktivierter vollständiger SSL-Inspection je nach Plattform 2–4 Gbps liefern. Das ist kein Fehler oder Anbietermangel — SSL-Entschlüsselung ist rechenintensiv, und Hardware-SSL-Beschleunigung (bei höherwertigen Modellen verfügbar) ist das, was in der Praxis Einstiegs- von Mittelklasseplattformen unterscheidet.

**Die Berechnung, die zählt:**

Bei der Dimensionierung einer Firewall lautet die Frage nicht „wie viel Bandbreite habe ich?" sondern „wie viel dieser Bandbreite wird SSL-inspiziert?" Für die meisten Organisationen:
- Internetgebundener Datenverkehr: nahezu 100% HTTPS → alles SSL-inspiziert
- Interner Segmentierungsdatenverkehr: Mix aus verschlüsseltem und unverschlüsseltem Anwendungsdatenverkehr
- Server-zu-Server-Datenverkehr: zunehmend TLS aus Compliance-Gründen

Wenn Sie 2 Gbps Internetbandbreite haben und planen, alles zu inspizieren, dimensionieren Sie die Firewall für 2 Gbps SSL-Inspection-Durchsatz — nicht für 2 Gbps Rohdurchsatz. Das sind oft sehr unterschiedliche Zahlen.

---

## Multi-Firewall-Architektur: Eine Größe passt nicht allen

In vielen Produktionsumgebungen ist eine einzelne Firewall, die alle Rollen übernimmt, ein Design-Kompromiss statt einer Design-Wahl. Verschiedene Datenverkehrstypen haben unterschiedliche Anforderungen:

```
Internet Edge Firewall:
  → Hoher SSL-Inspection-Durchsatz (der meiste Datenverkehr ist HTTPS)
  → VPN-Terminierungskapazität
  → IPS für aus dem Internet stammende Bedrohungen
  → Moderate Sitzungsanzahl

Interne Segmentierungs-Firewall (Ost-West):
  → Hohe PPS (interner Datenverkehr besteht oft aus kleinen Paketen)
  → Sehr hohe gleichzeitige Sitzungsanzahl
  → Geringere SSL-Inspection-Anforderungen (interner Datenverkehr oft unverschlüsselt)
  → Hohe neue Sitzungsrate

Rechenzentrum / Server-Firewall:
  → Extreme Sitzungsanzahlen (Server haben viele gleichzeitige Verbindungen)
  → Geringe Latenz (anwendungsleistungsempfindlich)
  → Hoher Durchsatz für Massendatenübertragungen
  → IPS abgestimmt auf serverseitige Exploits
```

Dasselbe Firewall-Modell für alle drei Rollen zu verwenden bedeutet, bei mindestens einer Kompromisse einzugehen. Die für SSL-Inspection optimierte Internet-Edge-Firewall ist oft falsch für Ost-West-Segmentierung. Die hochsitzungsanzahl-DC-Firewall ist oft überentwickelt für eine Zweigstelle.

Das ist nicht theoretisch — ich habe Netzwerke gesehen, wo die Internet-Edge-Firewall bei 30% ihres Nenndurchsatzes sättigte, weil die Sitzungsanzahlgrenze erreicht wurde, während die DC-Firewall reichlich Durchsatz-Headroom hatte, aber aufgrund von PPS-Grenzen Pakete verlor.

---

## Anbieter-Praxisnotizen

Was folgt, basiert auf direkter Produktionserfahrung. Das sind operative Beobachtungen, keine Benchmark-Vergleiche. Anbieterfähigkeiten entwickeln sich mit Softwareversionen und neuen Hardwaregenerationen — validieren Sie aktuelle Spezifikationen für jedes aktive Projekt.

### Fortinet FortiGate

Fortinet ist dort, wo der Großteil meiner Produktions-Firewall-Erfahrung konzentriert ist — über kleine Zweigstellen-Deployments, Banking-Hauptsitze und große Fertigungsumgebungen.

**Wo FortiGate wirklich glänzt:**

Hochdurchsatzumgebungen mit moderaten Sicherheits-Inspection-Anforderungen. Fortinets benutzerdefinierte NP (Netzwerkprozessor)- und CP (Inhaltsprozessor)-ASICs lagern spezifische Funktionen auf Hardware aus — Paketverarbeitung, IPsec-VPN und einige Inspection-Aufgaben laufen auf dedizierten Siliziumchips statt auf Allzweck-CPUs. Bei hoher Bandbreite macht diese Hardware-Beschleunigung einen bedeutenden Unterschied.

Für Umgebungen, die große Datenverkehrsvolumina bewegen müssen — Server-zu-Server, große Dateiübertragungen, Hochbandbreiten-Zweigstellenkonnektivität — liefert FortiGate Durchsatz, mit dem softwarebasierte Architekturen zu gleichwertigen Preispunkten nicht mithalten können.

Das Fortinet Security Fabric ist ein echter operativer Vorteil für Organisationen, die FortiGate neben FortiSwitch, FortiAP, FortiAnalyzer und FortiManager betreiben. Richtlinien, Protokollierung und Verwaltung sind auf eine Weise vereinheitlicht, die die Integrationsarbeit reduziert, die Multi-Vendor-Umgebungen erfordern.

**Wo FortiGate Einschränkungen hat:**

Tiefe Inspection im großen Maßstab. Wenn IPS, Anwendungskontrolle, SSL-Inspection und Antivirus gleichzeitig auf stark frequentierten Links aktiviert sind, kann der Durchsatz erheblich unter die Titelzahlen fallen. Fortinet veröffentlicht „Bedrohungsschutz"-Durchsatzzahlen, die dies widerspiegeln — aber diese Zahlen sind im Vergleich zu dem, was Sie mit Ihrem spezifischen Datenverkehrsmix und vollständiger Funktionsaktivierung sehen werden, immer noch oft optimistisch.

**Hardware-Generationsupdate (2024–2025):** Fortinets neuere Appliance-Serien haben die SSL-Inspection-Kapazität erheblich verbessert. Die im Jahr 2025 von Keysight validierte FortiGate 700G-Serie erreicht bis zu 14 Gbps SSL-Deep-Inspection-Durchsatz — eine bedeutende Verbesserung gegenüber äquivalenten Mittelklassemodellen früherer Generationen. Verwenden Sie beim Dimensionieren immer die Datenblatt-Zahlen für das spezifische Modell und die Generation, die Sie bewerten.

**Praktische Anleitung:** Bei der Dimensionierung von FortiGate für vollständige SSL-Inspection-Deployments verwende ich 20–30% der SSL-Inspection-Durchsatzzahl aus dem Datenblatt als meine Arbeitsschätzung für Produktionsdatenverkehr. Das klingt konservativ, berücksichtigt aber Datenverkehrsmix, gleichzeitige Verbindungen und Protokollierungsaufwand. Wenn die Rechnung bei dieser Zahl aufgeht, haben Sie ausreichend Headroom.

---

### Palo Alto Networks

Palo Altos Architektur unterscheidet sich grundlegend von traditionellen Firewalls, und das Verstehen dieser Unterschiede ist sowohl für die Wertschätzung der Stärken als auch für die Planung der Einschränkungen wesentlich.

**Die App-ID-Architektur:**

Palo Alto identifiziert Datenverkehr nach Anwendung, bevor entschieden wird, was damit zu tun ist. Jede Sitzung wird analysiert, um zu bestimmen, welche Anwendung sie darstellt — nicht nur, welchen Port sie verwendet. HTTP auf Port 80, Port 8080 oder einem benutzerdefinierten Port wird alles als die spezifische Anwendung identifiziert, die darauf läuft.

Das ist architektonisch mächtig für die Sicherheit: die Richtlinie basiert auf „Salesforce vom Vertriebsteam erlauben" statt „TCP 443 aus Subnetz X erlauben". Unbekannte Anwendungen — Datenverkehr, der keiner bekannten Anwendungssignatur entspricht — werden standardmäßig als potenziell verdächtig behandelt.

**Der Sicherheitsvorteil, den das schafft:**

In Umgebungen, in denen das Bedrohungsmodell vollständige Anwendungssichtbarkeit erfordert — Finanzdienstleistungen, regulierte Branchen, Umgebungen mit strengen Compliance-Anforderungen — schafft Palo Altos Ansatz echte Sicherheitstiefe. Das Richtlinienmodell erzwingt explizite Entscheidungen über jeden Datenverkehrstyp. Nichts passiert ungeprüft.

**Der operative Kompromiss:**

Dieselbe Architektur, die Palo Alto in sicherheitsorientierten Umgebungen leistungsstark macht, erzeugt in anderen Reibung. Unbekannte oder ungewöhnliche Anwendungen erfordern Untersuchung und explizite Richtlinienentscheidungen. Für Organisationen ohne dedizierte Sicherheitsteams oder für Umgebungen mit vielfältigen, sich entwickelnden Anwendungssätzen kann der operative Aufwand der Pflege eines anwendungsbasierten Richtlinienmodells erheblich sein.

**Panorama:**

Die zentralisierte Verwaltung von Palo Alto Firewalls über Panorama ist wesentlich leistungsfähiger als die Verwaltung einzelner Geräte. Für Multi-Firewall-Umgebungen ist Panorama faktisch erforderlich, um Palo Alto im Großmaßstab zu betreiben.

**SASE-Führerschaft (Update 2025):** Palo Altos Cloud-Sicherheitsplattform (Prisma SASE) ist zu einem ihrer stärksten Wachstumsbereiche geworden — drei aufeinanderfolgende Jahre bis 2025 als Gartner SASE Leader benannt, mit 1,3 Milliarden Dollar ARR bei 35% Jahreswachstum. Wenn Ihre Organisation eine breitere Sicherheitsplattform statt nur einer Perimeter-Firewall evaluiert, ist dies relevant.

---

### Cisco Firepower (Jetzt Cisco Secure Firewall)

Ciscos NGFW-Geschichte hat eine Geschichte, die es wert ist, verstanden zu werden. Die ursprüngliche ASA (Adaptive Security Appliance) war eine starke Stateful-Firewall — zuverlässig, weit verbreitet deployt, aber in Next-Generation-Fähigkeiten begrenzt. Ciscos Antwort war der Kauf von Sourcefire, dessen IPS-Technologie (Snort-basiert) wirklich stark war und bleibt, und der Aufbau der Firepower-Plattform auf der ASA-Architektur.

**Wo Firepower stark ist:**

Die IPS-Fähigkeit ist real. Sourcefires Bedrohungsintelligenz und -erkennung, jetzt Cisco Talos (eine der größten Bedrohungsintelligenzorganisationen der Welt), treibt Firepowers IPS mit einer Erkennungsqualität an, die allgemein respektiert wird.

Die Integration mit Ciscos breiterem Ökosystem — ISE, Umbrella, Stealthwatch (jetzt Secure Network Analytics), SecureX — ist zunehmend kohärent.

**Die Verwaltungsherausforderung:**

Cisco Firepower wurde historisch für Verwaltungskomplexität kritisiert. Firepower ohne Firepower Management Center (FMC) zu betreiben bedeutet, erhebliche Einschränkungen bei Sichtbarkeit und Richtlinienverwaltung zu akzeptieren.

Die Plattform hat sich erheblich weiterentwickelt, und Cisco hat stark in die Verbesserung der Verwaltungserfahrung investiert. Im Jahr 2024 benannte Cisco den Cisco Defense Orchestrator als **Security Cloud Control** um — eine KI-eingebettete Cloud-Verwaltungsplattform, die FMC, ASA und andere Cisco-Sicherheitsprodukte unter einer Oberfläche vereint. Es enthält jetzt einen KI-Assistenten für die Erstellung von Richtlinienregeln, AIOps-Einblicke für proaktive Empfehlungen und Cloud-geliefertes FMC, das den On-Premise-Infrastrukturaufwand reduziert. Teams, die von einfacheren Firewall-Plattformen kommen, werden immer noch eine Anpassungszeit haben, aber die Lücke hat sich im Vergleich zu vor einigen Jahren verringert.

**Architektonischer Kontext:**

Cisco ist am stärksten in Umgebungen, die bereits tief in das Cisco-Ökosystem investiert sind — wo ISE Identität, Catalyst Switching und DNA Center / Catalyst Center zentralisierte Verwaltung bereitstellt.

---

### Check Point

Check Point ist einer der ursprünglichen Enterprise-Firewall-Anbieter — das Unternehmen, das in den 1990er Jahren Firewall-Technologie zum Mainstream machte. Ihre Architektur spiegelt dieses Erbe wider: ausgereift, sicherheitsorientiert und um ein Betriebssystem (Gaia, basierend auf Linux) aufgebaut, das Administratoren erhebliche Kontrolle gibt, aber entsprechende Expertise erfordert.

**Wo Check Point stark ist:**

Tiefe Sicherheitsrichtlinien und Inspektionsqualität. Check Points Richtlinienmodell ist granular, und ihre Inspektionsfähigkeiten sind ausgereift. In Umgebungen, wo die Komplexität der Sicherheitsrichtlinien hoch ist — viele Regeln, viele Ausnahmen, detaillierte Protokollierungsanforderungen — verwaltet Check Points Verwaltungsinfrastruktur die Skalierung gut.

**Die operative Realität:**

Check Points Verwaltungsmodell unterscheidet sich von anderen Anbietern. Verwaltung ist von Durchsetzung getrennt — der Verwaltungsserver, der Security Management Server (SMS), ist von den Durchsetzungs-Gateways getrennt. Das Verstehen und Arbeiten mit dieser Trennung, dem Richtlinieninstallationsprozess und dem zugrunde liegenden Gaia-OS erfordert echte Expertise.

Aus der Perspektive eines Netzwerkingenieurs ist Check Point nicht die betrieblich transparenteste Plattform. Vertrautheit mit Linux-Administration hilft erheblich. Richtlinienverwaltung ohne ein solides Verständnis des Objektmodells und der Regelbasenstruktur führt zu Komplexität, die sich im Laufe der Zeit anhäuft.

---

## HA-Architektur: Aktiv-Standby vs. Aktiv-Aktiv

Enterprise-Firewall-Deployments erfordern Hochverfügbarkeit. Die zwei Modelle haben unterschiedliche Eigenschaften:

**Aktiv-Standby:**
- Eine Firewall verarbeitet den gesamten Datenverkehr; der Standby überwacht und übernimmt bei Ausfall
- Sitzungszustand wird zum Standby synchronisiert — Failover ist für bestehende Verbindungen transparent
- Einfacher zu fehlersuchen — zu jedem Zeitpunkt gesamter Datenverkehr durch ein Gerät
- Verschwendet 50% der Hardwarekapazität im Normalbetrieb
- Standardwahl für die meisten Enterprise-Edge-Deployments

**Aktiv-Aktiv:**
- Beide Firewalls verarbeiten gleichzeitig Datenverkehr, typischerweise für verschiedene Datenverkehrsflüsse oder Zonen
- Komplexer zu konfigurieren und zu fehlersuchen — asymmetrisches Routing muss vermieden werden
- Nutzt beide Geräte, kompliziert aber die Zustandssynchronisierung
- Besser geeignet für sehr hohe Durchsatzanforderungen, wo ein Gerät nicht ausreicht
- Erfordert sorgfältiges Traffic Engineering — asymmetrische Flüsse (Anfrage durch FW-1, Antwort durch FW-2) verursachen Sitzungsabbrüche

In der Praxis ist Aktiv-Standby die richtige Wahl für die Mehrheit der Enterprise-Deployments. Der Durchsatzvorteil von Aktiv-Aktiv rechtfertigt die operative Komplexität nicht, es sei denn, Sie benötigen wirklich mehr Durchsatz als ein Gerät mit berücksichtigtem HA-Overhead bereitstellen kann.

---

## Policy-Hygiene: Das Problem, das sich langsam aufbaut

Firewall-Kapazität ist nicht nur eine Hardware-Frage. Die Firewall-Leistung verschlechtert sich, wenn die Regelbasenkomplexität zunimmt — besonders wenn Regelbasen ohne regelmäßige Bereinigung wachsen.

Eine Regelbasis mit 5.000 Regeln, bei der der meiste Datenverkehr in den ersten 50 Regeln übereinstimmt, funktioniert sehr unterschiedlich von einer 5.000-Regel-Basis, bei der der Datenverkehr über Hunderte von Regeln verteilt ist. Jedes Paket durchläuft die Regelbasis von oben nach unten, bis es übereinstimmt — oder das implizite Ablehnen erreicht.

**Was Policy-Hygiene in der Praxis bedeutet:**

- Regeln, die nie übereinstimmen (Schattenregeln, veraltete Regeln), sollten vierteljährlich identifiziert und entfernt werden
- Stark frequentierte Regeln sollten oben in der Regelbasis positioniert werden
- Übermäßig breite Regeln (Beliebig/Beliebig-Genehmigungen mit deaktivierter Protokollierung) sollten dokumentiert und überprüft werden
- Anwendungsspezifische Regeln sollten portbasierte Regeln ersetzen, wo die Plattform dies unterstützt

FortiManager, Panorama und FMC haben alle Regelnutzungsstatistiken und Schattenregelerkennung. Diese Tools zu verwenden ist Teil des verantwortungsvollen Firewall-Betriebs — keine periodische Bereinigungsübung.

---

## Kapazitätsplanung: Der praktische Rahmen

Bei der Dimensionierung einer Firewall arbeiten Sie diese Metriken der Reihe nach durch:

**1. Grundlegende Datenverkehrscharakterisierung**
- Was ist die aktuelle Spitzenbandbreite (nicht Durchschnitt)?
- Welcher Prozentsatz ist SSL/HTTPS?
- Wie hoch ist die gleichzeitige Sitzungsanzahl bei Spitzenlast?
- Wie hoch ist die neue Sitzungsrate bei Spitzenlast?

**2. Wachstumsprojektion**
- 40–50% Headroom über erwartetem Spitzenbedarf für 3-jährigen Lebenszyklus hinzufügen
- Neue Anwendungen und Dienste berücksichtigen, die hinzugefügt werden

**3. Funktionsauswirkung**
- Welche Sicherheitsfunktionen werden aktiviert? (IPS, SSL-Inspection, App-ID, AV)
- Anbieter-„Bedrohungsschutz"-Durchsatzzahlen verwenden, nicht Rohdurchsatz
- Für SSL-Inspection spezifisch: mit Anbieter-Dimensionierungstools mit geschätztem HTTPS-Prozentsatz validieren

**4. HA-Overhead**
- Aktiv-Standby: jede Einheit für 100% des Datenverkehrs dimensionieren (Standby muss volle Last bewältigen können)
- Planen Sie nicht, Standby-Kapazität zu nutzen — sie muss für Failover verfügbar sein

**5. Verwaltung und Protokollierung**
- Hohe Protokollierungsraten verbrauchen CPU der Firewall selbst
- Externe Protokollverwaltung (FortiAnalyzer, Panorama, FMC) ist bei Skalierung nicht optional

Ein einfaches Dimensionierungsbeispiel:
```
Umgebung:
  Spitzenbandbreite: 2 Gbps
  SSL-Prozentsatz: 80% (1,6 Gbps HTTPS)
  IPS + App-ID + SSL-Inspection: alle aktiviert
  3-jähriger Wachstums-Headroom: 50%

Erforderlicher SSL-Inspection-Durchsatz:
  1,6 Gbps × 1,5 (Wachstum) = 2,4 Gbps

Modell auswählen, das für ≥ 2,4 Gbps SSL-Inspection-Durchsatz bewertet ist
(nicht 2,4 Gbps Rohdurchsatz)
```

---

## Wichtigste Erkenntnisse

- **Datenblatt-Durchsatz ist nicht Produktions-Durchsatz.** SSL-Inspection, IPS und Anwendungskontrolle reduzieren den effektiven Durchsatz erheblich. Dimensionieren Sie basierend auf Bedrohungsschutz- oder SSL-Inspection-Zahlen, nicht auf Rohzahlen.
- **SSL-Inspection-Kapazität ist die bindende Einschränkung** für die meisten Internet-Edge-Deployments. Der Großteil des Datenverkehrs ist HTTPS, und dessen Inspektion ist kostspielig.
- **Fortinet** glänzt in Hochdurchsatzumgebungen, wo Hardware-Beschleunigung wichtig ist. Vollständige Tiefeninspektion im Maßstab erfordert sorgfältige Modellauswahl — der Durchsatz fällt mit allen aktivierten Funktionen erheblich.
- **Palo Alto** bietet die tiefste Anwendungssichtbarkeit und das rigoroseste Richtlinienmodell. Die Architektur ist mächtig für sicherheitsreife Organisationen; sie fügt operativen Overhead für solche ohne dedizierte Sicherheitsteams hinzu. Panorama ist faktisch für die Verwaltung mehrerer Geräte erforderlich.
- **Cisco Firepower** bringt starkes IPS (Talos-Intelligenz) und Cisco-Ökosystem-Integration. Verwaltungskomplexität ist real — FMC ist erforderlich, um den Wert der Plattform zu realisieren.
- **Check Point** ist ausgereift und sicherheitsorientiert mit tiefer Richtlinienkontrolle. Erfordert Linux/Gaia-OS-Vertrautheit und diszipliniertes Regelbasenverwaltung für effektiven Betrieb.
- **Multi-Firewall-Architektur** — verschiedene Firewalls für Edge, interne Segmentierung und DC — ist oft die richtige Antwort statt einer Plattform für alles.
- **Regel-Hygiene** ist ein Leistungs- und Sicherheitsproblem, keine bloße Haushaltsführung. Vernachlässigte Regelbasen verschlechtern beides.

---

## Verwandte Artikel

- 🏗️ [Switch, Firewall, AP — Warum die Auswahl der richtigen Produkte nicht ausreicht](/de/architecture/core-network-is-not-a-product-list/) — Architektonischer Kontext für Firewall-Platzierung
- 🔐 [Die Zero-Trust-Mentalität: Sicherheit als Architektur entwickeln](/de/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — Richtlinienphilosophie hinter Firewall-Design
- 🛡️ [DDoS-Schutzstrategien](/de/technology/ddos-schutzstrategien-isp-scrubbing-on-premise-cloud/) — Was upstream der Firewall sitzt
- 🛡️ [F5 WAF Deep Dive](/de/technology/f5-waf-asm-advanced-waf-anwendungssicherheit/) — Layer-7-Schutz, der Firewall-Richtlinien ergänzt
- 📊 [Monitoring richtig gemacht](/de/architecture/monitoring-not-just-seeing/) — Firewall-Verhalten sichtbar machen