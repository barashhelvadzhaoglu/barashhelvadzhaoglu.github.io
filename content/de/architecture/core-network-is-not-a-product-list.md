---
title: "Switch, Firewall, AP — Warum die richtige Produktwahl allein nicht ausreicht"
description: "Unternehmensnetzwerke scheitern an fragmentierter Architektur. Deep-Dive zu Firewall, Switching, AP-Auswahl und Kapazitätsplanung aus 11+ Jahren Praxis."
date: 2026-01-02
draft: false
author: "Barash Helvadzhaoglu"
language: "de"

cover:
  image: "/img/postimages/a-core-network-is-not-a-product-list.webp"
  alt: "Switch, Firewall, AP — Warum die richtige Produktwahl allein nicht ausreicht"
  relative: false

categories:
  - Netzwerk
  - IT-Infrastruktur
  - Netzwerkarchitektur

tags:
  - core netzwerk
  - firewall
  - switching
  - access point
  - unternehmensnetzwerk
  - netzwerkdesign
  - netzwerkarchitektur
  - vendor auswahl
  - kapazitätsplanung

keywords:
  - enterprise netzwerk design
  - firewall auswahl leitfaden
  - switch auswahl unternehmen
  - access point architektur
  - netzwerk kapazitätsplanung
  - NGFW vs UTM
  - core netzwerk architektur
  - serverraum verkabelung
  - Cisco vs Fortinet vs Palo Alto
  - netzwerk vendor vergleich
  - enterprise firewall durchsatz
  - zero trust netzwerk design
  - netzwerk segmentierung
  - SD-Access architektur

toc: true
tocopen: true
---

# Switch, Firewall, AP — Warum die richtige Produktwahl allein nicht ausreicht
## Architektur, Kapazitätsplanung und die Vendor-Realität, über die niemand spricht

Die meisten Unternehmensnetzwerkprojekte beginnen am gleichen Punkt: der Produktauswahl. Und die meisten scheitern ebenfalls dort: an Produkten, die nicht sauber miteinander arbeiten. Denn das, was wir ein „Core-Netzwerk" nennen, besteht nicht aus drei Geräten (Switch, Firewall, Access Point), die nebeneinander stehen; es sind diese drei Komponenten, die gemeinsam Identität tragen, gemeinsam segmentieren, gemeinsam Policies durchsetzen und vor allem gemeinsam den Betrieb aufrechterhalten.

Was ich seit Jahren beobachte, ist Folgendes: Unternehmen leiden nicht daran, dass ihr Netzwerk schlecht ist, sondern daran, dass der Entscheidungsmechanismus des Netzwerks fragmentiert ist. Die teuersten Geräte, die besten Lizenzen, der höchste Durchsatz – alles ist vorhanden. Doch sobald ein Incident auftritt, weiß niemand genau, welches Gerät auf welcher Basis entscheidet, wo Traffic getrennt wird, wo er kontrolliert wird. Das Ergebnis: Es gibt „ein Netzwerk", aber kein definiertes „Netzwerkverhalten".

In diesem Artikel betrachte ich das Core-Netzwerk anhand von drei Säulen: Firewall, Switching und Access (Wi-Fi). Bevor ich darauf eingehe, möchte ich jedoch eines klar festhalten: Im Auswahlprozess gibt es zwei Faktoren, die mindestens genauso entscheidend sind wie „technische Spezifikationen", die jedoch von vielen Teams erst zu spät erkannt werden: Reports/Validierung und Support/Lifecycle.

{{< figure src="/img/postimages/core-network-architecture-overview.webp" title="Core Network Architekturübersicht" >}}

## Reports filtern, Tests einordnen und Marketingrauschen ausblenden

Eine der Referenzen bei der Produktauswahl sind – ja – Gartner-Reports. Denn Berichte wie die von Gartner geben eine Vorstellung von der Marktposition eines Produkts: Wer ist Leader, wer Visionär, wer bewegt sich in einer Nische. Gerade gegenüber Entscheidern ist das hilfreich, weil es eine strukturierte Antwort auf die Frage „Warum diese Marke?" liefert.

Doch hier liegt eine kritische Falle: Gartner sagt dir nicht, welches Produkt für dein konkretes Szenario richtig ist. Gartner liefert eine Marktkarte; deine Aufgabe ist es, eine Architekturkarte zu zeichnen. Deshalb ist es sinnvoll, Gartner als ersten Filter zu nutzen: Er reduziert Optionen, trifft aber keine finale Entscheidung.

