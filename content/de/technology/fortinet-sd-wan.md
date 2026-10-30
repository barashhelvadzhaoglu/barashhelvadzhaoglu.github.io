---
title: "Fortinet SD-WAN: Security-Driven Networking in der Praxis"
seoTitle: "Fortinet SD-WAN Test | FortiOS-Integration, Gartner Leader & Performance"
description: "Ein detaillierter Einblick in Fortinets SD-WAN-Ansatz: FortiOS-Integration, Security-Driven Networking, Gartner Magic Quadrant-Positionierung und der Vergleich zu reinen SD-WAN-Anbietern."
date: 2026-10-30T06:36:11+01:00
keywords:
  - Fortinet SD-WAN
  - FortiGate SD-WAN
  - Fortinet SASE
  - FortiOS SD-WAN
  - Gartner SD-WAN Magic Quadrant
  - Fortinet vs Cisco SD-WAN
  - Security-Driven Networking
  - FortiManager SD-WAN
tags:
  - SD-WAN
  - Fortinet
  - Security
draft: false
---

# Fortinet SD-WAN: Security-Driven Networking in der Praxis

Fortinet nimmt im SD-WAN-Markt eine ungewöhnliche Position ein. Das Unternehmen hat kein eigenständiges SD-WAN-Produkt entwickelt, um es nachträglich um Security-Funktionen zu ergänzen – noch hat es einen WAN-Optimization-Anbieter übernommen und dessen Technologie umbenannt. Stattdessen hat Fortinet SD-WAN-Funktionen direkt in FortiOS integriert, dasselbe Betriebssystem, auf dem auch seine NGFW-, IPS-, SSL-Inspection- und Application-Control-Funktionen laufen. Das Ergebnis ist eine Architektur, die das Unternehmen **Security-Driven Networking** nennt und die Fortinet seit mehreren Jahren in Folge eine führende Position im Gartner SD-WAN Magic Quadrant sichert.

Dieser Artikel untersucht, was der Ansatz von Fortinet in der Praxis leistet, wo seine größten Stärken liegen und welche Kompromisse damit verbunden sind.

---

## Das FortiOS-Fundament

Der entscheidende Unterschied beim SD-WAN von Fortinet besteht darin, dass es keinen separaten SD-WAN-Daemon oder Overlay-Software-Layer gibt. SD-WAN ist eine native Funktion von FortiOS und läuft auf demselben Kernel wie die Firewall, die IPS-Engine und die Engine zur Applikationserkennung.

Dies hat eine konkrete architektonische Konsequenz: Jedes Paket, das ein FortiGate für das SD-WAN-Routing erreicht, wird gleichzeitig durch den Security-Stack inspiziert. Es gibt keinen Performance-Verlust, wenn Security parallel zu SD-WAN aktiviert wird, da beide dieselbe Verarbeitungs-Pipeline nutzen. Auf Hardware-Appliances mit den proprietären ASICs von Fortinet (NP7, SP5) werden sowohl das SD-WAN-Traffic-Steering als auch die Security-Inspection simultan hardwarebeschleunigt ausgeführt.

In der Praxis bedeutet dies, dass ein Branch-FortiGate Folgendes leisten kann:
- Die Anwendung mittels DPI identifizieren (dieselbe DPI-Engine, die auch für Firewall-Policies verwendet wird)
- Eine SD-WAN-Pfadauswahl basierend auf der Applikationsidentität und der Link-Qualität in Echtzeit anwenden
- Gleichzeitig eine vollständige NGFW-Inspection für denselben Datenverkehr durchführen
- Eine SSL-Deep-Inspection ohne zusätzliche Appliance anwenden

Konkurrierende Anbieter, die SD-WAN und Security als separate Produkte vertreiben – sei es als physisch getrennte Systeme oder als getrennte Softwaremodule –, verursachen entweder zusätzliche Latenz, zusätzliche Kosten oder beides. Der Single-OS-Ansatz von Fortinet eliminiert diese architektonischen Reibungsverluste.

---

## SD-WAN Traffic Steering: Funktionsweise in FortiOS

Das SD-WAN-Traffic-Steering von Fortinet basiert auf drei Kernkonzepten:

**SD-WAN Rules**
Richtlinien, die Datenverkehr nach Anwendung, Benutzer, Quelle/Ziel oder DSCP-Markierung abgleichen und ihn einer SD-WAN-Interface-Gruppe (einer logischen Gruppierung von WAN-Links) zuweisen. Die Regeln werden wie Firewall-Policies von oben nach unten ausgewertet.

**Performance SLAs**
Kontinuierliches, aktives Monitoring jedes WAN-Links mithilfe konfigurierbarer Probes (ICMP, HTTP, DNS). FortiOS misst Latenz, Jitter und Paketverlust in Echtzeit und vergleicht diese mit definierten Schwellenwerten. Fällt die Qualität eines Links unter den Schwellenwert, wird er für SLA-sensitive Anwendungen automatisch nicht mehr berücksichtigt.

