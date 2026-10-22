---
title: "Cisco ROMMON Recovery: Switch oder Router aus Flash, über TFTP oder USB starten"
description: "Cisco Switch oder Router hängt am Prompt switch: oder rommon? Wiederherstellungsszenarien für Catalyst 9300, 9200, 3850, 2960, 3560 und ISR 4000 — Start aus Flash, ROMMON-Netzwerkvariablen, Start über TFTP oder USB und ein veralteter ROMMON."
date: 2026-10-22
draft: false
aliases:
  - "/de/posts/catalyst-3560-boot-loader-recovery/"

tags: ["Cisco", "ROMMON", "Boot Loader", "Recovery", "IOS-XE", "Catalyst 9300", "Catalyst 9200", "Catalyst 3850", "Catalyst 2960", "Catalyst 3560", "ISR 4000"]
categories: ["Netzwerkbetrieb"]
keywords: ["Cisco ROMMON Wiederherstellung", "Cisco Switch hängt im ROMMON", "switch: Prompt", "rommon boot tftp", "IP_ADDRESS DEFAULT_GATEWAY rommon", "boot usbflash0", "emergency-install", "Cisco ROMMON zu alt", "Catalyst 9300 Bootloader", "ISR 4331 rommon"]
showToc: true
TocOpen: true
---

Nach einem Neustart kommt das Gerät nicht zurück. Auf der Konsole steht nur `switch:` (Catalyst Switches) oder `rommon 1 >` (Router). Das ist der ROMMON, auch Boot Loader genannt: das kleine Programm, das IOS startet. Er ist stehen geblieben, weil er kein gültiges Image finden oder starten konnte.

In den meisten Fällen ist das kein Hardwaredefekt, und das Gerät muss nicht getauscht werden. Welcher Weg hinausführt, hängt von einer Frage ab: **Liegt noch ein gutes Image im Flash?**

| Szenario | Situation | Ausweg |
| --- | --- | --- |
| 1 | Das richtige Image liegt im Flash | Starten, Boot-Variable korrigieren |
| 2 | Das Image fehlt oder ist beschädigt | Über TFTP oder USB starten, dann das Image in den Flash kopieren |
| 3 | Das Image ist da, aber der ROMMON ist zu alt dafür | Älteres Image starten, ROMMON aktualisieren, dann upgraden |

## Vorab: Konsolenzugang

Der ROMMON ist nur über die Konsole erreichbar. In einer Filiale heißt das Laptop und Konsolenkabel. Im Rechenzentrum, wo man selten direkt am Rack steht, macht erst ein Konsolenserver die Wiederherstellung überhaupt möglich: [Next-Gen Console Server Architektur](/de/posts/next-gen-console-server-architecture/).

Zuerst die Umgebung ansehen:

```
switch: dir flash:
switch: set
```

Auf Routern:

```
rommon 1 > dir bootflash:
rommon 2 > set
```

`set` zeigt die Boot-Loader-Variablen. Wichtig sind `BOOT` (welches Image gestartet wird) und bei manchen Switches `MANUAL_BOOT` (bei `yes` hält der Switch immer am Prompt an). Auf Routern prüfen Sie zusätzlich das Konfigurationsregister mit `confreg`. Der Wert `0x2100` hält den Router im ROMMON. Der normale Wert ist `0x2102`.

`help` oder `?` listet die Befehle, die Ihre ROMMON-Version unterstützt.

## Szenario 1: Das richtige Image liegt im Flash

Das Image ist da, aber die Boot-Variable stimmt nicht: ein Tippfehler nach einem Upgrade, ein gelöschter Dateiname oder `MANUAL_BOOT=yes`.

### Manuell starten

Catalyst 9000 und andere IOS-XE-Switches im Install Mode:

```
switch: boot flash:packages.conf
```

Im Bundle Mode oder auf klassischen Catalyst Switches:

```
switch: boot flash:<image>.bin
```

Auf klassischen Catalyst Switches liegen Images, die mit `archive download-sw` installiert wurden, in einem Unterverzeichnis. Prüfen Sie den vollständigen Pfad mit `dir flash:<verzeichnis>`.

Router:

```
rommon 1 > boot bootflash:<image>.bin
```

Ist der Router wegen des Konfigurationsregisters im ROMMON geblieben:

```
rommon 1 > confreg 0x2102
rommon 2 > reset
```

### Boot-Variable in IOS korrigieren

Sobald IOS läuft, machen Sie die Korrektur dauerhaft, sonst kehrt das Problem beim nächsten Neustart zurück:

```
configure terminal
no boot system
boot system flash:packages.conf
end
write memory
show boot
```

