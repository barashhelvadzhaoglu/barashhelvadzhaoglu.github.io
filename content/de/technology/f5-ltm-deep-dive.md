---
title: "F5 LTM Deep Dive: Virtual Server, iRules, SSL Offloading & HA"
description: "F5 BIG-IP LTM Deep Dive — Full-Proxy-Architektur, Virtual Server, Pool-Konfiguration, iRules, SSL Offloading und Zero-Downtime-Migration."
date: 2026-04-08
draft: false

cover:
  image: "/img/postimages/f5-ltm-deep-dive-cover.webp"
  alt: "F5 BIG-IP LTM Deep Dive — Virtual Server, iRules, HA"
  relative: false

tags: ["F5", "LTM", "BIG-IP", "iRules", "SSL Offloading", "Load Balancing", "High Availability", "TMOS"]
categories: ["Technologie"]
keywords:
  - F5 LTM Virtual Server Konfiguration
  - F5 iRule Beispiele
  - F5 SSL Offloading
  - F5 BIG-IP Pool Health Monitor
  - F5 Session Persistence Cookie
  - F5 LTM High Availability
  - F5 TMOS Migration
  - F5 Full Proxy Architektur
  - F5 Aktiv-Standby Failover
  - F5 2000 5000 Migration

showToc: true
TocOpen: true
---

# F5 LTM Deep Dive: Virtual Server, iRules, SSL Offloading & HA

Dieser Artikel ist Teil der F5 BIG-IP-Serie.

> **Neu bei F5?** Beginnen Sie zuerst mit der Plattformübersicht: [F5 BIG-IP ist kein Load Balancer — Es ist eine Application Delivery Platform](/de/technology/f5-bigip-application-delivery-platform-overview/)

Wenn Sie das Gesamtbild bereits kennen und tief in LTM eintauchen möchten — Konfiguration, iRules, Migrations-Praxisnotizen — sind Sie hier richtig.

---

## Die Full-Proxy-Architektur: Warum sie alles verändert

Das Wichtigste an LTM ist, dass es ein **Full-Proxy** ist. Das ist kein Marketingbegriff — er hat direkte betriebliche Konsequenzen, die LTM von jedem einfacheren Load Balancer unterscheidet.

Wenn ein Client durch F5 LTM verbindet, gibt es zwei vollständig separate TCP-Verbindungen:

```
Client ──[TCP-Verbindung 1]──→ F5 LTM ──[TCP-Verbindung 2]──→ Backend-Server
         (Virtual Server IP)             (Pool Member IP)
```

F5 beendet die Client-Verbindung vollständig, inspiziert sie, trifft alle Routing- und Policy-Entscheidungen und öffnet dann eine neue Verbindung zum Backend. Client und Backend-Server kommunizieren niemals direkt.

Dies gibt LTM Fähigkeiten, die Pass-Through Load Balancer nicht bieten können:
- Vollständige Sichtbarkeit auf jedes Byte von Anfrage und Antwort
- Möglichkeit, jeden Teil des Datenverkehrs neu zu schreiben — Header, URIs, Cookies, Antwort-Bodies
- SSL-Terminierung im Namen der Backends — Backends sehen unverschlüsseltes HTTP
- Unabhängige TCP-Anpassung für client- und serverseitige Verbindungen
- Verbindungsmultiplexing und HTTP-Pipelining-Optimierungen

In der Praxis bedeutet die Full-Proxy-Position, dass Probleme upstream (clientseitig) und downstream (serverseitig) vollständig isoliert sind. Dies vereinfacht die Fehlerbehebung bei Produktionsvorfällen erheblich.

---

## Virtual Server: Der Einstiegspunkt

Ein **Virtual Server** ist die IP-Adresse und Port-Kombination, zu der Clients verbinden. Es ist das primäre Objekt in LTM und der Container für alle Traffic-Policies:

```
Virtual Server: vs_webapp_443
  Ziel-IP:              10.10.1.100
  Port:                 443
  Protokoll:            TCP
  HTTP-Profil:          http_profile_xforward
  SSL-Client-Profil:    clientssl_webapp
  SSL-Server-Profil:    serverssl_backend
  Standard-Pool:        pool_webapp_8080
  Persistence:          cookie_persistence
  iRule:                /Common/rule_uri_routing
```

