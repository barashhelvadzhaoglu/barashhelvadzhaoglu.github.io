---
title: "OT-Netzwerke: Was ein IT-Ingenieur auf dem Fabrikboden wirklich antrifft"
description: "IT-Leitfaden zur OT-Sicherheit — Purdue-Modell, Layer-2-Firewall, OT-Signaturen, Legacy-Systeme und 802.1X in industriellen Umgebungen."
date: 2026-04-03
draft: false

cover:
  image: "/img/postimages/ot-network-security-cover.webp"
  alt: "OT-Netzwerksicherheit — IT-Ingenieurs-Leitfaden für industrielle Netzwerke"
  relative: false

tags: ["OT-Sicherheit", "Industrienetzwerk", "Purdue-Modell", "SCADA", "ICS", "Firewall", "Netzwerksicherheit", "Modbus", "PROFINET"]
categories: ["Technologie"]
keywords:
  - OT Netzwerksicherheit IT-Ingenieur
  - Purdue-Modell industrielles Netzwerk
  - OT Firewall Layer 2 Deployment
  - OT-fähige Firewall-Signaturen
  - Modbus PROFINET industrielle Protokolle
  - IT OT Netzwerksegmentierung
  - Legacy PLC Windows XP Sicherheit
  - 802.1X OT-Netzwerk Herausforderungen
  - industrielles Netzwerk DMZ
  - Fortinet OT-Firewall

showToc: true
TocOpen: true
---

# OT-Netzwerke: Was ein IT-Ingenieur auf dem Fabrikboden wirklich antrifft

Die meisten Netzwerkingenieure verbringen ihre Karriere in der IT-Infrastruktur — Unternehmens-LANs, Rechenzentren, Campus-Netzwerke, Cloud-Konnektivität. Dann landet eines Tages ein Projekt auf Ihrem Schreibtisch, das eine Fabrik, ein Lagerautomatisierungssystem oder eine Versorgungsanlage betrifft. Und plötzlich gelten die vertrauten Regeln nicht mehr ganz.

OT (Operational Technology) Netzwerke sind keine IT-Netzwerke. Die Geräte sind anders, die Protokolle sind anders, die Prioritäten sind anders, und — entscheidend — die Konsequenzen eines Fehlers sind anders. In der IT verursacht ein falsch konfigurierter Switch einen Netzwerkausfall. In der OT kann eine falsch konfigurierte Netzwerkänderung eine Produktionslinie stoppen, teure Ausrüstung beschädigen oder in kritischen Infrastrukturszenarien physische Sicherheitsrisiken schaffen.

Dieser Artikel ist aus der Perspektive des IT-Ingenieurs geschrieben — der Person, die hinzugezogen wird, um eine Firewall hinzuzufügen, ein Netzwerk zu segmentieren oder ein industrielles System mit dem Unternehmensnetzwerk zu verbinden. Kein tiefer SCADA-Engineering-Leitfaden, sondern eine praktische Orientierung für das, was Sie antreffen werden und worüber Sie nachdenken müssen, bevor Sie irgendetwas berühren.

---

## Der Kernunterschied: Verfügbarkeit vor Vertraulichkeit

In der IT-Sicherheit lautet die klassische Prioritätsreihenfolge **CIA: Confidentiality, Integrity, Availability** (Vertraulichkeit, Integrität, Verfügbarkeit). Vertraulichkeit steht an erster Stelle — der Schutz von Daten vor unbefugtem Zugriff ist das primäre Anliegen.

In der OT lautet die Prioritätsreihenfolge im Wesentlichen **AIC: Availability, Integrity, Confidentiality** (Verfügbarkeit, Integrität, Vertraulichkeit). Die Produktionslinie muss weiter laufen. Ein 30-sekündiger Netzwerkausfall in einer IT-Umgebung ist eine Unannehmlichkeit. Ein 30-sekündiger Netzwerkausfall in einer Fertigungsanlage kann Ausschussprodukte, beschädigte Maschinen oder einen Sicherheitsvorfall bedeuten.

