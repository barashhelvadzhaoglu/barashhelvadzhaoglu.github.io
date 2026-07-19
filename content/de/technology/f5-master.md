---
title: "F5 BIG-IP ist kein Load Balancer — Es ist eine Application Delivery Platform"
description: "F5 BIG-IP ist mehr als ein Load Balancer. Master-Leitfaden für LTM, GTM, WAF, APM, AFM und BGP-Routing mit Links zu den Deep Dives."
date: 2026-03-27
draft: false

cover:
  image: "/img/postimages/f5-bigip-platform-overview-cover.webp"
  alt: "F5 BIG-IP Application Delivery Platform — Enterprise-Architektur Übersicht"
  relative: false

tags: ["F5", "BIG-IP", "LTM", "GTM", "WAF", "APM", "ADC", "Load Balancing", "Application Delivery", "Netzwerksicherheit"]
categories: ["Technologie"]
keywords:
  - F5 BIG-IP Übersicht
  - F5 Application Delivery Controller
  - F5 LTM GTM WAF
  - F5 APM SSL VPN
  - F5 BGP Routing
  - F5 AFM Firewall
  - F5 vs Load Balancer
  - F5 BIG-IP Module
  - Enterprise ADC
  - F5 TMOS

showToc: true
TocOpen: false
---

# F5 BIG-IP: Es ist eine Application Delivery Platform

Die häufigste Einführung in F5 in einem Unternehmen verläuft so: Jemand öffnet ein Ticket mit dem Text *„der Load Balancer ist ausgefallen"* und zeigt auf den F5. Das Problem steckt bereits in diesem Satz.

F5 BIG-IP ist kein Load Balancer. Ihn so zu nennen ist wie ein Rechenzentrum als Serverraum zu bezeichnen — technisch nicht falsch, aber es verfehlt den Kern völlig.

F5 BIG-IP ist ein **Application Delivery Controller (ADC)**: eine Full-Proxy-Plattform, die Anwendungen über lokale und globale Infrastruktur hinweg verwaltet, absichert, optimiert und hochverfügbar macht. Load Balancing ist eines von vielleicht einem Dutzend Dingen, die er tut.

---

## Wie Sie diese Serie lesen

Dieser Artikel gibt Ihnen das **Gesamtbild** — was F5 ist, wo es steht, was jedes Modul tut und wann es gegenüber Alternativen sinnvoll ist.

**Wenn Sie Netzwerk- oder Sicherheitsingenieur sind** und tief in Konfiguration, iRules, Migrations-Praxisnotizen und Architekturdetails einsteigen möchten — springen Sie direkt zum Modul, das Sie interessiert:

- 🔧 **[F5 LTM Deep Dive](/de/technology/f5-ltm-virtual-server-irules-ssl-offloading-ha/)** — Virtual Server, Pools, iRules, SSL Offloading, HA und eine Migration von 30 Geräten ohne Downtime
- 🌐 **[F5 GTM & GSLB Deep Dive](/de/technology/f5-gtm-gslb-global-traffic-management/)** — iQuery, Wide IPs, Topologie-Routing, DNS-TTL-Strategie, Multi-DC-Failover-Design
- 🛡️ **[F5 WAF Deep Dive](/de/technology/f5-waf-asm-advanced-waf-application-security/)** — ASM vs. Advanced WAF, OWASP Top 10, Bot-Abwehr, Deployment-Strategie von transparent zu blockierend

**Wenn Sie Architekt oder Entscheidungsträger sind** und bewerten, ob F5 zu Ihrer Infrastruktur passt — lesen Sie hier weiter. Dieser Artikel beantwortet diese Frage, ohne dass Sie iRule-Syntax verstehen müssen.

---

## Wo steht F5 in der Enterprise-Architektur?

F5 BIG-IP arbeitet zwischen Firewall und Anwendungsservern:

```
Internet
    │
[DDoS-Scrubbing / ISP]
    │
[NGFW — Palo Alto / Fortinet]   ← L3/L4: Routing, IP-Filterung, VPN, Stateful Inspection
    │
[F5 BIG-IP]                     ← L4–L7: Application Delivery, SSL, Gesundheit, Routing-Logik
    │
[Backend-Server / App-Cluster]
```

Die Firewall trifft Entscheidungen auf Netzwerkebene. F5 übernimmt alles oberhalb dieser Schicht — SSL-Terminierung, gesundheitsbewusstes Load Balancing, Session Persistence, Traffic-Manipulation und Layer-7-Sicherheit.

Diese Trennung ist wichtig, weil eine Firewall nicht dafür ausgelegt ist, was F5 tut. Sie kann nicht effizient Tausende von SSL-Sitzungen pro Sekunde beenden, HTTP-Antwort-Bodies für das Gesundheitsmonitoring inspizieren, Anwendungs-Header on-the-fly neu schreiben oder Routing-Entscheidungen basierend auf URI-Pfaden, Cookies oder Benutzeridentität treffen.