**Eine VIP, mehrere Anwendungen:** Eine einzelne Virtual-Server-IP kann mehrere Anwendungen bedienen, indem iRules verwendet werden, um basierend auf dem HTTP-Host-Header oder URI-Pfad zu routen. Dies reduziert den IP-Verbrauch und vereinfacht Upstream-Firewall-Regeln.

**Virtual-Server-Status ist unabhängig von der Pool-Gesundheit:** Wenn ein Virtual Server deaktiviert ist, erreicht kein Datenverkehr den Pool — unabhängig davon, ob Pool-Members gesund sind. Überwachen Sie die Virtual-Server-Verfügbarkeit immer separat von der Pool-Member-Verfügbarkeit.

**Drei Virtual-Server-Typen:**
- **Standard** — Full Proxy, der häufigste Typ
- **Performance Layer 4** — umgeht den Proxy für Hochdurchsatz-Szenarien, bei denen L7-Inspektion nicht benötigt wird
- **Forwarding** — Pass-Through-Routing ohne Proxy-Verhalten, für transparente Deployments verwendet

---

## Pools und Load-Balancing-Methoden

Ein **Pool** ist die Gruppe der Backend-Server, auf die der Virtual Server den Datenverkehr verteilt:

```
Pool: pool_webapp_8080
  Load-Balancing-Methode: Least Connections (member)
  Slow Ramp Time:         30 Sekunden
  Monitor:                http_monitor_webapp
  Members:
    192.168.10.11:8080   Prioritätsgruppe: 1
    192.168.10.12:8080   Prioritätsgruppe: 1
    192.168.10.13:8080   Prioritätsgruppe: 2  ← Standby, aktiviert nur wenn Gruppe 1 ausfällt
```

**Load-Balancing-Methoden im Vergleich:**

- **Round Robin** — sequenzielle Verteilung. Funktioniert für zustandslose, einheitliche Workloads. Schlechte Wahl, wenn Verbindungsdauern erheblich variieren.
- **Least Connections (member)** — sendet an das Member mit den wenigsten aktiven Verbindungen. Am besten für Anwendungen mit variablen Sitzungslängen. Standardwahl in den meisten Produktionsumgebungen.
- **Least Connections (node)** — zählt Verbindungen über alle Pools zu einer Server-IP, nicht nur in diesem Pool. Verwenden wenn ein Server in mehreren Pools teilnimmt.
- **Ratio** — gewichtete Verteilung. Member A erhält 3× mehr Verbindungen als Member B. Für Server mit unterschiedlichen Kapazitäten.
- **Fastest** — sendet an das zuletzt antwortende Member. Kann Hot Spots erzeugen; verwenden Sie stattdessen Observed für mehr Stabilität.

**Slow Ramp Time** wird zu wenig genutzt, ist aber wichtig. Wenn ein Pool-Member von einem Ausfall wiederhergestellt wird, ist es sofort verfügbar — aber möglicherweise noch nicht vollständig aufgewärmt (JVM, Caches, Datenbankverbindungspools). Slow Ramp Time erhöht das Gewicht eines neu verfügbaren Members schrittweise über die angegebenen Sekunden und verhindert, dass ein kalter Server sofort überflutet wird.

**Prioritätsgruppen** ermöglichen aktive und Standby-Member-Sets innerhalb eines Pools. Gruppe-1-Members erhalten den gesamten Datenverkehr, solange sie über dem Schwellenwert für minimale aktive Members liegen. Gruppe-2-Members aktivieren automatisch, wenn Gruppe 1 unter den Schwellenwert fällt.

---

## Health Monitors: Wichtiger als die Load-Balancing-Methode

Ein Pool-Member kann TCP-erreichbar und auf Anwendungsebene vollständig defekt sein. Ein Zahlungsverarbeitungsserver, der bei jeder Anfrage HTTP 500 zurückgibt, ist immer noch TCP-erreichbar — ein einfacher TCP-Monitor wird das Problem niemals erkennen.

Das ist das häufigste Ausfallszenario, das ich in Produktionsumgebungen gesehen habe, und der häufigste Ort, an dem Teams zu wenig investieren.

### TCP-Monitor: Notwendig, aber unzureichend

```
Monitor: tcp_monitor_basic
  Typ:       TCP
  Interval:  5 Sekunden
  Timeout:   16 Sekunden
```