Diese Umkehrung hat direkte Konsequenzen für jede Netzwerkentscheidung in einer OT-Umgebung:

- **Sie starten OT-Geräte nicht ohne umfangreiche Planung neu.** Ein Cisco-Switch in einer IT-Umgebung kann in 3 Minuten ohne Drama neugestartet werden. Ein in eine Produktionslinie eingebetteter Switch benötigt möglicherweise ein geplantes Wartungsfenster, einen Produktionsstopp und Koordination mit dem Anlagenbetriebsteam.
- **Patch-Management ist nicht unkompliziert.** In der IT patchen Sie Systeme regelmäßig. In der OT können viele Systeme nicht gepatcht werden — der Hersteller zertifiziert die Softwareversion, und jede Änderung macht die Zertifizierung ungültig oder erfordert eine kostspielige Neubewertung.
- **Netzwerkänderungen erfordern Koordination.** In der IT ist das Hinzufügen eines VLANs Routine. In der OT kann dieselbe Änderung die Genehmigung von Produktionsmanagern, Sicherheitsingenieuren und Ausrüstungslieferanten erfordern.

Das zu verstehen, bevor Sie mit der Arbeit beginnen, ist nicht nur professionelle Höflichkeit — es verhindert echte Betriebsvorfälle.

---

## Das Purdue-Modell: Eine Karte der OT-Netzwerkarchitektur

Das Purdue-Modell (ISA-95) ist das Standardframework für das Verständnis industrieller Netzwerkarchitektur. Es definiert Ebenen vom physischen Prozess unten bis zur Unternehmens-IT oben:

```
Ebene 4/5  — Unternehmens-IT-Netzwerk (ERP, E-Mail, Unternehmens-LAN)
─────────────────────────────────────────────────────────────────────
               IT/OT-DMZ  ← Die Grenze, wo IT-Ingenieure arbeiten
─────────────────────────────────────────────────────────────────────
Ebene 3    — Betrieb / Standortverwaltung
               (Historian-Server, Engineering-Workstations,
                HMI-Server, Batch-Management)

Ebene 2    — Aufsichtssteuerung
               (SCADA-Server, HMI-Clients, DCS-Workstations)

Ebene 1    — Grundlegende Steuerung
               (PLCs, DCS-Controller, RTUs)

Ebene 0    — Physischer Prozess
               (Sensoren, Aktoren, Motoren, Ventile)
```

**Wo IT-Ingenieure typischerweise arbeiten:** Die IT/OT-DMZ und Ebene 3. Hier wird die Verbindung zwischen dem Unternehmens-IT-Netzwerk und der OT-Umgebung verwaltet. Hier finden Firewall-Projekte, Historian-Konnektivität, Fernzugriffslösungen und Netzwerksegmentierungsarbeiten statt.

**Was IT-Ingenieure selten direkt berühren:** Ebenen 0, 1 und 2 — die eigentlichen Steuerungssysteme, PLCs und SCADA-Komponenten. Das ist die Domäne der OT/Automatisierungsingenieure und Ausrüstungslieferanten.

Die DMZ zwischen IT und OT ist die kritischste Grenze in der industriellen Netzwerkarchitektur. Sie muss existieren. Der Datenverkehr sollte nicht frei zwischen dem Unternehmensnetzwerk und der OT-Umgebung fließen.

---

## OT-Protokolle: Was in diesen Netzwerken läuft

Wenn Sie zum ersten Mal einen Netzwerkanalysator an ein OT-Netzwerk anschließen, sehen Sie Protokolle, die in keinem IT-Netzwerk vorkommen. Zu verstehen, was sie sind — selbst auf Oberflächenebene — hilft Ihnen, vernünftige Firewall- und Segmentierungsentscheidungen zu treffen.

### Modbus

Das älteste industrielle Protokoll, entwickelt 1979. Noch weit verbreitet in der Fertigung, in Versorgungsunternehmen und in der Gebäudeautomation.

