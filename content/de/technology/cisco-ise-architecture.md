---
title: "Cisco ISE: Architektur, Lizenzierung und wann es sinnvoll ist"
description: "Cisco ISE Architekturleitfaden — Deployment-Modelle, Node-Rollen, Lizenzstufen, pxGrid-Integrationen und wann ISE die richtige Wahl ist."
date: 2026-04-20
draft: false

cover:
  image: "/img/postimages/cisco-ise-architecture-cover.webp"
  alt: "Cisco ISE Architektur und Lizenzierungsleitfaden"
  relative: false

tags: ["Cisco ISE", "NAC", "802.1X", "TACACS", "Netzwerksicherheit", "Zero Trust", "Identität", "pxGrid"]
categories: ["Architektur"]
keywords:
  - Cisco ISE Architektur
  - ISE Lizenzstufen
  - ISE vs NPS vs ClearPass
  - Cisco ISE Deployment-Modelle
  - ISE pxGrid Integration
  - ISE TACACS Geräteverwaltung
  - ISE Endpoint-Lizenzierung
  - ISE DNA Center Integration
  - Cisco ISE Base Plus Apex
  - Enterprise Netzwerkzugangskontrolle

showToc: true
TocOpen: false
---

# Cisco ISE: Architektur, Lizenzierung und wann es sinnvoll ist

Die Cisco Identity Services Engine (ISE) ist das Policy-Gehirn hinter der Enterprise-Netzwerkzugangskontrolle. Es ist die Plattform, die für jedes Gerät, das versucht, sich mit dem Netzwerk zu verbinden, folgende Frage beantwortet: *Wer bist du, was bist du, bist du gesund und was darfst du tun?*

Wenn Sie den [802.1X-Feldleitfaden](/de/technology/identity-based-microsegmentation-8021x/) gelesen haben, haben Sie ISE bereits in Aktion gesehen: den RADIUS-Server, der dynamische VLAN-Zuweisungen zurückgibt, die NAC-Plattform, die Geräte profiliert, die Policy-Engine, die Posture-Compliance erzwingt. Dieser Artikel tritt einen Schritt zurück von den Protokolldetails und betrachtet ISE als Architektur- und Investitionsentscheidung — wie es strukturiert ist, wie es lizenziert wird und wann es das richtige Werkzeug ist.

---

## Was ISE tut — in einem Absatz

ISE ist eine zentrale Policy-Plattform. Geräte und Benutzer, die sich mit dem Netzwerk verbinden — kabelgebunden, kabellos oder über VPN — authentifizieren sich über ISE. ISE prüft ihre Identität gegen Active Directory, bewertet Gerätetyp und Compliance-Posture und gibt eine Zugriffsentscheidung an das Netzwerkgerät zurück: vollständigen Zugriff gewähren, in Quarantäne-VLAN versetzen, zu einem Remediation-Portal weiterleiten oder vollständig ablehnen. Diese Entscheidung kann VLAN-Zuweisung, herunterladbare ACLs und Security Group Tags (SGTs) umfassen, die den Benutzer durch das Netzwerk verfolgen.

Eine Plattform übernimmt, was früher mehrere separate Tools erforderte: RADIUS-Server, NAC-Appliance, Gästeportal, Geräte-Profiler, Posture-Engine.

---

## Deployment-Architektur

### Node-Rollen

ISE ist keine einzelne monolithische Anwendung. Es trennt seine Funktionen in unterschiedliche Node-Rollen:

**PAN — Policy Administration Node:** Die Verwaltungsschnittstelle. Alle Konfigurationen erfolgen hier. In einem verteilten Deployment gibt es einen aktiven PAN und einen Standby.

**PSN — Policy Service Node:** Die Laufzeit-Enforcement-Engine. Hier kommunizieren Netzwerkgeräte — RADIUS-Anfragen, TACACS-Anfragen, Gästeportal-Weiterleitungen, Posture-Checks. In großen Umgebungen verteilen mehrere PSNs die Authentifizierungslast.

