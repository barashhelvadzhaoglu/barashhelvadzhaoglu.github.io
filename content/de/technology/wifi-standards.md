---
title: "802.11 Standards Deep Dive: WiFi 4, 5, 6, 6E und was sich wirklich geändert hat"
description: "802.11 Wireless-Standards Deep Dive — was n, ac, ax und be liefern, OFDMA, MU-MIMO, BSS Coloring und die richtige Standardwahl."
date: 2026-05-01
draft: false

cover:
  image: "/img/postimages/wifi-80211-standards-cover.webp"
  alt: "802.11 WiFi-Standards — WiFi 4 5 6 6E Vergleich"
  relative: false

tags: ["WiFi", "802.11ax", "WiFi 6", "802.11ac", "WiFi 5", "OFDMA", "MU-MIMO", "Wireless-Standards"]
categories: ["Technologie"]
keywords:
  - 802.11ax WiFi 6 erklärt
  - WiFi 6 vs WiFi 5 Enterprise
  - OFDMA vs OFDM Wireless
  - MU-MIMO 802.11ac
  - BSS Coloring 802.11ax
  - WiFi 6E 6GHz Band
  - WiFi 7 802.11be
  - Wireless Kanalbreite 80MHz 160MHz
  - TWT Target Wake Time IoT
  - 802.11 Standard Vergleich

showToc: true
TocOpen: true
---

# 802.11 Standards Deep Dive: WiFi 4, 5, 6, 6E und was sich wirklich geändert hat

Dieser Artikel ist Teil der Enterprise-WiFi-Serie.

> **Neu im Enterprise-Wireless-Bereich?** Beginnen Sie mit der Übersicht: [Enterprise WiFi-Architektur: Von Standards bis zur Deployment](/de/technology/enterprise-wifi-architektur-vollstaendiger-leitfaden/)

---

## Das Problem mit Marketingzahlen

Jede WiFi-Generation kommt mit beeindruckenden theoretischen Durchsatzzahlen. 802.11ac versprach 3,5 Gbps. 802.11ax verspricht 9,6 Gbps. In der Praxis überschreitet ein einzelner Client in einer realen Umgebung selten 400–600 Mbps bei WiFi 5 und 800 Mbps–1,2 Gbps bei WiFi 6.

Das ist keine Täuschung — die theoretischen Raten sind unter idealen Bedingungen mathematisch korrekt. Die Lücke zwischen Theorie und Praxis entsteht, weil:

- Theoretische Raten gleichzeitig maximale Kanalbreite (160 MHz), maximale räumliche Streams (8) und maximale Modulation (1024-QAM) voraussetzen
- Echte Clients haben 1–2 räumliche Streams, nicht 8
- Die Kanalbreite durch Regulierungsregeln und Interferenzvermeidung begrenzt ist
- Signaldämpfung die Modulation mit zunehmender Entfernung auf niedrigere Raten reduziert

Was bei der Enterprise-Wireless-Auswahl wirklich wichtig ist, ist nicht der Spitzendurchsatz — es ist, wie sich der Standard unter Last, in dichten Client-Umgebungen und in überlasteten RF-Bedingungen verhält. Hier unterscheiden sich die Generationen tatsächlich.

---

## 802.11n (WiFi 4): Das Fundament

2009 veröffentlicht. Führte zwei Technologien ein, die grundlegend bleiben:

**MIMO (Multiple Input, Multiple Output):** Mehrere Antennen sowohl am AP als auch am Client übertragen und empfangen gleichzeitig auf demselben Kanal. Ein 2×2-MIMO-AP verwendet 2 Sende- und 2 Empfangsantennen und verdoppelt den Durchsatz im Vergleich zu Einantennen-Designs (SISO) effektiv. Enterprise-APs verwenden häufig 3×3 oder 4×4 MIMO.

**5-GHz-Unterstützung:** 802.11n war der erste Standard, der auf 2,4 GHz und 5 GHz betrieben. Das 5-GHz-Band hat mehr nicht überlappende Kanäle (25 vs. 3 in 2,4 GHz in den meisten Regionen) und weniger Interferenz von Nachbarnetzwerken und Mikrowellenherden.

