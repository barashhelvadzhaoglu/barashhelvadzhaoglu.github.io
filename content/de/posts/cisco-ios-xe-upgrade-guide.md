---
title: "Cisco IOS und IOS-XE Upgrade-Leitfaden: Catalyst Switches und ISR Router"
description: "Cisco IOS- und IOS-XE-Software-Upgrade Schritt für Schritt für Catalyst Switches (2960, 3560, 3850, 9200, 9300, 9500) und Router (ISR 4000, ISR 1100, Catalyst 8000) — Flash-Prüfung, ROMMON, Install Mode, Bundle Mode, MD5 und Rollback."
date: 2026-10-22
draft: false
aliases:
  - "/de/posts/catalyst-3560-ios-upgrade/"

tags: ["Cisco", "IOS", "IOS-XE", "Upgrade", "Catalyst 9300", "Catalyst 9200", "Catalyst 9500", "Catalyst 3850", "Catalyst 2960", "Catalyst 3560", "ISR 4000", "ISR 1100", "Catalyst 8000"]
categories: ["Netzwerkbetrieb"]
keywords: ["Cisco IOS Upgrade", "Cisco IOS XE Upgrade", "install add file activate commit", "Catalyst 9300 Upgrade", "ISR 4331 Upgrade", "Cisco ROMMON Upgrade", "upgrade rom-monitor filename", "Bundle Mode zu Install Mode", "Cisco verify md5", "archive download-sw", "packages.conf", "install remove inactive"]
showToc: true
TocOpen: true
---

Die meisten Cisco-Upgrades scheitern, bevor der erste Befehl eingegeben ist: das falsche Image für die Plattform, zu wenig Platz im Flash, ein ROMMON, der für das Ziel-Release zu alt ist, oder eine Boot-Variable, die ins Leere zeigt. Dieser Leitfaden stellt die Prüfungen an den Anfang und die Befehle danach.

Er behandelt beide Familien aus der Praxis:

| Familie | Typische Modelle | Software | Dateisystem | Upgrade-Methode |
| --- | --- | --- | --- | --- |
| Klassische Catalyst Switches | 2960, 2960-X, 3560, 3750 | IOS | `flash:` | `archive download-sw` oder `.bin` + `boot system` |
| IOS-XE Catalyst Switches | 3650, 3850, 9200, 9300, 9400, 9500 | IOS-XE | `flash:` (bei manchen Modellen `bootflash:`) | Install Mode (`packages.conf`) |
| IOS-XE Router | ISR 4000, ISR 1100, Catalyst 8200/8300, Catalyst 8000V | IOS-XE | `bootflash:` | Install Mode oder Bundle Mode |
| Klassische IOS-Router | ISR G2, C900 | IOS | `flash:` | `.bin` + `boot system` |

Die Befehle sind die, die ich in der Praxis auf Catalyst Switches und ISR Routern verwende. IP-Adressen und Pfade in den Beispielen sind Platzhalter.

## 1. Zuerst die Plattform prüfen

### Dateisystem: flash: oder bootflash:?

Nicht raten, sondern das Gerät fragen:

```
show file systems
dir
```

Klassische Catalyst Switches und Catalyst 9200/9300 verwenden `flash:`. ISR- und Catalyst-8000-Router verwenden `bootflash:`. Auf vielen IOS-XE-Plattformen ist ein Name ein Alias für den anderen. Verwenden Sie, was das Gerät anzeigt. Jeder Befehl in diesem Leitfaden funktioniert mit beiden Namen.

### Modell, Version und Boot-Modus

```
show version
show inventory
show boot            ! Switches
show bootvar         ! Router
show install summary ! nur IOS-XE
```

Notieren Sie:

- **Genaues Modell und Plattformfamilie.** Ein Image für einen ISR 4300 startet nicht auf einem ISR 4400. Die Plattformfamilie steht im Dateinamen, zum Beispiel `isr4300-universalk9`, `c1100-universalk9`, `cat9k_iosxe`.
- **Aktuelle Version.**
- **Boot-Modus bei IOS-XE.** Zeigt die Boot-Variable auf `packages.conf`, läuft das Gerät im **Install Mode**. Zeigt sie auf eine `.bin`-Datei, läuft es im **Bundle Mode**.

### Freier Speicher

`dir` zeigt ganz unten den freien Speicher. Ein IOS-XE-Image ist groß, und der Install Mode braucht zusätzlichen Platz zum Entpacken. Ist es knapp, räumen Sie vorher auf:

```
install remove inactive   ! IOS-XE Install Mode: entfernt ungenutzte Pakete
delete flash:<altes-image>.bin
```

## 2. Release Notes lesen: Upgrade-Pfad und ROMMON

Zwei Angaben in den Release Notes entscheiden, ob das Upgrade funktioniert:

