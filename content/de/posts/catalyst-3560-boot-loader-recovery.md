---
title: "Wenn ein Catalyst 3560 nicht startet: Wiederherstellung über den Boot Loader"
description: "Einen Cisco Catalyst 3560 wiederherstellen, der am Prompt switch: hängt — Boot-Loader-Variablen, ein anderes Image starten und ein neues IOS-Image per Xmodem über die Konsole übertragen."
date: 2026-10-16
draft: false

tags: ["Cisco", "Catalyst", "Switch", "Boot Loader", "IOS", "Recovery"]
categories: ["Netzwerkbetrieb"]
keywords: ["Catalyst 3560 Boot Loader", "Cisco Switch Prompt Wiederherstellung", "copy xmodem flash", "Cisco Switch Boot-Schleife", "BOOT Variable Cisco", "MANUAL_BOOT", "Cisco 3560 kein IOS Image", "Cisco Switch Xmodem Baudrate"]
showToc: true
TocOpen: true
---

Früher oder später erlebt es jeder Netzwerk-Engineer: Nach einem Neustart kommt der Switch nicht zurück. Auf der Konsole steht nur der Prompt `switch:`. Das IOS-Image fehlt, ist beschädigt, oder die Boot-Variable zeigt auf eine Datei, die es nicht gibt.

Das ist kein Grund, den Switch zu tauschen. Der Boot Loader des Catalyst 3560 hat alles, was Sie brauchen, um IOS wieder zum Laufen zu bringen, selbst wenn das Image im Flash fehlt. Dieser Leitfaden behandelt:

- Wie Sie die Boot-Loader-Umgebung lesen und warum der Switch dort stehen geblieben ist
- Wie Sie ein Image starten, das schon im Flash liegt
- Wie Sie ein neues Image per **Xmodem** über die Konsole übertragen, wenn der Flash leer ist
- Wie Sie die Lösung dauerhaft machen

> **Lab-Hinweis:** Ich teste diese Szenarien auf meinem eigenen Catalyst 3560 mit 8 PoE-Ports. Konsolenausgaben und Übertragungszeiten aus diesem Lab werden ergänzt.

## Warum der Switch im Boot Loader stehen bleibt

Der Boot Loader startet IOS von dem Image, das in der Variable `BOOT` steht. Schlägt das fehl, oder ist keine `BOOT`-Variable gesetzt und der Boot Loader findet selbst kein startfähiges Image, bleibt der Switch am Prompt `switch:` stehen. Typische Ursachen:

- Das Upgrade ist schiefgegangen: ein Tippfehler in `boot system`, oder das alte Image wurde gelöscht, bevor das neue bereitstand.
- Die Image-Datei ist beschädigt, zum Beispiel nach einem abgebrochenen Kopiervorgang.
- Die Variable `MANUAL_BOOT` steht auf `yes`, der Switch wartet also immer am Prompt.
- Das Flash-Dateisystem ist beschädigt.

Ein weiteres Symptom ist eine **Boot-Schleife**: Der Switch beginnt IOS zu laden, stürzt ab und startet immer wieder neu. Um die Schleife zu unterbrechen, halten Sie beim Einschalten die Mode-Taste gedrückt. Das Vorgehen steht im [Leitfaden zur Passwort-Wiederherstellung](/de/posts/catalyst-3560-password-recovery/).

## Schritt 1: Bestandsaufnahme

Flash initialisieren und den Inhalt anzeigen:

```
switch: flash_init
switch: dir flash:
```

Dann die Umgebungsvariablen des Boot Loaders anzeigen:

```
switch: set
```

Die wichtigsten Variablen:

| Variable | Bedeutung |
| --- | --- |
| `BOOT` | Image(s), die der Switch zu starten versucht, durch Semikolon getrennt |
| `MANUAL_BOOT` | `yes` = immer am Boot-Loader-Prompt anhalten |
| `BAUD` | Konsolengeschwindigkeit. Standard ist 9600, wenn die Variable nicht gesetzt ist |
| `CONFIG_FILE` | Name der Konfigurationsdatei, Standard `config.text` |

Mit `help` sehen Sie, welche Befehle Ihre Boot-Loader-Version unterstützt.

## Schritt 2: Ein Image aus dem Flash starten

Zeigt `dir flash:` ein gültiges IOS-Image, können Sie es direkt starten. Images, die mit `archive download-sw` installiert wurden, liegen in einem Unterverzeichnis. Prüfen Sie also den vollständigen Pfad:

```
switch: dir flash:c3560-ipservicesk9-mz.<version>
switch: boot flash:c3560-ipservicesk9-mz.<version>/c3560-ipservicesk9-mz.<version>.bin
```

War `MANUAL_BOOT` das Problem, korrigieren Sie es:

```
switch: set MANUAL_BOOT no
```

Sobald IOS läuft, setzen Sie die Boot-Variable dauerhaft:

