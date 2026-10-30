---
title: "HPE Aruba SD-WAN: EdgeConnect und das Erbe der WAN-Optimierung"
seoTitle: "HPE Aruba SD-WAN im Test | EdgeConnect, Silver Peak-Architektur & SASE"
description: "Ein detaillierter Einblick in die SD-WAN-Plattform von HPE Aruba: die Übernahme von Silver Peak, die EdgeConnect-Architektur, anwendungsdefiniertes WAN und Arubas Differenzierung im Enterprise-Markt."
date: 2026-10-30T06:39:14+01:00
keywords:
  - HPE Aruba SD-WAN
  - Aruba EdgeConnect
  - Silver Peak SD-WAN
  - Aruba SD-WAN SASE
  - anwendungsdefiniertes WAN
  - Aruba Orchestrator
  - HPE Aruba SSE
  - EdgeConnect Ultra
tags:
  - SD-WAN
  - Aruba
  - HPE
  - Netzwerk
draft: false
---

# HPE Aruba SD-WAN: EdgeConnect und das Erbe der WAN-Optimierung

Die SD-WAN-Geschichte von HPE Aruba beginnt nicht bei einem klassischen Netzwerkriesen, sondern bei einem Spezialisten für WAN-Optimierung. Silver Peak Systems verbrachte Jahre damit, die anspruchsvollsten Probleme der WAN-Performance in Unternehmen zu lösen – Deduplizierung, Komprimierung, TCP-Optimierung, Anwendungsbeschleunigung –, bevor das Unternehmen auf SD-WAN umschwenkte, als der Technologiewandel den Markt reif für eine neue Architektur machte. HPE übernahm Silver Peak im Jahr 2020 für rund 925 Millionen US-Dollar und integrierte die Technologie als **Aruba EdgeConnect SD-WAN** in das Aruba-Portfolio.

Das Erbe von Silver Peak ist deshalb so bedeutsam, weil es erklärt, was das SD-WAN von Aruba von Mitbewerbern unterscheidet: ein Fundament zur WAN-Optimierung, das die meisten reinen SD-WAN-Anbieter erst später oder gar nicht entwickelt haben, kombiniert mit Arubas Campus- und Wireless-Infrastruktur für eine durchgängige End-to-End-Transparenz.

---

## EdgeConnect-Architektur

Aruba EdgeConnect ist die physische und virtuelle Appliance, die an jedem Standort die SD-WAN-Data-Plane bildet. Die Architektur trennt Management- und Datenfunktionen:

**Aruba Orchestrator** (ehemals Silver Peak Unity Orchestrator) – die zentrale Management- und Richtlinienplattform. Ob in der Cloud gehostet oder On-Premises: Orchestrator bietet intent-basierte Richtliniendefinition, Zero-Touch Provisioning und Echtzeit-Topologie-Visualisierung. Netzwerkingenieure definieren den geschäftlichen Intent – „Microsoft 365-Traffic erfordert niedrige Latenz und hohe Zuverlässigkeit“ – und Orchestrator übersetzt diesen Intent in eine SD-WAN-Konfiguration, die auf alle EdgeConnect-Appliances verteilt wird.

**Aruba EdgeConnect Appliances** – die Edge-Geräte an jedem Standort. Verfügbar als Hardware-Appliances (Modellreihen EC-US, EC-S, EC-M, EC-L, EC-XL für unterschiedliche Durchsatzanforderungen), virtuelle Appliances (für AWS, Azure, Google Cloud) sowie als reine Software-Deployments auf Standard-x86-Hardware.

**Aruba Central** – das einheitliche Management-Portal, das die Transparenz über SD-WAN hinaus auf Arubas Wireless- (APs), kabelgebundene Switching- (CX-Serie) und Sicherheitsinfrastruktur erweitert. Für Unternehmen, die Aruba im Campus, in Branches und im WAN einsetzen, bietet Central eine zentrale Betriebsansicht.

---

## Anwendungsdefiniertes WAN: Das zentrale Differenzierungsmerkmal

Arubas Marketingbegriff für seinen SD-WAN-Ansatz lautet **application-defined WAN (AD-WAN)**. Das Konzept entspricht im Wesentlichen dem Application-Aware Routing anderer Hersteller – Datenverkehr wird anhand der Anwendung identifiziert und basierend auf der Echtzeit-Verbindungsqualität gesteuert –, doch die Implementierung spiegelt die Wurzeln von Silver Peak in der WAN-Optimierung wider.

