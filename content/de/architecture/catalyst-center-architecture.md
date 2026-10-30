---
title: "Cisco DNA Center / Catalyst Center: Wann es Sinn ergibt und wann nicht"
description: "Ehrliche Bewertung von Cisco DNA Center – Bereitstellungskosten, Komplexität der Einrichtung, ISE-Integration und wann kleinere Unternehmen sich anderweitig umsehen sollten."
date: 2026-10-31T00:30:00+01:00
draft: false

cover:
  image: "/img/postimages/cisco-dna-center-architecture-cover.webp"
  alt: "Cisco DNA Center Catalyst Center Architektur-Leitfaden"
  relative: false

tags: ["Cisco", "DNA Center", "Catalyst Center", "SD-Access", "ISE", "Netzwerkautomatisierung", "Campus-Netzwerk", "Enterprise-Architektur"]
categories: ["Architektur"]
keywords:
  - Cisco DNA Center Architektur
  - Catalyst Center Enterprise
  - DNA Center vs. traditionelles Campus-Netzwerk
  - Cisco SD-Access Design
  - DNA Center ISE-Integration
  - DNA Center Kostenrechtfertigung
  - Cisco Fabric-Netzwerk
  - DNA Center Cluster-Anforderungen
  - Campus-Netzwerk-Automatisierung
  - Cisco DNA Center Vor- und Nachteile

showToc: true
TocOpen: false
---

# Cisco DNA Center / Catalyst Center: Wann es Sinn ergibt und wann nicht

Cisco DNA Center – heute unter dem Namen Catalyst Center bekannt – ist eine dieser Plattformen, bei denen das Marketingversprechen und die Realität in der Praxis deutlich voneinander abweichen. Das Marketingversprechen ist überzeugend: Eine zentrale Steuerungsoberfläche („Single Pane of Glass“) für Ihr gesamtes Campus-Netzwerk, automatisierte Bereitstellung, KI-gestützte Analysen, Intent-Based Networking. Die Realität in der Praxis sieht so aus, dass das Erreichen dieses Zustands erhebliche Investitionen, beträchtlichen Vorabaufwand und eine organisatorische Reife erfordert, die viele Unternehmen unterschätzen.

Ich habe DNA Center in großen Enterprise-Umgebungen implementiert, darunter ein Projekt in der Fertigungsindustrie, das Cisco als Erfolgsgeschichte veröffentlich hat – eine der ersten großflächigen DNA Center- und Stealthwatch-Integrationen in der Türkei. Diese Erfahrung hat mir ein klares Bild davon vermittelt, was die Plattform tatsächlich leistet und wo sie Reibungspunkte erzeugt.

Dieser Artikel ist eine ehrliche architektonische Bewertung – weder ein Produkt-Pitch noch eine pauschale Ablehnung. Die Frage ist nicht, ob DNA Center gut oder schlecht ist. Es geht darum, ob es das richtige Werkzeug für Ihre spezifische Situation ist.

---

## Was DNA Center / Catalyst Center tatsächlich ist

DNA Center ist eine Plattform für Netzwerkmanagement, Automatisierung und Assurance. Sie läuft auf dedizierten physischen Appliances und bietet eine zentrale Steuerung für das gesamte Campus-Netzwerk:

- **Design:** Netzwerkhierarchien definieren – Standorte, Gebäude, Etagen – und Einstellungen skaliert anwenden
- **Policy:** Definieren, wer worauf Zugriff erhält, mit konsistenter Durchsetzung der Richtlinien über Kabel- und WLAN-Netzwerke hinweg
- **Provisioning:** Konfigurationen automatisiert über Templates auf Switche, APs und Router ausrollen
- **Assurance:** Telemetriedaten von allen verwalteten Geräten erfassen, Health-Dashboards, Metriken zur Client-Experience und Anomalieerkennung bereitstellen
- **Automatisierung:** Workflows, ITSM-Integration, automatisierte Fehlerbehebung

Die zugrundeliegende Campus-Fabric-Technologie ist **SD-Access** – Ciscos Software-Defined-Campus-Architektur, die VXLAN für die Data Plane und LISP für die Control Plane verwendet, mit ISE als Policy-Engine. DNA Center ist die Management-Plattform, die diese Fabric orchestriert.

---

## Die Kostenrealität: Eine Investition für Großunternehmen

