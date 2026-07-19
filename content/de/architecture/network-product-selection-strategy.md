---
title: "Produktauswahl in der Netzwerkinfrastruktur: Strategische Kriterien und Felderfahrungen"
description: "Produktauswahl in Unternehmensnetzwerken ist mehr als eine Checkliste. Framework zur Bewertung von Firewalls, Switches und APs jenseits von Datenblättern."
date: 2026-01-02
draft: false
author: "Barash Helvadzhaoglu"
language: "de"

cover:
  image: "/img/postimages/network-product-selection-strategy.webp"
  alt: "Produktauswahl in der Netzwerkinfrastruktur: Strategische Kriterien und Felderfahrungen"
  relative: false

categories:
  - Netzwerk
  - IT-Infrastruktur
  - Netzwerkarchitektur

tags:
  - produktauswahl
  - core netzwerk
  - firewall
  - switching
  - access point
  - unternehmensnetzwerk
  - netzwerkstrategie
  - herstellerbewertung
  - kapazitätsplanung
  - felderfahrung

keywords:
  - netzwerk produktauswahl kriterien
  - unternehmensnetzwerk strategie
  - firewall hersteller bewertung
  - switch kapazitätsplanung
  - serverraum design
  - IT operative erfahrung
  - netzwerk herstellervergleich
  - Gartner netzwerk bewertung
  - firewall durchsatz realität
  - netzwerk lifecycle management
  - PoE switch planung
  - wireless controller architektur

toc: true
tocopen: true
---

# Produktauswahl in der Netzwerkinfrastruktur: Strategische Kriterien und Felderfahrungen
## Switch, Firewall und AP jenseits des Datenblatts bewerten

Die meisten Unternehmensnetzwerkprojekte beginnen am gleichen Punkt: der Produktauswahl. Und die meisten scheitern am gleichen Punkt: Produkte arbeiten nicht zusammen. Denn was wir ein "Core-Netzwerk" nennen, sind nicht nur drei Boxen nebeneinander; es geht darum, dass diese drei Komponenten gemeinsam Identität tragen, gemeinsam segmentieren, gemeinsam Policies durchsetzen und vor allem gemeinsam den Betrieb aufrechterhalten.

Was ich über die Jahre beobachte: Ein Unternehmen kämpft nicht, weil sein Netzwerk "schlecht" ist, sondern weil der Entscheidungsmechanismus des Netzwerks fragmentiert ist. Die teuersten Geräte, die besten Lizenzen, der höchste Durchsatz — alles vorhanden. Aber wenn ein Incident eintritt, weiß niemand, welches Gerät mit welchem Kontext entscheidet, wo Traffic divergiert oder wo er kontrolliert wird. Das Ergebnis: Es gibt ein "Netzwerk," aber kein "Netzwerkverhalten."

{{< figure src="/img/postimages/network-product-selection-strategy.webp" title="Strategisches Produktauswahl-Framework" >}}

In diesem Artikel teile ich ein praxiserprobtes Framework zur Bewertung von Core-Network-Produkten über drei Säulen: Firewall, Switching und Access (Wi-Fi). Aber vorab: Zwei Faktoren sind genauso entscheidend wie "technische Spezifikationen" — und die meisten Teams erkennen das zu spät: **Reports/Validierung** und **Support/Lifecycle**.

> Für die architektonische Philosophie hinter diesem Auswahlprozess: [IT-Infrastruktur ist keine Produktsammlung](/de/architecture/it-infrastructure-not-a-collection-of-products/)

## Schritt 1: Reports, Tests und Marketing-Rauschen filtern

Eine der ersten Referenzen bei der Produktauswahl sind, ja, Gartner-Reports. Sie geben eine Vorstellung von der Marktposition eines Produkts: Wer ist Leader, wer Visionär, wer spielt in einer Nische. Das ist besonders nützlich, um Entscheidungsträger zu überzeugen.