**Deep Packet Inspection und Anwendungsklassifizierung**
EdgeConnect nutzt DPI zur Klassifizierung Tausender Anwendungssignaturen. Anders als manche SD-WAN-Plattformen, die sich primär auf Ziel-IPs oder einfaches Port-Matching stützen, kann die Klassifizierungs-Engine von EdgeConnect Anwendungen innerhalb verschlüsselter Flows mithilfe statistischer Analysen und Flow-Metadaten identifizieren – und nicht nur über die Paketprüfung von Klartext-Headern.

**Kontinuierliches Monitoring der Verbindungsqualität mit Mikrosekunden-Granularität**
EdgeConnect prüft jeden WAN-Tunnel kontinuierlich in Messintervallen im Subsekundenbereich. Das System führt eine fortlaufende Übersicht über Latenz, Jitter und Paketverlust für jeden aktiven Tunnel. Dies ermöglicht Entscheidungen zur Pfadauswahl auf Basis von Daten in Beinahe-Echtzeit statt periodischer Polling-Durchschnitte. Dies ist ein direktes Erbe der WAN-Optimierungsarbeit von Silver Peak, bei der die Granularität der Latenzmessung unmittelbaren Einfluss auf Entscheidungen zur TCP-Optimierung hatte.

**First-Packet-Anwendungserkennung**
Eine praktische Einschränkung mancher SD-WAN-Plattformen besteht darin, dass die Pfadauswahl erst greift, nachdem die Anwendung identifiziert wurde – was mehrere Pakete erfordern kann. EdgeConnect von Aruba kann Entscheidungen zur Pfadauswahl für bekannte Anwendungen bereits beim ersten Paket auf Basis von Ziel und Port treffen, während DPI die Klassifizierung für den nachfolgenden Datenverkehr weiter verfeinert. Für latenzempfindliche Anwendungen wie VoIP ist das entscheidend: Die ersten Pakete eines Anrufs werden nicht suboptimal geroutet, während das System den Flow noch identifiziert.

---

## WAN-Optimierung: Was Silver Peak beigesteuert hat

Die technisch differenzierteste Funktion in Arubas SD-WAN gegenüber den meisten Mitbewerbern ist der von Silver Peak übernommene **WAN-Optimierungs-Stack**.

**Datenreduktion (Deduplizierung und Komprimierung)**
EdgeConnect verwaltet einen gemeinsamen Datenspeicher zwischen den Tunnel-Endpunkten. Wurde derselbe Datenblock bereits zuvor übertragen – was bei Dateitransfers, Backup-Traffic und Anwendungsdaten, die häufig auf geteilte Objekte verweisen, regelmäßig vorkommt –, wird lediglich eine Hash-Referenz statt des vollständigen Datenblocks übertragen. Dies kann den WAN-Bandbreitenbedarf bei geeigneten Workloads um 50 bis 90 % reduzieren.

**TCP-Optimierung**
Standard-TCP wurde für lokale Netzwerke mit geringer Latenz und minimalem Paketverlust konzipiert. Über WAN-Strecken mit hoher Latenz oder burstartigem Paketverlust führen die Congestion-Control-Mechanismen von TCP zu erheblichen Durchsatzeinbußen. Die TCP-Optimierungs-Engine von EdgeConnect fungiert als TCP-Proxy: Sie stellt der Anwendung auf beiden Seiten der WAN-Strecke einen lokalen TCP-Endpunkt bereit und nutzt zwischen den EdgeConnect-Geräten ein optimiertes Transportprotokoll. Anwendungen profitieren so von einer TCP-Performance nahe dem LAN-Niveau – unabhängig von den tatsächlichen WAN-Bedingungen.

**Anwendungsbeschleunigung**
Für spezifische Anwendungen (CIFS/SMB-Dateitransfers, MAPI für On-Premises-Exchange, Oracle Forms und weitere) enthält EdgeConnect protokollspezifische Beschleunigungsmodule, die über eine generische TCP-Optimierung hinausgehen. Diese Module verstehen die Protokolle auf Anwendungsebene und führen intelligentes Prefetching oder Caching von Daten durch.

Es ist erwähnenswert, dass sich der Wert klassischer WAN-Optimierung verschoben hat, da immer mehr Unternehmensanwendungen auf cloud-native Architekturen mit integrierter CDN-Beschleunigung und cloud-optimierten Protokollen umgestellt werden. SaaS-Anwendungen wie Microsoft 365 sind bereits für die Bereitstellung über das Internet optimiert. Der WAN-Optimierungs-Stack bleibt vor allem für Anwendungen mit älteren, WAN-sensiblen Protokollen und für Site-to-Site-Datenreplikations-Workloads von größtem Wert.