In einem Dual-Datacenter-Design erweitert sich die Architektur:

```
               [F5 GTM]        ← DNS-Ebene: leitet Clients zum richtigen DC
              /         \
         [DC-1]         [DC-2]
       [F5 LTM]       [F5 LTM] ← Lokal: verteilt Datenverkehr innerhalb jedes DC
           │               │
      App-Server        App-Server
```

GTM sitzt über beiden LTMs und beantwortet DNS-Abfragen — leitet Clients basierend auf Gesundheit, Last und Geografie zum geeigneten Rechenzentrum. Das macht Multi-DC-Failover automatisch statt manuell.

---

## Die vollständige Modulübersicht

TMOS (Traffic Management Operating System) ist das Fundament. Jedes F5-Modul läuft darauf. Zu verstehen, welches Modul welches Problem löst, ist der Schlüssel sowohl für das Architekturdesign als auch für Lizenzierungsgespräche.

### LTM — Local Traffic Manager

Das Kernmodul. Fast jedes F5-Deployment beginnt hier.

LTM ist ein **Full-Proxy-ADC**: Es beendet jede Client-Verbindung, inspiziert sie, trifft Routing- und Policy-Entscheidungen und öffnet dann eine neue Verbindung zum Backend. Diese Full-Proxy-Position bietet vollständige Sichtbarkeit und Kontrolle über den Anwendungsdatenverkehr.

Was LTM bietet:
- Load Balancing über Pools von Backend-Servern — mit Gesundheitsmonitoring, das Anwendungsantworten versteht, nicht nur TCP-Erreichbarkeit
- SSL/TLS Offloading — HTTPS im Namen der Backends beenden, ihre Verschlüsselungslast entfernen
- Session Persistence — Benutzer über Anfragen hinweg mit demselben Backend-Server verbunden halten
- iRules — eine programmierbare Skriptschicht, die Datenverkehr mit Leitungsgeschwindigkeit manipuliert: Header neu schreiben, nach URI routen, Inhalte einfügen, Ratenbegrenzungen erzwingen
- Hochverfügbarkeit — Aktiv-Standby- oder Aktiv-Aktiv-Clustering mit Failover unter einer Sekunde

→ **[F5 LTM Deep Dive: Virtual Server, iRules, SSL Offloading & HA](/de/technology/f5-ltm-virtual-server-irules-ssl-offloading-ha/)**

---

### GTM / DNS — Global Traffic Manager

LTM verwaltet Datenverkehr innerhalb eines Rechenzentrums. GTM verwaltet Datenverkehr **zwischen** Rechenzentren — auf DNS-Ebene.

Wenn ein Client `webapp.unternehmen.de` auflöst, beantwortet GTM die DNS-Abfrage. Die Antwort hängt davon ab, welches Rechenzentrum gesund ist, wie die aktuelle Last ist und wo sich der Client geografisch befindet.

GTMs Schlüsselfähigkeit ist **iQuery** — ein proprietäres Protokoll, das ihm Echtzeit-Anwendungsgesundheitsdaten direkt von LTM liefert. Wenn eine Backend-Anwendung ausfällt und LTM ihren Pool als ausgefallen markiert, weiß GTM das sofort und leitet neue Clients nicht mehr zu diesem Rechenzentrum, ohne auf das Ablaufen des DNS-TTL zu warten.

Was GTM bietet:
- Global Server Load Balancing (GSLB) über mehrere Rechenzentren
- Automatisches DNS-level Failover, wenn ein DC offline geht
- Topologiebasiertes Routing — europäische Benutzer zu EU-Rechenzentren, Nahost-Benutzer zu regionalen DCs
- Flexible Richtlinien: Primär bevorzugen (Global Availability), gleichmäßige Verteilung (Round Robin) oder verbindungsbewusst (Least Connections)

→ **[F5 GTM & GSLB Deep Dive: Globales Traffic-Management und DNS-Failover](/de/technology/f5-gtm-gslb-global-traffic-management/)**

---

### WAF — Web Application Firewall (ASM / Advanced WAF)

Eine Netzwerk-Firewall arbeitet auf L3/L4. Sie kann nicht inspizieren, ob ein POST-Anfrage-Body eine SQL-Injection-Payload enthält. WAF kann das.

F5 WAF sitzt inline auf dem LTM Virtual Server und inspiziert HTTP/HTTPS-Anwendungsdatenverkehr nach der SSL-Terminierung. Diese Positionierung gibt vollständige Sichtbarkeit auf entschlüsselten Inhalt.