**MnT — Monitoring and Troubleshooting Node:** Sammelt Logs von PSNs und stellt das Betriebsdashboard bereit — Authentifizierungsberichte, fehlgeschlagene Versuche, aktive Sitzungen, Alarme. Von den Policy-Nodes getrennt, damit die Logging-Last die Authentifizierungsleistung nicht beeinträchtigt.

**pxGrid Controller:** Der Integrationsbus. Mehr dazu weiter unten.

### Deployment-Modelle

**Standalone (einzelner Node):** Alle Rollen auf einer VM oder Appliance. Geeignet für Lab, PoC oder sehr kleine Deployments. Kein HA. Fällt der Node aus, stoppt die Authentifizierung. Nicht geeignet für Produktionsumgebungen, in denen der Netzwerkzugriff von ISE abhängt.

**Klein verteilt (2 Nodes):** Ein Node als PAN+MnT, einer als PSN. Grundlegende Redundanz. Geeignet für mittelgroße Umgebungen mit moderater Authentifizierungslast.

**Vollständig verteilt mit HA:** Dedizierte Nodes für jede Rolle, PAN in Aktiv/Standby, mehrere PSNs für Lastverteilung und geografische Redundanz. Dies ist das, was große Enterprise- und regulierte Umgebungen benötigen. Es erfordert auch deutlich mehr Infrastruktur — planen Sie mindestens 4–6 VMs für ein ordnungsgemäß redundantes Deployment.

Die praktische Konsequenz: ISE ist kein „auf einer freien VM deployen"-Projekt. Ein produktionstaugliches verteiltes Deployment erfordert dedizierte Infrastruktur, angemessene Dimensionierung und fortlaufende betriebliche Aufmerksamkeit.

---

## Lizenzierung: Die Stufenstruktur

Die ISE-Lizenzierung hat sich im Laufe der Jahre weiterentwickelt. Das aktuelle Modell verwendet drei Stufen, die als jährliche Abonnements pro Endpoint verkauft werden:

### Essentials (früher Base)

Die Einstiegsstufe. Deckt den grundlegenden 802.1X-Anwendungsfall ab:
- RADIUS-Authentifizierung (802.1X kabelgebunden und kabellos)
- Grundlegender Gastzugang
- MAB (MAC Authentication Bypass)
- Grundlegende VLAN-Zuweisung

Dies ist ausreichend für Organisationen, die Port-Authentifizierung und grundlegenden Gastzugang benötigen, nicht mehr. NPS kann vieles davon kostenlos — der Mehrwert von Essentials gegenüber NPS liegt hauptsächlich in der Verwaltungsschnittstelle, Skalierbarkeit und Cisco-Ecosystem-Integration.

### Advantage (früher Plus)

Fügt die Funktionen hinzu, die ISE bedeutend leistungsfähiger als NPS machen:
- **Geräte-Profiling** — Identifizierung des Gerätetyps anhand von DHCP, CDP, LLDP, HTTP-Signaturen
- **Gast-Lebenszyklusmanagement** — Sponsor-Portale, Selbstregistrierung, zeitlich begrenzter Zugang
- **BYOD-Onboarding** — Zertifikatsbereitstellung für persönliche Geräte
- **TrustSec / Security Group Tags (SGT)** — Policy-Enforcement jenseits der VLAN-Zuweisung

Advantage ist die Stufe, bei der die meisten Enterprise-Deployments landen, wenn der Anwendungsfall über die grundlegende Port-Authentifizierung hinausgeht.

### Premier (früher Apex)

Fügt Posture-Bewertung und erweiterte Bedrohungsreaktion hinzu:
- **Posture** — Überprüfung des Gerätezustands vor der Zugriffsgewährung (AV-Status, OS-Patch-Level, Festplattenverschlüsselung, bestimmte Registry-Werte)
- **Threat-centric NAC** — Integration mit Bedrohungsintelligenznetzwerken, um die Zugriffsrichtlinie automatisch zu ändern, wenn ein Gerät als kompromittiert identifiziert wird
- **Passive Identity** — Sammlung von Identitätsinformationen aus AD-Ereignisprotokollen ohne 802.1X auf jedem Port

