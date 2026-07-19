---
title: "SecureCRT und SuperPutty: Terminal-Tools, die jeder Netzwerkingenieur kennen sollte"
description: "Praxisleitfaden für SecureCRT und SuperPutty — Session-Logging, Portabilität, Credential-Management, Scripting und warum SuperPutty das PuTTY-Upgrade ist."
date: 2026-04-13
draft: false

cover:
  image: "/img/postimages/securecrt-superputty-cover.webp"
  alt: "SecureCRT und SuperPutty — Terminal-Tools für Netzwerkingenieure"
  relative: false

tags: ["SecureCRT", "SuperPutty", "PuTTY", "SSH", "Netzwerktools", "Terminal-Client", "Netzwerkingenieur", "Automatisierung"]
categories: ["Technologie"]
keywords:
  - SecureCRT automatisches Logging
  - SecureCRT Session-Management
  - SecureCRT Scripting
  - SuperPutty PuTTY Alternative
  - SecureCRT vs SuperPutty
  - Netzwerkingenieur Terminal-Tools
  - SecureCRT Session Export Import
  - SuperPutty Tabbed Sessions
  - SecureCRT Credential-Speicherung
  - SSH Terminal-Client Netzwerkingenieur

showToc: true
TocOpen: true
---

# SecureCRT und SuperPutty: Terminal-Tools, die jeder Netzwerkingenieur kennen sollte

Wenn Sie mehr als ein paar Jahre Netzwerkengineering betreiben, haben Sie wahrscheinlich Tausende von Stunden in einem Terminal-Client verbracht. SSH zu einem Switch, einige Show-Befehle ausführen, eine Änderung vornehmen, zum nächsten Gerät wechseln. Das ist der sich am meisten wiederholende Workflow im Job — und das richtige Tool macht ihn erheblich weniger schmerzhaft.

Die meisten Ingenieure beginnen mit PuTTY. Es funktioniert, es ist kostenlos und macht, was es verspricht. Aber es gibt zwei Tools, die den Terminal-Workflow von funktional zu wirklich effizient machen: **SecureCRT** (der professionelle Standard) und **SuperPutty** (das kostenlose Upgrade, von dem PuTTY-Benutzer nicht wissen, dass sie es brauchen).

Dieser Artikel behandelt beide — was sie wirklich tun, welche Funktionen bei der täglichen Netzwerkarbeit wichtig sind und wann welches sinnvoll ist.

---

## Warum einfaches PuTTY irgendwann nicht mehr ausreicht

PuTTY ist ein solides Tool. Für gelegentliche Verbindungen ist es völlig ausreichend. Aber bei täglicher Netzwerkingenieur-Arbeit — Verwaltung von Dutzenden von Geräten, gleichzeitiges Troubleshooting über mehrere Sessions, Benötigen von Aufzeichnungen über ausgeführte Befehle — erzeugt einfaches PuTTY Reibung:

- **Keine Tabs:** Jede Verbindung ist ein separates Fenster. 15 Geräte gleichzeitig zu verwalten bedeutet 15 Fenster in der Taskleiste und ständiges Suchen nach dem richtigen.
- **Kein automatisches Logging:** Wenn etwas schief geht und Sie wissen müssen, welche Befehle vor 20 Minuten ausgeführt wurden, hält PuTTY diesen Datensatz nicht, es sei denn, Sie haben das Logging manuell vor der Session konfiguriert. Unter Incident-Druck wird das selten getan.
- **Keine Session-Portabilität:** PuTTY-Sessions werden in der Windows-Registry gespeichert. Der Wechsel auf einen neuen Laptop bedeutet manuelles Neuerstellen jeder gespeicherten Session oder den Export von Registry-Schlüsseln und Hoffen, dass nichts kaputtgeht.
- **Keine Credential-Speicherung pro Session:** Sie können Hostname und Port speichern, aber keine Anmeldedaten. Jede Session erfordert das Eingeben (oder Einfügen) von Benutzername und Passwort.

Diese Einschränkungen sind bei der Verwaltung von fünf Geräten handhabbar. Bei Hunderten von Geräten summieren sie sich zu echtem Overhead.

---

## SecureCRT: Der professionelle Standard

SecureCRT ist ein kommerzieller Terminal-Client von VanDyke Software. Er ist seit Jahrzehnten das bevorzugte Tool in professionellen Netzwerkengineering-Umgebungen. Der Grund ist nicht die Oberfläche — es sind die operativen Funktionen, die bei echter Ingenieurarbeit wichtig sind.