{{< figure src="/img/postimages/filtering-reports-tests-and-marketing-noise.webp" >}}

Zusätzlich zu Gartner müssen Performance- und Security-Tests von Herstellern oder unabhängigen Laboren, Vergleichsberichte und reale Benchmarks berücksichtigt werden. Denn der Durchsatz auf dem Datenblatt ist nicht identisch mit dem Durchsatz im Echtbetrieb, wenn IPS aktiv ist, SSL-Entschlüsselung läuft und Application Control eingeschaltet ist. Reports dienen hier als zweiter Filter: Sie helfen, eine nicht-marketinggetriebene Antwort auf die Frage zu finden: „Was leistet diese Box unter genau dieser Last?"

## Support und Lifecycle: die unsichtbare Säule der Architektur

Genauso wichtig wie technische Fähigkeiten sind Supportmodell und Lifecycle eines Produkts. Denn Netzwerkdesign endet nicht am Installationstag. Die eigentliche Frage lautet: Was passiert drei Jahre später?
* Wie lauten die EoL- / EoS-Daten?
* Wie schnell kommen Patches, Bugfixes und Security-Updates?
* Wie erreichbar ist der Support wirklich, und wie funktionieren Eskalationen?
* Wie realistisch sind RMA-Prozesse und Ersatzteilverfügbarkeit?
* Gibt es Lizenzüberraschungen nach einem Jahr?
* Passt die Roadmap des Herstellers zur eigenen strategischen Richtung?

Ich betone diesen Punkt bewusst, weil ich im Feld immer wieder dasselbe sehe: Teams wählen ein technisch fast passendes Produkt, doch wegen Support- oder Lifecycle-Problemen wird der Betrieb nach zwölf Monaten zur Belastung. Die Schuld wird dann dem Gerät gegeben, obwohl das eigentliche Problem die mangelnde Gewichtung des Supports in der Entscheidungsphase war.

## Firewall: UTM, NGFW oder mehrere Rollen?

Eine Firewall ist längst nicht mehr nur ein „Security-Gerät am Netzrand". Richtig positioniert wird sie zum Policy-Gehirn; falsch positioniert wird sie zum Bottleneck, auf dem alles kollabiert.

Begrifflich lohnt sich eine klare Trennung: UTM und NGFW werden in vielen Umgebungen vermischt.

Der UTM-Ansatz folgt meist der Idee „alles in einer Box": klassische Firewall, IPS, Webfilter, AV und einige Gateway-Funktionen. Gerade in kleinen und mittleren Umgebungen wird dies wegen einfacher Verwaltung und gebündelter Lizenzen bevorzugt.

NGFW hingegen ist auf Applikationssichtbarkeit, Benutzer- und Identitätskontext sowie tiefere Policy-Kontrolle ausgelegt. In modernen Enterprise-Umgebungen reicht es oft nicht mehr, Security nur anhand von Port und Protokoll zu betreiben – hier kommt NGFW ins Spiel.

Der entscheidende Punkt ist jedoch: Die Anforderungen eines Unternehmens lassen sich oft nicht mit einem einzigen „Firewall-Typ" abdecken. Eine Firewall übernimmt je nach Layer und Zweck unterschiedliche Rollen.

{{< figure src="/img/postimages/firewall-selection.webp" >}}

### Warum zwei (oder sogar drei) Firewalls im selben Unternehmen sinnvoll sind

In vielen Organisationen sind folgende Szenarien völlig legitim:
* Perimeter- / Internet-Edge-Firewall: Internetzugang, VPN, NAT, Inbound/Outbound-Policy.
* Interne Segmentierungs-Firewall (ISFW): interne Netzsegmentierung, East-West-Kontrolle, Schutz kritischer Zonen.
* Datacenter- / High-Performance-Firewall: DC-Traffic, hohe Session-Zahlen, hohe PPS, geringe Latenz.
* In manchen Architekturen zusätzliche Komponenten wie WAF oder Cloud-Firewalls.

Das bedeutet nicht „zwei Firewalls kaufen", sondern „zwei unterschiedliche Aufgaben mit passenden Werkzeugen abdecken". Wenn alles in eine Box gepackt wird, leidet entweder Performance, Manageability oder Security – meist mindestens eines davon.