**Link Cost and Bandwidth Management**
Über das leistungsorientierte Steering hinaus unterstützt FortiOS Load Balancing über mehrere Links hinweg mittels gewichteter Verteilung (Weighted Distribution), Spillover (Nutzung des sekundären Links, sobald der primäre einen Bandbreitenschwellenwert überschreitet) und volumenbasiertes Abrechnungsmanagement für Links mit Datenlimits.

Die Steering-Entscheidung fällt auf Kernel-Ebene und nicht in einem User-Space-Prozess, wodurch die Forwarding-Latenz selbst bei hohem Durchsatz minimal bleibt.

---

## Positionierung im Gartner Magic Quadrant

Fortinet wird seit mehreren Jahren in Folge im Leaders-Quadranten des Gartner Magic Quadrant für SD-WAN geführt, typischerweise hervorgehoben für:

- **Completeness of vision:** Integrierte Security und SD-WAN, SASE-Roadmap, globale Threat Intelligence durch die FortiGuard Labs
- **Ability to execute:** Große Installationsbasis, breites Partner-Ökosystem, konsistente Bereitstellung über alle Hardware-Klassen hinweg – vom FG-40F für kleine Außenstellen bis hin zu Data-Center-Appliances

Die beständigste Kritik von Analysten betrifft die **Management-Komplexität** bei sehr großen Umgebungen sowie die **Lernkurve** für Unternehmen, die bisher keine Fortinet-Lösungen einsetzen. FortiManager ist eine leistungsfähige zentrale Management-Plattform, doch seine Benutzeroberfläche ist komplex und erfordert Einarbeitungszeit für einen effektiven Betrieb. Organisationen ohne bestehende Fortinet-Expertise sollten dies in ihrer Evaluierung berücksichtigen.

---

## FortiManager und zentrale Orchestrierung

Große SD-WAN-Deployments erfordern eine zentrale Orchestrierung – Hunderte von Branch-Appliances können nicht individuell konfiguriert werden. FortiManager ist Fortinets On-Premises- (oder Cloud-gehostete) Management-Plattform für diesen Zweck.

FortiManager bietet:
- Template-basierte Konfiguration mit gerätespezifischer Variablenersetzung
- SD-WAN-Overlay-Provisionierung (Hub-and-Spoke-, Full-Mesh- oder hybride Topologien)
- Zentrales Performance-SLA-Monitoring über alle Standorte hinweg
- Policy-Pakete, die auf Gruppen von Geräten angewendet werden können
- Automatisierte Provisionierungs-Workflows (Zero-Touch Provisioning für neue Standorte)

Die Zero-Touch-Provisioning-Funktion ist besonders für große Rollouts relevant. Ein neues FortiGate an einem Standort bootet, verbindet sich mit dem FortiManager-Registrierungsserver, authentifiziert sich über eine vorab hinterlegte Seriennummer und empfängt automatisch seine Konfiguration. Ein Network Engineer kann einen neuen Außenstellen-Standort bereitstellen, ohne das Gerät jemals physisch berühren zu müssen – abgesehen vom Anschließen der WAN-Kabel.

FortiAnalyzer arbeitet mit FortiManager zusammen, um Log-Aggregation, Reporting und SD-WAN-Applikations-Performance-Analysen bereitzustellen.

---

## SASE-Integration: Fortinets Cloud-basierte Erweiterung

Fortinet erweitert seine SD-WAN-Architektur über **FortiSASE** zu einem SASE-Angebot – einem Cloud-basierten Sicherheitsdienst, der Remote-Benutzern und Außenstellen sicheren Internetzugang bietet, ohne dass der gesamte Datenverkehr über ein physisches FortiGate zurückgeführt (Backhaul) werden muss.

FortiSASE umfasst Cloud-basierte NGFW-, Secure Web Gateway-, CASB-, ZTNA- und DNS-Filtering-Funktionen, die alle über dasselbe FortiOS-Policy-Modell verwaltet werden, das Fortinet-Administratoren vertraut ist. Für Unternehmen, die bereits in FortiOS-Know-how investiert haben, ist die operative Konsistenz zwischen On-Premises- und Cloud-basierter Sicherheit ein echter Vorteil.

---

## Wo Fortinet SD-WAN überzeugt

**Security-First-Umgebungen**
Wenn die primäre WAN-Anforderung nicht nur Konnektivität ist, sondern auch Threat Prevention, SSL Inspection und Application Control umfasst, eliminiert das integrierte Modell von Fortinet die Notwendigkeit, separate Security-Appliances an jedem Standort zu dimensionieren, zu implementieren und zu verwalten. Die Total Cost of Ownership (TCO) ist häufig niedriger als bei einer Kombination aus einer dedizierten SD-WAN-Appliance und einer separaten NGFW.

**Bestehende FortiGate-Installationsbasis**
Organisationen, die an ihren Standorten bereits FortiGate-Firewalls betreiben, können SD-WAN-Funktionen auf der vorhandenen Hardware häufig allein durch eine Lizenzänderung aktivieren. Dies reduziert den Migrationsaufwand im Vergleich zum Austausch bestehender Geräte gegen ein neues SD-WAN-Overlay drastisch.