---

## Boost: Zuverlässigkeitssteigerung auf Paketebene

Arubas **Boost**-Funktion setzt bei der WAN-Zuverlässigkeit auf Paketebene statt auf Anwendungsebene an. Sie umfasst:

**Forward Error Correction (FEC):** Fügt dem Datenstrom redundante Paritätspakete hinzu, sodass der Empfänger verworfene Pakete ohne erneute Übertragung (Retransmission) rekonstruieren kann. Bei Verbindungen mit moderatem Paketverlust (1–3 %) kann FEC einen effektiven Paketverlust von nahezu null wiederherstellen – ohne die Round-Trip-Verzögerung einer TCP-Retransmission.

**Packet Order Correction:** Bringt Pakete, die in falscher Reihenfolge eintreffen, beim Empfänger wieder in die korrekte Reihenfolge, bevor sie an die Anwendung weitergeleitet werden. Dies ist besonders relevant für Breitbandverbindungen, die Pakete gelegentlich asynchron zustellen.

**High Availability (HA) Tunneling:** Leitet Kopien latenzempfindlicher Pakete gleichzeitig über zwei verschiedene WAN-Pfade weiter und stellt diejenige Kopie zu, die zuerst eintrifft. Der effektive Paketverlust nähert sich null an; die Latenz wird durch den besseren der beiden Pfade bestimmt.

Diese Fähigkeiten sind vor allem für Sprach- und Videoanwendungen über Internet-Breitband relevant, bei denen Paketverlust und Jitter unvorhersehbar sind.

---

## Aruba SSE und SASE-Integration

Die SASE-Strategie von HPE Aruba basiert auf **Aruba SSE** (Security Service Edge) – einer Cloud-basierten Sicherheitsplattform, die Folgendes bietet:
- Secure Web Gateway (SWG)
- Cloud Access Security Broker (CASB)
- Zero Trust Network Access (ZTNA)
- Digital Experience Monitoring (DEM)

EdgeConnect SD-WAN integriert sich mit Aruba SSE, um internetgerichteten Datenverkehr von Zweigstellen zur Überprüfung an den nächstgelegenen SSE-PoP weiterzuleiten. Dies ermöglicht ein lokales Internet-Breakout (Direct Internet Breakout), ohne den Datenverkehr über die zentrale Rechenzentrums-Firewall zurückführen (backhaulen) zu müssen.

Aruba Central bietet ein einheitliches Management über EdgeConnect SD-WAN und Aruba SSE hinweg – mit einem gemeinsamen Richtlinienmodell für WAN-Routing und Cloud-Sicherheit. Dies ist Arubas Antwort auf das Problem der Management-Fragmentierung, das die meisten aus separaten Produkten zusammengestellten SASE-Architekturen betrifft.

---

## Wo HPE Aruba SD-WAN überzeugt

**Anforderungen an die WAN-Optimierung**
Unternehmen mit erheblicher Site-to-Site-Datenreplikation, Legacy-Anwendungsverkehr, der empfindlich auf WAN-Performance reagiert, oder häufigen großen Dateitransfers zwischen Standorten profitieren messbar vom WAN-Optimierungs-Stack von EdgeConnect, den die meisten konkurrierenden SD-WAN-Plattformen nicht bieten können.

**Hohe Zuverlässigkeitsanforderungen an breitbandabhängigen Standorten**
Die Kombination aus Boost FEC, Packet Order Correction und HA-Tunneling macht EdgeConnect ideal für Standorte, an denen Internet-Breitband der primäre oder einzige WAN-Uplink ist und Paketverlust oder Jitter problematisch sind – etwa im Einzelhandel, in der verteilten Hotellerie/Gastronomie oder an Standorten in Regionen mit minderwertiger ISP-Infrastruktur.

**Einheitliches Management für Aruba-Campus und WAN**
Unternehmen, die Aruba CX-Switches und Aruba-Wireless einsetzen (verwaltet über Aruba Central), erhalten operative Konsistenz, indem sie EdgeConnect im WAN nutzen. Dasselbe Aruba Central-Portal, das Campus-Switching und Wireless verwaltet, liefert auch die WAN-Transparenz und reduziert so die Anzahl der Management-Plattformen, die das Netzwerk-Betriebsteam überwachen muss.