> Für ein tieferes Verständnis der Sicherheitsphilosophie hinter dieser Architektur empfehle ich: [Zero Trust Mindset: Sicherheit als Architektur, nicht als Produkt](/de/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/)

Und damit sind wir direkt bei der Kapazitätsplanung.

## Firewall-Kapazitätsplanung: Durchsatz allein ist trügerisch

Der gefährlichste Fehler bei der Firewall-Auswahl ist der Fokus auf die reine Gbps-Zahl. In der Praxis scheitern Firewalls selten am Durchsatz, sondern an:
* PPS (Packets per Second)
* Anzahl gleichzeitiger Sessions
* New-Session-Rate
* NAT-Tabellen und State-Handling
* Performance mit aktivem IPS/AV/App-ID
* SSL/TLS-Entschlüsselung
* Log-Erzeugung und Log-Transport (z. B. SIEM)

{{< figure src="/img/postimages/firewall-capacity-planning.webp" title="Firewall Kapazitätsplanung Metriken" >}}

Ein reales Beispiel: Die Aussage „wir haben eine 10-Gbps-Firewall gekauft" ist isoliert wertlos. Diese 10 Gbps gelten meist nur unter Idealbedingungen. Sobald IPS, URL-Filter, Application Control und Decryption aktiv sind, sieht die Realität völlig anders aus. Die richtige Frage lautet daher:
„Wie viel Last kann diese Firewall mit genau den Security-Features und genau meinem Traffic-Profil tragen?"

Gibt es darauf keine belastbare Antwort, ist die Auswahl riskant.

## Switching: Rolle und Last sind wichtiger als Portanzahl

Switch-Auswahl beginnt häufig mit der Portanzahl: wie viele Kupferports, wie viele Glasfaserports, PoE ja oder nein. Das ist wichtig, aber aus Core-Netzwerk-Sicht nicht ausreichend. Ein Switch ist kein Verlängerungskabel; er ist ein Entscheidungspunkt für Traffic-Konzentration, -Trennung und Weiterleitung.

Ein häufiger Fehler im Access-Bereich ist die Planung nur für den Ist-Zustand. Dabei ist die Access-Schicht die dynamischste Ebene im Netzwerk. Heute reichen 1G-Kupferports, morgen hängen dort High-Density-APs oder andere Edge-Geräte. Deshalb werden Multi-Gig-Ports (2.5G/5G), PoE-Budgets pro Port und die tatsächliche Uplink-Kapazität entscheidend.

Uplinks werden oft unterschätzt. Aussagen wie „2×10G reichen" hört man häufig, ohne das Traffic-Profil zu analysieren. Mit steigender Userzahl, mehr East-West-Traffic und veränderter Broadcast-Dynamik sind diese Links schneller gesättigt als erwartet. Hier zählen nicht nur die Uplink-Geschwindigkeit, sondern auch Backplane-Kapazität und Oversubscription-Ratios des Switches.

Auch die Abgrenzung zwischen Edge- und Datacenter-Switches ist oft unscharf. Edge-Switches sind auf Portdichte und PoE optimiert, Datacenter-Switches auf hohen Durchsatz, niedrige Latenz und hohe PPS. Beides von einem Gerät zu erwarten, führt meist zu unnötigen Kosten oder zu Performanceproblemen. Die Frage „Wo steht dieser Switch und welchen Traffic trägt er?" muss vor der Frage „Wie viele Ports?" kommen.

{{< figure src="/img/postimages/switching-selection.webp" >}}

Inter-VLAN-Routing ist ebenfalls ein Architekturaspekt. Wenn Routing auf dem Switch erfolgen soll, reichen Layer-3-Fähigkeiten allein nicht aus. Route-Scale, TCAM-Kapazität, Policy-Integration und das Zusammenspiel mit der Firewall sind entscheidend. Andernfalls entsteht aus einer vermeintlichen Performance-Optimierung später eine komplexe, schwer wartbare Struktur.

## Access / Wi-Fi: Uplink und Control Plane sind Teil der Architektur

Bei WLAN wird oft über Standards gesprochen: Wi-Fi 6, 6E, 7. In der Praxis limitiert jedoch häufig nicht der Funk, sondern das Kabel. Ein leistungsfähiger Access Point ist wertlos, wenn der dahinterliegende Uplink den Traffic nicht tragen kann.