Premier eignet sich für hochsichere Umgebungen, in denen Compliance-Posture eine regulatorische Anforderung ist oder automatisierte Bedrohungsreaktion benötigt wird.

### Geräteverwaltung (TACACS+) — Separate Lizenz

Dies ist eine häufige Verwirrungsquelle: **TACACS+ für die Netzwerkgeräteverwaltung wird separat von den obigen Endpoint-Zugriffslizenzen lizenziert.**

Die Endpoint-Lizenzen (Essentials/Advantage/Premier) decken Benutzer und Geräte ab, die sich mit dem Netzwerk verbinden. Die Geräteverwaltung deckt Netzwerkingenieure ab, die sich in Switches, Router und Firewalls einloggen — Authentifizierung über TACACS+ mit ISE als AAA-Server, Befehlsautorisierung pro Benutzer oder Gruppe.

Wenn ISE sowohl die Endpoint-Zugangskontrolle als auch die Netzwerkgerät-Admin-Authentifizierung handhaben soll, benötigen Sie beide Lizenztypen. Viele Organisationen deployen ISE primär für den Endpoint-Zugang und verwenden weiterhin eine separate TACACS+-Lösung für die Geräteverwaltung.

---

## pxGrid: Die Integrationsplattform

pxGrid (Platform Exchange Grid) ist ISEs Integrationsframework — es ermöglicht externen Plattformen, ISE-Daten zu abonnieren und Ereignisse zurück an ISE zu veröffentlichen.

In der Praxis ermöglicht dies Szenarien wie:

**Firewall-Integration:** Wenn ISE einen Benutzer authentifiziert und ihm einen Security Group Tag zuweist, kann die Firewall (Palo Alto, Cisco Firepower) diese Zuordnung über pxGrid empfangen. Die Firewall-Policy kann dann gegen SGTs statt IP-Adressen geschrieben werden — „Finance-SGT den Zugriff auf Finance-Server erlauben" statt IP-basierte ACLs zu pflegen, die sich ändern, wenn Benutzer sich bewegen.

**SIEM-Integration:** Sicherheitsplattformen (Splunk, IBM QRadar) abonnieren ISE-Sitzungsdaten — wer sich authentifiziert hat, von wo, mit welchem Gerät, wann. Dies bereichert die Sicherheitsereigniskorrelation mit Identitätskontext, den rohe Netzwerklogs nicht transportieren.

**Bedrohungsreaktion:** Eine SIEM- oder EDR-Plattform erkennt ein kompromittiertes Gerät. Über pxGrid veröffentlicht sie ein Bedrohungsereignis an ISE. ISE ändert automatisch die Zugriffsrichtlinie des Geräts — Quarantäne-VLAN, Weiterleitung zum Remediation-Portal — ohne menschliches Eingreifen.

pxGrid verwandelt ISE von einem Netzwerkzugriffstool in eine Sicherheitsplattform, die Kontext über die gesamte Infrastruktur hinweg teilt. Dieser Integrationswert ist ein wesentlicher Teil der Rechtfertigung für ISE in ausgereiften Sicherheitsarchitekturen.

---

## ISE + DNA Center: Der integrierte Campus

Wenn ISE zusammen mit DNA Center (Catalyst Center) betrieben wird, ist die Integration nativ und tiefgreifend. DNA Center verwendet ISE als Policy-Engine für SD-Access Fabric-Deployments:

- DNA Center definiert die Netzwerkhierarchie und Fabric-Infrastruktur
- ISE definiert, wer auf was zugreifen darf (Security Group Policies)
- Wenn sich ein Benutzer authentifiziert, weist ISE seinen SGT zu
- DNA Center propagiert die SGT-basierte Policy automatisch durch das Fabric

Das Ergebnis: Eine Policy-Änderung in ISE — „Finance-Benutzer können jetzt auf den neuen Reporting-Server zugreifen" — wird automatisch über das gesamte Campus-Fabric reflektiert, ohne einzelne Switch-Konfigurationen anzufassen. Policy wird einmal definiert und überall durchgesetzt.