- **Modbus RTU:** Seriell-basiert (RS-232, RS-485). Läuft über physische serielle Verbindungen, nicht Ethernet.
- **Modbus TCP:** Modbus in TCP/IP gekapselt. Läuft auf Port 502.

Modbus hat **keine Authentifizierung, keine Verschlüsselung, keine Autorisierung**. Jedes Gerät im Netzwerk, das Port 502 eines Modbus-fähigen Controllers erreichen kann, kann Sensorwerte lesen oder Steuerbefehle schreiben. Das ist kein historisches Versehen — Modbus wurde für isolierte serielle Netzwerke konzipiert, wo physischer Zugang die Sicherheitskontrolle war.

Wenn Modbus TCP in einem Ethernet-Netzwerk ist, das von außerhalb des OT-Segments zugänglich ist, ist das Fehlen der Authentifizierung ein erhebliches Risiko. Die Firewall-Richtlinie muss einschränken, welche Geräte Modbus-fähige Controller erreichen können.

### DNP3 (Distributed Network Protocol)

Verbreitet in Versorgungsunternehmen — Stromerzeugung, Wasseraufbereitung, Öl und Gas. Ursprünglich für SCADA-Kommunikation zwischen Steuerzentralen und entfernten Feldgeräten (Umspannwerke, Pumpstationen) konzipiert.

DNP3 hat grundlegende Authentifizierungserweiterungen (Secure Authentication Version 5), aber viele bereitgestellte Implementierungen verwenden noch die ursprüngliche nicht authentifizierte Version.

### OPC-UA (OPC Unified Architecture)

Der moderne industrielle Kommunikationsstandard, der speziell entwickelt wurde, um die Sicherheitslücken in älteren Protokollen zu schließen. OPC-UA unterstützt:
- Zertifikatbasierte Authentifizierung
- Verschlüsselte Kommunikation
- Feinkörnige Autorisierung (welche Clients welche Datenpunkte lesen können)

OPC-UA ist das Protokoll, dem Sie in neueren Installationen und bei Historian-Server-Konnektivität begegnen werden.

### PROFINET

Siemens' industrielles Ethernet-Protokoll, dominant in der europäischen Fertigung (Automobil, Lebensmittelverarbeitung, Pharmazie). PROFINET läuft über Standard-Ethernet, verwendet aber spezifische EtherType-Werte und ist echtzeitsensitiv — Verzögerungen von Millisekunden sind wichtig.

PROFINET hat fast keine inhärente Sicherheit. Es setzt ein physisch isoliertes Netzwerk voraus. In Umgebungen mit PROFINET-Controllern muss die Netzwerksegmentierung strikt sein — PROFINET-Datenverkehr sollte niemals sein dediziertes VLAN verlassen.

### EtherNet/IP

Rockwell Automation / Allen-Bradleys industrielles Ethernet-Protokoll. Verbreitet in der nordamerikanischen Fertigung. Ähnliche Sicherheitsmerkmale wie PROFINET — für isolierte Netzwerke konzipiert, begrenzte Authentifizierung.

---

## Was der IT-Ingenieur tatsächlich gefragt wird zu tun

In der Praxis fällt die Anfrage, wenn IT/Netzwerkingenieure in OT-Projekte eingebunden werden, normalerweise in eine dieser Kategorien:

### Szenario 1: „Füge eine Firewall zwischen PC und Maschine ein"

Das häufigste Szenario. Ein Windows-PC (der SCADA-Software oder HMI ausführt) ist direkt über Ethernet mit einem PLC oder einer Produktionsmaschine verbunden — kein Netzwerkgerät dazwischen. Die Anfrage ist, eine Sicherheitsschicht hinzuzufügen.

```
Vorher:
  [Windows HMI PC] ──────────────── [PLC / Maschinencontroller]

Nachher (typischer Ansatz):
  [Windows HMI PC] ── [Firewall] ── [PLC / Maschinencontroller]
```

