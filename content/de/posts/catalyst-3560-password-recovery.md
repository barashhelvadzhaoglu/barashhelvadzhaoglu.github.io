---
title: "Cisco Catalyst 3560 Passwort-Wiederherstellung: Zwei Methoden Schritt für Schritt"
description: "Verlorenes Enable- oder Konsolen-Passwort auf einem Cisco Catalyst 3560 wiederherstellen — mit Erhalt der Konfiguration über den Boot Loader oder per Reset, wenn die Passwort-Wiederherstellung deaktiviert ist."
date: 2026-10-16
draft: false

tags: ["Cisco", "Catalyst", "Switch", "Password Recovery", "Boot Loader", "IOS"]
categories: ["Netzwerkbetrieb"]
keywords: ["Catalyst 3560 Passwort zurücksetzen", "Cisco Switch Passwort Wiederherstellung", "flash_init", "config.text umbenennen", "no service password-recovery", "Cisco Boot Loader", "Cisco 3560 Mode-Taste", "enable secret zurücksetzen"]
showToc: true
TocOpen: true
---

Sie übernehmen einen Switch, die Dokumentation fehlt und niemand kennt das Enable-Passwort. Oder ein Lab-Switch kommt aus dem Lager zurück und die Konsole fragt nach einem Passwort, das Sie nie gesetzt haben. Auf einem Cisco Catalyst 3560 lässt sich beides lösen, ohne die Konfiguration zu verlieren, solange Sie physischen Zugang und ein Konsolenkabel haben.

Dieser Leitfaden behandelt die zwei Situationen aus der Praxis:

- **Methode 1: Konfiguration behalten.** Der Switch startet ohne Startkonfiguration, Sie setzen die Passwörter neu und spielen die ursprüngliche Konfiguration wieder ein.
- **Methode 2: Passwort-Wiederherstellung ist deaktiviert.** Jemand hat `no service password-recovery` konfiguriert. Der Switch lässt sich trotzdem zurückholen, aber nur über einen Reset auf Werkseinstellungen.

> **Lab-Hinweis:** Ich führe diese Schritte auf meinem eigenen Catalyst 3560 mit 8 PoE-Ports durch. Die Konsolenausgaben aus diesem Lab werden ergänzt.

## Was Sie brauchen

- Physischen Zugang zum Switch. Eine Passwort-Wiederherstellung aus der Ferne ist absichtlich nicht möglich.
- Ein Konsolenkabel (RJ-45-Rollover oder USB-Seriell) und ein Terminalprogramm wie SecureCRT, PuTTY oder `screen`.
- Terminaleinstellungen: **9600 Baud, 8 Datenbits, keine Parität, 1 Stoppbit, keine Flusskontrolle**.
- Ein Wartungsfenster. Der Switch startet zweimal neu und leitet währenddessen keinen Verkehr weiter.

Für Konsolenzugriff aus der Ferne ist ein Konsolenserver die professionelle Lösung. Siehe [Next-Gen Console Server Architektur](/de/posts/next-gen-console-server-architecture/).

## So funktioniert die Wiederherstellung

Der Catalyst 3560 speichert seine Startkonfiguration als Datei `config.text` im Flash. Beim normalen Start lädt IOS diese Datei. Bei der Passwort-Wiederherstellung wird der Startvorgang unterbrochen, bevor IOS startet. Sie landen im **Boot Loader**, einer kleinen Umgebung mit dem Prompt `switch:`.

Im Boot Loader haben Sie Zugriff auf das Flash-Dateisystem. Wenn `config.text` umbenannt ist, startet IOS ohne Konfiguration und damit ohne Passwörter. Danach melden Sie sich an, stellen die Konfiguration manuell wieder her und setzen neue Passwörter.

## Methode 1: Passwort zurücksetzen und Konfiguration behalten

### Schritt 1: Startvorgang unterbrechen

1. Konsolenkabel anschließen und Terminalsitzung öffnen.
2. Stromkabel ziehen.
3. Die **Mode**-Taste an der Vorderseite gedrückt halten.
4. Strom wieder anschließen und die Taste weiter gedrückt halten.
5. Die Taste nach etwa 15 Sekunden loslassen, wenn die Konsole meldet, dass das System vor der Initialisierung des Flash-Dateisystems unterbrochen wurde.

Jetzt sollte der Prompt `switch:` erscheinen. Startet der Switch normal, schalten Sie ihn aus und versuchen es erneut, diesmal mit etwas längerem Drücken.

### Schritt 2: Flash initialisieren

Das Flash-Dateisystem ist noch nicht eingebunden. Initialisieren Sie es:

```
switch: flash_init
```

Bei einigen älteren Boot-Loader-Versionen müssen zusätzlich Hilfsdateien geladen werden:

```
switch: load_helper
```

Dann den Inhalt des Flash anzeigen:

```
switch: dir flash:
```

Sie sollten das IOS-Image (oder ein Verzeichnis mit dem Image), `config.text`, `vlan.dat` und eventuell `private-config.text` sehen.

### Schritt 3: Konfigurationsdatei umbenennen

```
switch: rename flash:config.text flash:config.text.old
```

Löschen Sie `config.text` **nicht**. Das Umbenennen reicht, damit IOS die Datei nicht lädt, und den Inhalt brauchen Sie später noch.

### Schritt 4: IOS ohne Konfiguration starten

```
switch: boot
```

Der Switch startet mit leerer Konfiguration. Auf die Frage nach dem Initial Configuration Dialog antworten Sie mit **no**.

