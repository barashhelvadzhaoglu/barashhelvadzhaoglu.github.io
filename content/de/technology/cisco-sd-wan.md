---
title: "Cisco SD-WAN: Catalyst SD-WAN und der Enterprise-Architekturansatz"
seoTitle: "Cisco SD-WAN Review | Catalyst SD-WAN, Viptela-Architektur & Enterprise-Use-Cases"
description: "Ein detaillierter Blick auf Ciscos SD-WAN-Plattform: die Viptela-Übernahme, die Catalyst SD-WAN-Architektur, vManage und wie sich Ciscos Ansatz im Enterprise-Umfeld gegenüber dem Wettbewerb behauptet."
date: 2026-10-29T08:37:33+01:00
keywords:
  - Cisco SD-WAN
  - Catalyst SD-WAN
  - Cisco Viptela
  - vManage SD-WAN
  - Cisco SASE
  - Cisco SD-WAN-Architektur
  - Cisco ThousandEyes SD-WAN
  - Enterprise SD-WAN
tags:
  - SD-WAN
  - Cisco
  - Netzwerk
draft: false
---

# Cisco SD-WAN: Catalyst SD-WAN und der Enterprise-Architekturansatz

Ciscos Weg zu SD-WAN führte über eine der bedeutendsten Akquisitionen im Enterprise-Networking-Bereich des letzten Jahrzehnts. 2017 übernahm Cisco Viptela – ein dediziertes SD-WAN-Startup – für rund 610 Millionen US-Dollar. Diese Akquisition bildete das Fundament für das, was Cisco heute als **Catalyst SD-WAN** bezeichnet (zuvor bekannt als Cisco SD-WAN und davor als Viptela SD-WAN). Ein Verständnis des Viptela-Erbes hilft dabei, sowohl die architektonischen Stärken als auch die operationelle Komplexität zu verstehen, die Ciscos Plattform heute prägen.

---

## Die Viptela-Architektur

Viptela wurde von Grund auf als verteiltes, skalierbares SD-WAN-Fabric konzipiert. Das Kerndesign unterteilte die WAN-Architektur in vier funktionale Ebenen (Planes):

**vManage** – die zentrale Management- und Orchestrierungsebene. Ein zentrales Dashboard für Konfiguration, Monitoring und Policy-Management über alle SD-WAN-Standorte hinweg. vManage ist die primäre Schnittstelle für Netzwerkadministratoren.

**vSmart Controller** – die Control Plane. Verteilt Routing-Informationen und SD-WAN-Policies an alle Edge-Devices über das Overlay Management Protocol (OMP). vSmart leitet keinen Datenverkehr weiter – er steuert lediglich, wohin der Datenverkehr fließt.

**vBond** – die Orchestration Plane. Vermittelt die initiale Verbindung zwischen Edge-Geräten und dem restlichen SD-WAN-Fabric und übernimmt NAT-Traversal sowie die Authentifizierung. Sobald die Edges eingerichtet sind, ist die Rolle von vBond minimal.

**vEdge / Catalyst SD-WAN Router** – die Data Plane an jedem Standort. Cisco bietet die SD-WAN-Funktionalität mittlerweile auf Routern der Catalyst 8000-Serie und ISR-Routern (über SD-WAN-Software) sowie als Virtual Appliances für Cloud-Deployments an.

Diese Vier-Komponenten-Architektur ist komplexer als bei manchen konkurrierenden Plattformen – Fortinets FortiOS beispielsweise integriert alle SD-WAN-Funktionen in ein einziges OS-Image. Sie wurde jedoch gezielt für Skalierbarkeit entwickelt. Sehr große Deployments mit Tausenden von Standorten profitieren von der Trennung der Zuständigkeiten (Separation of Concerns): Die Control Plane skaliert horizontal, ohne die Data-Plane-Performance zu beeinträchtigen.

---

## OMP: Das Fabric-Protokoll

OMP (Overlay Management Protocol) ist das Protokoll, das das Cisco SD-WAN-Fabric zusammenhält. Es läuft zwischen vSmart-Controllern und allen vEdge/Catalyst-Routern und verteilt:

- Routing-Informationen (ähnlich wie BGP-Route-Advertisements)
- SD-WAN-Policies (Application-Aware-Routing-Regeln, Data Policies)
- Sicherheitsinformationen (Security Associations für IPsec-Tunnel)

Dieses zentrale Verteilungsmodell führt dazu, dass sich Policy-Änderungen schnell und konsistent über alle Standorte hinweg propagieren. Wenn ein Network Engineer in vManage eine Application-Aware-Routing-Policy ändert, pusht vSmart die aktualisierte Policy automatisch an alle betroffenen Edges. Es ist nicht notwendig, einzelne Geräte manuell anzupassen.

Die IPsec-Tunnel zwischen den Edges werden auf Basis der von OMP verteilten Informationen aufgebaut und unterstützen **BFD (Bidirectional Forwarding Detection)** für die Verbindungsqualitätsüberwachung im Subsekundenbereich – der Mechanismus, der ein schnelles Path-Failover ermöglicht, wenn ein WAN-Link degradiert.

---

## Application-Aware Routing in Catalyst SD-WAN

Ciscos Application-Aware Routing funktioniert auf konzeptioneller Ebene ähnlich wie bei anderen SD-WAN-Herstellern, weist jedoch einige charakteristische Implementierungsmerkmale auf:

**Anwendungsidentifikation** nutzt Ciscos NBAR2-Engine (Network-Based Application Recognition) – eine der ausgereiftesten Technologien zur Anwendungsklassifizierung in der Branche, gestützt auf eine kontinuierlich aktualisierte Bibliothek von Tausenden Anwendungssignaturen. NBAR2 erkennt Anwendungen, die dynamische Ports, verschlüsselte Protokolle oder Cloud-Anwendungsvarianten nutzen.

**SLA-Klassen** definieren akzeptable Performance-Schwellenwerte (Latenz, Jitter, Paketverlust) für jede Verkehrskategorie. Fällt die gemessene Leistung eines WAN-Tunnels unter den SLA-Schwellenwert, erfolgt automatisch ein Failover des betroffenen Verkehrs auf einen Tunnel, der die Anforderungen erfüllt.

**Data Policies** ermöglichen ein feingranulares Traffic Steering über einfache SLA-Matches hinaus – sie können Datenverkehr basierend auf Quelle/Ziel, Anwendung, DSCP-Wert oder einer Kombination daraus steuern und Direct Internet Access (DIA), Service Chaining über Security Appliances oder Backhauling über einen Hub erzwingen.

---

## ThousandEyes-Integration: Visibility über das WAN hinaus

Ein Alleinstellungsmerkmal der SD-WAN-Plattform von Cisco ist die Integration mit **ThousandEyes** – der Plattform für Internet- und Cloud-Intelligence, die Cisco 2020 übernommen hat.

ThousandEyes bietet End-to-End-Visibility über das Internet und Cloud-Provider-Netzwerke hinweg, nicht nur über das Enterprise-WAN. Im SD-WAN-Kontext bedeutet dies: Cisco-Kunden sehen nicht nur, dass ihr MPLS-Link nach Frankfurt 5 % Paketverlust aufweist, sondern auch, dass das Azure ExpressRoute-Peering in Frankfurt überlastet ist und die Microsoft 365-Performance für alle Benutzer an einem Standort beeinträchtigt – noch bevor beim Helpdesk die ersten Tickets eingehen.

Diese Visibility-Ebene erweitert das Monitoring der Anwendungs-Performance weit über das hinaus, was eine reine On-Premises-SD-WAN-Plattform eigenständig erfassen kann. Für Großunternehmen mit komplexen Cloud-Abhängigkeiten liefert die ThousandEyes-Integration wertvollen Kontext für das Troubleshooting, den konkurrierende SD-WAN-Hersteller mit ihren nativen Bordmitteln nicht bieten können.

---

## Catalyst 8000-Serie: Die Hardware-Plattform