### Automatisches Session-Logging

Das ist die Funktion, die den täglichen Workflow am meisten verändert.

SecureCRT kann so konfiguriert werden, dass für jede Session automatisch eine Log-Datei erstellt wird — nach dem Gerät benannt, mit Zeitstempel, in einer Ordnerstruktur Ihrer Wahl gespeichert. Sie müssen nicht darüber nachdenken. Sie verbinden sich mit einem Gerät, und SecureCRT schreibt bereits alles auf die Festplatte:

```
Logs/
  2026-03/
    core-sw-01_20260314_143022.log
    fw-dc1_20260314_151437.log
    router-edge-01_20260314_162005.log
```

**Warum das in der Praxis wichtig ist:**

Während eines Netzwerkvorfalls müssen Sie genau wissen, welche Befehle in welcher Reihenfolge ausgeführt wurden und was das Gerät geantwortet hat. Manuelles Gedächtnis ist unter Druck unzuverlässig. Automatische Logs geben Ihnen ohne zusätzliche Schritte einen vollständigen, zeitgestempelten Datensatz jeder Session.

Für das Change-Management in regulierten Umgebungen (Banking, Gesundheitswesen) sind Session-Logs oft eine Compliance-Anforderung. SecureCRT erledigt das automatisch, anstatt darauf zu vertrauen, dass Ingenieure daran denken, das Logging zu aktivieren.

Für die Fehlersuche „was hat sich letzten Donnerstag an diesem Gerät geändert" — grep durch Ihren Log-Ordner.

**Automatisches Logging in SecureCRT konfigurieren:**

`Options → Global Options → Log File` — Log-Dateinamensmuster mit Variablen setzen:

```
%D\%H_%Y%M%D_%h%m%s.log
```

`%H` ist Hostname, `%Y%M%D` ist Datum, `%h%m%s` ist Uhrzeit. SecureCRT erstellt Verzeichnisse automatisch, wenn sie nicht existieren.

Sie können Logging auch pro Session oder pro Session-Gruppe konfigurieren — nützlich, wenn Sie verschiedene Log-Speicherorte für verschiedene Kundenumgebungen wünschen.

---

### Session-Management und Portabilität

SecureCRT speichert alle Sessions in einem portablen dateibasierten Format, nicht in der Windows-Registry. Das ist ein grundlegender Unterschied zu PuTTY.

**Session-Ordner und Organisation:**

Sessions werden in einer Baumstruktur organisiert — genau wie ein Datei-Explorer. Eine typische Organisation für einen Netzwerkingenieur, der mehrere Kunden oder Umgebungen verwaltet:

```
Sessions/
  Kunde-A/
    Core/
      core-sw-01
      core-sw-02
    Verteilung/
      dist-sw-etage1
      dist-sw-etage2
    Firewalls/
      fw-primär
      fw-sekundär
  Kunde-B/
    ...
  Labor/
    ...
```

Jede Session speichert: Hostname/IP, Port, Protokoll, Benutzername, Verbindungseinstellungen und optional das Passwort (verschlüsselt). Wenn Sie einen Session-Ordner öffnen, sehen Sie alle Ihre Geräte genau so organisiert, wie Ihr Netzwerk strukturiert ist.

**Portabilität — Wechsel auf einen neuen Rechner:**

Da Sessions dateibasiert sind, ist der Wechsel auf einen neuen Laptop unkompliziert:

1. SecureCRT Sessions-Ordner auf den neuen Rechner kopieren (oder über Cloud-Speicher / Netzlaufwerk synchronisieren)
2. SecureCRT auf den Ordner zeigen
3. Alle Sessions, Organisation und Einstellungen sind sofort verfügbar

In Umgebungen mit mehreren Ingenieuren kann ein gemeinsames Netzlaufwerk eine gemeinsame Session-Datenbank halten — jeder greift auf dieselbe Geräteliste zu, und Ergänzungen eines Ingenieurs sind sofort für andere sichtbar.

**Export und Sicherung:**

`File → Export Settings` exportiert die gesamte Session-Datenbank in eine einzige Datei. Für Ingenieure, die eine persönliche Sicherung vor einem Laptop-Austausch wünschen, dauert das 30 Sekunden.

---

### Credential-Speicherung und automatischer Login