Sprechen wir zuerst den wichtigsten Faktor an, da dieser bestimmt, ob alles weitere für Ihre Situation überhaupt relevant ist.

### Hardware-Appliance-Kosten

DNA Center läuft auf Ciscos dedizierter DN2-HW-APL-Appliance. Eine Single-Node-Bereitstellung (geeignet für kleinere Umgebungen) besteht aus einer Appliance. **Ein produktionsfähiger Cluster erfordert drei Appliances** – eine für das Management, eine für Policies und eine für die Datenerfassung –, die in einem HA-Cluster konfiguriert sind.

Die Hardwarekosten für einen Drei-Knoten-Cluster sind erheblich. Noch vor der Softwarelizenzierung sprechen wir von einer beträchtlichen Kapitalinvestition, die DNA Center für kleine und mittlere Bereitstellungen sofort ausschließt. Dies ist keine Plattform, die man bereitstellt, weil es nett wäre, sie zu haben – man setzt sie ein, weil die Größe der Umgebung es rechtfertigt.

### Software-Lizenzierung

Die Lizenzierung von DNA Center basiert auf einem Abonnement pro Gerät und Jahr. Die Lizenzierungsstufen (Essentials, Advantage, Premier) bestimmen, welche Funktionen verfügbar sind. Der vollständige Funktionsumfang – einschließlich erweiterter Assurance, KI-Analysen und SD-Access-Funktionen – erfordert die höheren Stufen.

Für ein Unternehmen mit 500 Switchen summieren sich die jährlichen Lizenzkosten zu einer erheblichen laufenden betrieblichen Ausgabe zusätzlich zur Hardwareinvestition.

### Die ehrliche Größenschwelle

Aus Erfahrung in der Praxis: DNA Center beginnt wirtschaftlich und operational erst dann Sinn zu ergeben, wenn Sie über **eine große Anzahl von Switchen** verfügen – typischerweise im Bereich von mehreren hundert oder mehr verwalteten Geräten über mehrere Standorte hinweg. Unterhalb dieser Schwelle ist das Kosten-Nutzen-Verhältnis schwer zu rechtfertigen.

Für kleine und mittlere Unternehmen ist das für DNA Center erforderliche Kapital – Hardware, Lizenzierung, Implementierungszeit, Schulung – an anderer Stelle besser angelegt. Ein gut gestaltetes traditionelles Campus-Netzwerk mit guten Monitoring-Tools bietet im operativen Alltag einen ähnlichen Mehrwert zu einem Bruchteil der Kosten.

> **Die Schlüsselfrage vor jeder DNA Center-Evaluierung:** Wie viele Netzwerkgeräte verwalten Sie an wie vielen Standorten mit wie vielen Ingenieuren? Wenn die Antwort lautet: „Weniger als ein paar hundert Geräte, ein oder zwei Standorte, ein Netzwerkteam“, prüfen Sie zuerst Alternativen.

---

## Die Realität bei der Bereitstellung: Komplex, zeitintensiv, unnachgiebig

Der zweite wesentliche Faktor, der Unternehmen überrascht, ist der hohe Aufwand für die Erstbereitstellung und Konfiguration.

### Die Ersteinrichtung geht nicht schnell

Einen DNA Center-Cluster aufzubauen, ihn in Ihr bestehendes Netzwerk zu integrieren und in einen funktionsfähigen Zustand zu bringen, ist ein mehrwöchiges Projekt – keine Aufgabe für ein Wochenende. Der Prozess umfasst:

- Physische Appliance-Installation und Cluster-Bildung
- Definition der Netzwerkhierarchie (Standort-, Gebäude-, Etagenstruktur)
- Device Discovery und Onboarding
- Template-Design für Gerätekonfigurationen
- Integration mit ISE (bei Nutzung von Policy-Funktionen)
- WLAN-Integration, falls APs verwaltet werden
- Konfiguration der Datenerfassung für Assurance

Jeder dieser Schritte weist Abhängigkeiten auf. Das Design von Templates erfordert das Verständnis darüber, wie Ihr Netzwerk aussehen soll, und das Kodieren dieser Zielstruktur als reproduzierbare Konfiguration. Das bedeutet, dass die Arbeit zur Netzwerkstandardisierung, die eigentlich vor DNA Center hätte erledigt werden sollen, im Rahmen der Bereitstellung nachgeholt werden muss.