Im Bundle Mode verwenden Sie statt `packages.conf` den Namen der `.bin`-Datei, auf Routern `bootflash:`.

## Szenario 2: Das Image fehlt oder ist beschädigt

Das Image wurde versehentlich gelöscht, der Kopiervorgang wurde abgebrochen, oder der Flash ist leer. Sie müssen ein Image von außen auf das Gerät bringen. Dafür gibt es zwei praktische Wege.

| | TFTP aus dem ROMMON | USB |
| --- | --- | --- |
| Jemand vor Ort nötig | Nein | Ja |
| Funktioniert über einen Konsolenserver | Ja | Nur wenn jemand den Stick einsteckt |
| Geschwindigkeit | Abhängig vom Netzwerk | Schnell |
| Typischer Einsatz | Rechenzentrum, entfernte Standorte | Filiale, Lab |

### Option A: Start über TFTP aus dem ROMMON

Sind Sie über einen Konsolenserver aus der Ferne verbunden und funktioniert das Netzwerk um das Gerät herum, ist TFTP die praktischste Option. Der schwierige Teil ist die Netzwerkkonfiguration im ROMMON, denn der ROMMON hat kein IOS, kein Routing und kein DHCP. Sie setzen alles von Hand.

**Voraussetzungen:**

- Der **Management-Port** ist verbunden und erreichbar. Bei Catalyst 9000 Switches ist das der dedizierte Management-Port (Gi0/0). Der ROMMON verwendet nicht die Ports an der Vorderseite.
- Ein TFTP-Server mit dem Image ist aus dem Management-Netz erreichbar. Einrichtung und Firewall-Regeln: [TFTP-, FTP- und SCP-Server für Cisco-Upgrades](/de/posts/tftp-ftp-server-cisco-upgrades/).

**Catalyst 9000 Switches:**

```
switch: set IP_ADDRESS 192.0.2.50
switch: set IP_SUBNET_MASK 255.255.255.0
switch: set DEFAULT_GATEWAY 192.0.2.1
switch: ping 192.0.2.10
switch: boot tftp://192.0.2.10/cat9k_iosxe.<version>.SPA.bin
```

Testen Sie zuerst mit `ping`. Schlägt der Ping fehl, hat der Start keinen Sinn. Prüfen Sie das Kabel am Management-Port, das Gateway und die Firewall auf dem TFTP-Server.

Laut Cisco gelten zwei Einschränkungen:

- Der Switch startet über TFTP **im Bundle Mode**.
- Das Image wird **nicht in den Flash kopiert**. Es läuft nur aus dem Arbeitsspeicher. Nach dem nächsten Neustart stehen Sie wieder am Prompt.

**ISR 4000 und andere IOS-XE-Router:**

```
rommon 1 > IP_ADDRESS=192.0.2.50
rommon 2 > IP_SUBNET_MASK=255.255.255.0
rommon 3 > DEFAULT_GATEWAY=192.0.2.1
rommon 4 > TFTP_SERVER=192.0.2.10
rommon 5 > TFTP_FILE=isr4300-universalk9.<version>.SPA.bin
rommon 6 > set
rommon 7 > boot tftp://192.0.2.10/isr4300-universalk9.<version>.SPA.bin
```

Variablennamen und die genaue Boot-Syntax unterscheiden sich je nach ROMMON-Version. Prüfen Sie mit `set` und `help`. Ältere Router (ISR G2) verwenden stattdessen den Befehl `tftpdnld`, der das Image direkt in den Flash schreibt.

**Nachdem das Gerät über TFTP gestartet ist:** Image in den Flash kopieren, prüfen und sauber einrichten, wie im [Upgrade-Leitfaden](/de/posts/cisco-ios-xe-upgrade-guide/) beschrieben:

```
copy tftp://192.0.2.10/<image>.bin flash:
verify /md5 flash:<image>.bin
install add file flash:<image>.bin activate commit
```

Auf Geräten im Bundle Mode oder mit klassischem IOS setzen Sie statt `install add` die Boot-Variable `boot system` auf die kopierte Datei.

### Option B: Start von USB

Kann jemand einen USB-Stick einstecken, ist das der einfachste und schnellste Weg. Formatieren Sie den Stick mit FAT32 und kopieren Sie das Image darauf.

```
switch: dir usbflash0:
switch: boot usbflash0:<image>.bin
```

Auf ISR-Routern heißt das USB-Gerät meist `usb0:` (bei manchen Modellen `usb1:`):

```
rommon 1 > dir usb0:
rommon 2 > boot usb0:<image>.bin
```

Wenn das Gerät läuft, kopieren Sie das Image vom USB-Stick in den Flash und korrigieren die Boot-Variable:

```
copy usbflash0:<image>.bin flash:
verify /md5 flash:<image>.bin
```

