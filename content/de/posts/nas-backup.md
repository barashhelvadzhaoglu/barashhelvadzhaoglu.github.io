---
title: "Ihr NAS ohne RAID ist eine Zeitbombe — und die Lösung kostet €1 im Monat"
description: "NAS ohne RAID ist ein ernstes Unternehmensrisiko. AWS S3 automatisches Backup und warum Glacier bis zu €1 im Monat kostet."
date: 2026-03-02
draft: false

cover:
  image: "/img/postimages/nas-backup-cover.webp"
  alt: "NAS Backup mit AWS S3 Cloud — Datensicherheit für KMU"
  relative: false

tags: ["NAS", "Backup", "AWS S3", "Datensicherheit", "KMU", "München"]
categories: ["IT-Tipps"]
keywords: ["NAS Backup AWS S3", "NAS ohne RAID Risiko", "Hyper Backup Synology", "AWS Glacier KMU", "Cloud Backup DSGVO", "NAS Festplattenausfall", "S3 Glacier Deep Archive", "automatisches Backup München", "NAS Datenverlust verhindern", "verschlüsseltes Cloud Backup"]
showToc: true
TocOpen: true
---

Stellen Sie sich eine Arztpraxis vor. Acht Jahre Patientendaten, Rechnungen, Befunde. Alles auf einem kleinen NAS-Gerät im Büro. Eines Morgens startet das Gerät nicht mehr. Festplattenausfall. Man ruft ein Datenrettungsunternehmen an — "wir versuchen es, €800-2000, ohne Garantie."

Dieses Szenario passiert jeden Tag. Und es zu verhindern kostet nur ein paar Euro im Monat.

{{< figure src="/img/postimages/nas-backup-cover.webp" title="NAS Backup mit AWS S3 — Datensicherheit für KMU" >}}

## Der Irrglaube: "Ich habe ein NAS, also habe ich ein Backup"

Ein NAS (Network Attached Storage) ist ein hervorragendes Gerät — zentraler Speicher, von jedem Computer im Netzwerk erreichbar. Aber die meisten NAS-Geräte in kleinen Unternehmen laufen mit einer einzigen Festplatte. Kein RAID.

**Was ist RAID?**
RAID schreibt Daten gleichzeitig auf mehrere Festplatten. In seiner einfachsten Form schreibt RAID 1 dieselben Daten auf zwei Platten gleichzeitig. Fällt eine aus, übernimmt die andere. Kein Datenverlust.

Bei einem NAS mit einer einzigen Festplatte ohne RAID ist in dem Moment, in dem die Platte ausfällt, alles verloren. Keine Vorwarnung, keine Wiederherstellung.

**"Aber mein NAS hat RAID"** — gut, aber nicht genug. RAID schützt vor Festplattenausfall. Vor Feuer, Wasserschaden, Diebstahl, Ransomware oder versehentlichem Löschen schützt es nicht. Ein externes Backup ist unerlässlich.

## Die Lösung: AWS S3 Cloud-Backup

AWS S3 (Simple Storage Service) ist Amazons Cloud-Speicherdienst. Das klingt nach etwas für Großkonzerne — aber kleine Unternehmen können es für nur wenige Euro im Monat nutzen.

**So funktioniert es:**

```
NAS-Gerät (Synology/QNAP)
        ↓ (automatisch, nächtlich)
Hyper Backup Software
        ↓ (verschlüsselt)
AWS S3 — Frankfurt (eu-central-1)
        ↓
Ihre Daten: sicher, verschlüsselt, redundant
```

Synology-NAS-Geräte haben eine eingebaute "Hyper Backup"-Anwendung. Sie konfigurieren sie einmal, und jede Nacht sendet sie automatisch geänderte Dateien an S3. Ihr Backup läuft, während Sie schlafen.

## AWS S3 Storage-Tiers — Was passt zu Ihnen?

AWS S3 bietet verschiedene Speicherebenen mit unterschiedlichen Preisen und Zugriffszeiten:

| Tier | Am besten für | Zugriff | Kosten |
|---|---|---|---|
| **S3 Standard** | Häufig abgerufene Daten | Sofort | ~€23/TB/Monat |
| **S3 Infrequent Access** | Einige Male pro Monat | Sofort | ~€12/TB/Monat |
| **S3 Glacier Instant** | Selten abgerufene Archive | Millisekunden | ~€4/TB/Monat |
| **S3 Glacier Deep Archive** | Langzeitarchivierung | 12 Stunden | ~€1/TB/Monat |

