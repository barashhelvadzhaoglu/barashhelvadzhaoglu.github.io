---
title: "Cyberangriffe auf Supermarkt-Kühlschränke in Europa: So sichern Sie OT- und IoT-Geräte"
description: "Im Oktober und November 2026 wurden Kühlgeräte in europäischen Supermärkten aus der Ferne aufgeheizt. Was bisher bekannt ist, warum eine Kühlsteuerung überhaupt erreichbar ist und sieben Maßnahmen, um OT- und IoT-Geräte in Handel und KMU abzusichern."
date: 2026-11-06
draft: false

tags: ["OT-Sicherheit", "IoT-Sicherheit", "Cybersicherheit", "Netzwerksegmentierung", "Fernzugriff", "Einzelhandel"]
categories: ["Netzwerkarchitektur", "Cybersicherheit"]
keywords: ["Cyberangriff Supermarkt Kühlschrank", "Kühlschrank gehackt Europa", "Danfoss Kühlsteuerung Cyberangriff", "OT-Sicherheit Einzelhandel", "IoT-Geräte absichern", "sicherer Fernzugriff OT", "Netzwerksegmentierung IoT", "Gebäudeautomation Sicherheit"]
showToc: true
TocOpen: true
---

Im Oktober und November 2026 wurden Kühl- und Gefriergeräte in Supermärkten in ganz Europa auf Temperaturen gestellt, bei denen die Ware verdarb. Niemand hat die Geräte vor Ort angefasst. Dieser Artikel fasst zusammen, was öffentlich bekannt ist, erklärt, warum eine Kühlsteuerung überhaupt über das Netzwerk angreifbar ist, und nennt die Maßnahmen, die einen solchen Angriff deutlich erschwert hätten.

> **Stand:** Grundlage sind Medienberichte und Unternehmensangaben bis zum 6. November 2026. Die Ermittlungen laufen noch. Wo etwas nicht bestätigt ist, sage ich das.

## Was passiert ist

- **Frankreich, 12. Oktober 2026:** In Filialen von Intermarché, Carrefour, Monoprix und Coopérative U wurden Kühlgeräte aufgeheizt und Lebensmittel verdorben. Die Muttergesellschaft von Intermarché rechnete mit Verlusten von mehreren Millionen Euro.
- **2. November 2026:** Eine zweite Welle traf rund 75 Filialen in Belgien (unter anderem Delhaize, Carrefour, Intermarché, Spar und eine IKEA-Filiale), 13 SuperValu-Märkte in Irland, ICA- und Coop-Filialen in Schweden sowie Unternehmen in den Niederlanden, Estland und Finnland. In Stockholm wurde ein Gefriergerät Berichten zufolge auf 50 °C aufgeheizt.
- **Gemeinsamer Nenner:** Ein Teil der betroffenen Anlagen nutzte Kühlsteuerungssoftware von Danfoss. Laut Danfoss hatten die betroffenen Kunden ihre Software nicht aktualisiert. Sicherheitsforscher von Claroty hatten im August Schwachstellen in Danfoss-Kühlsteuerungen gemeldet, die Danfoss nach eigenen Angaben mit einem Update behoben hat.
- **Mechanismus:** Der belgische Kältetechnik-Dienstleister Sabcobel erklärte, die Geräte seien in den Abtaumodus geschaltet worden. Ein Software-Update allein reiche nicht aus, es seien auch physische Änderungen nötig.

**Bisher nicht bestätigt:** wie sich die Angreifer Zugang verschafft haben, ob die im August gemeldeten Schwachstellen ausgenutzt wurden und wer hinter den Angriffen steht. Die belgische Bundesstaatsanwaltschaft ermittelt. Der EU-Agrarkommissar bezeichnete die Angriffe als gezielten Versuch, die Lebensmittelversorgung zu stören.

## Warum hängt ein Kühlschrank überhaupt im Netzwerk?

Gewerbliche Kühlung ist kein Haushaltskühlschrank. Ein Supermarkt betreibt Dutzende Kühlstellen, die zentral gesteuert werden: Temperaturen, Abtauzyklen, Alarme und Energieoptimierung. Der Servicedienstleister muss nachts Alarme sehen und Einstellungen ändern können, ohne in die Filiale zu fahren.

Das ist ein berechtigter Bedarf. Das Problem ist, wie er oft gelöst wird:

- Die Steuerung oder ihre Weboberfläche ist **direkt aus dem Internet erreichbar**, manchmal über eine Portweiterleitung, die vor Jahren eingerichtet wurde.
- Sie hängt im **selben Netzwerk** wie Kassen, Büro-PCs und Gäste-WLAN.
- Der Dienstleister nutzt einen **dauerhaften Fernzugang**, den niemand überwacht.
- Die Software wurde seit der Installation **nie aktualisiert**, weil „es ja läuft“.
- **Standardpasswörter** wurden nie geändert.

Nichts davon ist typisch nur für Kühlanlagen. Dasselbe Muster gibt es bei Gebäudeautomation, Heizung und Lüftung, Zutrittskontrolle, Kameras, PV-Wechselrichtern und Produktionsmaschinen. Deshalb ist dieser Vorfall auch über Supermärkte hinaus relevant.

## Sieben Maßnahmen, um OT- und IoT-Geräte abzusichern

### 1. Wissen, was vorhanden ist