Dann installieren oder `boot system` setzen wie in Szenario 1.

### Option C: emergency-install (Catalyst 9000)

Catalyst 9000 Switches (außer der Serie 9200) haben im ROMMON den Befehl `emergency-install`. Er installiert ein Image von TFTP direkt in den Flash:

```
switch: emergency-install tftp://192.0.2.10/cat9k_iosxe.<version>.SPA.bin
switch: boot flash:packages.conf
```

Achtung: Das **löscht das gesamte Flash-Dateisystem**, einschließlich der Konfiguration. Verwenden Sie es nur, wenn Option A und B nicht möglich sind, und nur mit einem Konfigurations-Backup.

### Option D: Xmodem über die Konsole (klassische Catalyst)

Klassische Catalyst Switches wie 2960 und 3560 haben im Boot Loader keinen Netzwerk-Stack und oft keinen USB-Port. Der letzte Ausweg ist eine Übertragung über die Konsole mit Xmodem:

```
switch: flash_init
switch: set BAUD 115200
switch: copy xmodem: flash:<image>.bin
```

Nach `set BAUD` stellen Sie Ihr Terminalprogramm auf 115200 Baud um. Selbst bei dieser Geschwindigkeit dauert die Übertragung lange. Setzen Sie die Geschwindigkeit danach mit `set BAUD 9600` zurück, sonst sieht die nächste Person, die sich mit 9600 Baud verbindet, nur Zeichensalat.

## Szenario 3: Der ROMMON ist zu alt für das neue Image

Das Image liegt korrekt im Flash, aber das Gerät startet es trotzdem nicht. Bei ISR-4000-Routern passiert das, wenn das Ziel-Release einen neueren ROMMON braucht als das Gerät hat, zum Beispiel 17.x-Releases, die ROMMON 16.12(2r) voraussetzen.

Soweit ich weiß, lässt sich der ROMMON auf diesen Plattformen nicht vom ROMMON-Prompt aus aktualisieren. Das Upgrade läuft aus IOS-XE. Der Ausweg:

1. Ein **älteres Image** starten, das mit dem aktuellen ROMMON funktioniert. Aus dem Flash, wenn Sie es behalten haben, sonst über TFTP oder USB wie in Szenario 2.
2. In IOS-XE den ROMMON aktualisieren: `upgrade rom-monitor filename bootflash:<rommon>.pkg R0`, dann neu starten.
3. Mit `show rom-monitor r0` prüfen.
4. Jetzt das neue Image installieren.

Deshalb steht die ROMMON-Prüfung im [Upgrade-Leitfaden](/de/posts/cisco-ios-xe-upgrade-guide/) vor dem Upgrade.

Ein verwandter Fall: Die Boot-Variable zeigt auf ein Image einer anderen Plattformfamilie, zum Beispiel ein ISR-4300-Image auf einem ISR 4400. Das Gerät bleibt im ROMMON. Starten Sie das richtige Image manuell und korrigieren Sie die Boot-Variable.

## Vorbeugung

- Bewahren Sie das aktuelle und das vorherige Image auf einem Server auf, der aus dem Management-Netz erreichbar ist.
- Prüfen Sie vor jedem geplanten Neustart `show boot` (oder `show bootvar`) und die ROMMON-Anforderung.
- Schließen Sie den Management-Port an und testen Sie ihn, bevor Sie ihn brauchen.
- Halten Sie bei jedem Upgrade Konsolenzugang bereit: [Next-Gen Console Server Architektur](/de/posts/next-gen-console-server-architecture/).

## Verwandte Artikel

- [Cisco IOS und IOS-XE Upgrade-Leitfaden](/de/posts/cisco-ios-xe-upgrade-guide/)
- [TFTP-, FTP- und SCP-Server für Cisco-Upgrades](/de/posts/tftp-ftp-server-cisco-upgrades/)
- [Cisco Switch und Router Passwort-Wiederherstellung](/de/posts/cisco-switch-password-recovery/)
- [Cisco Nexus NX-OS Upgrade-Leitfaden (mit ROMMON-Wiederherstellung)](/de/posts/cisco-nexus-nxos-upgrade-guide/)

Quellen: [Cisco: Troubleshoot Bootloader and Password Recovery on Catalyst 9000](https://cisco.com/c/en/us/support/docs/switches/catalyst-9300-series-switches/216944-troubleshoot-bootloader-rommon-and-pas.html) · [Cisco: ISR 4000 Stuck in ROMMON](https://www.cisco.com/c/en/us/support/docs/routers/4000-series-integrated-services-routers/200678-Troubleshoot-Cisco-4000-Series-ISR-Stuck.html)