Erkennt: Netzwerkkonnektivitätsverlust, Server-Abstürze, Port nicht lauschend.

Erkennt nicht: Anwendungsfehler, Datenbankverbindungsfehler, Speichererschöpfung, teilweise initialisierte Anwendungszustände.

### HTTP-Monitor: Der Produktionsstandard

```
Monitor: http_monitor_webapp
  Typ:            HTTP
  Send String:    GET /health HTTP/1.1\r\nHost: webapp.internal\r\nConnection: close\r\n\r\n
  Receive String: "status":"healthy"
  Interval:       5 Sekunden
  Timeout:        16 Sekunden
```

LTM markiert das Member nur dann als UP, wenn der Antwort-Body die exakt erwartete Zeichenfolge enthält. Die Anwendung muss aktiv bestätigen, dass sie gesund ist — nicht nur, dass der Port offen ist.

Ein guter `/health`-Endpunkt prüft: Datenbankverbindung, Cache-Verfügbarkeit, Status wichtiger Abhängigkeiten und Speicherplatz falls relevant. Eine Anwendung, die HTTP 200 mit `{"status":"degraded"}` zurückgibt, sollte die Monitor-Prüfung nicht bestehen.

### HTTPS-Monitor für verschlüsselte Backends

```
Monitor: https_monitor_webapp
  Typ:          HTTPS
  SSL-Profil:   serverssl_monitor (für selbstsignierte Zertifikate intern konfigurieren)
  Send String:  GET /health HTTP/1.1\r\nHost: webapp.internal\r\n\r\n
  Receive String: "status":"healthy"
```

### Die Timeout-Formel

Eine häufige Fehlkonfiguration: Timeout ≤ Interval setzen. Die korrekte Formel:

```
Timeout = (Interval × Wiederholungen) + 1
```

Mit Interval=5 und 3 Wiederholungen: Timeout = 16. Dies gibt LTM Zeit für Wiederholungsversuche, bevor das Member als ausgefallen markiert wird, und vermeidet Falschpositive durch vorübergehende Netzwerkschwankungen.

---

## SSL Offloading und SSL Bridging

### SSL Offload (nur Client-SSL)

```
Client ──(HTTPS/TLS 1.3)──→ F5 LTM ──(HTTP)──→ Backend
```

F5 beendet TLS vom Client und leitet unverschlüsseltes HTTP an Backends weiter. Maximale Backend-CPU-Einsparung. Erfordert ein **Client-SSL-Profil** auf dem Virtual Server:

```
Client-SSL-Profil: clientssl_webapp
  Zertifikat:  /Common/webapp_cert
  Schlüssel:   /Common/webapp_key
  Kette:       /Common/intermediate_ca
  Cipher:      TLSv1.2:TLSv1.3
  Optionen:    Kein TLSv1, Kein TLSv1.1
```

### SSL Bridging (Client + Server SSL)

```
Client ──(HTTPS/TLS 1.3)──→ F5 LTM ──(HTTPS/TLS)──→ Backend
```

F5 entschlüsselt, inspiziert und verschlüsselt dann erneut für das Backend. Erforderlich in regulierten Umgebungen (Banking, Gesundheitswesen), wo Compliance Ende-zu-Ende-Verschlüsselung vorschreibt. Fügt etwas Latenz hinzu — zwei TLS-Handshakes pro Verbindung — bietet aber vollständige Compliance und Sichtbarkeit.

In der Banking-Umgebung liefen alle Produktions-Virtual-Server mit SSL Bridging. Jede Verbindung wurde entschlüsselt, vom WAF inspiziert und zum Backend neu verschlüsselt.

### Zertifikatsverwaltung

Wichtige betriebliche Punkte:
- F5 warnt standardmäßig nicht, wenn Zertifikate dem Ablauf nähern. Externes Monitoring (SolarWinds, Zabbix) einrichten, um den Zertifikatsablauf auf Virtual Servern zu prüfen.
- Zertifikatsaustausch erfolgt ohne Downtime: Zertifikatsobjekt aktualisieren, das Profil referenziert es automatisch.
- **SNI** ermöglicht es einer einzelnen VIP, mehrere Anwendungen mit unterschiedlichen Zertifikaten zu bedienen.

---