F5 bietet zwei WAF-Stufen:
- **ASM** — signaturbasierter Schutz gegen bekannte Angriffe, OWASP-Top-10-Abdeckung, Parameter- und Cookie-Erzwingung
- **Advanced WAF** — fügt verhaltensbasierte Bot-Abwehr, Credential-Stuffing-Schutz, JavaScript-Challenges und L7-DoS-Mitigation hinzu

Was WAF schützt: SQL-Injection, XSS, CSRF, Parameter-Tampering, Cookie-Poisoning, erzwungenes Durchsuchen, Bot-Datenverkehr und Anwendungsschicht-DoS.

→ **[F5 WAF Deep Dive: Anwendungssicherheit mit ASM und Advanced WAF](/de/technology/f5-waf-asm-advanced-waf-application-security/)**

---

### APM — Access Policy Manager

APM ist F5s Identitäts- und Zugriffsmodul — wo F5 über die Datenverkehrsbereitstellung hinaus in die **Zugangskontrolle** geht.

- **SSL VPN** — vollständiger Netzwerk-Level-Fernzugang über BIG-IP Edge Client, vergleichbar mit Cisco AnyConnect oder Fortinet SSL VPN
- **Zero Trust Network Access (ZTNA)** — identitätsbewusster, anwendungsspezifischer Zugang ohne Offenlegung des gesamten Netzwerks
- **SSO** — Kerberos-, SAML-, OAuth-Integration für nahtlose Authentifizierung über Anwendungen hinweg
- **MFA-Integration** — RADIUS, LDAP, Active Directory, RSA SecurID
- **Endpoint-Inspektion** — Überprüfung der Gerätezustand (AV-Status, Patch-Level, Domain-Mitgliedschaft) vor der Zugriffsgewährung

APMs Vorteil gegenüber eigenständigen VPN-Lösungen: Es teilt dieselbe Hardware und Management-Ebene wie LTM. Eine Plattform für Application Delivery und Fernzugang.

---

### AFM — Advanced Firewall Manager

AFM fügt der F5-Plattform Netzwerk-Level-Firewall-Fähigkeiten hinzu:

- L3/L4 Stateful Packet Inspection — ähnlich einer traditionellen Netzwerk-Firewall, inline auf dem ADC betrieben
- **DoS- und DDoS-Schutz** — Ratenbegrenzung, Protokoll-Anomalieerkennung, TCP-SYN-Flood-Mitigation mit Hardwaregeschwindigkeit
- **IP-Intelligenz** — Blockierung bekannt bösartiger IPs, Tor-Exit-Nodes, Botnet-C2-Adressen über F5s Bedrohungsintelligenznetzwerke
- Network Address Translation (NAT)-Richtlinien

AFM wird eingesetzt, wenn Organisationen Firewall- und ADC-Funktionen auf einer einzigen Plattform konsolidieren möchten oder wenn der ADC selbst eine dedizierte Schutzschicht benötigt.

---

### BGP und dynamisches Routing

Eine der am wenigsten bekannten F5-Fähigkeiten: **BIG-IP betreibt einen vollständigen Routing-Stack**.

TMOS unterstützt BGP, OSPF, statische Routen mit Route Domains (VRF-Äquivalent) und ECMP. In der Praxis ist BGP am relevantesten:

- F5 kann am BGP-Routing teilnehmen und Virtual-IP-Adressen als BGP-Routen ankündigen
- In großen Enterprise- und Service-Provider-Umgebungen ermöglicht die **Anycast-VIP-Ankündigung** über BGP, dass dieselbe VIP-IP von mehreren Rechenzentren angekündigt wird — Routing leitet Clients natürlich zum nächsten gesunden Standort
- BGP-Rücknahme während Wartungsfenstern verschiebt Datenverkehr automatisch zu DR-Standorten ohne manuelle DNS-Änderungen

In der Banking-Umgebung, in der ich gearbeitet habe, verwendeten wir BGP zwischen F5 und der Kern-Routing-Schicht, um VIP-Ankündigungen während geplanter Wartung dynamisch zurückzuziehen — sauber, automatisch, keine DNS-Änderungen erforderlich.

---

### Link Controller

Link Controller verwaltet ausgehende Internetkonnektivität über mehrere ISP-Links:

- Load Balancing über mehrere Upstream-ISP-Verbindungen
- Kostenbasiertes Routing — günstigere Links bevorzugen, bei Bedarf auf Premium-Links failovern
- ISP-Gesundheitsmonitoring mit automatischer Umleitung bei Link-Ausfall

Am relevantesten für Organisationen mit mehreren ISP-Verbindungen, die intelligente Verteilung statt einfachem Aktiv-Standby möchten.

---

### iRules und iRules LX

iRules sind F5s programmierbare Datenverkehrsschicht — Tcl-basierte Skripte, die in der TMOS-Datenebene mit Leitungsgeschwindigkeit ausgeführt werden. Sie gelten modulübergreifend und können jeden Aspekt des Datenverkehrs manipulieren: Header, URIs, Cookies, Routing-Entscheidungen, SSL-Attribute.