Ciscos primäre Hardwareplattform für SD-WAN-Edge-Deployments ist die **Catalyst 8000-Serie**, die die ISR 4000-Serie im Branch-Portfolio von Cisco abgelöst hat. Auf dem Catalyst 8000 läuft IOS XE mit dem SD-WAN-Software-Stack, wodurch das vertraute Cisco IOS-Routing-Featureset mit SD-WAN-Overlay-Funktionen kombiniert wird.

Wesentliche Vorteile des SD-WAN-Betriebs auf dem Catalyst 8000:
- Volles IOS XE-Featureset parallel zu SD-WAN: OSPF, BGP, EIGRP für das Underlay-Routing; HSRP/VRRP für LAN-Redundanz; QoS mit MQC
- Hardwarebasiertes Forwarding mit Ciscos QuantumFlow-Prozessoren
- Dasselbe Gerät kann an kleineren Standorten als WAN-Router, SD-WAN-Edge und LAN-Distribution-Router fungieren
- Vertrautes Betriebsmodell für Organisationen mit bestehender Cisco IOS-Expertise

Cisco bietet zudem **Catalyst SD-WAN Virtual** (ehemals vEdge Cloud) für Deployments in AWS, Azure und Google Cloud an – wodurch sich das SD-WAN-Fabric nativ in Cloud-Umgebungen erweitern lässt.

---

## Cisco SASE: Umbrella- und Meraki-Integration

Ciscos SASE-Strategie basiert im Kern auf **Cisco Umbrella** für Cloud-delivered Security (DNS Security, Secure Web Gateway, CASB, ZTNA) in Kombination mit Catalyst SD-WAN am WAN-Edge. Diese Integration ermöglicht es SD-WAN-Policies, internetgebundenen Datenverkehr von Branch-Standorten direkt zum nächstgelegenen Umbrella-PoP zur Überprüfung zu leiten, ohne dass ein Backhaul zu einem zentralen Rechenzentrum erforderlich ist.

Für einfachere Deployments bietet Cisco Meraki eine Cloud-managed SD-WAN-Alternative mit einem deutlich unkomplizierteren Betriebsmodell, wenngleich mit weniger erweiterten Funktionen als Catalyst SD-WAN. Meraki zielt auf den Mittelstand sowie verteilte Retail- und Hospitality-Umgebungen ab, in denen operative Einfachheit schwerer wiegt als Funktionstiefe.

---

## Wo Cisco SD-WAN überzeugt

**Große Enterprise-Umgebungen mit bestehender Cisco-Infrastruktur**
Unternehmen, die Cisco Catalyst Switching, Cisco Wireless (DNA Center), Cisco ISE für NAC und Cisco Firewalls einsetzen, ziehen den größten Nutzen aus Catalyst SD-WAN. Die Integration zwischen SD-WAN und Cisco DNA Center ermöglicht Intent-based Networking simultan über Campus und WAN. Einmal im DNA Center definierte Policies greifen konsistent vom Access Layer bis zum WAN-Edge.

**Komplexe Routing-Anforderungen**
Catalyst SD-WAN behält den vollständigen IOS XE-Routing-Stack bei. Zweigstellen mit anspruchsvollen Underlay-Routing-Anforderungen – BGP-Peering mit mehreren ISPs, komplexes Policy-based Routing, MPLS-VPN-Integration – sind mit Ciscos Plattform besser aufgestellt als mit Lösungen von Anbietern, deren Edge-Geräte nur eingeschränkte Non-SD-WAN-Routing-Funktionen bieten.

**Visibility und Troubleshooting im Enterprise-Maßstab**
Die Kombination aus vManage-Analytics und ThousandEyes verleiht Cisco SD-WAN ein Troubleshooting-Potenzial, das im Markt seinesgleichen sucht. Für Network Operations Teams, die die WAN-Performance für Tausende von Benutzern verwalten, rechtfertigen diese Visibility-Tools erhebliche Plattform-Investitionen.