## Session Persistence

### Cookie Persistence (Empfohlen)

F5 fügt ein Cookie, das das Pool-Member identifiziert, in die HTTP-Antwort ein:

```
Persistence-Profil: cookie_persistence
  Methode:     Insert
  Cookie-Name: BIGipServer_webapp
  Ablauf:      Session
  Verschlüsseln: Aktiviert
```

Bei nachfolgenden Anfragen sendet der Browser dieses Cookie. F5 leitet unabhängig von der aktuellen Lastverteilung zum richtigen Member. Für die Anwendung transparent, funktioniert durch NAT, übersteht Client-IP-Änderungen.

### Quelladress-Persistence

Leitet gesamten Datenverkehr von derselben Client-IP zum selben Member:

```
Persistence-Profil: source_addr_persistence
  Timeout: 3600 Sekunden
```

Einfach, aber problematisch, wenn viele Benutzer eine NAT-IP teilen — alle Benutzer hinter demselben NAT treffen denselben Backend-Server und brechen die Lastverteilung.

### iRule-basierte universelle Persistence

Für benutzerdefinierte Sitzungsidentifikatoren (nicht-standardmäßige Cookies, URL-Parameter, benutzerdefinierte Header):

```tcl
when HTTP_REQUEST {
  persist uie [HTTP::header "X-Session-Token"]
}
```

Persistiert basierend auf einem benutzerdefinierten Header-Wert — etwas, das kein Standardprofil unterstützt.

---

## iRules: Die programmierbare Traffic-Schicht

iRules sind Tcl-basierte Skripte, die in der TMOS-Datenebene mit Leitungsgeschwindigkeit ausgeführt werden. Sie sind der leistungsstärkste LTM-Differenziator — Traffic-Logik, die sonst Anwendungscode-Änderungen erfordern würde.

### Ereignismodell

iRules werden bei Ereignissen im Traffic-Lebenszyklus ausgeführt:
- `HTTP_REQUEST` — vollständige HTTP-Anfrage vom Client empfangen
- `HTTP_RESPONSE` — Antwort vom Backend empfangen
- `CLIENT_ACCEPTED` — TCP-Verbindung vom Client hergestellt
- `SERVER_CONNECTED` — F5 mit Backend verbunden
- `SSL_HANDSHAKE_START` — während der TLS-Verhandlung

### Produktions-iRule-Beispiele

**Client-IP-Weiterleitung an Backend:**
```tcl
when HTTP_REQUEST {
  HTTP::header insert "X-Forwarded-For"   [IP::client_addr]
  HTTP::header insert "X-Real-IP"         [IP::client_addr]
  HTTP::header insert "X-Forwarded-Proto" "https"
}
```

**URI-basiertes Pool-Routing:**
```tcl
when HTTP_REQUEST {
  if { [HTTP::uri] starts_with "/api/v2/" } {
    pool pool_api_v2_servers
  } elseif { [HTTP::uri] starts_with "/api/" } {
    pool pool_api_v1_servers
  } elseif { [HTTP::uri] starts_with "/admin/" } {
    pool pool_admin_servers
  } else {
    pool pool_web_servers
  }
}
```

**Wartungsweiterleitung wenn Pool leer:**
```tcl
when HTTP_REQUEST {
  if { [active_members pool_webapp_8080] < 1 } {
    HTTP::redirect "https://status.unternehmen.de/wartung"
  }
}
```

**Host-Header-basiertes Routing — mehrere Anwendungen auf einer VIP:**
```tcl
when HTTP_REQUEST {
  switch [HTTP::host] {
    "app1.unternehmen.de" { pool pool_app1 }
    "app2.unternehmen.de" { pool pool_app2 }
    "api.unternehmen.de"  { pool pool_api  }
    default               { pool pool_default }
  }
}
```

**Verbindungsratenbegrenzung nach Client-IP:**
```tcl
when CLIENT_ACCEPTED {
  set conn_limit 50
  if { [table lookup -notouch [IP::client_addr]] > $conn_limit } {
    reject
  } else {
    table incr [IP::client_addr]
    table timeout [IP::client_addr] 60
  }
}
```

### iRule-Leistungshinweise