Geräte, die Sie nicht kennen, können Sie nicht schützen. Führen Sie ein Verzeichnis aller vernetzten Steuerungen, Gateways und Sensoren: Hersteller, Modell, Softwareversion, IP-Adresse, wer sie betreut und wie der Fernzugriff erfolgt.

### 2. Keine direkte Erreichbarkeit aus dem Internet

Die Verwaltungsoberfläche eines OT-Geräts darf nie aus dem Internet erreichbar sein. Prüfen Sie Ihre Firewall auf Portweiterleitungen und suchen Sie Ihre öffentlichen IP-Adressen in Diensten wie Shodan, um zu sehen, was von außen sichtbar ist.

### 3. Netzwerk segmentieren

OT- und IoT-Geräte gehören in ein eigenes VLAN oder Netzsegment. Die Firewall zwischen den Segmenten entscheidet, wer mit wem kommunizieren darf:

- Die Kühlsteuerung spricht nur mit ihrem Verwaltungsserver und, falls genutzt, mit der Cloud des Herstellers.
- Kassen, Büro-PCs und Gäste-WLAN erreichen die Steuerung überhaupt nicht.

Mehr zur Segmentierung in industriellen Netzen: [OT-Netzwerke: Was ein IT-Ingenieur auf dem Fabrikboden wirklich antrifft](/de/technology/ot-network-security/).

### 4. Ausgehenden Verkehr einschränken

Viele Geräte müssen nur eine Handvoll Ziele erreichen. Erlauben Sie genau diese Adressen und Ports und blockieren Sie alles andere. Wird ein Gerät kompromittiert, kann es weder Werkzeuge nachladen noch einen Server des Angreifers erreichen.

### 5. Fernzugriff für Dienstleister absichern

Der Dienstleister braucht Zugriff, aber zu Ihren Bedingungen:

- Zugriff über **IPsec-VPN oder ZTNA (Zero Trust Network Access)** mit **Multi-Faktor-Authentifizierung**, nie über einen offenen Port.
- Zugriff nur auf die Systeme, die der Dienstleister betreut, nicht auf das ganze Netzwerk.
- Zugriff **nur bei Bedarf freigeschaltet** und danach wieder deaktiviert, mit Protokollierung, wer sich wann verbunden hat.

### 6. Updates und Zugangsdaten

Planen Sie Software-Updates für OT-Geräte wie für Server, abgestimmt mit dem Hersteller. Ändern Sie alle Standardpasswörter und verwenden Sie persönliche Konten statt eines gemeinsamen Logins.

### 7. Sicherheitsgrenzen, die Software nicht aushebeln kann

Das ist die Lehre, die am spezifischsten für diesen Vorfall ist. Wenn eine gehackte Steuerung ein Gefriergerät auf 50 °C aufheizen kann, fehlt eine unabhängige Sicherheitsgrenze. Physische oder hardwarebasierte Grenzwerte und lokale Alarme, die ohne Netzwerk funktionieren, sorgen dafür, dass eine kompromittierte Steuerung keinen physischen Schaden anrichten kann. Auch Überwachung hilft: Ungewöhnliche Temperatur- oder Konfigurationsänderungen um 3 Uhr nachts sollten sofort einen Alarm auslösen.

## Kurze Checkliste für kleine Unternehmen

- Wissen wir, welche Geräte in unserer Filiale mit dem Netzwerk verbunden sind?
- Ist eines davon aus dem Internet erreichbar?
- Liegen sie in einem anderen Netz als Kassen und Gäste-WLAN?
- Wie verbindet sich unser Servicedienstleister, und sehen wir, wann er das tut?
- Wann wurde die Software zuletzt aktualisiert? Wurden die Standardpasswörter geändert?
- Gibt es einen Alarm, der auch funktioniert, wenn Netzwerk oder Steuerung ausfallen?

Wenn Sie eine dieser Fragen nicht beantworten können, ist das der Ausgangspunkt.

## Verwandte Artikel

- [OT-Netzwerke: Was ein IT-Ingenieur auf dem Fabrikboden wirklich antrifft](/de/technology/ot-network-security/)
- [Zero Trust Mindset: Sicherheit als Architektur, nicht als Produkt](/de/architecture/zero-trust-architecture-behaviors/)
- [802.1X-Projekte: Implementierung der identitätsbasierten Architektur in der Praxis](/de/technology/identity-based-microsegmentation-8021x/)
- [Firewall-Auswahl und Kapazitätsplanung](/de/technology/firewall-selection-capacity/)

## Quellen

- [Euronews: Cyberattacks hit supermarket fridges and freezers in Europe](https://www.euronews.com/2026/11/02/cyberattack-hits-belgian-supermarket-fridges-and-freezers)
- [Forbes: New wave of refrigerator cyberattacks roils European supermarkets](https://www.forbes.com/sites/conormurray/2026/11/02/new-wave-of-refrigerator-cyberattacks-roils-european-supermarkets-everything-is-destroyed/)
- [Al Jazeera: Suspected cyberattacks trigger supermarket fridge failures across Europe](https://www.aljazeera.com/news/2026/11/2/freezers-in-sweden-belgium-overheat-following-possible-cyberattacks)
- [Axios: Europe's fridges are getting hacked](https://www.axios.com/2026/11/02/europe-supermarket-fridges-attacks-food)