**Empfehlung für KMU:**
Aktive Geschäftsdaten: **S3 Infrequent Access** — günstiger Preis, sofortiger Zugriff bei Bedarf.
Ältere Unterlagen und Archivdateien: **S3 Glacier Instant** — sehr geringe Kosten, trotzdem sofort abrufbar.

Ein typisches Szenario für eine Arztpraxis: aktive Patientendaten in S3 IA (~€5-8/Monat), ältere Archivjahre in Glacier (~€1-2/Monat). **Gesamtkosten pro Monat: €6-10.**

## DSGVO und rechtliche Aspekte

Wenn Sie Patienten-, Mandanten- oder Kundendaten verarbeiten, unterliegen Sie der DSGVO. Für Cloud-Backups sind zwei Dinge entscheidend:

**1. Frankfurt Region (eu-central-1) ist Pflicht** — Ihre Daten müssen innerhalb der EU-Grenzen bleiben.

**2. Verschlüsselung ist Pflicht** — Hyper Backup verschlüsselt Ihre Daten, bevor sie an S3 gesendet werden. Der Verschlüsselungsschlüssel verbleibt bei Ihnen — nicht einmal AWS kann den Inhalt einsehen.

**3. Das Konto ist auf Ihren Namen** — Ich eröffne für jeden Kunden ein separates AWS-Konto auf Ihren Namen. Die Daten und das Konto gehören vollständig Ihnen.

Für Arztpraxen und Kanzleien erstelle ich außerdem einen **AVV (Auftragsverarbeitungsvertrag)** — nach DSGVO vorgeschrieben.

## Wie läuft die Einrichtung ab?

1. AWS-Konto wird auf Ihren Namen eröffnet
2. S3-Bucket mit korrektem Tier und Lifecycle-Richtlinien erstellt
3. Hyper Backup auf Ihrem NAS installiert
4. Erstes vollständiges Backup erstellt
5. Ab dem nächsten Tag werden nur geänderte Dateien gesendet
6. Monatlicher Kontrollbericht per E-Mail

**Was Sie nach der Einrichtung tun müssen:** Nichts. Alles läuft automatisch.

## Was, wenn ich kein NAS habe?

S3-Backup ist auch ohne NAS möglich. Wir installieren einen kleinen Backup-Agent auf Ihren PCs (Duplicati — kostenlos), und ausgewählte Ordner werden automatisch an S3 gesendet.

## Fazit

Ein NAS mit einer einzigen Festplatte kann jederzeit ohne Vorwarnung ausfallen. Selbst ein RAID-NAS schützt nicht vor Ransomware oder physischen Schäden. Mit AWS S3 sind Ihre Daten für nur wenige Euro im Monat verschlüsselt, redundant und sicher.

Das Konto gehört Ihnen, die Daten gehören Ihnen, der Verschlüsselungsschlüssel gehört Ihnen.

**📱 WhatsApp:** [wa.me/4916098665971](https://wa.me/4916098665971)

---

## Verwandte Artikel

**Schutz & Sicherheit**
- 🔋 [Was passiert, wenn der Strom ausfällt? USV-Schutz für Ihr Büro](/de/posts/ups-office/) — NAS und Netzwerkgeräte vor Stromausfall schützen
- 🔒 [SSL-Zertifikat — Warum "Nicht sicher" Kunden kostet](/de/posts/ssl-websecurity/) — Website-Sicherheit für KMU
- 📶 [WLAN-Probleme? Dauerhafte Mesh-Lösung ohne Kabel](/de/posts/wifi-mesh-solution/) — Professionelles WLAN für Büro und Villa

**Architektur & Infrastruktur**
- 📐 [IT-Infrastruktur ist keine Produktsammlung](/de/architecture/it-infrastructure-not-a-collection-of-products/) — Systemdenken für resiliente Infrastruktur
- 📊 [Monitoring richtig gemacht](/de/architecture/monitoring-not-just-seeing/) — IT-Probleme erkennen bevor sie eskalieren