Aber es gibt eine kritische Falle: **Gartner sagt Ihnen nicht, welches Produkt für Ihr spezifisches Szenario richtig ist.** Gartner ist eine Marktkarte; Ihre Aufgabe ist es, die Architekturkarte zu zeichnen. Nutzen Sie Gartner als ersten Filter — er grenzt Optionen ein, trifft aber keine endgültige Entscheidung.

{{< figure src="/img/postimages/filtering-reports-tests-and-marketing-noise.webp" title="Reports und Marketing-Rauschen filtern" >}}

Zusätzlich zu Gartner müssen Performance- und Sicherheitstests von Herstellern oder unabhängigen Laboren, Vergleichsberichte und Real-World-Benchmarks berücksichtigt werden. Der Durchsatz auf einem Datenblatt ist nicht derselbe wie der Durchsatz in Produktion, wenn IPS aktiv ist, SSL-Entschlüsselung läuft und App-Control eingeschaltet ist.

## Schritt 2: Support und Lifecycle — Die unsichtbaren Säulen

Die technischen Fähigkeiten eines Produkts sind nur die halbe Geschichte. Das Supportmodell und der Lifecycle sind ebenso kritisch. Netzwerkdesign endet nicht am Installationstag. Die eigentliche Frage ist: **Was passiert 3 Jahre später?**

- Wie lauten die EoL / EoS-Daten?
- Wie schnell kommen Patches, Bugfixes und Security-Updates?
- Ist TAC/Support wirklich zugänglich?
- Was ist die Realität der RMA-Prozesse?
- Wird das Lizenzmodell nach Jahr eins Überraschungen bringen?
- Passt die Vendor-Roadmap zu Ihrer strategischen Richtung?

Das häufigste Problem im Feld: Das Team wählt ein technisch solides Produkt, aber weil Support/Lifecycle deprioritisiert wurde, wird der Betrieb 12 Monate später zum Alptraum. Das Gerät bekommt die Schuld — aber das eigentliche Problem war nie das Gerät.

## Schritt 3: Die Firewall-Schicht bewerten

Die Firewall hat längst aufgehört, nur ein "Sicherheitsgerät am Netzwerkrand" zu sein. Richtig positioniert ist sie das Policy-Gehirn der Architektur. Falsch positioniert wird sie zum Bottleneck.

**UTM vs. NGFW — eine notwendige Unterscheidung:**

Der UTM-Ansatz folgt der "alles in einer Box"-Philosophie: Firewall + IPS + Web-Filter + AV + Gateway-Funktionen. In kleineren Umgebungen wegen Verwaltungseinfachheit und gebündelter Lizenzierung bevorzugt.

NGFW ist um Anwendungsbewusstsein, Benutzer/Identitätskontext und tiefere Policy-Kontrolle herum positioniert. In modernen Enterprise-Umgebungen reicht die Sicherheit nur auf Port/Protokoll-Basis nicht mehr aus.

{{< figure src="/img/postimages/firewall-selection.webp" title="Firewall-Auswahl: UTM vs. NGFW vs. Multi-Rolle" >}}

**Warum zwei oder drei Firewalls in derselben Organisation normal ist:**
- **Perimeter/Internet Edge Firewall:** Internet-Egress, VPN, NAT, Inbound/Outbound-Policy
- **Internal Segmentation Firewall (ISFW):** East-West-Kontrolle, interne Segmentierung
- **Datacenter / High-Performance FW:** DC-Traffic, hohe Session-Zahlen, hohe PPS, geringe Latenz

> Für einen tieferen Blick auf Firewall-Architektur im breiteren Netzwerkdesign: [Switch, Firewall, AP — Warum die richtige Produktwahl allein nicht ausreicht](/de/architecture/core-network-is-not-a-product-list/)

## Schritt 4: Firewall-Kapazitätsplanung — Durchsatz kann lügen

Der gefährlichste Fehler bei der Firewall-Auswahl ist, sich nur auf die Gbps-Zahl zu konzentrieren. In der Praxis scheitern Firewalls selten am Durchsatz — sie scheitern an:

- PPS (Packets per Second)
- Anzahl gleichzeitiger Sessions
- New-Session-Rate
- NAT-Tabellen und State-Handling
- Performance mit aktivem IPS/AV/App-ID
- SSL/TLS-Entschlüsselungslast
- Log-Generierung und SIEM-Transport

Die richtige Frage ist immer:

> *"Mit den Sicherheitsfunktionen, die ich aktivieren werde, und meinem spezifischen Traffic-Profil — wie viel Last kann diese Firewall tatsächlich tragen?"*

Wenn es keine glaubwürdige Antwort auf diese Frage gibt, ist die Auswahl riskant.

## Schritt 5: Switch-Bewertung — Rolle und Last statt Portanzahl

Die Switch-Auswahl beginnt oft mit Portanzahlen. Diese sind wichtig — aber aus Core-Network-Perspektive nicht ausreichend. Ein Switch ist nicht nur eine Steckdose; er ist ein Entscheidungspunkt, der bestimmt, wo Traffic sich konzentriert, divergiert und nach oben getragen wird.

**Der häufigste Access-Layer-Fehler:** nur für den heutigen Bedarf planen. Der Access-Layer ist die sich am schnellsten verändernde Schicht. Multi-Gig-Ports (2,5G/5G), PoE-Nachhaltigkeit pro Port und echte Uplink-Kapazität werden kritisch.

Uplinks werden konsequent unterschätzt. "2×10G Uplinks reichen" hört man oft — ohne das Traffic-Profil zu analysieren. Backplane-Kapazität und Oversubscription-Ratios sind genauso wichtig wie die Uplink-Geschwindigkeit.

{{< figure src="/img/postimages/switching-selection.webp" title="Switch-Auswahl: Access vs. Core vs. Datacenter" >}}

Beim Entwurf des Core-Netzwerks muss die Frage **"Wo steht dieser Switch und welchen Traffic trägt er?"** vor **"Wie viele Ports hat er?"** kommen.

## Schritt 6: Wireless — Uplink und Controller-Architektur

Bei WLAN verschiebt sich der Fokus meist auf Wi-Fi-Standards: Wi-Fi 6, 6E, 7. In der Praxis wird die Wireless-Performance oft nicht durch das Radio, sondern durch das Kabel begrenzt. Viele Enterprise-APs können ihr volles Potenzial auf einem 1-Gbps-Uplink nicht ausschöpfen.

2,5G und 5G Kupfer-Uplink-Unterstützung ist in High-Density-Umgebungen kein Luxus — es ist eine Designanforderung. Und kritisch: Wenn der AP 2,5G unterstützt, aber der Switch-Port nicht, ist die gesamte Investition verschwendet. **AP- und Switch-Auswahl müssen zusammen erfolgen.**

{{< figure src="/img/postimages/wifi-selection.webp" title="Wireless-Architektur: AP, Uplink und Controller" >}}

Controller-Architektur ist ebenso kritisch. Kapazität muss über CPU, Speicher, Session-Handling und Policy-Enforcement bewertet werden — nicht nur nach Lizenzanzahl.

## Schritt 7: Herstellerbewertung — Feldrealitäten

**Cisco** bleibt einer der stärksten Akteure in Switching und Routing. Wireless ist seit Jahren ausgereift. Im Firewall-Bereich nach Akquisitionen wie Sourcefire deutlich wettbewerbsfähiger.
Vorbehalt: Eine vollständige Cisco-Umgebung ist leistungsfähig, aber selten einfach.

**HPE Aruba** ist durch Akquisitionen inklusive Juniper erheblich gewachsen. Switching weit verbreitet. Wireless nach meiner persönlichen Einschätzung einer der stärksten in der Branche.
Das Fehlen einer starken nativen Firewall-Familie bleibt eine Lücke.

**Fortinet** bietet eines der breitesten Portfolios unter einem Dach. Firewall-Kompetenz ist stark. Switching reifte später, ist aber zunehmend im Feld präsent.
Größter operativer Vorteil: relative Einfachheit der Integration und Verwaltung.