Viele Enterprise-APs können ihr Potenzial mit 1-Gbps-Uplinks nicht ausschöpfen. Deshalb sind 2.5G- und 5G-Uplinks in High-Density-Umgebungen kein Luxus, sondern Designanforderung. Doch auch hier gilt: Die Kette ist nur so stark wie ihr schwächstes Glied. Ein 2.5G-fähiger AP an einem 1G-Switchport ist eine Fehlinvestition. AP- und Switch-Auswahl müssen gemeinsam erfolgen.

{{< figure src="/img/postimages/wifi-selection.webp" >}}

Ein weiterer kritischer Punkt ist die Controller-Architektur. Anzahl unterstützter APs, gleichzeitige Clients und Roaming-Verhalten bestimmen die reale Stabilität. Ein Controller, der „500 APs" unterstützt, kann in High-Density-Umgebungen deutlich früher an Grenzen stoßen. Entscheidend sind nicht nur Lizenzen, sondern CPU, Memory, Session-Handling und Policy-Durchsetzung.

WLAN gilt oft als Edge-Thema, belastet aber das Core-Netzwerk besonders stark: mobile Clients, häufige Reauthentifizierung, intensive Policy-Zyklen. Kleine Designfehler im Access-Bereich erzeugen unerwartete Lasten im Core. AP-Auswahl ist daher keine reine Coverage-Frage, sondern eine Core-Architekturentscheidung.

## Abschluss: Vendor-Auswahl, architektonische Reife und Realität

Die folgenden Einschätzungen basieren ausschließlich auf meinen eigenen Felderfahrungen. Ziel ist weder Lob noch Kritik, sondern eine nüchterne Einordnung von Stärken und Schwächen.

Cisco ist im Switching und Routing weiterhin extrem stark, insbesondere in großen Campus- und Datacenter-Umgebungen. Wireless ist seit Jahren ausgereift. Im Firewall-Bereich hat Cisco durch Akquisitionen deutlich aufgeholt.
Gleichzeitig gilt: Eine durchgängige Cisco-Landschaft ist leistungsfähig, aber selten einfach. Integration ist möglich, erfordert jedoch Erfahrung und Aufwand.

HPE Aruba habe ich über Jahre intensiv begleitet. Das Portfolio ist durch europäische Akquisitionen und zuletzt Juniper stark gewachsen. Aruba ist im Switching breit akzeptiert, im WLAN meiner Ansicht nach branchenführend.
Historisch gab es Lücken im Routing, die sich mit Juniper weitgehend schließen dürften. Eine starke eigenständige Firewall-Familie fehlt jedoch weiterhin.

Fortinet bietet ein sehr breites Portfolio aus einer Hand. Besonders die Firewall-Kompetenz ist stark. Switching und Wireless sind später gereift, werden aber zunehmend eingesetzt.
Ein großer Vorteil ist die vergleichsweise einfache Integration und Bedienbarkeit – ein Pluspunkt für kleinere IT-Teams.

Palo Alto Networks ist im Firewall-Bereich klar führend. Switching und Wireless gehören bewusst nicht zum Fokus. Viele Organisationen setzen Palo Alto ausschließlich für Firewalls ein – aus guten Gründen.
Besonders bei Application Visibility, Policy-Tiefe und SASE sehe ich Palo Alto klar an der Spitze.

{{< figure src="/img/postimages/vendor-selection.webp" >}}

In der Praxis existieren alle Mischformen: Single-Vendor-Ansätze, Dual-Vendor-Strategien oder Best-of-Breed-Architekturen. Diese Entscheidungen sind ebenso organisatorisch wie technisch geprägt.

Meine persönliche Haltung: Wo Teams reif genug sind, profitieren Architekturen oft von spezialisierten Herstellern pro Layer. Wo Einfachheit, Klarheit und ein zentraler Supportkanal wichtiger sind, ist ein Single-Vendor-Ansatz völlig legitim.

Ein letzter Punkt ist mir besonders wichtig: Automatisierung. API-Fähigkeit ist heute kein Bonus mehr, sondern ein Auswahlkriterium. Produkte sollten nicht zuerst nach Hardware, sondern nach Automatisierbarkeit bewertet werden.

> Einen praktischen Rahmen für den Aufbau von Infrastruktur-Sichtbarkeit finden Sie hier: [Der Monitoring-Mindset: Nicht nur sehen, sondern verstehen und proaktiv handeln](/de/architecture/monitoring-mindset-not-just-seeing-but-understanding-and-acting-proactively/)