Diese Integration ist eines der stärksten Argumente für ISE in Umgebungen, die bereits DNA Center betreiben. Separat sind beide Plattformen leistungsfähig. Zusammen liefern sie das identitätsbewusste Netzwerk-Fabric, das keine der beiden allein bereitstellen kann.

---

## ISE vs. NPS vs. ClearPass: Wann welches verwenden

Dies ist die Entscheidung, die die meisten Organisationen treffen müssen, bevor sie sich auf ISE festlegen.

**Windows NPS (Network Policy Server)** ist kostenlos mit Windows Server. Er handhabt RADIUS-Authentifizierung, grundlegende VLAN-Zuweisung und 802.1X. Für Organisationen, die grundlegende Port-Authentifizierung gegen Active Directory benötigen, funktioniert NPS. Seine Einschränkungen: kein Geräte-Profiling, kein Gästeportal, kein Posture, keine SGT-Unterstützung, begrenzte Skalierbarkeit und keine zentralisierte Verwaltung über mehrere RADIUS-Server. NPS ist die richtige Antwort für kleine Umgebungen mit einfachen Anforderungen und begrenztem Budget.

**Aruba ClearPass** ist ISEs primärer Wettbewerber. Es bietet gleichwertige Funktionen — 802.1X, Profiling, Gästeportal, Posture, TACACS. ClearPass ist herstellerneutral (funktioniert mit Switches und APs jedes Netzwerkherstellers), hat einen guten Ruf für starke Gast- und BYOD-Workflows und wird oft in Aruba-Wireless-Umgebungen oder Multi-Vendor-Netzwerken bevorzugt, wo die Abhängigkeit vom Cisco-Ecosystem ein Anliegen ist.

**Cisco ISE** ist die richtige Wahl, wenn:
- Die Umgebung überwiegend Cisco ist (Switches, APs, DNA Center, Firepower) — native Integrationen liefern den größten Mehrwert
- SGT-basierte Policy-Durchsetzung über den Campus eine Anforderung ist
- pxGrid-Integrationen mit Sicherheitsplattformen geplant sind
- Skalierung eine verteilte, HA-fähige Plattform erfordert
- Posture-Durchsetzung eine Compliance-Anforderung ist

Die ehrliche Zusammenfassung:

| | NPS | ClearPass | Cisco ISE |
|---|---|---|---|
| Kosten | Kostenlos | Pro-Endpoint-Abo | Pro-Endpoint-Abo |
| 802.1X / RADIUS | ✅ | ✅ | ✅ |
| Geräte-Profiling | ❌ | ✅ | ✅ |
| Gästeportal | Grundlegend | ✅ | ✅ |
| Posture | ❌ | ✅ | ✅ (Premier) |
| SGT / TrustSec | ❌ | ❌ | ✅ |
| DNA Center Integration | ❌ | ❌ | ✅ (nativ) |
| pxGrid-Ecosystem | ❌ | Begrenzt | ✅ |
| Herstellerneutralität | ✅ | ✅ | Cisco-optimiert |
| Betriebskomplexität | Niedrig | Mittel | Hoch |

---

## Praxisnotizen: Dimensionierung und betriebliche Realität

Einige Beobachtungen aus Produktions-Deployments:

**PSN-Dimensionierung ist wichtiger als die meisten Teams planen.** Authentifizierungsanfragen steigen bei Schichtwechseln, morgendlichen Login-Fluten und Netzwerkereignissen sprunghaft an. PSNs, die für die Durchschnittslast korrekt dimensioniert sind, können bei Spitzenlast Schwierigkeiten haben. Dimensionieren Sie für den Spitzenbetrieb mit ausreichend Puffer.