### Das Problem der Voraussetzungen

DNA Center setzt einen Grad an Netzwerkstandardisierung voraus, den viele reale Umgebungen nicht aufweisen. Wenn Ihre Switche uneinheitliche Konfigurationen, abweichende Namenskonventionen oder Legacy-Setups haben, die über Jahre hinweg organisch gewachsen sind, zwingt Sie die DNA Center-Bereitstellung dazu, all dies zu bereinigen, bevor die Plattform die Geräte zuverlässig verwalten kann.

Dies ist eigentlich ein verdeckter Vorteil – DNA Center erzwingt Best Practices. Es bedeutet jedoch auch, dass das Implementierungsprojekt oft länger dauert als geplant, da die Vorarbeiten umfangreicher sind als erwartet.

### „Einrichten und vergessen“ ist keine Option

DNA Center ist keine Plattform, die man einmal einrichtet und dann einfach laufen lässt. Sie erfordert kontinuierliche Aufmerksamkeit:

- Software-Updates für die Appliance selbst (regelmäßige Wartungsfenster)
- Template-Anpassungen bei Änderungen der Netzwerkstandards
- ISE-Policy-Updates, wenn sich Zugriffsanforderungen ändern
- Überwachung des Systemzustands der Plattform selbst parallel zum verwalteten Netzwerk

Unternehmen, die DNA Center ohne dedizierte Ressourcen für den Betrieb einsetzen, stellen fest, dass der Wert der Plattform im Laufe der Zeit sinkt, da sie nicht mehr mit dem tatsächlichen Netzwerkzustand synchron ist.

---

## Was Sie nach der Stabilisierung erhalten: Der tatsächliche Mehrwert

Sobald DNA Center bereitgestellt, konfiguriert und stabilisiert ist – was Zeit und Aufwand erfordert –, ändert sich das operative Bild erheblich. Hier zahlt sich die Plattform aus.

### Zentrale Steuerungsoberfläche für Kabel und WLAN

Der unmittelbarste operative Vorteil: Alles ist an einem Ort sichtbar. Kabelgebundene Switche, WLAN-APs, Router, WAN-Konnektivität – alles wird über eine einzige Oberfläche verwaltet und überwacht. Sie sehen das Netzwerk als Ganzes, nicht als getrennte Domänen, die von unterschiedlichen Tools verwaltet werden.

Das klingt einfach, aber in großen Umgebungen, in denen das Kabel- und das WLAN-Team historisch unterschiedliche Tools und Sichtweisen hatten, verändert die einheitliche Ansicht die Fehlerdiagnose grundlegend. Ein Client-Konnektivitätsproblem, das früher das Korrelieren von Daten aus mehreren Quellen erforderte, kann in einem einzigen Workflow über den gesamten Pfad hinweg verfolgt werden – vom Client über den AP und Switch bis zur Firewall.

### Integriertes Logging und historische Analysen

DNA Center erfasst und speichert Telemetriedaten von verwalteten Geräten. Schnittstellenstatistiken, Historie der Client-Verbindungen, Topologieänderungen, Konfigurationsänderungen – alles wird protokolliert und ist abfragbar.

Der praktische Nutzen: Wenn letzten Dienstag um 2 Uhr morgens etwas schiefgelaufen ist, können Sie zurückgehen und genau sehen, wie das Netzwerk zu diesem Zeitpunkt aussah. Schnittstellenauslastung, Client-Zahlen, Fehlerraten, Konfigurationsstatus. Diese rückwirkende Sichtbarkeit fehlt im traditionellen Netzwerkmanagement oft – Geräte speichern Logs intern, aber diese im Nachhinein über hunderte von Geräten hinweg zu korrelieren, ist manuell und langsam.

Das bedeutet auch, dass **Sie nicht zwingend eine separate Drittanbieter-Logging-Plattform** für Netzwerkgerätedaten benötigen. DNA Center übernimmt diese Funktion für verwaltete Geräte und reduziert so die Anzahl der Tools im Stack.

### Automatisierung: Der operative Multiplikator