**Regulierte Branchen mit hohen Compliance-Vorgaben**
Ciscos Positionierung im Enterprise-Segment, Audit-Trail-Funktionen in vManage und umfassende Compliance-Zertifizierungen machen Catalyst SD-WAN zu einer bewährten Wahl für Finanzdienstleister, das Gesundheitswesen und den öffentlichen Sektor mit strikten Beschaffungs- und Compliance-Anforderungen.

---

## Wo Cisco SD-WAN an Grenzen stößt

**Operative Komplexität**
Die Vier-Komponenten-Architektur (vManage, vSmart, vBond, Edges) erfordert mehr betrieblichen Aufwand als einfachere Plattformen. Das Management der vSmart-Redundanz, Zertifikats-Lifecycles und Controller-Software-Updates bringt eine Komplexität mit sich, die für kleinere Unternehmen oder Teams mit begrenzten Netzwerkressourcen eine spürbare Belastung darstellen kann.

**Kosten**
Cisco SD-WAN-Lizenzen sind kostenintensiv. Das Lizenzmodell der Plattform (DNA Software-Abonnementstufen) in Kombination mit den Hardwarekosten positioniert Catalyst SD-WAN im oberen Preissegment des Marktes. Kleine und mittelständische Unternehmen finden andernorts häufig ein besseres Preis-Leistungs-Verhältnis.

**Security-Integration**
Anders als bei Fortinet, wo SD-WAN und NGFW in einem einzigen Betriebssystem vereint sind, handelt es sich bei Ciscos SD-WAN und Security um getrennte Produkte, die über APIs und Policy-Koordination interagieren. Diese Integration funktioniert, ist jedoch nicht so nahtlos wie der Unified-Ansatz von Fortinet. Unternehmen, die eine tiefgehende Security Inspection an jeder Zweigstelle benötigen, müssen separate Security Appliances oder Cloud-delivered Security betreiben und verwalten – was zusätzliche Kosten und Komplexität verursacht.

---

## Typische Deployment-Architektur

Ein standardmäßiges Cisco Catalyst SD-WAN Deployment:

- **vManage / vSmart / vBond** als Cloud-Services gehostet (von Cisco gehostet oder selbst gehostet On-Premises/Cloud)
- **Hub-Standorte:** Catalyst 8300- oder 8500-Serie mit mehreren WAN-Links, die als regionale Hubs für Spoke-Standorte fungieren
- **Branch-Standorte:** Catalyst 8200- oder 8300-Serie mit Dual-WAN (MPLS + Broadband), automatisiert bereitgestellt via Zero-Touch-Provisioning über vManage
- **Cloud-Standorte:** Catalyst SD-WAN Virtual in AWS/Azure, um konsistente Policies über On-Premises- und Cloud-Workloads hinweg zu ermöglichen
- **Remote-Benutzer:** Cisco AnyConnect oder Cisco Secure Client mit Umbrella für Cloud-delivered Security

---

## Fazit

Cisco Catalyst SD-WAN ist eine Plattform für Enterprise-Ansprüche mit einer Funktionstiefe, die sowohl das Viptela-Erbe als auch Ciscos kontinuierliche Investitionen in die Architektur widerspiegelt. Sie glänzt in großen, komplexen Umgebungen, in denen ausgefeiltes Routing, End-to-End-Visibility und die nahtlose Integration in eine breitere Cisco-Infrastruktur entscheidend sind.

Die Kehrseite sind Kosten und Komplexität. Organisationen, die ein einfacheres Betriebsmodell, eine engere Security-Integration oder geringere Kosten pro Standort benötigen, finden in Fortinet, HPE Aruba oder Palo Alto unter Umständen eine passendere Lösung für ihre spezifischen Anforderungen.

Für Unternehmen, die bereits tief im Cisco-Ökosystem verankert sind – DNA Center, ISE, Umbrella, Catalyst Switching –, bietet Catalyst SD-WAN eine architektonische Kohärenz, die sich mit einem anderen WAN-Hersteller nur schwer nachbilden lässt.

---

*Als Nächstes in dieser Serie: [HPE Aruba SD-WAN – EdgeConnect und das Erbe der WAN-Optimierung](/en/posts/hpe-aruba-sd-wan/)*
