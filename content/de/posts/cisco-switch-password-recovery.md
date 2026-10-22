---
title: "Cisco Switch und Router Passwort-Wiederherstellung: Catalyst 9000, 2960, 3560 und ISR"
description: "Verlorenes Enable- oder Konsolen-Passwort auf Cisco-Geräten ohne Konfigurationsverlust wiederherstellen — klassische Catalyst (2960, 3560, 3750), Catalyst 9000 und 3850 mit SWITCH_IGNORE_STARTUP_CFG, ISR-Router mit confreg 0x2142 und was tun, wenn die Passwort-Wiederherstellung deaktiviert ist."
date: 2026-10-22
draft: false
aliases:
  - "/de/posts/catalyst-3560-password-recovery/"

tags: ["Cisco", "Password Recovery", "ROMMON", "IOS", "IOS-XE", "Catalyst 9300", "Catalyst 9200", "Catalyst 2960", "Catalyst 3560", "ISR 4000"]
categories: ["Netzwerkbetrieb"]
keywords: ["Cisco Passwort Wiederherstellung", "Cisco Switch Passwort zurücksetzen", "Catalyst 9300 Passwort zurücksetzen", "SWITCH_IGNORE_STARTUP_CFG", "no system ignore startupconfig switch all", "flash_init config.text", "confreg 0x2142", "no service password-recovery", "Cisco 2960 Passwort", "ISR 4331 Passwort"]
showToc: true
TocOpen: true
---

Sie übernehmen ein Gerät ohne Dokumentation, oder ein Lab-Switch kommt aus dem Lager zurück und fragt nach einem Passwort, das niemand kennt. Auf Cisco Switches und Routern lässt sich das lösen, ohne die Konfiguration zu verlieren, solange Sie physischen Zugang und ein Konsolenkabel haben.

Das Prinzip ist überall gleich: Startvorgang unterbrechen, IOS **ohne** Startkonfiguration starten, dann die Konfiguration zurückholen und neue Passwörter setzen. Unterschiedlich ist nur, wie Sie dem Gerät sagen, dass es die Konfiguration überspringen soll:

| Plattform | Typische Modelle | So wird die Konfiguration übersprungen |
| --- | --- | --- |
| Klassische Catalyst | 2960, 2960-X, 3560, 3750 | `config.text` im Boot Loader umbenennen |
| IOS-XE Catalyst | 3650, 3850, 9200, 9300, 9400, 9500 | `SWITCH_IGNORE_STARTUP_CFG=1` |
| Router | ISR 4000, ISR 1100, Catalyst 8000, ISR G2 | Konfigurationsregister `0x2142` |

## Was Sie brauchen

- Physischen Zugang zum Gerät oder einen Konsolenserver. Eine Passwort-Wiederherstellung über das Netzwerk ist absichtlich nicht möglich. Siehe [Next-Gen Console Server Architektur](/de/posts/next-gen-console-server-architecture/).
- Ein Konsolenkabel und ein Terminalprogramm. Einstellungen: **9600 Baud, 8 Datenbits, keine Parität, 1 Stoppbit, keine Flusskontrolle**.
- Ein Wartungsfenster. Das Gerät startet neu und leitet währenddessen keinen Verkehr weiter.

## Switches: Zum Prompt switch: gelangen

Bei Catalyst Switches unterbrechen Sie den Start mit der **Mode**-Taste:

1. Konsole anschließen und Terminalsitzung öffnen.
2. Strom trennen.
3. Die **Mode**-Taste an der Vorderseite gedrückt halten und den Strom wieder anschließen.
4. Gedrückt halten, bis die Konsole meldet, dass der Start unterbrochen wurde, etwa 10 bis 15 Sekunden, dann loslassen.

Sie sind jetzt am Prompt `switch:`.

Bei einem Catalyst 9400 mit zwei Supervisors empfiehlt Cisco, den sekundären Supervisor vorher zu entfernen.

## Klassische Catalyst (2960, 3560, 3750): config.text umbenennen

```
switch: flash_init
switch: dir flash:
switch: rename flash:config.text flash:config.text.old
switch: boot
```

Manche älteren Boot Loader brauchen nach `flash_init` zusätzlich `load_helper`. Löschen Sie `config.text` **nicht**. Umbenennen reicht, und den Inhalt brauchen Sie später.

Der Switch startet ohne Konfiguration. Antworten Sie auf den Initial Configuration Dialog mit **no**, dann:

```
Switch> enable
Switch# rename flash:config.text.old flash:config.text
Switch# copy flash:config.text system:running-config
```

Weiter mit dem Abschnitt „Neue Passwörter setzen und speichern“ weiter unten.

## Catalyst 9000 und 3850: SWITCH_IGNORE_STARTUP_CFG

IOS-XE-Switches brauchen das Umbenennen nicht. Eine Boot-Loader-Variable weist IOS an, die Startkonfiguration zu ignorieren:

```
switch: SWITCH_IGNORE_STARTUP_CFG=1
switch: boot flash:packages.conf
```