SecureCRT unterstützt das Speichern von Benutzernamen und Passwörtern pro Session, mit Passwörtern verschlüsselt mit dem gewählten Algorithmus (AES-256).

**Automatische Login-Sequenz:**

Über das Speichern von Anmeldedaten hinaus unterstützt SecureCRT Login-Automatisierung mit **Login-Skripten** oder **Auto-Login**-Mustern. Für Geräte mit einer Standardlogin-Sequenz (Benutzernameaufforderung → Passworteingabe → optionale Enable-Passworteingabe) konfigurieren Sie:

```
Session-Eigenschaften → Verbindung → SSH2:
  Benutzername: admin
  Passwort: [gespeichert, verschlüsselt]

Session-Eigenschaften → Terminal → Emulation → Expect-Skripte:
  Benutzername bei "Username:"-Aufforderung senden
  Passwort bei "Password:"-Aufforderung senden
  Enable-Passwort bei ">"-Aufforderung senden
```

Nach der Konfiguration verbindet das Öffnen einer Session automatisch und meldet sich an. Für einen Netzwerkingenieur, der Hunderte von Geräten verwaltet, ist die durch wiederholtes Eintippen von Anmeldedaten gesparte Zeit erheblich — aber noch wichtiger, es eliminiert das Risiko, Anmeldedaten im falschen Fenster einzugeben.

**Hinweis zur Credential-Sicherheit:**

SecureCRTs Passwortspeicherung verwendet ein Master-Passwort (oder Windows-Credential-Store-Integration), um gespeicherte Passwörter zu verschlüsseln. Die verschlüsselte Passwortdatei ist für einen Angreifer ohne das Master-Passwort nicht verwendbar. Für Umgebungen mit strengen Credential-Management-Richtlinien integriert sich SecureCRT auch mit SSH-schlüsselbasierter Authentifizierung.

---

### Tabbed Interface und Multi-Session-Management

SecureCRT zeigt mehrere Sessions als Tabs in einem einzigen Fenster an. Das klingt nach einer Kleinigkeit, bis Sie während einer Netzwerkmigration 20 gleichzeitige Sessions verwalten:

```
[core-sw-01] [core-sw-02] [dist-sw-01] [fw-primär] [router-edge] [+]
```

Wichtige Funktionen für die Arbeit mit mehreren Sessions:

**Session-Tiling:** Fenster aufteilen, um mehrere Sessions gleichzeitig anzuzeigen. Während eines Failover-Tests könnten Sie einen Bereich mit dem aktiven Gerät und einen anderen mit dem Standby wünschen — beide gleichzeitig beobachten.

**In Tab verbinden:** Rechtsklick auf eine gespeicherte Session → „In Tab verbinden." So viele Sessions wie benötigt öffnen, ohne neue Fenster.

**Befehle an mehrere Sessions senden:** SecureCRTs „Chat-Fenster" und „An alle Tabs senden"-Funktion ermöglicht das gleichzeitige Senden desselben Befehls an mehrere Sessions. Für die Anwendung einer konsistenten Änderung auf eine Gruppe von Switches muss derselbe Befehl nicht 10 Mal neu eingegeben werden.

---

### Scripting und Automatisierung

SecureCRT enthält eine integrierte Scripting-Engine, die VBScript, JScript und Python unterstützt. Skripte interagieren programmatisch mit der Terminal-Session — senden Befehle, lesen Ausgaben, treffen Entscheidungen basierend auf Antworten.

**Was Scripting ermöglicht:**

- Automatisierte Konfigurations-Backups: Liste von Geräten verbinden, `show running-config` ausführen, Ausgabe pro Gerät in Datei speichern
- Massenkonfigurationsänderungen: dieselbe Änderung auf eine Gruppe von Geräten anwenden, die Ausgabe jedes einzelnen protokollieren
- Datenerfassung: Schnittstellenstatistiken, Routing-Tabelleneinträge oder VLAN-Informationen von mehreren Geräten sammeln und in einem Bericht zusammenstellen
- Interaktive Automatisierung: Skripte, die auf bestimmte Ausgaben warten, bevor sie den nächsten Befehl senden

**Einfaches Python-Beispiel — show version von einer Geräteliste sammeln:**