- **Upgrade-Pfad.** Manche Sprünge werden nicht direkt unterstützt. Cisco dokumentiert zum Beispiel, dass Catalyst 9500 Switches im Bundle Mode von 16.x auf 17.x über ein Zwischen-Release gehen sollten, während der Install Mode den direkten Sprung unterstützt.
- **Minimale ROMMON-Version.** Jedes IOS-XE-Release braucht eine minimale ROMMON-Version (Boot Loader). Hat das Gerät einen älteren ROMMON, startet das neue Image eventuell nicht, und das Gerät bleibt am `rommon`-Prompt stehen.

Aktuelle ROMMON-Version prüfen:

```
show rom-monitor r0          ! ISR 4000 und ähnliche Router
show version | include ROM   ! die meisten Plattformen
```

### Braucht der ROMMON ein eigenes Upgrade?

- **Catalyst 9000:** Meist nicht von Hand. Enthält ein neues Release einen neueren ROMMON, aktualisiert der Switch seinen primären ROMMON beim ersten Start automatisch. Der Golden-ROMMON (Backup) wird manuell mit dem Befehl `upgrade rom-monitor capsule golden` aktualisiert. Die genauen Argumente unterscheiden sich je nach Modell, prüfen Sie den Upgrade-Leitfaden Ihrer Plattform.
- **ISR 4000 und ähnliche Router:** Jedes Mal prüfen. Ein bekannter Fall sind ISR-4000-Router, die ROMMON 16.12(2r) brauchen, bevor sie 17.x-Releases starten.

### ROMMON-Upgrade auf einem ISR 4000

Der ROMMON wird aus dem laufenden IOS-XE aktualisiert, nicht vom ROMMON-Prompt aus. ROMMON-Paket kopieren, prüfen, dann:

```
copy ftp://192.0.2.10/images/isr4200_4300_rommon_1612_2r_SPA.pkg bootflash:
verify /md5 bootflash:isr4200_4300_rommon_1612_2r_SPA.pkg
upgrade rom-monitor filename bootflash:isr4200_4300_rommon_1612_2r_SPA.pkg R0
reload
show rom-monitor r0
```

Führen Sie das ROMMON-Upgrade **vor** dem Software-Upgrade durch. Startet das Gerät danach nicht mehr, hilft [Cisco ROMMON Recovery](/de/posts/cisco-rommon-recovery/).

### Secure Boot und signierte Images

IOS-XE-Images sind signiert. Das `.SPA` im Dateinamen steht für ein signiertes Produktions-Image. Das Gerät prüft die Signatur beim Start. Ein Image für die falsche Plattform oder eine beschädigte Datei besteht diese Prüfung nicht und startet nicht. Verwenden Sie nur Images aus Cisco Software Download und prüfen Sie immer die Prüfsumme.

## 3. Image kopieren und prüfen

FTP ist für große IOS-XE-Images schneller und zuverlässiger als TFTP:

```
copy ftp://192.0.2.10/images/isr4300-universalk9.17.12.08.SPA.bin bootflash:
copy ftp://192.0.2.10/images/c1100-universalk9.17.12.08.SPA.bin bootflash:
copy tftp://192.0.2.10/cat9k_iosxe.<version>.SPA.bin flash:
```

Server-Einrichtung, Zugangsdaten, der doppelte Schrägstrich in FTP-Pfaden und das Management-VRF stehen in [TFTP-, FTP- und SCP-Server für Cisco-Upgrades](/de/posts/tftp-ftp-server-cisco-upgrades/).

MD5-Prüfsumme mit dem Wert von der Cisco-Download-Seite vergleichen:

```
verify /md5 bootflash:c1100-universalk9.17.12.08.SPA.bin
```

Stimmen die Werte nicht überein, löschen Sie die Datei und kopieren sie erneut. Installieren Sie nie ein Image, dessen Prüfung fehlgeschlagen ist.

## 4. Upgrade im Install Mode (IOS-XE)

Der Install Mode ist der empfohlene Modus für Catalyst 9000 Switches und aktuelle ISR- und Catalyst-8000-Router. Ein Befehl fügt die neue Software hinzu, aktiviert und bestätigt sie:

```
install add file bootflash:isr4300-universalk9.17.12.08.SPA.bin activate commit
```

Das Gerät fragt, ob es neu starten darf. Antworten Sie mit `y`. Nach dem Neustart:

```
show version
show install summary
install remove inactive
```

`show install summary` sollte die neue Version als `Committed` zeigen. `install remove inactive` entfernt die alten Pakete und schafft Platz.

Auf Catalyst 9000 Switches ist der Befehl derselbe, mit dem Dateisystem des Switches:

```
install add file flash:cat9k_iosxe.<version>.SPA.bin activate commit
```