Läuft der Switch im Bundle Mode, verwenden Sie `boot flash:<image>.bin`. Nach dem Start antworten Sie auf den Initial Configuration Dialog mit **no** und laden die Konfiguration:

```
Switch> enable
Switch# copy startup-config running-config
```

**Wichtig:** Setzen Sie die Variable aus IOS zurück. Sonst ignoriert der Switch seine Konfiguration bei jedem Neustart:

```
Switch# configure terminal
Switch(config)# no system ignore startupconfig switch all
Switch(config)# end
```

Weiter mit dem nächsten Abschnitt, dann speichern.

## Router (ISR 4000, ISR 1100, Catalyst 8000): confreg 0x2142

Router haben keine Mode-Taste. Unterbrechen Sie den Start, indem Sie in den ersten Sekunden nach dem Einschalten aus dem Terminalprogramm ein **Break** senden. Sie landen am Prompt `rommon 1 >`.

```
rommon 1 > confreg 0x2142
rommon 2 > reset
```

Der Wert `0x2142` weist den Router an, die Startkonfiguration zu ignorieren. Nach dem Start antworten Sie auf den Initial Configuration Dialog mit **no**:

```
Router> enable
Router# copy startup-config running-config
Router# configure terminal
Router(config)# config-register 0x2102
```

Das Zurücksetzen auf `0x2102` ist entscheidend. Sonst ignoriert der Router seine Konfiguration bei jedem Neustart.

## Neue Passwörter setzen und speichern

Sie sind jetzt im privilegierten Modus, die ursprüngliche Konfiguration ist geladen. Setzen Sie neue Zugangsdaten passend zur bisherigen Authentifizierung:

```
configure terminal
enable secret <neues-enable-secret>
username admin privilege 15 secret <neues-passwort>
line con 0
 login local
line vty 0 15
 login local
end
```

Nutzt das Gerät TACACS+ oder RADIUS, prüfen Sie, ob der lokale Fallback-Account funktioniert.

Beim Kopieren in die Running-Config wird die Konfiguration zusammengeführt. Interfaces können administrativ heruntergefahren bleiben, besonders VLAN-Interfaces (SVIs) auf Switches. Prüfen und korrigieren:

```
show ip interface brief
```

Interfaces, die aktiv sein sollen, mit `no shutdown` aktivieren. Dann speichern und testen:

```
write memory
reload
```

Melden Sie sich nach dem Neustart mit den neuen Zugangsdaten an, um sicherzugehen, dass Konfiguration und Passwörter den Neustart überstehen.

## Wenn die Passwort-Wiederherstellung deaktiviert ist

Ist `no service password-recovery` konfiguriert, verhält sich der Ablauf anders. Das Gerät lässt das Überspringen der Konfiguration nicht zu. Stattdessen meldet es, dass die Passwort-Wiederherstellung deaktiviert ist, und fragt, ob es auf die Werkskonfiguration zurückgesetzt werden soll.

- **Yes:** Die Konfiguration (und bei Switches die VLAN-Datenbank) wird gelöscht. Das Gerät startet mit Standardeinstellungen. Das IOS-Image bleibt.
- **No:** Das Gerät startet normal mit der aktuellen Konfiguration, und Sie stehen wieder vor der Passwortabfrage.

Das ist der Zweck der Funktion. Wer physischen Zugang hat, kann die Konfiguration nicht auslesen, aber Sie verlieren sie ebenfalls. Bevor Sie mit yes antworten, sollten Sie ein aktuelles Konfigurations-Backup aus einer anderen Quelle haben. Nach dem Reset stellen Sie die Konfiguration wieder her und legen die VLANs neu an, falls das Backup sie nicht enthält.

`no service password-recovery` ist sinnvoll für Geräte an öffentlichen oder unverschlossenen Orten, sofern die Konfiguration woanders gesichert ist.

## Häufige Fehler

- **`config.text` löschen statt umbenennen.** Dann hilft nur ein Backup.
- **`no system ignore startupconfig switch all` oder `config-register 0x2102` vergessen.** Das Gerät startet beim nächsten Neustart ohne Konfiguration.
- **Nach dem Setzen der Passwörter nicht speichern.** Beim nächsten Neustart sind die alten Passwörter zurück.
- **SVIs bleiben nach dem Zusammenführen heruntergefahren.** Der Management-Zugriff über das Netzwerk schlägt fehl, obwohl die Konfiguration korrekt aussieht.

## Verwandte Artikel

- [Cisco ROMMON Recovery: Start aus Flash, über TFTP oder USB](/de/posts/cisco-rommon-recovery/)
- [Cisco IOS und IOS-XE Upgrade-Leitfaden](/de/posts/cisco-ios-xe-upgrade-guide/)
- [Next-Gen Console Server Architektur](/de/posts/next-gen-console-server-architecture/)

Quelle: [Cisco: Troubleshoot Bootloader and Password Recovery on Catalyst 9000](https://cisco.com/c/en/us/support/docs/switches/catalyst-9300-series-switches/216944-troubleshoot-bootloader-rommon-and-pas.html)