```python
# SecureCRT Python-Skript
import time

def main():
    tab = crt.GetScriptTab()
    devices = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]

    for device in devices:
        crt.Session.Connect("/SSH2 /L admin /PASSWORD pass " + device)
        tab.Screen.WaitForString("#")
        tab.Screen.Send("terminal length 0\n")
        tab.Screen.WaitForString("#")
        tab.Screen.Send("show version\n")
        tab.Screen.WaitForString("#")
        output = tab.Screen.ReadString("#")

        with open(f"C:\\logs\\{device}_version.txt", "w") as f:
            f.write(output)

        crt.Session.Disconnect()
        time.sleep(1)

main()
```

Für komplexere Automatisierung (vollständiges Netzwerkinventar, Konfigurationskonformitätsprüfung, Massen-VLAN-Änderungen) bietet SecureCRT-Scripting in Kombination mit Python eine leistungsfähige Automatisierungsplattform ohne ein vollständiges Ansible- oder Netmiko-Setup zu benötigen.

---

### SecureFX-Integration

SecureFX ist VanDykes SFTP/FTP-Client — separat verkauft, aber eng in SecureCRT integriert. Die Integration ist nützlich für:

- Übertragung von Konfigurations-Backups von Netzwerkgeräten auf einen lokalen Server
- Hochladen von Firmware-Images auf Geräte
- Verschieben von Log-Dateien von Netzwerkgeräten in ein zentrales Repository

Innerhalb von SecureCRT können Sie SecureFX mit denselben Session-Anmeldedaten starten — kein separater Login erforderlich.

---

### Protokollunterstützung

SecureCRT unterstützt alle Protokolle, die ein Netzwerkingenieur regelmäßig verwendet:

- **SSH1 / SSH2** — primäres Protokoll für moderne Netzwerkgeräte
- **Telnet** — Legacy-Geräte, Laborumgebungen
- **Seriell (COM-Port)** — Konsolkabelverbindungen für die erstmalige Geräteeinrichtung oder Wiederherstellung
- **RDP** — Remote-Desktop-Verbindungen
- **SFTP / FTP** (über SecureFX-Integration)

Die serielle Verbindungsunterstützung ist für Netzwerkingenieure besonders wertvoll. Die Verbindung zu einem Gerät über ein Konsolkabel verwendet dieselbe Session-Manager-Oberfläche wie SSH — Sie können eine Konsol-Session und mehrere SSH-Sessions zum selben Gerät gleichzeitig geöffnet haben, alles im selben Fenster.

---

## SuperPutty: Das kostenlose Upgrade, von dem PuTTY-Benutzer nichts wissen

Wenn Sie PuTTY täglich verwenden, haben Sie SuperPutty wahrscheinlich noch nie gehört. Es wird nicht gut vermarktet, hat kein großes Unternehmen dahinter und sieht auf den ersten Blick aus wie ein weiteres PuTTY-Fenster. Aber es löst PuTTYs größte Einschränkungen bei der täglichen Nutzung, ohne PuTTY selbst zu ersetzen.

### Was SuperPutty eigentlich ist

SuperPutty ist ein **Session-Manager und Tabbed-Interface-Wrapper für PuTTY**. Es ersetzt PuTTY nicht — PuTTY muss für SuperPutty installiert sein. Was SuperPutty hinzufügt, ist alles, was PuTTY für ernsthafte Multi-Session-Arbeit fehlt:

- Tabbed Interface mit mehreren PuTTY-Sessions in einem Fenster
- Persistente Session-Bibliothek mit Ordnerorganisation
- Import bestehender PuTTY-Sessions — Ihre bestehende Konfiguration geht nicht verloren
- Tiled Layout — mehrere Sessions gleichzeitig sichtbar
- Schnellverbindungsleiste
- Session-Suche

**Es ist vollständig kostenlos und Open Source.**

---

### Ihre PuTTY-Sessions importieren

Das Erste nach der Installation von SuperPutty: bestehende PuTTY-Sessions importieren.

`Tools → Import Sessions → From PuTTY Settings`

SuperPutty liest die PuTTY-Session-Daten aus der Windows-Registry und erstellt entsprechende Sessions in seiner eigenen Session-Datenbank. Alle gespeicherten Hostnamen, Port-Einstellungen und Verbindungseinstellungen werden automatisch importiert. Sie beginnen nicht von vorne.

Nach dem Import erscheinen Ihre PuTTY-Sessions im Session-Baum von SuperPutty — sofort einsatzbereit. PuTTY selbst funktioniert weiterhin normal; SuperPutty und PuTTY koexistieren.