**Kanal-Bonding:** 40-MHz-Kanäle (Verbindung zweier 20-MHz-Kanäle) verdoppelten den theoretischen Durchsatz auf Kosten der Kanalverfügbarkeit.

**Praktische Realität 2026:** 802.11n-Hardware ist End-of-Life. Jedes neue Deployment sollte mindestens 802.11ac verwenden. Das Verstehen von 802.11n ist für die Verwaltung von Legacy-Geräten relevant, die in vielen Enterprise-Umgebungen noch existieren.

---

## 802.11ac (WiFi 5): Der Wechsel zu 5 GHz

2013 (Wave 1), 2016 (Wave 2) veröffentlicht. Wesentliche Verbesserungen gegenüber 802.11n:

**Nur 5 GHz:** 802.11ac arbeitet ausschließlich auf 5 GHz. Das zwang das 2,4-GHz-Band in Legacy/IoT-Nutzung und verschob Hochdurchsatz-Clients ins weniger überlastete 5-GHz-Spektrum.

**Breitere Kanäle:** 80-MHz-Kanäle (Wave 1) und 160-MHz-Kanäle (Wave 2). Ein 80-MHz-Kanal liefert etwa 4× die Datenrate eines 20-MHz-Kanals — verbraucht aber 4× das Spektrum. In dichten Deployments mit vielen APs verursachen 80-MHz-Kanäle schwere Gleichkanal-Interferenz. Viele Enterprise-Deployments verwenden 40 MHz, um die Kanalverfügbarkeit zu erhalten.

**256-QAM:** Höhere Modulationsdichte als 802.11ns 64-QAM. Mehr Bits pro Symbol bei gleicher Signalstärke — erfordert aber bessere Signalqualität.

**MU-MIMO (Wave 2):** 802.11ac Wave 2 führte **Multi-User MIMO** für den Downlink ein. Statt zu einem Client auf einmal zu übertragen (SU-MIMO) kann der AP gleichzeitig an bis zu 4 Clients über räumliches Multiplexing übertragen.

**Die MU-MIMO-Einschränkung:** Wave 2 MU-MIMO funktioniert nur Downlink (AP zu Client). Der Uplink (Client zu AP) ist immer noch Einzelbenutzer. Clients müssen in räumlich unterschiedlichen Positionen sein, damit MU-MIMO effektiv funktioniert — in der Praxis ist der Nutzen oft weniger dramatisch als theoretisch.

**Praktische Auswirkung:** WiFi 5 bleibt der am häufigsten deployierte Enterprise-Standard. Die meisten Enterprise-APs, die zwischen 2016 und 2021 deployt wurden, sind 802.11ac Wave 2. Die Leistung ist für typische Büroarbeitslasten ausgezeichnet.

---

## 802.11ax (WiFi 6): Für Dichte entwickelt

2019 veröffentlicht. WiFi 6 zielte nicht primär auf schnelleren Einzelclient-Durchsatz — es zielte auf **Effizienz in hochdichten Umgebungen**. Das ist der entscheidende Unterschied.

### OFDMA: Die wichtigste WiFi-6-Funktion

Bei 802.11n und 802.11ac wird der Kanal jeweils einem Client zugewiesen. Selbst wenn ein Client nur eine kleine Bestätigung senden muss, hält er den Kanal, während andere Clients warten:

```
WiFi 5 (OFDM — Zeitmultiplex):
  Zeit: |─ Client A ─|─ Client B ─|─ Client C ─|─ Client A ─|
  Kanal: 100% einem Client auf einmal zugewiesen
```

WiFi 6 führte **OFDMA (Orthogonal Frequency Division Multiple Access)** ein, aus LTE/5G Mobilfunk entliehen. Der Kanal wird in Unterkanäle namens **Resource Units (RUs)** unterteilt, und mehrere Clients können gleichzeitig in verschiedenen RUs bedient werden:

```
WiFi 6 (OFDMA — Frequenz + Zeitmultiplex):
  Zeit: |─────────── Einzelne TXOP ────────────|
        | Client A | Client B | Client C       |
        | (klein)  | (klein)  | (große Daten)  |
  Kanal: gleichzeitig unter mehreren Clients unterteilt
```

**Warum das in der Praxis wichtig ist:**
- IoT-Geräte, Telefone und Tablets senden häufig kleine Pakete (Bestätigungen, Keep-Alives, Sensordaten). Unter WiFi 5 hält jede dieser kleinen Übertragungen den vollen Kanal.
- OFDMA ermöglicht dem AP, diese kleinen Übertragungen zu bündeln und mehrere Clients in der Zeit zu bedienen, die eine einzelne WiFi-5-Übertragung benötigen würde.
- In dichten Umgebungen (Konferenzräume, Klassenräume, offene Büros) reduziert das die Kanalüberlastung dramatisch und verbessert den Gesamtdurchsatz für alle Clients.

OFDMA gilt für Down- und Uplink bei WiFi 6, anders als WiFi 5s Nur-Downlink MU-MIMO.

### BSS Coloring: Gleichkanal-Interferenz reduzieren

In dichten AP-Deployments teilen benachbarte APs oft Kanäle. Bei 802.11n/ac muss ein Client-Gerät warten, wenn es Aktivität auf seinem Kanal erkennt — selbst wenn diese Aktivität von einem AP im benachbarten Gebäude stammt, der unmöglich interferieren kann.

WiFi 6 BSS Coloring weist jedem Basic Service Set eine „Farbe" (ein numerisches Tag) zu. Geräte können zwischen Übertragungen von ihrem eigenen BSS und Übertragungen von anderen BSSs, die denselben Kanal teilen, unterscheiden:

```
Ohne BSS Coloring:
  Client hört AP-1 (eigenes Netzwerk) → wartet
  Client hört AP-2 (Nachbar)          → wartet auch (unnötig)

Mit BSS Coloring:
  Client hört AP-1 (gleiche Farbe)     → wartet (relevant)
  Client hört AP-2 (andere Farbe, niedriger RSSI) → überträgt (Wiederverwendung)
```

In der Praxis verbessert BSS Coloring die räumliche Wiederverwendung in dichten Deployments — mehr APs können auf überlappenden Kanälen arbeiten, ohne übermäßige Interferenz zu verursachen.

### Target Wake Time (TWT): IoT-Akkulaufzeit

WiFi 6 führte TWT ein, das es APs ermöglicht, spezifische Aufwachzeiten für IoT- und akkubetriebene Geräte zu planen. Statt ihr Radio kontinuierlich aktiv zu halten und auf Daten zu warten, schlafen Geräte und wachen nur zu geplanten Intervallen auf.

**Enterprise-Relevanz:** Gebäude haben zunehmend WiFi-verbundene Sensoren, Kameras, Zugangskontrollleser und Asset-Tracking-Tags. TWT verlängert die Akkulaufzeit dieser Geräte dramatisch ohne ihre Funktionalität zu beeinflussen.

### 1024-QAM und höherer Durchsatz

WiFi 6 unterstützt 1024-QAM (vs. 256-QAM bei WiFi 5) — kodiert 10 Bits pro Symbol vs. 8. Etwa 25% Durchsatzverbesserung aus nächster Nähe bei ausgezeichneter Signalqualität. Für die meisten Deployments weniger bedeutend als OFDMA.

---

## 802.11ax (WiFi 6E): Das 6-GHz-Band

WiFi 6E ist 802.11ax, erweitert auf das **6-GHz-Band** (5,925–7,125 GHz in den meisten Regionen). Das 6-GHz-Band bietet:

- **1.200 MHz neues Spektrum** — verglichen mit 500 MHz in 5 GHz
- **Bis zu 59 nicht überlappende 20-MHz-Kanäle** — vs. 25 in 5 GHz (regionabhängig)
- **Keine Legacy-Geräte:** Das 6-GHz-Band ist ausschließlich WiFi 6E/7. Keine 802.11n- oder 802.11ac-Geräte dort. Keine Interferenz von älteren Protokollen.
- **Breite Kanäle ohne Überlastung:** 160-MHz-Kanäle sind in 6 GHz praktisch ohne die Kanalerschöpfung, die sie in 5 GHz verursachen.