**Layer-2 transparentes Firewall-Deployment:**

Der betrieblich sicherste Weg, eine Firewall in diesen Pfad einzufügen, ist im **Layer-2 transparenten Modus** (auch „Bump-in-the-Wire" oder Bridge-Modus genannt). Die Firewall leitet Datenverkehr transparent weiter — kein Gerät weiß, dass sie existiert, keine IP-Adressen ändern sich, keine Routing-Änderungen. Wenn die Firewall ausfällt, kann der Datenverkehr durch Entfernen der Firewall und direktes Wiederverbinden wiederhergestellt werden.

Das ist wichtig, weil das Ändern von IP-Adressen auf einem PLC oder industriellen Controller oft das Neukonfigurieren der Anwendungssoftware erfordert, die mit ihm kommuniziert — ein Prozess, der Lieferantenunterstützung, Re-Zertifizierung und Produktionsausfallzeiten umfassen kann.

Im transparenten Modus:
- Der PLC behält seine vorhandene IP-Adresse
- Der HMI-PC behält seine vorhandene IP-Adresse
- Die Firewall inspiziert Datenverkehr und wendet Richtlinien an, ohne ein gerouteter Hop zu sein

Die Firewall-Richtlinie in diesem Szenario ist typischerweise:
- Spezifischen OT-Protokolldatenverkehr vom HMI zum Controller erlauben (Modbus Port 502, PROFINET, EtherNet/IP)
- Nur notwendige Verwaltungsprotokolle erlauben
- Alles andere blockieren
- Gesamten Datenverkehr für Sichtbarkeit protokollieren

### Szenario 2: „OT-Netzwerk mit Unternehmens-IT verbinden"

Das Produktionsteam möchte Daten vom Fabrikboden in Unternehmenssysteme bringen — Produktionsstatistiken in ERP, Sensordaten in eine Berichtsdatenbank, Fernüberwachungsfähigkeit.

Das erfordert eine DMZ-Architektur:

```
[Unternehmens-IT-Netzwerk]
           │
      [IT/OT-Firewall]   ← Strenge Richtlinie: nur bestimmte Flüsse erlaubt
           │
      [OT-DMZ]
      [Historian-Server]  ← Sammelt Daten aus OT, stellt sie IT bereit
           │
      [OT-Firewall]       ← Separate Firewall, schützt OT vor DMZ
           │
      [OT-Netzwerk — Ebene 2/3]
```

Das DMZ-Prinzip: Das Unternehmensnetzwerk kann OT-Geräte nicht direkt erreichen. Der Historian-Server in der DMZ sammelt Daten von OT-Systemen (durch die OT-Firewall erlaubt) und macht sie für Unternehmenssysteme verfügbar (durch die IT-Firewall erlaubt).

**Warum zwei Firewalls und nicht eine?** Wenn der Historian-Server in der DMZ kompromittiert wird, sollte er keinen Pfad in eines der Netzwerke bieten. Eine einzelne Firewall mit einem DMZ-Segment bietet weniger Isolation als zwei separate Firewalls.

### Szenario 3: „Netzwerksegmentierung zum flachen OT-Netzwerk hinzufügen"

Viele ältere OT-Umgebungen haben ein völlig flaches Netzwerk — alle PLCs, HMIs, Engineering-Workstations und manchmal sogar unternehmensverbundene PCs in derselben Layer-2-Broadcast-Domain. Jedes Gerät kann jedes andere Gerät erreichen.

Die Segmentierung dieses Netzwerks umfasst:
- Hinzufügen von verwalteten Switches mit VLAN-Fähigkeit
- Definieren von VLANs nach Gerätetyp oder Funktion
- Routing zwischen VLANs durch eine Firewall mit strikter Inter-VLAN-Richtlinie

**Die kritische Einschränkung:** Dokumentieren Sie vor jeder Netzwerkänderung die bestehenden Kommunikationsflüsse erschöpfend. In der OT treten einige Kommunikationsflüsse nur in bestimmten Produktionsphasen auf — ein wöchentlicher Batch-Prozess, ein Schichtendebericht — und erscheinen nicht während eines kurzen Überwachungsfensters. Arbeiten Sie mit dem OT-Team zusammen, um alle Kommunikationsanforderungen zu dokumentieren, bevor Sie die Segmentierung implementieren.

---

## OT-fähige Firewalls: Was die Hersteller entwickelt haben

Standard-IT-Firewalls (selbst NGFWs) haben begrenzte Sichtbarkeit in OT-Protokolle. Sie können IP-Header und TCP/UDP-Ports inspizieren, aber sie können den Inhalt eines Modbus-TCP-Befehls nicht verstehen — sie können „Sensorwert lesen" nicht von „Steuerbefehl an Aktor schreiben" unterscheiden.

OT-fähige Firewalls fügen **industrielle Protokollinspektion** hinzu — die Fähigkeit, OT-Protokoll-Payloads zu parsen und Richtlinienentscheidungen basierend auf protokollspezifischem Inhalt zu treffen.

### Der Signaturunterschied

Eine Standard-NGFW könnte 2.000–5.000 Anwendungssignaturen haben — überwiegend IT-Anwendungen (HTTP, TLS, DNS, SMB, Office 365, usw.). Eine OT-fähige Firewall-Lizenz fügt Hunderte zusätzlicher Signaturen für industrielle Protokolle hinzu:

- **Modbus TCP:** Leseanfragen (von HMI akzeptabel) von Schreibbefehlen unterscheiden (auf autorisierte Systeme beschränken)
- **PROFINET:** Spezifische PROFINET-Dienste identifizieren und kontrollieren
- **EtherNet/IP:** CIP (Common Industrial Protocol) Befehle parsen
- **DNP3:** DNP3-Funktionscodes und Objekttypen inspizieren
- **OPC-DA/UA:** OPC-Kommunikationsrichtung und Datentypen kontrollieren
- **BACnet:** Gebäudeautomationsprotokoll-Inspektion
- Dutzende weitere industrielle und Gebäudeautomationsprotokolle

**Warum das wichtig ist:** Ohne OT-Protokollinspektion kann eine Firewall nur steuern, ob diese IP jene IP auf diesem Port erreichen kann. Mit OT-Inspektion kann sie durchsetzen, dass der HMI Modbus-Holding-Register vom PLC lesen kann, aber nicht in Coils schreiben darf — ein grundlegend anderes Kontrollniveau.

### Anbieter-Landschaft

**Fortinet FortiGate mit OT-Bundle:**
Fortinet bietet spezifische OT/ICS-Lizenzierung an, die die Basis-NGFW mit industriellen Protokollsignaturen und OT-spezifischer Bedrohungsintelligenz erweitert. FortiGate kann im transparenten Modus (Layer 2) oder im gerouteten Modus deployt werden.

**Palo Alto Networks mit ICS/SCADA-Inhalt:**
Das App-ID-Engine von Palo Alto umfasst industrielle Protokollidentifikation. Das Industrial IoT Security-Abonnement fügt OT-Gerätesichtbarkeit, Risikobewertung und protokollspezifische Richtlinien hinzu.

**Claroty, Nozomi Networks, Dragos (OT-spezialisiert):**
Das sind keine traditionellen Firewalls — sie sind OT-spezifische Sicherheitsüberwachungsplattformen. Sie verbinden sich via SPAN-Port mit dem OT-Netzwerk (passives Monitoring) und bieten tiefe Sichtbarkeit: Asset-Discovery, Protokollanalyse, Verhaltensbaseline, Anomalieerkennung. Sie blockieren keinen Datenverkehr, bieten aber Sichtbarkeit, die generische IT-Tools nicht bereitstellen können.

### Lizenzierungsrealität

OT-Firewall-Fähigkeiten werden separat von Standard-IT-NGFW-Funktionen lizenziert. Wenn Sie eine Firewall für ein OT-Projekt spezifizieren, reicht die Standard-Enterprise-Lizenz nicht aus — Sie benötigen das OT/ICS-Bundle oder Äquivalent. Das beeinflusst sowohl die Kosten als auch das Gespräch zur Anbieterauswahl mit dem Kunden.

---

## Das Patch-Problem: Legacy-Systeme, die Sie nicht berühren können

In der IT ist Patchen Routine. In der OT ist Patchen oft unmöglich.

Die Gründe sind spezifisch und legitim:

**Herstellerzertifizierung:** Industrielle Gerätehersteller (Siemens, Rockwell, Schneider, ABB, usw.) zertifizieren ihre Systeme mit bestimmten Softwareversionen. Das Ändern der Betriebssystemversion oder das Anwenden eines OS-Patches kann die Gerätezertifizierung ungültig machen.

**Produktionsabhängigkeit:** Patchen erfordert Ausfallzeiten. In kontinuierlichen Prozessindustrien (Chemiewerke, Stahlwerke) kann „Ausfallzeit" ein geplantes jährliches Wartungsfenster bedeuten.

**End-of-Life-Software:** Sie werden Windows XP, Windows 2003 Server und noch ältere Systeme mit kritischer industrieller Software antreffen. Microsoft hat seit Jahren keine Sicherheitspatches für diese Systeme veröffentlicht.

**Was das für die Netzwerksicherheit bedeutet:**

- **Strikte Netzwerksegmentierung:** Systeme, die nicht gepatcht werden können, dürfen von keinem Netzwerk erreichbar sein, das sie Internet-Bedrohungen aussetzen könnte
- **Anwendungs-Whitelisting:** Nur speziell autorisierte Anwendungen können auf OT-Endpunkten laufen
- **Kompensierende Kontrollen:** Die Firewall muss die Arbeit tun, die normalerweise Patching erledigen würde
- **Offline-Antivirus-Updates:** AV-Updates über USB oder Offline-Medien in air-gapped Umgebungen

---

## 802.1X und NAC in OT: Warum Standard-IT-Ansätze sich nicht direkt übertragen

**PLCs und Controller haben keine 802.1X-Supplicants.** Ein Siemens S7 PLC oder ein Allen-Bradley ControlLogix Controller läuft kein Standard-Betriebssystem mit einem 802.1X-Client. Er kann sich nicht mit Benutzername/Passwort oder Zertifikat bei einem RADIUS-Server authentifizieren.

**MAC Authentication Bypass (MAB) als Workaround:** Der Standardansatz für OT-Geräte ist MAB — die MAC-Adresse des Geräts wird als Authentifizierungsanmeldedaten verwendet. Der Switch sendet die MAC-Adresse an RADIUS, der sie gegen eine autorisierte Gerätedatenbank prüft.

MAB bietet einige Kontrolle — unbekannte Geräte erhalten keinen Netzwerkzugang — aber es ist schwächer als zertifikat- oder anmeldedatenbasierte Authentifizierung. MAC-Adressen können gefälscht werden.

**Profiling als Alternative:** OT-Sicherheitsplattformen (Claroty, Nozomi, Cisco CyberVision) können Geräte im Netzwerk profilieren — PLC-Modelle, Firmware-Versionen und Kommunikationsmuster aus passiver Datenverkehrsanalyse identifizieren. Das bietet Asset-Sichtbarkeit ohne dass Geräte authentifizieren müssen.

**Das Netzwerkänderungsrisiko:** Das Aktivieren von 802.1X in einem bestehenden flachen OT-Netzwerk ohne äußerst sorgfältige Planung kann die Produktionslinie zum Stillstand bringen.

---

## Praktische Checkliste: Bevor Sie ein OT-Netzwerk berühren

Aus Felderfahrung — Dinge, die vor jeder Netzwerkänderung in einer OT-Umgebung passieren sollten:

- **Zuerst mit dem OT-Team sprechen.** Automatisierungsingenieure und Anlagenbetriebspersonal wissen Dinge über das Netzwerk, die nicht dokumentiert sind.
- **Bestehende Kommunikationsflüsse dokumentieren.** Welche Geräte kommunizieren mit welchen, auf welchen Ports, mit welcher Häufigkeit. Verlassen Sie sich nicht auf kurzfristiges Monitoring.
- **Den Produktionsplan verstehen.** Wann ist das Wartungsfenster? Wann hat die Anlage geplante Ausfallzeiten?
- **Wenn möglich, in einer Lab- oder Staging-Umgebung testen.**
- **Einen Rollback-Plan haben.** Für Layer-2-Firewall-Einführung ist der Rollback das Entfernen der Firewall und direktes Wiederverbinden.
- **Firmware/Konfigurationssicherungen koordinieren.** Vor jeder Netzwerkänderung sicherstellen, dass OT-Gerätekonfigurationen gesichert sind.
- **Definieren, was „funktioniert" vor und nach bedeutet.** Akzeptanzkriterien mit dem OT-Team vereinbaren, bevor eine Änderung als erfolgreich erklärt wird.

---

## Wichtigste Erkenntnisse

- **OT-Netzwerke priorisieren Verfügbarkeit über Vertraulichkeit** — das kehrt viele IT-Sicherheitsannahmen um und muss jede Entscheidung informieren.
- **Das Purdue-Modell** definiert, wo die IT/OT-Grenze liegt. Die DMZ zwischen Ebene 3 und Unternehmens-IT ist der häufigste Arbeitsort für IT-Ingenieure.
- **OT-Protokolle (Modbus, PROFINET, EtherNet/IP, DNP3)** haben keine Authentifizierung oder Verschlüsselung. Netzwerkkontrollen sind der primäre Sicherheitsmechanismus.
- **Layer-2 transparentes Firewall-Deployment** ist der sicherste Weg, Sicherheit zwischen OT-Geräten hinzuzufügen — keine IP-Adressänderungen, keine Routing-Änderungen, ohne Konfigurationsänderungen rückgängig zu machen.
- **OT-fähige Firewalls** verstehen industrielle Protokolle und können Richtlinien auf Protokollebene durchsetzen — eine grundlegend andere Fähigkeit als IP/Port-Filterung.
- **OT-Firewall-Lizenzierung ist separat** von IT-NGFW-Lizenzierung — das in die Projektplanung einbeziehen.
- **Ungepatchte Legacy-Systeme sind in OT normal** — kompensierende Netzwerkkontrollen ersetzen, was Patching in der IT bietet.
- **802.1X überträgt sich nicht direkt** — PLCs können sich nicht authentifizieren. MAB und Geräte-Profiling sind die praktischen Alternativen.
- **Mit OT-Teams koordinieren, bevor irgendetwas berührt wird** — die Konsequenzen von Netzwerkfehlern in Produktionsumgebungen sind erheblich ernster als in der IT.

---

## Verwandte Artikel

- 🔐 [802.1X Identitätsbasierte Architektur im Praxiseinsatz](/de/technology/identity-based-microsegmentation-8021x/) — Wie 802.1X in IT-Umgebungen funktioniert und warum OT anders ist
- 🔐 [Die Zero-Trust-Mentalität: Sicherheit als Architektur entwickeln](/de/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — Zero-Trust-Prinzipien auf IT/OT-Grenzdesign angewendet
- 🛡️ [DDoS-Schutzstrategien](/de/technology/ddos-schutzstrategien-isp-scrubbing-on-premise-cloud/) — OT-verbundene Infrastruktur vor volumetrischen Angriffen schützen
- 🏗️ [IT-Infrastruktur ist keine Produktsammlung](/de/architecture/it-infrastructure-not-a-collection-of-products/) — Systemdenken, das gleichermaßen für OT-Netzwerkdesign gilt