---

### Tabbed Interface und Session-Organisation

Sobald Sessions importiert (oder direkt in SuperPutty erstellt) wurden, öffnet die Verbindung zu einem Gerät es als Tab:

```
[core-sw-01] [fw-primär] [router-edge] [dist-sw-02] [+]
```

Sessions können in Ordnern organisiert werden — dieselbe Struktur, die Sie in SecureCRT verwenden würden, nur ohne die kommerzielle Lizenzkosten.

**Tiled Layout:** SuperPutty unterstützt das Aufteilen des Fensters in ein Raster von Session-Bereichen. Nützlich während Wartungsfenstern, wenn Sie mehrere Geräte gleichzeitig beobachten.

**Automatische Wiederverbindung:** SuperPutty kann Sessions, die abbrechen, automatisch wieder verbinden.

---

### Was SuperPutty nicht hat

Um direkt über Einschränkungen zu sein:

- **Kein automatisches Logging:** SuperPutty protokolliert Sessions nicht automatisch. Sie können PuTTYs integriertes Logging für jede Session konfigurieren, aber es gibt kein globales „alles automatisch protokollieren" äquivalent zu SecureCRTs Funktion.
- **Keine integrierte Scripting-Engine:** SuperPutty hat kein Äquivalent zu SecureCRTs VBScript/Python-Scripting. Für Automatisierung verwenden Sie separate Tools (Netmiko, Paramiko, Ansible).
- **Keine Credential-Verschlüsselung:** SuperPutty speichert Passwörter in seiner Session-Datenbank ohne die Verschlüsselungsoptionen, die SecureCRT bietet.
- **Weniger ausgereift:** SuperPutty ist ein von Freiwilligen betreutes Open-Source-Projekt. Es funktioniert gut, aber es fehlt die Ausgereiftheit und aktive Entwicklung eines kommerziellen Produkts.

---

## SecureCRT vs. SuperPutty: Wann welches verwenden

| | SecureCRT | SuperPutty |
|---|---|---|
| Kosten | Kommerzielle Lizenz (~99–150 $/Sitz) | Kostenlos |
| Automatisches Session-Logging | ✅ Integriert, global | ❌ Nur pro Session PuTTY-Logging |
| Session-Portabilität | ✅ Dateibasiert, einfacher Export | ✅ XML-basiert, importierbar |
| PuTTY-Session-Import | ❌ Nicht anwendbar | ✅ Direktimport aus Registry |
| Tabbed Interface | ✅ | ✅ |
| Tiled Sessions | ✅ | ✅ |
| Scripting (Python/VBScript) | ✅ Integrierte Engine | ❌ |
| Credential-Speicherung (verschlüsselt) | ✅ AES-256 | ⚠️ Nur grundlegend |
| Seriell/Konsol-Unterstützung | ✅ | ✅ (via PuTTY) |
| RDP-Unterstützung | ✅ | ✅ (via PuTTY/mRemoteNG) |
| SecureFX-Integration | ✅ | ❌ |
| Aktiver kommerzieller Support | ✅ | Nur Community |

**SecureCRT verwenden, wenn:**
- Automatisches Session-Logging erforderlich ist (Compliance, Incident Response)
- Sie Skripte für Automatisierung oder Massenoperationen ausführen
- Sie Hunderte von Geräten verwalten und einen robusten, zuverlässigen Session-Manager benötigen
- Ihre Organisation verschlüsselte Credential-Speicherung erfordert
- Sie in einer regulierten Umgebung arbeiten, wo Session-Aufzeichnungen obligatorisch sind

**SuperPutty verwenden, wenn:**
- Sie bereits PuTTY-Benutzer sind und Tabbed Sessions ohne Toolwechsel wünschen
- Kosten eine Einschränkung sind (individuelle Nutzung, kleines Team)
- Ihre Automatisierungsanforderungen von separaten Tools (Ansible, Netmiko) erfüllt werden
- Sie bewerten möchten, ob ein Session-Manager Ihren Workflow verbessert, bevor Sie sich für ein kommerzielles Tool entscheiden