**Palo Alto Networks** ist klarer Marktführer bei Firewalls — betritt bewusst nicht Switching oder Wireless. Anwendungssichtbarkeit, Policy-Tiefe und SASE-Führerschaft sind die stärksten Differenzierungsmerkmale.

{{< figure src="/img/postimages/vendor-selection.webp" title="Herstellervergleich: Feldrealität" >}}

**Abschließender Punkt:** API-Unterstützung ist kein Bonus mehr — es ist ein Auswahlkriterium. Die Frage "Wie werde ich diese Architektur automatisiert verwalten?" sollte vor der Wahl von Switch, Firewall oder AP kommen.

## Serverraum und Verkabelung: Was niemand besprechen will, aber jeder bezahlt

In Netzwerkprojekten dominieren die "glänzenden" Themen. Aber ein erheblicher Teil der Feldprobleme beginnt an einem viel grundlegenderen Ort: Serverraum-Design und Verkabelungsinfrastruktur.

Egal wie gut die Produkte oder wie korrekt die Architektur — wenn Serverraum und Verkabelung schwach sind, wird das Netzwerk irgendwann Probleme produzieren. Diese Probleme erscheinen als "Netzwerkausfälle," aber die Grundursache ist fast nie wirklich das Netzwerk.

{{< figure src="/img/postimages/server-room-and-cabling.webp" title="Serverraum und Verkabelung: Das Fundament, über das niemand spricht" >}}

Wärme, Strom, Luftströmung, Zugänglichkeit und Ordnung müssen zusammen berücksichtigt werden. Redundante Netzteile werden gekauft, ohne zu prüfen, ob sie tatsächlich an separate Stromleitungen angeschlossen sind. Es heißt, es gibt eine USV, aber keine Kapazitätsberechnung wird durchgeführt.

Verkabelung ist die langlebigste Komponente des Netzwerks. Switches, Firewalls und APs ändern sich — Kabel bleiben. Eine 1G-Infrastruktur stößt schnell an ihre Grenzen, wenn 2,5G/5G-APs ankommen.

In meiner Sicht sind Serverraum und Verkabelung nicht die "unterste Schicht" der Architektur — sie sind das Fundament. Ein gut funktionierendes Netzwerk ist unsichtbar, weil das Fundament solide ist. Niemand bemerkt es. Und das ist meiner Meinung nach das größte Lob, das ein Infrastrukturdesign erhalten kann.

## Hinweis

Dieser Artikel wurde ursprünglich auf **Substack** in einer kürzeren, erzählerischen Form veröffentlicht.
Diese Version erweitert die architektonische Grundlage der Serie.

👉 **Lesen Sie den Artikel auf Substack:** [Hier klicken](https://substack.com/home/post/p-183952844)

---

## Verwandte Artikel

**Architektur & Strategie**
- 📐 [IT-Infrastruktur ist keine Produktsammlung](/de/architecture/it-infrastructure-not-a-collection-of-products/) — Der Grundlagenartikel dieser Serie
- 🏗️ [Switch, Firewall, AP — Warum die richtige Produktwahl allein nicht ausreicht](/de/architecture/core-network-is-not-a-product-list/) — Architektur-zuerst Core-Network-Design
- 🛡️ [Zero Trust Mindset: Sicherheit als Architektur](/de/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — Sicherheit als Architektur

**Technisches Engineering**
- 📊 [Der Monitoring-Mindset: Nicht nur sehen, sondern verstehen](/de/architecture/monitoring-mindset-not-just-seeing-but-understanding-and-acting-proactively/) — Operative Sichtbarkeit
- 🛠️ [Die Hintertür des Netzwerks: Next-Gen Console Server Architektur](/de/posts/next-gen-console-server-terminal-server-architecture/) — Out-of-Band-Zugang
- 🛡️ [Network Packet Broker (NPB) Masterclass](/de/posts/network-packet-broker-npb-masterclass/) — Traffic-Sichtbarkeit und Sicherheitsstrategie