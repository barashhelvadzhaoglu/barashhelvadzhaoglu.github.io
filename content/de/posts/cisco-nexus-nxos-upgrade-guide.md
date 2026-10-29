---
title: "Cisco Nexus NX-OS Software-Upgrade-Leitfaden: Praxiserprobter Schritt-für-Schritt"
description: "Praxisleitfaden für Cisco Nexus NX-OS Upgrades — Vorbereitung, Upgrade-Pfad, Dateiübertragung, Rollback und ROMMON-Wiederherstellung."
date: 2025-12-30
draft: false

cover:
  image: "/img/postimages/nexus-nxos-upgrade-cover.webp"
  alt: "Cisco Nexus NX-OS Software-Upgrade-Leitfaden"
  relative: false

tags: ["Cisco", "Nexus", "NX-OS", "Netzwerk", "Upgrade", "Rechenzentrum"]
categories: ["Netzwerkbetrieb"]
keywords: ["Cisco Nexus Upgrade", "NX-OS Upgrade Leitfaden", "Nexus Software Update", "NX-OS ROMMON Wiederherstellung", "Nexus Upgrade Pfad", "Cisco Nexus Rollback", "NX-OS install all", "Nexus Bootflash Upgrade", "Cisco Rechenzentrum Upgrade", "NX-OS MD5 Verifikation"]
showToc: true
TocOpen: true
aliases:
  - "/de/posts/cisco-nexus-nxos-software-upgrade-leitfaden/"
---

Dieser Leitfaden behandelt den **Cisco Nexus NX-OS Software-Upgrade-Prozess** auf praktische, schrittweise Weise — einschließlich **Rollback- und Wiederherstellungsszenarien**. Das Ziel ist es, Serviceunterbrechungen zu minimieren und sicherzustellen, dass das Gerät im Fehlerfall immer wiederhergestellt werden kann.

Die meisten Upgrade-Fehler werden nicht durch das Upgrade selbst verursacht — sie entstehen durch das Überspringen von Vorbereitungsschritten. Dieser Leitfaden behandelt die Vorbereitung genauso ernst wie die Ausführung.

{{< figure src="/img/postimages/nexus-nxos-upgrade-cover.webp" title="Cisco Nexus NX-OS Upgrade-Prozess" >}}

> Für Out-of-Band-Zugang bei Upgrade-Fehlern: [Die Hintertür des Netzwerks: Next-Gen Console Server Architektur](/de/posts/next-gen-console-server-architecture/)

## 1. Vorbereitungschecks

Bevor Sie mit dem Software-Upgrade beginnen, müssen Sie die folgenden Vorbereitungsschritte abschließen. Diese Phase wird am häufigsten übersprungen — und ist die häufigste Problemquelle.

### Konfigurationssicherung

- Erstellen Sie zunächst eine **Sicherung der aktuellen Konfiguration**.
- Speichern Sie die Sicherung auf Ihrem eigenen Computer oder an einem **externen Ort** wie FTP/SFTP — nicht auf dem Switch selbst.
- Wenn das Upgrade fehlschlägt oder ein Rollback erforderlich ist, ist diese Sicherung kritisch.

### Switch-Modell und aktuelle Software-Version prüfen

Überprüfen Sie das Switch-Modell und die laufende NX-OS-Version mit diesen Befehlen:

```bash
show version
show module
show inventory
```

Beispielausgabe (gekürzt, Werte sind Platzhalter):

```
switch# show version
Cisco Nexus Operating System (NX-OS) Software
...
Software
  BIOS: version 05.xx
  NXOS: version 9.3(8)
  NXOS image file is: bootflash:///nxos.9.3.8.bin

Hardware
  cisco Nexus9000 C93180YC-FX Chassis
  Intel(R) Xeon(R) CPU with 24569476 kB of memory.
  Processor Board ID XXXXXXXXXXX
  Device name: N9K-LAB-01
  bootflash:  115805708 kB

switch# show inventory
NAME: "Chassis",  DESCR: "Nexus9000 C93180YC-FX Chassis"
PID: N9K-C93180YC-FX     ,  VID: V0x ,  SN: XXXXXXXXXXX
```

Diese Ausgaben sind erforderlich, um das richtige NX-OS-Image auszuwählen, den Upgrade-Pfad zu bestimmen und die Hardware-Kompatibilität zu überprüfen.

## 2. Software-Image herunterladen