iRules werden für jede Verbindung oder Anfrage durch den Virtual Server ausgeführt. Richtlinien:
- Vermeiden Sie komplexe Zeichenfolgenoperationen in hochfrequentierten iRules — verwenden Sie `table` zum Caching berechneter Werte
- Ein Syntaxfehler deaktiviert die gesamte iRule stillschweigend — zuerst in der Staging-Umgebung testen
- Verwenden Sie `log local0.debug` sparsam in der Produktion — übermäßiges Logging beeinträchtigt die Leistung
- Das `RULE_INIT`-Ereignis wird einmalig beim Start ausgeführt und ist ideal für die Initialisierung gemeinsamer Datenstrukturen

---

## High Availability: Aktiv-Standby in der Produktion

### Gerätegruppen und Traffic-Gruppen

F5 HA verwendet **Device Trust** (gegenseitige Authentifizierung zwischen Peers) und **Device Groups** (Sync-Failover-Konfiguration):

```
Gerätegruppe: dg_production
  Typ:      sync-failover
  Members:  bigip-01 (Aktiv), bigip-02 (Standby)

Traffic-Gruppe: traffic-group-1
  Floating IPs: 10.10.1.100 (VIP), 10.10.1.1 (Self IP)
  Aktiv auf:    bigip-01
```

Traffic-Gruppen enthalten die Floating IPs, die während des Failovers zwischen Geräten migrieren. Wenn bigip-01 ausfällt, übernimmt bigip-02 die Eigentümerschaft von traffic-group-1 und kündigt die VIP über Gratuitous ARP an.

### Das dedizierte Heartbeat-VLAN: Nicht verhandelbar

F5 HA verwendet Netzwerk-Failover — Heartbeat-Pakete zwischen Geräten erkennen Peer-Ausfall. Die kritische Regel:

**Verwenden Sie immer ein dediziertes Failover-VLAN, getrennt von Produktions- und Management-Netzwerken.**

Das Teilen der Produktionsschnittstelle für Heartbeat erzeugt falsche Failover-Ereignisse bei Netzwerküberlastung. Beide Geräte glauben, dass das andere ausgefallen ist, und werden gleichzeitig aktiv — Split-Brain. Datenverkehr wird dupliziert, Sitzungen brechen ab, und die Wiederherstellung vom Vorfall ist aufwendig.

```
Failover-VLAN: vlan_ha_heartbeat
  Schnittstelle:     1.3 (dediziert)
  bigip-01 Self IP:  192.168.100.1/24
  bigip-02 Self IP:  192.168.100.2/24
```

### Config Sync: Manuell vs. Automatisch

**Automatische Synchronisierung** — Änderungen am aktiven Gerät propagieren sofort zum Standby. Risiko: eine teilweise oder falsche Konfigurationsänderung propagiert, bevor Sie sie überprüfen können.

**Manuelle Synchronisierung** — Administrator löst die Synchronisierung explizit nach der Überprüfung der Änderungen aus. Sicherer für die Produktion. Standardwahl in regulierten Umgebungen.

### Verbindungsspiegelung

Standardmäßig verwirft Failover alle bestehenden Verbindungen — Clients müssen sich neu verbinden. Für die meisten Webanwendungen ist das akzeptabel.

Bei langlebigen Verbindungen (persistente WebSockets, große Dateiübertragungen, Datenbankverbindungen) hält **Verbindungsspiegelung** den Sitzungszustand auf dem Standby-Gerät aufrecht. Failover setzt diese Verbindungen mit minimalem Unterbrechung fort.

Aktivieren Sie Verbindungsspiegelung selektiv — sie verbraucht Speicher und CPU auf beiden Geräten. Nicht jeder Virtual Server benötigt sie.

---

## Praxisnotizen: Die 2000 → 5000 Migration

### Warum wir migrierten

Die BIG-IP-2000-Serie hatte zu Banking-Stoßzeiten ihre SSL-Offloading-Grenze erreicht. TMOS 13.x näherte sich dem End of Support. Die 5000er-Serie bot Hardware-SSL-Beschleunigung, 6-fache Durchsatzverbesserung und TLS-1.3-Unterstützung über TMOS 15.x.

### Zero-Downtime-Ansatz: 30+ Geräte, 0 Ausfälle

**Phase 1 — Paralleles Deployment**
5000er-Hardware neben bestehender 2000er-Serie installieren. Identische Virtual Server, Pools, Profile und iRules auf neuen Geräten konfigurieren. Noch kein Datenverkehr.