**Intent-basiertes Managementmodell**
Das intent-basierte Richtlinienmodell des Orchestrator gehört zu den intuitivsten im SD-WAN-Markt. Das Definieren geschäftlicher Richtlinien – „Unified-Communications-Traffic priorisieren, Cloud-Pfad für SaaS nutzen, ERP über MPLS schützen“ – und die automatische Übersetzung in die Gerätekonfiguration durch das System nehmen einen Großteil der manuellen Konfigurationskomplexität pro Gerät ab. Teams mit wenig SD-WAN-Erfahrung gelangen so schneller zu einem funktionierenden Deployment als bei Plattformen, die eine detailliertere technische Richtliniendefinition verlangen.

---

## Wo HPE Aruba SD-WAN an Grenzen stößt

**Sicherheitsintegration**
Anders als beim integrierten NGFW+SD-WAN-Modell von Fortinet enthält EdgeConnect keine vollwertige NGFW. Die Sicherheit an den Zweigstellen erfordert entweder Aruba SSE (Cloud-basiert) oder die Integration einer Drittanbieter-Firewall. Für Unternehmen, die an jedem Branch-Standort eine Stateful Firewall und IPS benötigen, entsteht dadurch eine zusätzliche Komponente in der Architektur, die Fortinet nativ abdeckt.

**Marktpräsenz und Partner-Ökosystem**
Fortinet und Cisco verfügen im SD-WAN-Markt über eine größere Installationsbasis und ein breiteres Partner-Ökosystem als Aruba. Arubas SD-WAN ist technisch ausgereift, in europäischen Enterprise-Umgebungen jedoch seltener anzutreffen als Cisco- oder Fortinet-Deployments, was die Verfügbarkeit erfahrener Implementierungspartner beeinflussen kann.

**Komplexität bei kleinen Umgebungen**
Bei sehr kleinen Deployments (unter 20 Standorten) rechtfertigen die Orchestrator-Lizenzierung und der operative Overhead den Aufwand möglicherweise nicht. Die Plattform ist auf die Skalierung auf Tausende von Standorten ausgelegt; in kleinerem Rahmen bieten einfachere Plattformen unter Umständen ein angenehmeres Betriebserlebnis.

---

## Typische Deployment-Architektur

Ein typisches Deployment von HPE Aruba EdgeConnect SD-WAN umfasst:

- **Orchestrator:** Cloud-gehostet (von Aruba verwaltet) oder als On-Premises-Virtual-Appliance
- **Hub-Standorte:** EdgeConnect XL- oder EC-L-Appliances in Rechenzentren, die Spoke-Tunnel terminieren und regionales Breakout bereitstellen
- **Branch-Standorte:** EdgeConnect EC-S- oder EC-M-Appliances mit Dual-WAN, via Orchestrator per Zero-Touch bereitgestellt. Boost für Voice-/Video-Traffic über Breitband aktiviert
- **Cloud-Konnektivität:** EdgeConnect Virtual in AWS/Azure für konsistente Richtlinien in Cloud-Umgebungen
- **Internet-Sicherheit:** Aruba SSE mit lokalem Traffic-Steering von den EdgeConnect-Edges

---

## Fazit

HPE Aruba EdgeConnect SD-WAN kombiniert die ausgereiftesten WAN-Optimierungsfunktionen am Markt mit einer modernen SD-WAN-Architektur. Für Unternehmen, bei denen WAN-Optimierung nach wie vor relevant ist – Site-to-Site-Replikation, latenzempfindliche Legacy-Anwendungen, hohe Zuverlässigkeitsanforderungen über Breitband –, bietet das Erbe von Silver Peak eine echte technische Differenzierung.

Die Aruba-Integration eröffnet Unternehmen mit Campus- und Branch-Standorten einen operativ überzeugenden Weg zu einem einheitlichen Management über Wireless-, Switching- und WAN-Infrastrukturen hinweg. Bei reinen SD-WAN-Deployments in Umgebungen ohne bestehende Aruba-Infrastruktur und ohne ausgeprägte Anforderungen an die WAN-Optimierung verringert sich dieser Differenzierungsvorteil gegenüber Cisco oder Fortinet jedoch.

---

*Als Nächstes in dieser Serie: [Palo Alto SD-WAN – Prisma SD-WAN und der Security-First-Ansatz](/en/posts/palo-alto-sd-wan/)*