Sobald Templates und Workflows eingerichtet sind, wird die Bereitstellung neuer Geräte oder Standorte drastisch schneller. Das Hinzufügen eines neuen Gebäudes zu einem bestehenden Campus, der vollständig von DNA Center verwaltet wird, umfasst folgendes:
- Physisches Anschließen der neuen Switche
- Ausführen der Device Discovery
- Anwenden des bestehenden Standort-Templates
- Fertig

Was früher die manuelle Konfiguration jedes einzelnen Geräts über eine Terminal-Sitzung erforderte – für einen großen Standort potenziell tagelange Arbeit –, dauert nur noch wenige Stunden oder weniger, wenn die Vorarbeit an den Templates bereits erledigt ist.

Gleiches gilt für Massenänderungen: das Aktualisieren eines VLANs über 200 Switche hinweg, das netzwerkweite Anwenden einer neuen QoS-Policy oder das Rotieren von Zugangsdaten auf allen verwalteten Geräten. Vorgänge, die früher Skripte oder manuelle Wiederholungen erforderten, werden zu template-gesteuerten Workflows.

### Fabric-Architektur: VXLAN über Ihren Campus

Für Unternehmen, die eine SD-Access-Fabric einsetzen, bildet DNA Center die Managementschicht über einer grundlegend anderen Campus-Architektur. In einem traditionellen Campus werden VLANs über 802.1Q-Trunks über Switche hinweg erweitert – die Layer-2-Domäne ist durch die Netzwerktopologie physisch eingeschränkt.

SD-Access verwendet VXLAN, um virtuelle Netzwerke über ein geroutetes Underlay zu legen (Overlay). Das Ergebnis: Jeder Endpunkt kann sich unabhängig vom physischen Standort in jedem virtuellen Netzwerk befinden, VLANs müssen nicht mehr über das physische Netzwerk hinweg erweitert werden, und die Makrosegmentierung wird am Fabric-Edge statt an der Firewall durchgesetzt.

Für große Campus-Netzwerke mit komplexen Segmentierungsanforderungen – verschiedene Abteilungen, IoT-Geräte, Gastnetzwerke, die alle isoliert werden müssen – vereinfacht das Fabric-Modell die Architektur im Vergleich zur manuellen Verwaltung erweiterter VLANs und Inter-VLAN-Routings erheblich.

---

## ISE-Integration: Wo die Plattform erstklassig wird

Wenn DNA Center für sich allein schon leistungsfähig ist, erreicht DNA Center in Kombination mit Cisco ISE ein grundlegend neues Leistungsniveau.

ISE stellt die Identitäts- und Policy-Engine bereit. DNA Center liefert die Netzwerkmanagement- und Enforcement-Plattform. Zusammen ergeben sie:

- Ein Benutzer verbindet sich mit dem Campus-Netzwerk (kabelgebunden oder WLAN)
- ISE authentifiziert den Benutzer über 802.1X gegenüber dem Active Directory
- ISE bestimmt die Security Group (SGT) basierend auf Identität, Gerätetyp und Posture
- DNA Center setzt die mit dieser Security Group verknüpfte Policy in der gesamten Fabric durch
- Die Policy folgt dem Benutzer, unabhängig davon, wo er sich verbindet – Gebäude A, Gebäude B, Kabel oder WLAN

Das ist identitätsbasiertes Networking in seiner reinsten Form. Die Zugriffs-Policy ist daran gebunden, wer der Benutzer ist und welches Gerät er verwendet, nicht daran, an welchem physischen Port oder in welchem IP-Subnetz er sich befindet. Ein Finanzmitarbeiter erhält Zugriff auf Finanzressourcen, egal ob er an seinem Schreibtisch, in einem Konferenzraum oder an einem entfernten Standort angeschlossen ist.

Die operative Auswirkung: **Netzwerksegmentierung ist kein physisches Problem mehr** (In welchem VLAN befindet sich dieser Port?), sondern wird zu einem Policy-Problem (Worauf darf dieser Benutzer zugreifen?). Diese Vereinfachung bietet in Umgebungen mit komplexen Zugriffsanforderungen einen echten Mehrwert.

Als ich dies in der Fertigungsumgebung implementierte, schuf die Kombination aus DNA Center, ISE, Umbrella, Stealthwatch und Firepower eine vollständig integrierte Sicherheits- und Netzwerk-Fabric. Policy-Änderungen in ISE wurden automatisch über DNA Center im gesamten Netzwerk verteilt. Die Sichtbarkeit von Stealthwatch speiste die Anomalieerkennung, die automatisierte Reaktionen auslöste. Dieses Ausmaß an Integration – über einen Campus mit hunderten von Geräten hinweg – wäre manuell unmöglich zu pflegen.