- Laden Sie das korrekte NX-OS-Image für Ihr Switch-Modell vom offiziellen Cisco-Portal herunter:
  [https://software.cisco.com/download/home](https://software.cisco.com/download/home)
- Ein gültiger **Cisco-Account mit den entsprechenden Berechtigungen** ist erforderlich.
- Notieren Sie nach dem Download den **MD5-Hash-Wert** — Sie benötigen ihn zur Überprüfung der Dateiintegrität nach der Übertragung.

> Die MD5-Überprüfung bestätigt, dass die Datei während des Downloads nicht beschädigt wurde. Dieser Schritt ist nicht optional.

## 3. Upgrade-Pfad überprüfen

Ein direktes Upgrade von Ihrer aktuellen NX-OS-Version auf die Zielversion ist **nicht immer unterstützt**. Einige Versionskombinationen erfordern Zwischenschritte.

Verwenden Sie Ciscos offizielle Tools zur Überprüfung:

- **Nexus Upgrade Matrix Tools**
- Nexus 9000 / 3000 Series
- Nexus 7000 Series

> Wenn mehrere Upgrade-Schritte erforderlich sind, laden Sie **alle Zwischen-Images** herunter, bevor Sie beginnen.

## 4. Software-Datei auf den Switch kopieren

### Option A: FTP-Transfer

FTP ist eine der gebräuchlichsten Methoden. Beachten Sie, dass NX-OS-Images bis zu 2 GB groß sein können.

```bash
copy ftp://<user>@10.10.10.5/nxos.9.3.10.bin bootflash: vrf management
```

Wenn mehrere VRFs auf dem Nexus konfiguriert sind, werden Sie gefragt, welches VRF für die Übertragung verwendet werden soll. Da die Management-Schnittstelle typischerweise das Management-VRF verwendet, wählen Sie Management-VRF.

### Option B: USB-Transfer (Empfohlen)

USB-Transfer ist meine bevorzugte Methode, wenn:

- Kein FTP-Server verfügbar ist
- Zeitdruck besteht
- Kein Netzwerk-Transferrisiko eingegangen werden soll

```bash
copy usb1:nxos.9.3.10.bin bootflash:
```

Stellen Sie sicher, dass das USB-Dateisystemformat vom Nexus-Gerät unterstützt wird.

### MD5-Hash-Überprüfung

Überprüfen Sie nach der Übertragung die Dateiintegrität:

```bash
show file bootflash:nxos.9.3.10.bin md5sum
```

Beispielausgabe (gekürzt, Werte sind Platzhalter):

```
switch# show file bootflash:nxos.9.3.10.bin md5sum
<32-character MD5 value of the file>
```

Vergleichen Sie diesen Wert mit dem MD5-Hash auf der Cisco-Download-Seite.

Die Ausgabe muss exakt mit dem MD5-Hash vom Cisco-Download-Portal übereinstimmen.

## 5. Upgrade durchführen

Sobald alle Checks abgeschlossen sind, starten Sie das Upgrade:

```bash
install all nxos bootflash:nxos.9.3.10.bin
```

Beispielausgabe (gekürzt, Werte sind Platzhalter):

```
switch# install all nxos bootflash:nxos.9.3.10.bin
Installer will perform compatibility check first. Please wait.
Installer is forced disruptive

Verifying image bootflash:/nxos.9.3.10.bin for boot variable "nxos".
[####################] 100% -- SUCCESS

Verifying image type.
[####################] 100% -- SUCCESS

Performing module support checks.
[####################] 100% -- SUCCESS

Compatibility check is done:
Module  bootable          Impact  Install-type  Reason
------  --------  --------------  ------------  ------
     1       yes      disruptive         reset  Default upgrade is not hitless

Images will be upgraded according to following table:
Module       Image   Running-Version(pri:alt)   New-Version   Upg-Required
------  ----------  -------------------------  ------------  ------------
     1        nxos                     9.3(8)        9.3(10)           yes

Switch will be reloaded for disruptive upgrade.
Do you want to continue with the installation (y/n)?  [n] y

Install is in progress, please wait.

Performing runtime checks.
[####################] 100% -- SUCCESS

Setting boot variables.
[####################] 100% -- SUCCESS

Performing configuration copy.
[####################] 100% -- SUCCESS

Finishing the upgrade, switch will reboot in 10 seconds.
```

- Der Switch speichert die aktuelle Konfiguration automatisch vor der Installation.
- Sie werden vor dem Neustart zur Bestätigung aufgefordert.
- Nach der Bestätigung startet das Gerät neu und das Upgrade beginnt.

Die Upgrade-Dauer variiert je nach Gerätemodell und Software-Größe.

## 6. Rollback und Wiederherstellungsszenarien

{{< figure src="/img/postimages/nexus-upgrade-rollback.webp" title="Nexus Upgrade Rollback und Wiederherstellungspfad" >}}

### ROMMON-Modus betreten

Wenn die Installation fehlschlägt oder das Gerät nicht startet:

- Drücken Sie während des Gerätestarts über die Console-Verbindung **CTRL + L** oder **CTRL + C**, um den **ROMMON-Modus** aufzurufen.

### Option 1: Das Image liegt noch im Bootflash

Liegt das Image im Bootflash, aber die Boot-Variable stimmt nicht, starten Sie es direkt:

```
loader > dir
loader > boot bootflash:nxos.9.3.10.bin
```

Sobald NX-OS läuft, korrigieren Sie die Boot-Variable wie am Ende dieses Abschnitts gezeigt.

### Option 2: Image über TFTP starten

Fehlt das Image, ist der Bootflash aber intakt, starten Sie das komplette Image über den Management-Port von einem TFTP-Server. Switch-IP und TFTP-Server sind zwei verschiedene Adressen, und der Pfad zum Image muss vollständig angegeben werden:

```
loader > set ip 10.10.10.20 255.255.255.0
loader > set gw 10.10.10.1
loader > boot tftp://10.10.10.5/tftpboot/nxos.9.3.10.bin
```

Beispielausgabe (gekürzt, Werte sind Platzhalter):

```
loader > set ip 10.10.10.20 255.255.255.0
Correct - ip addr is 10.10.10.20, mask is 255.255.255.0
loader > set gw 10.10.10.1
Correct gateway addr 10.10.10.1
loader > boot tftp://10.10.10.5/tftpboot/nxos.9.3.10.bin
Filesystem type is tftp, using whole disk
Booting nxos image: tftp://10.10.10.5/tftpboot/nxos.9.3.10.bin....
...
Image verification OK
```

Das Image läuft nur aus dem Arbeitsspeicher. Sobald NX-OS läuft, kopieren Sie es in den Bootflash und prüfen es:

```
copy tftp://10.10.10.5/tftpboot/nxos.9.3.10.bin bootflash: vrf management
show file bootflash:nxos.9.3.10.bin md5sum
```

### Option 3: Start von USB

```
loader > dir usb1:
loader > boot usb1:nxos.9.3.10.bin
```

Sobald NX-OS läuft, kopieren Sie das Image mit `copy usb1:nxos.9.3.10.bin bootflash:` in den Bootflash und prüfen den MD5-Wert.

### Option 4: Bootflash ist beschädigt (Recovery Mode)

Nur verwenden, wenn der Bootflash selbst beschädigt ist. **`init system` formatiert das Dateisystem des Geräts neu.** Stellen Sie vorher sicher, dass ein Konfigurations-Backup existiert.

```
loader > set ip 10.10.10.20 255.255.255.0
loader > set gw 10.10.10.1
loader > cmdline recoverymode=1
loader > boot tftp://10.10.10.5/tftpboot/nxos.9.3.10.bin
switch(boot)# init system
switch(boot)# load-nxos
```

`cmdline recoverymode=1` hält den Start am Prompt `switch(boot)#` an. `load-nxos` schließt danach das Laden von NX-OS ab. Anschließend das Image in den Bootflash kopieren und die Konfiguration wiederherstellen. Quelle: [Cisco Nexus 9000 NX-OS Troubleshooting Guide](https://www.cisco.com/c/en/us/td/docs/dcn/nx-os/nexus9000/102x/Troubleshooting/cisco-nexus-9000-series-nx-os-troubleshooting-guide-release-102x/m-troubleshooting-installations-upgrades-and-reboots.html).

### Boot-Variable korrigieren

```bash
configure terminal
  boot nxos bootflash:/nxos.9.3.10.bin
end
copy running-config startup-config
show boot
```

Beispielausgabe (gekürzt, Werte sind Platzhalter):

```
Current Boot Variables:

sup-1
NXOS variable = bootflash:/nxos.9.3.10.bin
Boot POAP Disabled

Boot Variables on next reload:

sup-1
NXOS variable = bootflash:/nxos.9.3.10.bin
Boot POAP Disabled
```

## Kritische Warnung

Während des Software-Upgrades:

- **Unterbrechen Sie nicht die Netzwerkverbindung**
- **Unterbrechen Sie nicht die Stromversorgung**

Beides kann das Gerät ohne physische Intervention unwiederherstellbar machen.

---

## Verwandte Artikel

**Architektur & Betrieb**
- 🛠️ [Die Hintertür des Netzwerks: Next-Gen Console Server Architektur](/de/posts/next-gen-console-server-architecture/) — Out-of-Band-Zugang wenn IP-Management verloren geht
- 📊 [Monitoring richtig gemacht](/de/architecture/monitoring-not-just-seeing/) — Probleme erkennen bevor sie eskalieren
- 🏗️ [Switch, Firewall, AP — Warum die richtige Produktwahl allein nicht ausreicht](/de/architecture/core-network-is-not-a-product-list/) — Architektur-zuerst Core-Network-Design
- 🎯 [Produktauswahl in der Netzwerkinfrastruktur: Strategische Kriterien](/de/architecture/network-product-selection-strategy/) — Hersteller strategisch bewerten

**Praktisches Engineering**
- 🛡️ [Network Packet Broker (NPB) Masterclass](/de/posts/network-packet-broker-masterclass/) — Traffic-Sichtbarkeit und Sicherheitsstrategie
- 🔐 [802.1X Feldbereitstellungsguide](/de/technology/identity-based-microsegmentation-8021x/) — Identitätsbasierte Netzwerkzugangskontrolle