**Phase 2 — Validierung auf nicht-kritischem Virtual Server**
Eine einzelne interne Anwendung zum neuen Gerät routen. 72 Stunden überwachen: Verbindungsraten, SSL-Handshake-Latenz, Health-Monitor-Verhalten, iRule-Ausführungslogs, HA-Failover-Test unter synthetischer Last.

**Phase 3 — Schrittweise Migration nach Geschäftsrisiko**
Virtual Server in Gruppen migrieren — zuerst interne Tools, dann allgemeine Anwendungen, zuletzt Zahlungsverarbeitung. Für jede Gruppe:
- Upstream-Routing / SNAT aktualisieren, um auf neues Gerät zu zeigen
- 48 Stunden überwachen
- Altes Gerät 72 Stunden pro Gruppe als Rollback behalten

**Phase 4 — HA-Paar-Abschluss**
Nachdem alle Virtual Server auf dem neuen aktiven Gerät validiert wurden:
1. Zuerst Standby (altes Gerät) ersetzen
2. Verifizieren, dass neuer Standby Konfiguration vom Aktiven synchronisiert
3. Erzwungenes Failover — neuen Standby unter Produktionslast testen
4. Alten Aktiven außer Betrieb nehmen

**Die Regel, die es zum Funktionieren brachte: Niemals beide HA-Geräte gleichzeitig ersetzen.** Es muss immer ein vollständig validiertes, produktionserprobtes Gerät den Datenverkehr übernehmen.

### TMOS-Kompatibilitätsprüfung: Vor dem Start durchführen

iRules, die für TMOS 13.x geschrieben wurden, verhalten sich auf 15.x nicht immer identisch. Vor der Migration alle iRules auf Folgendes prüfen:

- `HTTP::`-Befehle — Verhaltensänderungen in HTTP/2-Szenarien
- `SSL::`-Ereignisse — neue Ereignisse und geänderte Timings in TLS 1.3
- `RULE_INIT`-Ausführung — Timing-Unterschiede beim Start

Wir fanden 3 iRules, die vor dem Cutover Modifikationen erforderten. Diese im Staging zu finden sparte Stunden Produktions-Incident-Response.

---

## Wichtigste Erkenntnisse

- LTM ist ein **Full-Proxy** — kein Pass-Through. Diese Unterscheidung bestimmt alle seine Fähigkeiten und Fehlerbehebungsansätze.
- **Health Monitors** sind wichtiger als die Load-Balancing-Methode. HTTP-Monitore, die Anwendungsantworten prüfen, sind immer besser als TCP-Monitore.
- **iRules** ermöglichen Traffic-Logik mit Leitungsgeschwindigkeit ohne Anwendungscode-Änderungen — der leistungsstärkste LTM-Differenziator.
- **SSL Offloading** entlastet Backends von der Verschlüsselungsarbeit. SSL Bridging ist in regulierten Umgebungen erforderlich.
- Verwenden Sie immer ein **dediziertes Heartbeat-VLAN** für HA. Geteilte Schnittstellen verursachen Split-Brain.
- Bei Migrationen: **Zuerst Standby, dann Aktiv**. Niemals gleichzeitig.

---

## Diese Serie

- 📖 [F5 BIG-IP Plattformübersicht — Alle Module](/de/technology/f5-bigip-application-delivery-platform-overview/) ← Beginnen Sie hier, wenn Sie neu bei F5 sind
- 🌐 [F5 GTM & GSLB Deep Dive](/de/technology/f5-gtm-gslb-global-traffic-management/)
- 🛡️ [F5 WAF Deep Dive](/de/technology/f5-waf-asm-advanced-waf-application-security/)

## Verwandte Artikel

- 🛠️ [Die Hintertür des Netzwerks: Next-Gen Console Server Architektur](/de/posts/next-gen-console-server-architecture/) — Out-of-Band-Zugang während F5-Wartungsfenstern
- 🛡️ [Network Packet Broker (NPB) Masterclass](/de/posts/network-packet-broker-masterclass/) — Datenverkehrssichtbarkeit neben ADC
- 🔐 [Die Zero-Trust-Mentalität](/de/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — Wo LTM in einer Zero-Trust-Architektur passt