```
Switch# configure terminal
Switch(config)# boot system flash:<pfad>/<image>.bin
Switch(config)# end
Switch# copy running-config startup-config
Switch# show boot
```

## Schritt 3: Flash ist leer: Image per Xmodem übertragen

Gibt es kein brauchbares Image im Flash, müssen Sie eines übertragen. Beim klassischen Catalyst 3560 hat der Boot Loader keinen Netzwerk-Stack und der Switch keinen USB-Speicheranschluss. Der Weg führt also über die Konsole. Das Protokoll ist **Xmodem**, das jedes ernsthafte Terminalprogramm unterstützt.

### Image vorbereiten

Verwenden Sie die `.bin`-Datei, nicht die `.tar`-Datei. Xmodem überträgt eine einzelne Datei, und der Boot Loader kann keine Archive entpacken. Prüfen Sie die MD5-Prüfsumme vorher auf Ihrem PC, denn die Übertragung dauert lange und Sie wollen sie nicht wiederholen.

### Konsolengeschwindigkeit erhöhen

Bei 9600 Baud dauert die Übertragung eines IOS-Images dieser Größe mehrere Stunden. Erhöhen Sie zuerst die Geschwindigkeit:

```
switch: set BAUD 115200
```

Die Konsolenausgabe wird sofort unlesbar. Stellen Sie Ihr Terminalprogramm auf 115200 Baud um und drücken Sie Enter, bis der Prompt `switch:` wieder erscheint.

### Übertragung starten

```
switch: copy xmodem: flash:c3560-ipservicesk9-mz.<version>.bin
```

Der Switch wartet auf die Datei. Starten Sie in Ihrem Terminalprogramm einen Xmodem-Versand:

- **SecureCRT:** Transfer > Send Xmodem
- **Tera Term:** File > Transfer > XMODEM > Send
- **minicom / screen:** `sx` aus dem Paket `lrzsz`

Bei 115200 Baud rechnen Sie je nach Image-Größe und Terminalprogramm mit einer halben bis einer Stunde. Berühren Sie die Konsolensitzung während der Übertragung nicht.

### Neues Image starten

```
switch: dir flash:
switch: boot flash:c3560-ipservicesk9-mz.<version>.bin
```

## Schritt 4: Aufräumen

Sobald IOS läuft:

1. Image prüfen: `verify /md5 flash:<image>.bin`
2. `boot system` auf das neue Image setzen und speichern, wie in Schritt 2.
3. **Konsolengeschwindigkeit zurücksetzen.** Bleibt `BAUD` im Boot Loader auf 115200, behält auch die Konsole diese Geschwindigkeit. Wer sich später mit den üblichen 9600 Baud verbindet, sieht nur Zeichensalat. Setzen Sie den Wert im Boot Loader zurück (`set BAUD 9600`) oder stellen Sie sicher, dass die Konsolengeschwindigkeit in IOS dem entspricht, was Ihr Team erwartet.
4. Einmal neu starten, um zu bestätigen, dass der Switch ohne Hilfe startet.

## Was ist mit TFTP und USB?

Auf neueren Catalyst-Plattformen kann der Boot Loader mehr. Manche Modelle haben einen USB-Speicheranschluss (`usbflash0:`) oder können ein Image über den Management-Port aus dem Netzwerk starten. Das ist viel schneller als Xmodem. Beim klassischen 3560 gibt es diese Optionen nicht, Xmodem ist bei leerem Flash also der einzige Weg. Mit `help` am Prompt `switch:` sehen Sie, was Ihre Plattform unterstützt.

Dieselbe Idee, also von TFTP oder USB starten, wenn das Gerät nicht hochkommt, behandelt der [Nexus NX-OS Upgrade-Leitfaden](/de/posts/cisco-nexus-nxos-upgrade-guide/) für Rechenzentrums-Switches.

## Vorbeugung

- Bewahren Sie das aktuelle und das vorherige Image auf einem erreichbaren TFTP-Server auf.
- Prüfen Sie die MD5-Prüfsumme vor jedem Neustart nach einem Upgrade.
- Prüfen Sie `show boot` vor jedem geplanten Neustart.
- Halten Sie bei jedem Upgrade einen Konsolenzugang bereit. Ein Konsolenserver macht das auch aus der Ferne möglich: [Next-Gen Console Server Architektur](/de/posts/next-gen-console-server-architecture/).

## Verwandte Artikel

- [Cisco Catalyst 3560 Passwort-Wiederherstellung: Zwei Methoden](/de/posts/catalyst-3560-password-recovery/)
- [Catalyst 3560 IOS-Upgrade: Zwei Methoden und Verifizierung](/de/posts/catalyst-3560-ios-upgrade/)
- [Cisco Nexus NX-OS Software-Upgrade-Leitfaden](/de/posts/cisco-nexus-nxos-upgrade-guide/)