**Mittelstand und verteilte Filialnetze**
Das Hardware-Portfolio von Fortinet reicht bis zu sehr kompakten, kosteneffizienten Appliances hinab, die sich für Einzelhandelsstandorte, kleine Außenstellen und sogar industrielle Umgebungen eignen. Das FG-40F und FG-60F decken das Small-Branch-Segment zu einem Preis ab, den spezialisierte SD-WAN-Anbieter bei vergleichbarem FortiOS-Funktionsumfang oft nicht erreichen können.

**Standorte mit hohem Durchsatz und Sicherheitsanforderungen**
Bei den High-End-Appliances sorgen Fortinets proprietäre ASICs für hardwarebeschleunigten Durchsatz – simultan für SD-WAN und Security-Funktionen. Standorte, die Multi-Gigabit-Durchsatz mit vollständiger Security-Inspection erfordern, sind mit der FortiGate-Hardware-Linie bestens bedient.

---

## Wo Fortinet SD-WAN an Grenzen stößt

**Kein reines SD-WAN-Spezialprodukt**
Organisationen, die SD-WAN rein nach Metriken der WAN-Optimierung bewerten – anspruchsvolle Applikationsbeschleunigung, WAN-Deduplizierung, erweiterte TCP-Optimierung –, werden feststellen, dass dedizierte SD-WAN-Anbieter wie Silver Peak (heute HPE Aruba) historisch granularere WAN-Optimization-Funktionen boten. Fortinets Stärke liegt in der Security-Integration, nicht in tiefgehender WAN-Optimierung.

**Management-Komplexität**
FortiManager ist leistungsstark, aber komplex. Kleinere Organisationen oder solche ohne spezialisiertes Network-Engineering-Personal empfinden den Administrationsaufwand möglicherweise als erheblich. Einfachere, Cloud-managed Alternativen können in solchen Umgebungen die passendere Wahl sein.

**Vendor Lock-in**
Die enge FortiOS-Integration ist in reinen Fortinet-Umgebungen eine Stärke, in Multi-Vendor-Umgebungen jedoch eine Einschränkung. Organisationen, die Cisco-Switching, Aruba-Wireless und Palo Alto-Firewalls einsetzen, stehen möglicherweise vor größeren Herausforderungen, Fortinets SD-WAN nahtlos zu integrieren, als dies bei einem herstellerunabhängigen Overlay der Fall wäre.

---

## Typische Deployment-Architektur

Ein standardmäßiges Fortinet SD-WAN Hub-and-Spoke-Deployment sieht wie folgt aus:

- **Hub-Standorte** (Rechenzentrum oder regionaler Hub): FortiGate mit zwei oder mehr WAN-Links, das als SD-WAN-Hub und SD-WAN-Gateway für die Spoke-Standorte fungiert. FortiManager verwaltet die Konfiguration zentral.
- **Spoke-Standorte** (Außenstellen): FortiGate-Appliances mit dualem WAN (z. B. MPLS + Breitband-Internet). Zero-Touch-provisioniert über FortiManager. SD-WAN Rules steuern den Anwendungsdatenverkehr auf den optimalen Pfad. Local Internet Breakout für Cloud-Anwendungen.
- **Remote-Benutzer**: FortiClient VPN oder FortiSASE für Cloud-basierten, sicheren Zugriff.

Overlay-Tunnel zwischen Spokes und Hubs nutzen IPsec mit automatischem Schlüsselmanagement. FortiOS unterstützt sowohl statische als auch dynamische Tunnel-Topologien (ADVPN — Auto Discovery VPN), bei denen Spoke-to-Spoke-Datenverkehr bei Bedarf direkte Tunnel aufbauen kann, anstatt stets über den Hub geroutet zu werden.

---

## Fazit

Fortinet SD-WAN ist die richtige Wahl, wenn Security und SD-WAN als einheitliche Funktion und nicht als nebeneinanderstehende Produkte agieren sollen. Die FortiOS-Integration bietet echten betrieblichen und wirtschaftlichen Nutzen für Unternehmen, die bereit sind, in diese Plattform zu investieren. Dieselbe DPI, die Anwendungen für das Traffic Steering identifiziert, setzt auch die Firewall-Policy durch – ohne Redundanz, ohne Performance-Einbußen.

Der Kompromiss besteht im Bekenntnis zum Ökosystem. Fortinet SD-WAN entfaltet sein volles Potenzial am besten in Fortinet-Umgebungen. Organisationen mit erheblichen bestehenden Investitionen in die Sicherheitsinfrastruktur anderer Hersteller sollten prüfen, ob der FortiOS-zentrierte Ansatz am Ende mehr Komplexität erzeugt als löst.

Im Gartner Magic Quadrant spiegelt Fortinets dauerhafte Platzierung unter den Leaders eine Plattform wider, die ihr Kernversprechen einlöst: Sicherheit und Konnektivität aus einem einzigen Betriebssystem – skalierbar über Hunderte oder Tausende von Standorten hinweg.

---

*Als Nächstes in dieser Serie: [Cisco SD-WAN — Catalyst SD-WAN and the Enterprise Architecture Approach](/en/posts/cisco-sd-wan/)*