iRules LX erweitert dies mit einer Node.js-Runtime für komplexere Logik und externe API-Integrationen.

iRules sind das, was F5 für Organisationen mit nicht-standardmäßigen Anwendungsanforderungen einzigartig flexibel macht — wenn kein Profil oder keine Richtlinie den Anwendungsfall abdeckt, kann eine iRule es normalerweise.

---

## Wann macht F5 Sinn — und wann nicht?

F5 BIG-IP ist leistungsstark, betrieblich ausgereift und teuer. Die Entscheidung für den Einsatz sollte auf spezifischen Anforderungen basieren, nicht allein auf dem Ruf.

**F5 ist die richtige Wahl, wenn:**
- Das SSL/TLS-Terminierungsvolumen hoch ist — Hardware-Beschleunigung auf physischen Appliances verarbeitet Tausende von Sitzungen pro Sekunde, die Softwarelösungen wirtschaftlich nicht erreichen können
- Anwendungen komplexe Datenverkehrslogik (iRules) erfordern, die einfachere Proxys ohne Anwendungscode-Änderungen nicht ausdrücken können
- Mehrere Rechenzentren automatisches DNS-Level-Failover (GTM) erfordern
- Regulatorische Anforderungen WAF mit detaillierten Audit-Logs vorschreiben
- Eine einzige Plattform für Application Delivery, VPN und L7-Sicherheit benötigt wird — operative Komplexität reduzieren
- Geschäftskritische Anwendungen Failover unter einer Sekunde mit Verbindungszustands-Spiegelung benötigen

**Erwägen Sie Alternativen, wenn:**
- Ihre Infrastruktur vollständig Cloud-nativ ist — AWS ALB, Azure Load Balancer oder GCP Load Balancing decken die meisten Anwendungsfälle ohne On-Premises-Hardware ab
- Datenverkehrsvolumina moderat sind und Nginx Plus oder HAProxy Ihre Anforderungen zu einem Bruchteil der Kosten erfüllen
- Anwendungen zustandslos sind und Session Persistence nicht erforderlich ist
- TCO die primäre Einschränkung ist und Open-Source-Lösungen für Ihr Team betrieblich realisierbar sind

Die ehrliche Zusammenfassung: Im Banking, Telekommunikation und großen Unternehmen mit On-Premises-Infrastruktur und geschäftskritischen Anwendungsanforderungen bleibt F5 die dominante Plattform. In Cloud-nativen oder kostenbeschränkten Umgebungen sollten Sie Alternativen ernsthaft evaluieren, bevor Sie sich auf F5-Lizenzierung festlegen.

---

## Diese Serie

Dieser Artikel ist der Ausgangspunkt. Jedes Modul hat einen eigenen Deep Dive:

- 🔧 **[F5 LTM Deep Dive: Virtual Server, iRules, SSL Offloading & HA](/de/technology/f5-ltm-virtual-server-irules-ssl-offloading-ha/)** — Full-Proxy-Architektur, Pool-Konfiguration, Health Monitors, iRule-Beispiele, Session Persistence, HA-Clustering und eine Zero-Downtime-Migration von 30 Geräten
- 🌐 **[F5 GTM & GSLB Deep Dive: Globales Traffic-Management und DNS-Failover](/de/technology/f5-gtm-gslb-global-traffic-management/)** — Wide IPs, iQuery, Topologie-Routing, TTL-Strategie, Aktiv-Aktiv- und Aktiv-Standby-DC-Muster
- 🛡️ **[F5 WAF Deep Dive: Anwendungssicherheit mit ASM und Advanced WAF](/de/technology/f5-waf-asm-advanced-waf-application-security/)** — Sicherheitsrichtlinienmodelle, OWASP-Top-10-Abdeckung, Bot-Abwehr, L7-DoS-Schutz und Deployment-Strategie von transparent zu blockierend

---

## Verwandte Artikel

- 🛡️ [Network Packet Broker (NPB) Masterclass](/de/posts/network-packet-broker-masterclass/) — Datenverkehrssichtbarkeit über den gesamten Stack
- 🔐 [Die Zero-Trust-Mentalität: Sicherheit als Architektur entwickeln](/de/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — Wo APM und WAF in Zero Trust passen
- 🏗️ [IT-Infrastruktur ist keine Produktsammlung](/de/architecture/it-infrastructure-not-a-collection-of-products/) — Systemdenken hinter der ADC-Platzierung
- 🎯 [Netzwerkinfrastruktur-Produktauswahl: Strategische Kriterien](/de/architecture/network-product-selection-strategy/) — Wie man ADC-Anbieter objektiv bewertet