**Der MnT-Node wird oft zu klein dimensioniert.** Logging von Hunderten von Netzwerkgeräten erzeugt erhebliches Datenvolumen. Ein unterdimensionierter MnT-Node wird zum Engpass für Troubleshooting-Sichtbarkeit — genau dann, wenn Sie ihn am dringendsten brauchen. Geben Sie ihm ausreichend Festplatte und Arbeitsspeicher.

**ISE-Upgrades sind bedeutende Wartungsereignisse.** Wie CUCM folgen ISE-Upgrades einer bestimmten Reihenfolge — zuerst PAN, dann MnT, dann PSNs — und erfordern Wartungsfenster. Das Betreiben einer alten ISE-Version häuft Sicherheitsschulden an. Bauen Sie regelmäßige Upgrade-Zyklen in den Betriebskalender ein.

**Beginnen Sie im Überwachungsmodus.** Wenn Sie ISE in einem bestehenden Netzwerk deployen, beginnen Sie im Monitor-Modus — ISE verarbeitet Authentifizierungsanfragen und protokolliert, was passieren würde, setzt aber keine Policy durch. Dies zeigt Geräte, die bei der Authentifizierung scheitern würden, bevor die Durchsetzung etwas kapatır. Wechseln Sie schrittweise zu Low-Impact-Modus und dann zu vollständiger Durchsetzung.

**Die Pro-Endpoint-Anzahl überrascht Menschen.** ISE lizenziert die Anzahl gleichzeitig aktiver Endpoints. In einem Campus mit 2.000 Mitarbeitern, die jeweils Laptop und Telefon tragen, sind das mindestens 4.000 Endpoints — plus Drucker, IP-Telefone, Kameras und IoT-Geräte. Holen Sie eine genaue Gerätezählung ein, bevor Sie die Lizenz dimensionieren.

---

## Wichtigste Erkenntnisse

- **ISE ist eine Plattform, kein Produkt** — es ersetzt mehrere Einzellösungen (RADIUS-Server, NAC, Gästeportal, Posture-Engine) durch eine integrierte Plattform.
- **Lizenzierung ist pro Endpoint, gestaffelt** — Essentials für grundlegendes 802.1X, Advantage für Profiling und Gäste, Premier für Posture. Geräteverwaltung (TACACS) ist separat.
- **Verteiltes HA-Deployment ist für die Produktion nicht optional** — planen Sie für dedizierte Infrastruktur und angemessene Node-Dimensionierung.
- **pxGrid-Integrationen multiplizieren ISEs Wert** — Firewall-Policy basierend auf Identität, SIEM mit Sitzungskontext angereichert, automatisierte Bedrohungsreaktion.
- **ISE + DNA Center ist die vollständige Campus-Fabric-Geschichte** — SGT-basierte Policy einmal definiert, überall automatisch durchgesetzt.
- **NPS ist die richtige Antwort für einfache Umgebungen** — überentwickeln Sie kleine Deployments nicht.
- **ClearPass ist die richtige Antwort für Multi-Vendor-Umgebungen** oder wo das Cisco-Ecosystem-Engagement begrenzt ist.
- **Beginnen Sie im Überwachungsmodus** — erzwingen Sie erst, nachdem Sie validiert haben, was die Authentifizierung mit Ihrer bestehenden Umgebung machen würde.

---

## Verwandte Artikel

- 🔐 [802.1X-Projekte: Die identitätsbasierte Architektur im Praxiseinsatz](/de/technology/identity-based-microsegmentation-8021x/) — Der Praxiseinsatz-Leitfaden, den ISE ermöglicht
- 🏛️ [Cisco DNA Center / Catalyst Center: Wann es sinnvoll ist](/de/architecture/cisco-dna-center-catalyst-center-architecture-guide/) — Die Campus-Management-Plattform, mit der ISE integriert
- 🔐 [Die Zero-Trust-Mentalität: Sicherheit als Architektur entwickeln](/de/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — Die Philosophie hinter identitätsbasierter Zugangskontrolle
- 🛡️ [F5 WAF Deep Dive](/de/technology/f5-waf-asm-advanced-waf-application-security/) — Ergänzende L7-Sicherheit neben ISEs L2/L3-Durchsetzung