---

## Cloud-Integration: AWS und darüber hinaus

DNA Center hat Cloud-Integrationsfunktionen hinzugefügt, die seine Relevanz über den On-Premise-Campus hinaus erweitern.

**Die AWS-Integration** ermöglicht es DNA Center, Netzwerkrichtlinien und Sichtbarkeit auf Cloud-Workloads auszuweiten. Transit Gateway-Integration, VPC-Konnektivitätsmanagement und konsistente Policies über On-Premise- und AWS-Umgebungen hinweg sind Teil der Ausrichtung der Plattform.

Ciscos übergeordnete Vision – und die Richtung, in die sich die Plattform bewegt – ist eine konsistente Policy und Sichtbarkeit über On-Premise-Campus, Niederlassungsnetzwerke und Cloud-Umgebungen hinweg aus einer einzigen Management-Ebene. Azure und andere Cloud-Anbieter stehen auf der Roadmap.

Dies entwickelt sich nach wie vor weiter. Das On-Premise-Campusmanagement ist ausgereift; die Multi-Cloud-Integration ist neuer und entwickelt sich stetig fort. Aber für Unternehmen mit erheblicher Cloud-Präsenz, die gleichzeitig eine Cisco-Campusinfrastruktur betreiben, lohnt es sich, diese Konvergenz im Auge zu behalten – es ist die Richtung, in die Cisco investiert.

---

## DNA Center vs. traditioneller Campus: Die Architekturentscheidung

Wann macht ein traditionelles Campus-Management mehr Sinn als DNA Center?

**Ein traditioneller Campus (managed Switche, separate Tools) ist angemessen, wenn:**
- Die Anzahl der Geräte unter der Skalierungsschwelle liegt, ab der Automatisierung einen klaren ROI liefert
- Das Unternehmen nicht über die Engineering-Ressourcen verfügt, um DNA Center ordnungsgemäß bereitzustellen und zu warten
- Budgetbeschränkungen die Hardware- und Lizenzinvestition schwer rechtfertigen lassen
- Das Netzwerk stabil und standardisiert ist – die Änderungshäufigkeit ist gering
- Eine Multi-Vendor-Umgebung vorliegt, in der Cisco nicht dominiert

**DNA Center ergibt Sinn, wenn:**
- Hohe Geräteanzahl (hunderte Switche, mehrere Standorte)
- Häufige Bereitstellung neuer Standorte oder Geräte
- Komplexe Segmentierungsanforderungen, die von einer Fabric-Architektur profitieren
- ISE bereits im Einsatz oder geplant ist – die Integration vervielfacht den Mehrwert
- Ausreichende Kapazität im Engineering-Team vorhanden ist, um die Plattform ordnungsgemäß zu betreiben
- Das Unternehmen langfristig auf das Cisco-Ökosystem setzt

Das schlechteste Ergebnis ist die Bereitstellung von DNA Center in einer Umgebung, deren Größe dies nicht rechtfertigt, um dann mit dem operativen Overhead einer komplexen Plattform zu kämpfen, die keinen verhältnismäßigen Mehrwert bietet. Das zweitschlechteste Ergebnis ist ein Netzwerk, das groß genug wäre, um von DNA Center zu profitieren, ohne jedoch die erforderlichen Engineering-Ressourcen für den ordnungsgemäßen Betrieb bereitzustellen.

---

## Praktische Beobachtungen aus dem Feld

Einige Dinge, die nicht in der Dokumentation stehen, aber in der Praxis von Bedeutung sind:

**Beginnen Sie mit der Netzwerkstandardisierung.** Überprüfen Sie vor der Bereitstellung von DNA Center Ihre bestehende Netzwerkkonfiguration. Uneinheitliche Hostnamen-Konventionen, unstandardisierte VLAN-Strukturen und Legacy-Konfigurationen verlangsamen das Device-Onboarding erheblich. DNA Center belohnt saubere, standardisierte Netzwerke.