## Serverraum und Verkabelung: Die Realität, über die niemand spricht – aber jeder bezahlt

In Netzwerkprojekten stehen meist die „glänzenden" Themen im Vordergrund. Doch viele Probleme entstehen viel tiefer: im Serverraum und in der Verkabelung.

Meine Erfahrung ist eindeutig: Schlechte Serverraum- oder Kabelinfrastruktur macht jede noch so gute Architektur angreifbar. Die Symptome heißen „Netzwerkausfall", die Ursache liegt fast nie im Netzwerkdesign.

Serverräume werden oft wie Abstellräume behandelt. Racks wachsen, Kabel häufen sich, Provisorien werden dauerhaft. Irgendwann entsteht ein Raum, den niemand anfassen will – aber jeder braucht. Genau hier beginnt das Risiko.

{{< figure src="/img/postimages/server-room-and-cabling.webp" >}}

Ein Serverraum ist das Herz des Netzwerks. Kühlung, Strom, Luftführung, Zugänglichkeit und Ordnung sind keine Nebensachen. Dauerhafte Hitze verkürzt Lebensdauer und erzeugt instabile Effekte.
Auch Stromkonzepte werden unterschätzt: Redundante Netzteile ohne getrennte Stromkreise, USVs ohne Kapazitätsplanung – im Ernstfall wertlos.

Verkabelung ist die langlebigste Komponente der Infrastruktur. Geräte wechseln, Kabel bleiben. Deshalb ist Planung nur für den Ist-Zustand ein Fehler. 1G-Designs stoßen mit Multi-Gig-APs schnell an Grenzen.

Kupfer oder Glasfaser ist keine Glaubensfrage, sondern Architektur. Patchpanel-Struktur, Beschriftung und Kabelmanagement sind operative Notwendigkeiten, keine Ästhetik.

Unklare Verkabelung macht jede Änderung riskant. Falscher Port, falsches Kabel – und ein anderer Service fällt aus. Dann heißt es wieder: „Das Netzwerk war schuld."

Physische Zugriffskontrolle wird ebenfalls oft ignoriert. Ohne klare Regeln verliert jede logische Security an Bedeutung.

Aus meiner Sicht sind Serverraum und Verkabelung nicht die „unterste Schicht" der Architektur, sondern das Fundament. Eine stabile Infrastruktur wird nicht gelobt – sie fällt nicht auf. Und genau das ist ihr größter Erfolg.

## Hinweis

Dieser Artikel erschien ursprünglich in kürzerer, erzählerischer Form auf **Substack**.
Diese Version erweitert die architektonische Grundlage der Serie.

👉 **Lesen Sie den Artikel auf Substack:** [Hier klicken](https://substack.com/home/post/p-183952844)

---

## Verwandte Artikel

Wenn Ihnen dieser Artikel gefallen hat, könnten auch diese Beiträge interessant sein:

**Architektur & Sicherheitsdesign**
- 📐 [IT-Infrastruktur ist keine Produktsammlung](/de/architecture/it-infrastructure-is-not-a-collection-of-products/) — Der Grundlagenartikel dieser Serie
- 🛡️ [Zero Trust Mindset: Sicherheit als Architektur, nicht als Produkt](/de/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — Warum Zero Trust eine Philosophie und kein Produkt ist
- 📊 [Der Monitoring-Mindset: Nicht nur sehen, sondern verstehen](/de/architecture/monitoring-mindset-not-just-seeing-but-understanding-and-acting-proactively/) — Echte Transparenz in der Infrastruktur aufbauen

**Technisches Engineering**
- 🛠️ [Die Hintertür des Netzwerks: Next-Gen Console Server Architektur](/de/posts/next-gen-console-server-terminal-server-architecture/) — Out-of-Band-Zugang wenn alles andere versagt
- 🛡️ [Network Packet Broker (NPB) Masterclass](/de/posts/network-packet-broker-npb-masterclass/) — Erweiterte Traffic-Sichtbarkeit und Sicherheitsstrategie
- 🔐 [802.1X Projekte erfolgreich umsetzen: Praxiseinblicke](/de/posts/unlocking-success-in-802-1x-projects-field-insights/) — Identitätsbasierter Zugang in Unternehmensnetzwerken
- ⚙️ [Nexus Software Upgrade Guide](/de/posts/cisco-nexus-nxos-upgrade-guide/) — NX-OS Upgrade ohne Ausfallzeit