### Schritt 5: Ursprüngliche Konfiguration wiederherstellen

```
Switch> enable
Switch# rename flash:config.text.old flash:config.text
Switch# copy flash:config.text system:running-config
```

Der Switch läuft jetzt mit der ursprünglichen Konfiguration, inklusive Hostname, VLANs, Interfaces und den alten Passwörtern. Sie sind weiterhin im privilegierten Modus, weil Sie ihn vor dem Laden der Konfiguration betreten haben.

### Schritt 6: Neue Passwörter setzen

```
Switch# configure terminal
Switch(config)# enable secret <neues-enable-secret>
Switch(config)# username admin privilege 15 secret <neues-passwort>
Switch(config)# line con 0
Switch(config-line)# login local
Switch(config-line)# line vty 0 15
Switch(config-line)# login local
Switch(config-line)# end
```

Passen Sie das an die bisherige Authentifizierung an. Nutzt der Switch TACACS+ oder RADIUS, prüfen Sie, ob der lokale Fallback-Account funktioniert.

### Schritt 7: Interfaces prüfen und speichern

Beim Kopieren in die Running-Config wird die Konfiguration zusammengeführt. Dabei wird nicht jeder Interface-Zustand wiederhergestellt. Prüfen Sie, ob Interfaces administrativ heruntergefahren sind, besonders VLAN-Interfaces (SVIs):

```
Switch# show ip interface brief
```

Interfaces, die aktiv sein sollen, mit `no shutdown` aktivieren. Dann speichern:

```
Switch# copy running-config startup-config
```

Starten Sie einmal neu und melden Sie sich mit den neuen Zugangsdaten an, um sicherzugehen, dass alles einen Neustart übersteht.

## Methode 2: Wenn die Passwort-Wiederherstellung deaktiviert ist

Wurde der Switch mit `no service password-recovery` konfiguriert, verhält sich die Mode-Taste anders. Sie haben im Boot Loader keinen Zugriff auf das Flash-Dateisystem. Stattdessen meldet der Switch, dass die Passwort-Wiederherstellung deaktiviert ist, und fragt, ob das System auf die Standardkonfiguration zurückgesetzt werden soll.

- Mit **yes** löscht der Switch die Konfigurationsdatei und die VLAN-Datenbank und startet mit Werkseinstellungen. Das IOS-Image bleibt im Flash.
- Mit **no** startet der Switch normal mit der aktuellen Konfiguration, und Sie stehen wieder vor der Passwortabfrage.

Das ist der gewollte Kompromiss dieser Funktion. Ein Angreifer mit physischem Zugang kann die Konfiguration nicht auslesen, aber Sie verlieren sie ebenfalls.

Vor dem Reset sollten Sie ein aktuelles Backup der Konfiguration aus einer anderen Quelle haben, zum Beispiel aus einem Konfigurationsmanagement-Tool, von einem TFTP-Server oder als archivierte `show running-config`. Nach dem Reset:

1. Ohne Passwort anmelden und neue Zugangsdaten setzen.
2. Konfiguration aus dem Backup wiederherstellen.
3. VLANs neu anlegen, falls das Backup sie nicht enthält. Die VLAN-Datenbank (`vlan.dat`) wird ebenfalls gelöscht.
4. Entscheiden, ob `no service password-recovery` wieder aktiviert werden soll. Das ist sinnvoll für Switches an öffentlichen oder unverschlossenen Orten, sofern die Konfiguration woanders gesichert ist.

## Neuere Boot Loader: Startkonfiguration ignorieren

Neuere Catalyst-Modelle und Boot-Loader-Versionen bieten eine sauberere Alternative zum Umbenennen von `config.text`: eine Boot-Loader-Variable, die IOS anweist, die Startkonfiguration für einen Start zu ignorieren. Ob Ihr Switch das unterstützt, hängt vom Modell und von der Boot-Loader-Version ab. Mit `set` am Prompt `switch:` sehen Sie, welche Variablen Ihr Boot Loader kennt.

Was der Boot Loader des 3560 hier bietet, dokumentiere ich, sobald die Lab-Ausgaben vorliegen.

## Häufige Fehler

- **`config.text` löschen statt umbenennen.** Die Konfiguration ist weg, und nur ein Backup hilft.
- **Vergessen, die Datei zurückzubenennen.** Beim nächsten Neustart startet der Switch ohne Konfiguration.
- **`copy startup-config running-config` vor dem Zurückbenennen.** Die Startkonfiguration existiert zu diesem Zeitpunkt nicht unter ihrem normalen Namen.
- **Nach dem Ändern der Passwörter nicht speichern.** Beim nächsten Neustart sind die alten Passwörter zurück.
- **Heruntergefahrene SVIs nach dem Zusammenführen.** Der Management-Zugriff über das Netzwerk schlägt fehl, obwohl die Konfiguration korrekt aussieht.

## Verwandte Artikel

- [Catalyst 3560 IOS-Upgrade: Zwei Methoden und Verifizierung](/de/posts/catalyst-3560-ios-upgrade/)
- [Wenn ein Catalyst 3560 nicht startet: Wiederherstellung über den Boot Loader](/de/posts/catalyst-3560-boot-loader-recovery/)
- [Cisco Nexus NX-OS Software-Upgrade-Leitfaden](/de/posts/cisco-nexus-nxos-upgrade-guide/)
- [Next-Gen Console Server Architektur](/de/posts/next-gen-console-server-architecture/)