**Das Template-Design ist die eigentliche Arbeit.** Die zeitliche Investition in die Erstellung guter Konfigurationstemplates zahlt sich über Jahre hinweg aus. Übereilte Templates führen zu manuellen Overrides und Ausnahmen, die den Automatisierungswert untergraben. Nehmen Sie sich von Anfang an die Zeit, Templates ordnungsgemäß zu entwerfen.

**Der Cluster ist für die Produktion nicht optional.** Eine Single-Node-Bereitstellung ist für Produktionsumgebungen nicht geeignet – sie stellt einen Single Point of Failure für Ihre Netzwerkmanagement-Plattform dar. Planen Sie das Budget von Anfang an für den Drei-Knoten-Cluster ein.

**ISE-Integration erfordert ISE-Expertise.** Die Integration von DNA Center mit ISE schöpft das volle Potenzial der Plattform aus, aber ISE selbst ist komplex. Das Integrationsprojekt setzt fundierte ISE-Kenntnisse im Team voraus. Wenn ISE zusammen mit DNA Center zum ersten Mal bereitgestellt wird, planen Sie eine entsprechende Lernkurve für beides ein.

**Upgrade-Planung ist essenziell.** DNA Center-Upgrades erfordern Wartungsfenster und sorgfältige Planung. Der Betrieb der Appliance auf einer alten Softwareversion führt zum Aufbau von Sicherheitsdefiziten und Funktionslücken. Planen Sie regelmäßige Upgrade-Zyklen fest in Ihren Betriebskalender ein.

---

## Die wichtigsten Erkenntnisse

- **DNA Center ist teuer** – der Drei-Knoten-Cluster für Produktions-HA ist eine erhebliche Hardwareinvestition noch vor jeglicher Softwarelizenzierung. Diese Kosten lassen sich erst ab einer gewissen Größe rechtfertigen.
- **Die Erstbereitstellung ist komplex und zeitaufwendig** – planen Sie Wochen statt Tage ein und kalkulieren Sie Vorarbeiten zur Netzwerkstandardisierung ein.
- **Nach der Stabilisierung ist der operative Mehrwert echt** – einheitliche Sichtbarkeit, integriertes Logging, Automatisierung und Fabric-Management verändern die Betriebsweise großer Netzwerke grundlegend.
- **Durch die ISE-Integration wird die Plattform erstklassig** – identitätsbasierte Policies werden über den gesamten Campus hinweg durchgesetzt und folgen dem Benutzer unabhängig vom Verbindungspunkt.
- **Integriertes Logging reduziert die Abhängigkeit von Drittanbieter-Tools** – DNA Center speichert Netzwerk-Telemetriedaten und verringert so den Bedarf an separater Logging-Infrastruktur für Netzwerkgerätedaten.
- **Die Cloud-Integration wächst** – AWS-Anbindung ist verfügbar, eine breitere Multi-Cloud-Unterstützung befindet sich in der Entwicklung.
- **Für kleine und mittlere Unternehmen: Suchen Sie anderweitig.** Bei geringerer Geräteanzahl steht die Investition in keinem Verhältnis zum Nutzen. Ein traditionelles Campus-Management mit guten Monitoring-Tools ist hier die richtige Antwort.
- **Das Produkt entwickelt sich stetig weiter** – Cisco investiert aktiv in die Plattform. Funktionen, die bei der Erstbereitstellung noch eingeschränkt waren, werden mit jedem Release ausgereifter.

---

## Verwandte Artikel

- 🔐 [Identitätsbasierte 802.1X-Architektur in der Praxis](/de/technology/identity-based-microsegmentation-8021x/) – Das Identitätsfundament, das DNA Center + ISE so leistungsfähig macht
- 🔐 [Das Zero-Trust-Mindset: Sicherheit als Architektur entwickeln](/en/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) – Die architektonische Philosophie hinter dem SD-Access-Policy-Modell
- 🏗️ [Switch, Firewall, AP – Warum die Wahl der richtigen Produkte nicht ausreicht](/de/architecture/core-network-is-not-a-product-list/) – Kontext der Campus-Architektur
- 📊 [Richtiges Monitoring](/de/architecture/monitoring-not-just-seeing/) – Wie sich DNA Center Assurance in eine umfassendere Monitoring-Strategie einfügt
- 🌐 [Enterprise WLAN-Controller-Architektur](/en/technology/enterprise-wifi-controller-architecture-cisco-aruba/) – WLAN-Integration mit DNA Center
