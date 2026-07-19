---
title: "IT-Sicherheitspflichten für kleine Unternehmen in Bayern — und wie der Digitalbonus Bayern bis zu 50% der Kosten übernimmt"
seoTitle: "DSGVO IT-Sicherheit KMU Bayern | Digitalbonus 2026 — Firewall, VLAN, Backup, E-Mail"
description: "Welche IT-Sicherheitsmaßnahmen sind in Bayern gesetzlich vorgeschrieben? Firewall, Netzwerktrennung, E-Mail-Schutz, Backup — mit Gesetzesangaben und Förderung bis €7.500."
date: 2026-04-17
draft: false
showToc: true
TocOpen: false
tags:
  - Digitalbonus Bayern
  - DSGVO
  - BSI IT-Grundschutz
  - Netzwerksicherheit
  - IT-Sicherheit
  - KMU München
keywords:
  - Digitalbonus Bayern 2026
  - DSGVO IT-Sicherheit Pflicht
  - BSI IT-Grundschutz KMU
  - Firewall Pflicht kleine Unternehmen
  - VLAN Trennung DSGVO
  - Netzwerksegmentierung Bayern
  - E-Mail Sicherheit DSGVO
  - Backup Pflicht Unternehmen
  - IT-Förderung Bayern 2026
---

# IT-Sicherheitspflichten für kleine Unternehmen — und wie der Digitalbonus Bayern bis zu 50% übernimmt

Viele kleine Unternehmen in Bayern glauben, IT-Sicherheit sei ein Thema für große Konzerne. Die Realität ist eine andere: Die DSGVO gilt für **jeden**, der personenbezogene Daten verarbeitet — vom Einzelhändler über die Arztpraxis bis zum Hotel. Und die Anforderungen sind konkret, verbindlich und mit Bußgeldern bewehrt.

Die gute Nachricht: Der **Digitalbonus Bayern** erstattet bis zu **50% der Investitionskosten** — für Firewall, Netzwerktrennung, E-Mail-Sicherheit, Backup und mehr. Das Programm läuft bis Dezember 2027.