**Die Einschränkung:** 6 GHz hat kürzere Reichweite als 5 GHz aufgrund höherer Frequenzdämpfung. Hervorragend für hochdichte Innenumgebungen, wo APs nah an Clients sind. Weniger nützlich für Außen- oder Langstrecken-Deployments.

**Client-Adoption:** WiFi-6E-fähige Clients (Smartphones, Laptops) werden bis 2026 zunehmend verbreitet. Enterprise-APs mit 6E-Unterstützung arbeiten typischerweise Tri-Band: 2,4 GHz (Legacy), 5 GHz (Mainstream) und 6 GHz (hoher Durchsatz, geringe Überlastung).

---

## 802.11be (WiFi 7): Aufkommend

802.11be / WiFi 7 wurde 2024 abgeschlossen und befindet sich bis 2026 in der frühen Enterprise-Deployment-Phase. Wichtige Innovationen:

**Multi-Link Operation (MLO):** Eine einzelne Client-Verbindung kann gleichzeitig mehrere Bänder und Kanäle nutzen — zum Beispiel gleichzeitig auf 5 GHz und 6 GHz übertragen. Das verbessert die Durchsatzaggregation und ermöglicht nahtloses Roaming zwischen Bändern ohne Verbindungsunterbrechung.

**320-MHz-Kanäle:** In 6 GHz verfügbar. Verdoppelt die Kanalbreite von WiFi 6Es 160-MHz-Maximum.

**4096-QAM:** Höhere Modulation, erfordert ausgezeichnete Signalbedingungen. ~20% Durchsatzverbesserung aus nächster Nähe gegenüber 1024-QAM.

**Enterprise-Bereitschaft:** WiFi-7-APs sind von Cisco, Aruba und anderen verfügbar. Client-Support wächst, ist aber noch nicht universal. Für neue Deployments machen WiFi-7-APs die Infrastruktur zukunftssicher, bleiben aber mit WiFi-5- und WiFi-6-Clients kompatibel.

---

## Kanalplanung: Wo Theorie auf Realität trifft

Standards zu verstehen ist nur die halbe Geschichte. Wie Sie Kanäle konfigurieren, bestimmt, ob Ihr WiFi-6-Deployment Ihr WiFi-5-Deployment übertrifft oder unterbietet.

### 2,4 GHz: Nur 3 nutzbare Kanäle

In den meisten Regionen hat 2,4 GHz 14 definierte Kanäle, aber nur **3 nicht überlappende** (Kanäle 1, 6, 11). Jeder AP auf Kanal 2, 3, 4, 5 überlappt teilweise mit Kanälen 1 und 6 — verursacht Interferenz.

In dichten Deployments ist das 2,4-GHz-Band für Hochdurchsatz-Clients im Wesentlichen nicht verwendbar. Reservieren Sie es für Legacy-Geräte und IoT, und steuern Sie fähige Clients zu 5 GHz oder 6 GHz.

### 5 GHz: Kanalbreite-Kompromisse

5 GHz hat 25 nicht überlappende 20-MHz-Kanäle (regionabhängig). Kanalbreiten:

```
20-MHz-Kanäle:   25 nicht überlappende Kanäle verfügbar
40-MHz-Kanäle:   12 nicht überlappende Kanäle
80-MHz-Kanäle:    6 nicht überlappende Kanäle
160-MHz-Kanäle:   3 nicht überlappende Kanäle
```

In einem Deployment mit 20 APs, die einen Campus abdecken, bedeutet die Verwendung von 80-MHz-Kanälen, dass nur 6 eindeutige Kanäle verfügbar sind — jeder AP ist auf einem Kanal, den sein Nachbar auch nutzt. Gleichkanal-Interferenz beeinträchtigt die Leistung.

**Enterprise-Empfehlung:** In dichten Deployments 40-MHz-Kanäle in 5 GHz verwenden, um die Kanalverfügbarkeit zu erhalten. 80 MHz+ für Bereiche mit niedriger Dichte oder 6 GHz reservieren, wo Spektrum reichlich vorhanden ist.