### Mehrere Zwischenschritte

Verlangen die Release Notes ein Zwischen-Release, wiederholen Sie den Ablauf pro Schritt: kopieren, prüfen, `install add ... activate commit`, kontrollieren, `install remove inactive`. Zum Beispiel erst 17.9, dann 17.12. Räumen Sie zwischen den Schritten auf, damit Platz für das nächste Image ist.

### Vom Bundle Mode in den Install Mode

Ein Gerät im Bundle Mode startet direkt eine `.bin`-Datei. So wechseln Sie in den Install Mode:

1. `install add file <image>.bin activate commit` wie oben ausführen. Das entpackt die Pakete und legt `packages.conf` an.
2. Sicherstellen, dass die Boot-Variable auf `packages.conf` zeigt:

```
configure terminal
no boot system
boot system flash:packages.conf
end
write memory
show boot
```

Auf Routern verwenden Sie `bootflash:packages.conf`.

## 5. Bundle Mode und klassisches IOS

### IOS-XE im Bundle Mode, ISR G2, C900

```
configure terminal
no boot system
boot system bootflash:<image>.bin
end
write memory
show bootvar
reload
```

Auf klassischen IOS-Routern wie der C900-Serie ist das Dateisystem `flash:` und der Image-Name hat das alte Format, zum Beispiel `c900-universalk9-mz.SPA.<version>.bin`.

### Klassische Catalyst Switches (2960, 3560, 3750)

Diese Switches bieten `archive download-sw`. Der Befehl überträgt eine `.tar`-Datei, entpackt sie, setzt die Boot-Variable und kann neu starten:

```
archive download-sw /overwrite /reload tftp://192.0.2.10/c3560-ipservicesk9-tar.<version>.tar
```

- `/overwrite` ersetzt das aktuelle Image, wenn der Flash nur für eines Platz hat.
- `/leave-old-sw` behält das alte Image, wenn Platz für beide ist. Ein Rollback ist dann nur eine Änderung der Boot-Variable.

Alternativ kopieren Sie die `.bin`-Datei, prüfen sie und setzen `boot system flash:<image>.bin` wie oben.

## 6. Nach dem Upgrade

```
show version
show install summary          ! IOS-XE Install Mode
show interfaces status        ! Switches
show ip interface brief
show power inline             ! PoE-Switches
show logging
```

Bei Stacks und redundanten Systemen prüfen Sie jedes Mitglied: `show switch` bei Catalyst-Stacks, `show redundancy` bei Systemen mit zwei Supervisors.

## 7. Rollback

- **Install Mode:** `show install rollback` listet die Rollback-Punkte.
- **Bundle Mode und klassisches IOS:** `boot system` auf das alte Image zurückstellen, sofern es noch im Flash liegt, und neu starten.
- **Gerät bleibt im ROMMON oder am Prompt `switch:` stehen:** siehe [Cisco ROMMON Recovery](/de/posts/cisco-rommon-recovery/).

## Häufige Fehler

- **Image für die falsche Plattformfamilie.** Es besteht die Signatur- oder Plattformprüfung nicht und startet nicht.
- **ROMMON nicht geprüft.** Das neue Image braucht einen neueren ROMMON, und das Gerät bleibt am `rommon`-Prompt stehen.
- **Kein Platz für den Install Mode.** Das Entpacken bricht ab. Vorher `install remove inactive` ausführen.
- **Boot-Variable zeigt nach dem Wechsel in den Install Mode noch auf die alte `.bin`.** Das Gerät startet die alte Version im Bundle Mode.
- **Kein Konsolenzugang während des Neustarts.** Ein Konsolenserver macht das auch aus der Ferne möglich: [Next-Gen Console Server Architektur](/de/posts/next-gen-console-server-architecture/).

## Verwandte Artikel

- [Cisco ROMMON Recovery: Start aus Flash, über TFTP oder USB](/de/posts/cisco-rommon-recovery/)
- [TFTP-, FTP- und SCP-Server für Cisco-Upgrades](/de/posts/tftp-ftp-server-cisco-upgrades/)
- [Cisco Switch und Router Passwort-Wiederherstellung](/de/posts/cisco-switch-password-recovery/)
- [Cisco Nexus NX-OS Software-Upgrade-Leitfaden](/de/posts/cisco-nexus-nxos-upgrade-guide/)

Quellen: [Cisco: Upgrading Catalyst 9500 Switches](https://www.cisco.com/c/en/us/support/docs/switches/catalyst-9500-series-switches/222279-upgrading-catalyst-9500-switches.html) · [Cisco: Upgrading Catalyst 9300 Switches](https://www.cisco.com/c/de_de/support/docs/switches/catalyst-9300-series-switches/222280-upgrading-catalyst-9300-switches.html)