**Die ehrliche Einschätzung:** Wenn Sie ein arbeitender Netzwerkingenieur sind, der täglich Produktionsinfrastruktur verwaltet, rechtfertigt SecureCRTs automatisches Logging allein die Lizenzkosten. Die Anzahl der Male, in denen Session-Logs während eines Vorfalls oder einer Post-Change-Überprüfung den genauen benötigten Datensatz geliefert haben, ist nicht gering. SuperPutty ist ein echtes Upgrade gegenüber einfachem PuTTY und kostet nichts — aber es ersetzt SecureCRT nicht für Ingenieure, die auf Logging und Scripting angewiesen sind.

---

## Praktische Einrichtung: SecureCRT-Konfiguration für den täglichen Einsatz

Einige Konfigurationsempfehlungen aus dem täglichen Einsatz:

**Globales Logging-Setup:**
`Options → Global Options → Log File`
```
Log-Dateiname: C:\NetworkLogs\%H_%Y%M%D_%h%m%s.log
Bei Verbindung: Log starten
Log-Daten:      Alle Session-Daten einschließlich Zeitstempel
```

**Session-Ordnerstruktur:**
Auf der obersten Ebene nach Kunde oder Umgebung organisieren, dann nach Geräterolle. Konsistente Benennung (Core, Distribution, Access, Firewall, Router) macht die Navigation auch bei Hunderten von Sessions schnell.

**Farbschemata pro Session-Gruppe:**
SecureCRT unterstützt verschiedene Terminal-Farbschemata pro Session oder Ordner. Die Verwendung einer anderen Farbe für Produktion vs. Labor verhindert den Falschfenster-Fehler — versehentlich einen Befehl auf einem Produktionsgerät ausführen, wenn man dachte, man sei im Labor.

**SSH-Schlüsselauthentifizierung:**
Für Produktionsumgebungen SSH-Schlüsselauthentifizierung statt gespeicherten Passwörtern konfigurieren:
`Session-Eigenschaften → Verbindung → SSH2 → PublicKey`
Auf Ihre private Schlüsseldatei zeigen. Der Schlüssel wird bei der Verbindung automatisch verwendet — keine Passworteingabe, kein gespeichertes Passwort.

**Schlüsselwort-Hervorhebung:**
`Options → Global Options → Advanced → Keyword Sets`
Schlüsselwörter wie `%Error`, `down`, `FAIL`, `alarm` konfigurieren, um in Rot zu erscheinen. Kritische Fehlermeldungen fallen in einem dichten Ausgabestrom sofort auf.

---

## Wichtigste Erkenntnisse

- **Einfaches PuTTY ist funktional hat aber echte Einschränkungen** für den täglichen professionellen Einsatz — keine Tabs, kein automatisches Logging, keine Session-Portabilität.
- **SecureCRTs automatisches Logging** ist seine betrieblich wertvollste Funktion — jede Session, jeder Befehl, jede Antwort, ohne zusätzliche Schritte automatisch mit Zeitstempel gespeichert.
- **Session-Portabilität** in SecureCRT bedeutet, dass der Wechsel auf einen neuen Laptop eine Kopieroperation ist, kein Neuaufbau.
- **Credential-Speicherung mit automatischem Login** eliminiert wiederholtes Tippen, sollte aber in sensiblen Umgebungen mit Master-Passwort oder schlüsselbasierter Authentifizierung kombiniert werden.
- **SecureCRT-Scripting** ermöglicht Automatisierung, die sonst ein separates Tool erfordern würde.
- **SuperPutty ist die richtige Antwort** für Ingenieure, die PuTTY kennen und Tabbed Sessions, Session-Organisation und PuTTY-Session-Import wünschen — zu null Kosten.
- Wenn Sie derzeit einfaches PuTTY verwenden und SuperPutty noch nie ausprobiert haben: Installieren Sie es heute. Importieren Sie Ihre bestehenden Sessions in zwei Minuten. Das Tab-Interface allein wird Ihren Workflow verändern.

---

## Verwandte Artikel

- 🛠️ [Die Hintertür des Netzwerks: Next-Gen Console Server Architektur](/de/posts/next-gen-console-server-architecture/) — Out-of-Band-Zugang wenn SSH fehlschlägt
- 🔐 [802.1X Identitätsbasierte Architektur im Praxiseinsatz](/de/technology/identity-based-microsegmentation-8021x/) — Das Authentifizierungsframework hinter SSH-Zugangskontrolle
- 📊 [Monitoring richtig gemacht](/de/architecture/monitoring-not-just-seeing/) — Manuelle CLI-Arbeit mit proaktivem Monitoring ergänzen