### Automatische Kanalzuweisung (ACA)

Enterprise-Controller (Cisco RRM, Aruba ARM) weisen Kanäle automatisch zu und passen die Sendeleistung basierend auf RF-Umgebungsmessungen an. Das ist für das initiale Deployment generell zuverlässig, sollte aber mit einem Post-Deployment-Survey validiert werden — automatische Algorithmen treffen manchmal suboptimale Entscheidungen in komplexen RF-Umgebungen.

---

## Den richtigen Standard für Ihr Deployment wählen

| Umgebung | Empfehlung | Grund |
|---|---|---|
| Neuer Enterprise-Campus | WiFi 6 Minimum, WiFi 6E bevorzugt | OFDMA-Dichtevorteil, Zukunftssicherheit |
| Hohe Dichte (Konferenz, Klassenraum) | WiFi 6 oder 6E | OFDMA für Dichte essentiell |
| IoT-lastige Umgebung | WiFi 6 | TWT für akkubetriebene Geräte |
| KMU / kleines Büro | WiFi-6-AP | Kostengünstig, unterstützt alle Clients |
| Außen / Langstrecke | WiFi 6 (5 GHz) | Bessere Reichweite als 6 GHz |
| Legacy-Gerät-lastig | WiFi-6-AP (abwärtskompatibel) | Alle 802.11-Standards abwärtskompatibel |
| Neubau, zukunftssicher | WiFi 7 | MLO, 6 GHz, 320-MHz-Kanäle |

**Wichtiger Hinweis:** WiFi-6-APs unterstützen alle vorherigen Clients — 802.11n-, 802.11ac-, 802.11ax-Clients verbinden sich alle mit demselben AP. Der AP handelt die besten gegenseitig unterstützten Fähigkeiten mit jedem Client aus.

---

## Wichtigste Erkenntnisse

- Marketing-Durchsatzzahlen sind in der Praxis nicht erreichbar — Standards nach Dichte- und Effizienzverbesserungen bewerten, nicht nach Spitzenraten.
- **OFDMA** ist WiFi 6s wirkungsvollste Innovation für Enterprise-Deployments — es transformiert, wie der Kanal in hochdichten Umgebungen geteilt wird.
- **BSS Coloring** reduziert unnötigen Kanalstreit zwischen benachbarten APs.
- **WiFi 6Es 6-GHz-Band** bietet unkongestioniertes Spektrum und praktische breite Kanäle — die bedeutendste Deployment-Verbesserung für dichte Innenumgebungen.
- **Kanalbreitenplanung** ist genauso wichtig wie der Standard — 160-MHz-Kanäle in 5 GHz schaden in dichten Deployments oft mehr als sie helfen.
- WiFi 7 / 802.11be führt MLO ein und befindet sich in früher Deployment-Phase — es lohnt sich, es für neue Infrastrukturinvestitionen zu berücksichtigen.

---

## Diese Serie

- 📖 [Enterprise WiFi-Architektur Übersicht](/de/technology/enterprise-wifi-architektur-vollstaendiger-leitfaden/) ← Beginnen Sie hier
- 🏢 [Enterprise Controller-Architektur: Cisco und Aruba](/de/technology/enterprise-wlan-controller-architektur-cisco-aruba/)
- 🏨 [WiFi-Design für KMU, Hotels und Arztpraxen](/de/technology/wifi-design-kmu-hotel-gesundheit/)
- 🔐 [WiFi-Sicherheit: WPA3, 802.1X, Rogue AP, Site Survey](/de/technology/wifi-sicherheit-wpa3-8021x-site-survey/)

## Verwandte Artikel

- 🔐 [802.1X Identitätsbasierte Architektur im Praxiseinsatz](/de/technology/identity-based-microsegmentation-8021x/) — Die Identitätsschicht für Wireless-Sicherheit
- 🏗️ [IT-Infrastruktur ist keine Produktsammlung](/de/architecture/it-infrastructure-not-a-collection-of-products/) — Systemdenken für Wireless-Design