> 💬 **Kostenlose IT-Analyse:** [WhatsApp](https://wa.me/4916098665971) oder [E-Mail](mailto:info@barashhelvadzhaoglu.com)
> Wir prüfen Ihre Infrastruktur kostenlos — kein Auftrag, kein Produktverkauf.

---

## Die rechtliche Grundlage: Was ist tatsächlich vorgeschrieben?

### DSGVO Artikel 32 — Sicherheit der Verarbeitung

**Quelle:** [Art. 32 DSGVO](https://gdpr.eu/article-32-security-of-processing/)

> „Der Verantwortliche und der Auftragsverarbeiter treffen geeignete technische und organisatorische Maßnahmen, um ein dem Risiko angemessenes Schutzniveau zu gewährleisten."

Das bedeutet: Jedes Unternehmen, das personenbezogene Daten verarbeitet — also Namen, E-Mail-Adressen, Gesundheitsdaten, Buchungsinformationen — muss **technische Schutzmaßnahmen** einrichten. Nicht als Empfehlung, sondern als **gesetzliche Pflicht**.

### BSI IT-Grundschutz — Der technische Standard

**Quelle:** [BSI IT-Grundschutz Kompendium](https://www.bsi.bund.de/grundschutz)

Das Bundesamt für Sicherheit in der Informationstechnik (BSI) definiert im IT-Grundschutz konkret, was „geeignete technische Maßnahmen" im Sinne der DSGVO bedeuten. Deutsche Gerichte und Datenschutzbehörden orientieren sich bei Prüfungen an diesem Standard.

**Gilt BSI IT-Grundschutz für kleine Unternehmen?**
Formal ist er freiwillig — aber: Die DSGVO schreibt „Stand der Technik" vor. In Deutschland entspricht dieser dem BSI IT-Grundschutz. Wer ihn nicht einhält, kann bei einer Prüfung nachweisen müssen, warum seine abweichenden Maßnahmen gleichwertig sind.

---

## Was konkret vorgeschrieben ist — Maßnahme für Maßnahme

### 1. Firewall — Pflicht nach BSI NET.3.2

**Rechtsgrundlage:** BSI IT-Grundschutz, Baustein [NET.3.2 Firewall](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/Kompendium/Bausteine/Infrastruktur/NET_3_2_Firewall.pdf)

BSI NET.3.2.A2 schreibt vor:
> „Es muss ein Regelwerk für die Firewall erstellt werden. Es darf kein Datenverkehr automatisch vom externen ins interne Netz gelangen."

BSI NET.3.2.A9 ergänzt:
> „Die Firewall muss alle wichtigen Ereignisse protokollieren."

**Was das in der Praxis bedeutet:**
- Ein einfacher DSL-Router ist **keine** Firewall im Sinne des BSI
- Eine UTM-Firewall (z. B. Fortinet FortiGate, Palo Alto) ist erforderlich
- Die Firewall muss zwischen **allen** Netzwerkzonen stehen — nicht nur zwischen Internet und internem Netz

**Förderfähig durch Digitalbonus:** ✅ Ja — Hardware und Konfigurationsleistung

---

### 2. Netzwerksegmentierung (VLANs) — Pflicht nach BSI NET.1.1 und DSGVO Art. 25

**Rechtsgrundlage:**
- BSI IT-Grundschutz, Baustein [NET.1.1 Netzarchitektur und -design](https://www.bsi.bund.de/grundschutz)
- DSGVO Art. 25 — Datenschutz durch Technikgestaltung (Privacy by Design)

> „Personenbezogene Daten sind so zu verarbeiten, dass nur die Personen Zugang haben, die ihn für ihre Aufgaben benötigen."

**Was das in der Praxis bedeutet:**

Folgende Geräteklassen müssen in **getrennten Netzwerken (VLANs)** betrieben werden:

| Netzwerk-Segment | Was gehört hinein | Risiko ohne Trennung |
|---|---|---|
| **Mitarbeiter-Netz** | PCs, Laptops | Zugriff auf Kundendaten |
| **Server / NAS** | Dateiserver, Backup-System | Datenverlust bei Angriff |
| **IoT-Geräte** | Drucker, IP-Kameras, Smart-TV, UPS | Bekannte Sicherheitslücken, kein Update |
| **Gäste-WLAN** | Kunden, Patienten, Hotelgäste | Zugriff auf interne Systeme |
| **Kasse / POS** | Kartenterminal, Kassensystem | PCI DSS Pflicht, Zahlungsdaten |

**Warum Drucker gefährlich sind:**
IP-Drucker haben oft veraltete Firmware und keine automatischen Sicherheitsupdates. Ein kompromittierter Drucker im gleichen Netzwerk wie der Buchhaltungs-PC gibt Angreifern direkten Zugriff auf alle Daten.

**Warum IP-Kameras gefährlich sind:**
Billige IP-Kameras (Hikvision, Dahua) werden regelmäßig in internationalen Hackerangriffen missbraucht — als Einstiegspunkt ins Unternehmensnetzwerk.

**Förderfähig durch Digitalbonus:** ✅ Ja — Managed Switches, Access Points, Konfigurationsleistung

---

### 3. Gäste-WLAN mit Captive Portal und Log-Speicherung

**Rechtsgrundlage:**
- DSGVO Art. 32 — Technische Schutzmaßnahmen
- § 100 TKG (Telekommunikationsgesetz) — Verkehrsdaten
- BSI IT-Grundschutz NET.2.2 — WLAN-Nutzung

**Was vorgeschrieben ist:**

**a) Vollständige Isolation:**
Das Gäste-WLAN darf **keinerlei** Zugriff auf interne Systeme haben. Ein Hotelgast oder Patient im Wartezimmer darf nicht auf Buchungssysteme, Drucker oder Mitarbeiter-Dateien zugreifen können.

**b) Verbindungsprotokolle — 12 Monate Speicherpflicht:**
Wer öffentliches WLAN anbietet, muss Verbindungsdaten (IP-Adresse, Verbindungszeitpunkt, Verbindungsdauer) für **12 Monate** aufbewahren — für eventuelle behördliche Anfragen.

**c) Captive Portal mit DSGVO-Einwilligung:**
Beim Login muss der Gast über die Datenverarbeitung informiert werden und aktiv zustimmen.

**Technische Umsetzung:**
Die Verbindungslogs werden von der Firewall (z. B. FortiGate) erfasst und automatisch auf ein NAS-Gerät übertragen — dort für 12 Monate gespeichert.

**Förderfähig durch Digitalbonus:** ✅ Ja — WLAN-Hardware und Konfiguration

---

### 4. E-Mail-Sicherheit — Pflicht nach BSI APP.5.3 und DSGVO Art. 32

**Rechtsgrundlage:**
- BSI IT-Grundschutz, Baustein [APP.5.3 Allgemeiner E-Mail-Client und -Server](https://www.bsi.bund.de/grundschutz)
- DSGVO Art. 32 — Schutz vor unbefugtem Zugriff und Datenverlust

BSI APP.5.3.A1 schreibt vor:
> „Es müssen Schutzmaßnahmen gegen Schadsoftware in E-Mails getroffen werden. Eingehende und ausgehende E-Mails müssen auf Schadsoftware überprüft werden."

**Was das in der Praxis bedeutet:**
Ein einfaches E-Mail-Postfach bei Ionos oder Strato ohne zusätzlichen Schutz ist **nicht ausreichend**.

Erforderlich ist:
- **Spam-Filterung:** Blockierung unerwünschter Massen-E-Mails
- **Malware-Schutz:** Erkennung schädlicher Anhänge (Ransomware, Trojaner)
- **Phishing-Schutz:** Erkennung gefälschter Absenderadressen (Business Email Compromise)
- **Protokollierung:** Nachweis aller gefilterten E-Mails

**Technische Lösung:**
Ein Cloud-basierter E-Mail-Security-Gateway (z. B. Hornetsecurity, FortiMail Cloud) leitet alle eingehenden E-Mails durch einen Sicherheitsfilter, bevor sie beim Empfänger ankommen. Funktioniert mit jedem bestehenden E-Mail-System — Office 365, Google Workspace oder einfachem Webmail.

**Förderfähig durch Digitalbonus:** ✅ Ja — als IT-Sicherheits-Softwarelizenz (bis 18 Monate)

---

### 5. Endpoint-Schutz (Antivirus / EDR) — Pflicht nach BSI SYS.2.1 und DSGVO Art. 32

**Rechtsgrundlage:**
- BSI IT-Grundschutz, Baustein [SYS.2.1 Allgemeiner Client](https://www.bsi.bund.de/grundschutz)
- DSGVO Art. 32 — Schutz vor Datenverlust durch Schadsoftware

BSI SYS.2.1.A6 schreibt vor:
> „Auf Clients muss ein Virenschutzprogramm installiert und aktiviert sein. Das Virenschutzprogramm muss regelmäßig aktualisiert werden."

BSI SYS.2.1.A7 ergänzt:
> „Sicherheitsrelevante Ereignisse müssen protokolliert und auf Auffälligkeiten geprüft werden."

**Was das in der Praxis bedeutet:**

Ein einzelnes Antivirusprogramm auf jedem PC — ohne zentrale Verwaltung — entspricht **nicht** dem BSI-Standard. Erforderlich ist:

- **Zentrales Management:** Ein Administrator sieht den Schutzstatus aller Geräte auf einen Blick
- **Echtzeit-Schutz:** Bedrohungen werden erkannt, bevor sie Schaden anrichten
- **Ransomware-Schutz:** Dateiverschlüsselung durch Schadsoftware wird blockiert
- **Protokollierung:** Alle Sicherheitsereignisse werden aufgezeichnet — für eventuelle Prüfungen
- **Monatliche Berichte:** Nachweis aktiver Schutzmaßnahmen

**Technische Lösung:**
Zentral verwaltete EDR-Lösungen wie Bitdefender GravityZone oder ESET Protect ermöglichen die Verwaltung aller Geräte über ein zentrales Dashboard.

**Förderfähig durch Digitalbonus:** ✅ Ja — Softwarelizenzen und Einrichtungsleistung

---

### 6. Datensicherung (Backup) — Pflicht nach BSI CON.3 und GoBD

**Rechtsgrundlage:**
- BSI IT-Grundschutz, Baustein [CON.3 Datensicherungskonzept](https://www.bsi.bund.de/grundschutz)
- GoBD (Grundsätze zur ordnungsgemäßen Buchführung) — gesetzliche Aufbewahrungspflichten
- DSGVO Art. 32 — Wiederherstellbarkeit personenbezogener Daten

BSI CON.3.A7 schreibt vor:
> „Die gesicherten Daten müssen regelmäßig wiederhergestellt werden, um die Funktionsfähigkeit der Datensicherung zu überprüfen."

**Die 3-2-1-Regel — Branchenstandard:**
- **3** Kopien der Daten
- **2** verschiedene Speichermedien (z. B. NAS + Cloud)
- **1** Kopie außerhalb des Gebäudes (z. B. AWS Frankfurt)

**Was das in der Praxis bedeutet:**
Eine einzelne externe Festplatte, die gelegentlich manuell bespielt wird, entspricht **nicht** dem BSI-Standard. Erforderlich ist:

- **Automatische tägliche Sicherung** — kein manueller Eingriff
- **Verschlüsselung** — Daten sind auch bei Diebstahl des Backupmediums geschützt
- **Externe Kopie** — bei Feuer oder Einbruch bleibt das Backup erhalten
- **Regelmäßige Wiederherstellungstests** — Nachweis, dass das Backup funktioniert
- **GoBD-Konformität** — Aufbewahrungsfristen von 6–10 Jahren für buchhalterische Daten

**Technische Lösung:**
NAS-Gerät (z. B. Synology) mit automatischer verschlüsselter Synchronisation zu AWS S3 Frankfurt — EU-Rechenzentrum, DSGVO-konform.

**Förderfähig durch Digitalbonus:** ✅ Ja — NAS-Hardware und Cloud-Backup-Einrichtung

---

## Reale Bußgelder — ausgelöst durch Beschwerden, nicht durch Inspektionen

Das BayLDA führt **keine regelmäßigen Routineprüfungen** durch. Bußgelder entstehen durch:

- **Kundenbeschwerden** — ein unzufriedener Patient, Gast oder Mitarbeiter
- **Datenpannen** — Hackerangriff, Datenverlust, versehentliche Weitergabe
- **Konkurrenzbeschwerden** — Mitbewerber erstatten Anzeige

Das Bayerische Landesamt für Datenschutzaufsicht (BayLDA) verhängte 2023 die höchste Anzahl an Bußgeldern seit Einführung der DSGVO. Reale Beispiele: Zahnarztpraxis in Bayern €3.500, Einzelhandel €1.200 — ausgelöst durch einzelne Kundenbeschwerden.

**Wichtig:** Unwissenheit schützt nicht vor Strafe. Die DSGVO gilt seit 2018 — jedes Unternehmen hatte Zeit, sich anzupassen.

---

## Was der Digitalbonus Bayern fördert

**Programm:** [Digitalbonus Bayern](https://www.digitalbonus.bayern)
**Förderquote:** 50% der förderfähigen Kosten
**Maximum:** €7.500 (Digitalbonus Standard) — je einmal pro Förderbereich (IT-Sicherheit und Digitalisierung)
**Laufzeit:** bis 31. Dezember 2027
**Antragstellung:** ausschließlich digital über ELSTER-Unternehmenskonto

| Maßnahme | Förderfähig |
|---|---|
| Firewall (Hardware + Lizenz + Konfiguration) | ✅ Ja |
| Managed Switch für VLAN-Trennung | ✅ Ja |
| WLAN Access Points | ✅ Ja |
| NAS + verschlüsseltes Cloud-Backup | ✅ Ja |
| E-Mail-Sicherheitslizenz (bis 18 Monate) | ✅ Ja |
| Antivirus/EDR-Lizenzen (bis 18 Monate) | ✅ Ja |
| Installations- und Konfigurationsleistung | ✅ Ja |
| Wartungsvertrag (bis 18 Monate) | ✅ Ja |
| Beratungsleistung (bis 50% der Gesamtkosten) | ✅ Ja |
| Standard-PCs, Laptops, Drucker | ❌ Nein |
| Standard-Bürosoftware (Office, Windows) | ❌ Nein |

**Wichtige Bedingung:** Der Antrag muss **vor** Projektbeginn gestellt werden. Weder Bestellung noch mündliche Auftragserteilung dürfen vor Eingang der Antragsbestätigung erfolgen.

---

## Beispielrechnung: Kleines Hotel (10 Zimmer, 5 Mitarbeiter)

| Maßnahme | Kosten | Nach Förderung (50%) |
|---|---|---|
| FortiGate Firewall + 1 Jahr Lizenz | €1.000 | €500 |
| Managed Switch (VLAN-fähig) | €500 | €250 |
| 3× WLAN Access Points | €900 | €450 |
| NAS + AWS Backup-Einrichtung | €500 | €250 |
| E-Mail-Sicherheit (18 Monate) | €400 | €200 |
| Antivirus/EDR 5 Geräte (18 Monate) | €300 | €150 |
| Installation & Konfiguration | €1.000 | €500 |
| 18 Monate Wartung | €900 | €450 |
| **Gesamt** | **€5.500** | **€2.750** |

Das Hotel zahlt **€2.750** — der Freistaat Bayern übernimmt **€2.750**.

---

## Für wen ist das relevant?

- **Hotels & Pensionen** — Gäste-WLAN, Kamerasysteme, Buchungsdaten, POS-Terminals
- **Arztpraxen & Therapiepraxen** — Patientendaten, Schweigepflicht, DSGVO + §75b SGB V
- **Anwaltskanzleien** — Mandantengeheimnis, strenge DSGVO-Pflichten
- **Cafés & Restaurants** — Gäste-WLAN, Kassensystem, Reservierungsdaten
- **Sprachschulen** — Schüler-WLAN, Verwaltungsdaten, Lehrerdaten
- **Kleine Büros (2–20 Personen)** — ohne eigene IT-Abteilung

---

## Was wir anbieten: Unabhängige Beratung — kein Produktverkauf

Wir verkaufen keine Produkte. Sie wählen Ihre eigenen Anbieter und Produkte — wir helfen bei Planung, Installation, Konfiguration und Dokumentation.

Als **Senior Network Security Engineer mit 11+ Jahren Erfahrung** in Banking, Industrie und Hotellerie (u. a. Hilton, Marriott, Crown Hotel Group, Wyndham Grand Europa) bieten wir:

1. **Kostenlose IT-Infrastruktur-Analyse** — wir schauen uns Ihre aktuelle Situation an und zeigen, wo die Lücken sind
2. **Unabhängige Produktempfehlung** — wir empfehlen, was zu Ihnen passt, nicht was am teuersten ist
3. **Technische Umsetzung** — VLAN-Konfiguration, Firewall-Einrichtung, Backup-Setup, E-Mail-Sicherheit
4. **Digitalbonus-Antragsvorbereitung** — wir helfen bei der Dokumentation der förderfähigen Maßnahmen
5. **Laufende Wartung** — monatliche Überwachung, Updates, Ansprechpartner bei Problemen

---

## Nächster Schritt: Kostenlose Analyse

**📱 WhatsApp:** [wa.me/4916098665971](https://wa.me/4916098665971)

**📧 E-Mail:** [info@barashhelvadzhaoglu.com](mailto:info@barashhelvadzhaoglu.com)

*Kostenlose Analyse. Kein Auftrag ohne Ihre Zustimmung. Kein Produktverkauf — nur Beratung und technisches Know-how.*

---

## Weiterführende Links

- [Digitalbonus Bayern — Offizielles Förderprogramm](https://www.digitalbonus.bayern)
- [DSGVO Artikel 32 — Sicherheit der Verarbeitung](https://gdpr.eu/article-32-security-of-processing/)
- [BSI IT-Grundschutz Kompendium](https://www.bsi.bund.de/grundschutz)
- [BayLDA — Bayerisches Landesamt für Datenschutzaufsicht](https://www.lda.bayern.de)
- [GoBD — Grundsätze zur Buchführung](https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Weitere_Steuerthemen/Abgabenordnung/2019-11-28-GoBD.pdf)