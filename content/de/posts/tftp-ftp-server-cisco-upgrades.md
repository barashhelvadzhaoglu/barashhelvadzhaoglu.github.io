---
title: "TFTP-, FTP- und SCP-Server für Cisco-Upgrades: Einrichtung und Fehlersuche"
description: "TFTP-, FTP- oder SCP-Server für Cisco IOS- und IOS-XE-Image-Übertragungen unter Windows, macOS und Linux einrichten — Befehle auf dem Gerät, Management-VRF, der doppelte Schrägstrich im FTP-Pfad, Größenlimits und Firewall-Probleme."
date: 2026-10-22
draft: false

tags: ["Cisco", "TFTP", "FTP", "SCP", "IOS", "IOS-XE", "Upgrade"]
categories: ["Netzwerkbetrieb"]
keywords: ["Cisco TFTP Server einrichten", "copy tftp flash", "copy ftp bootflash", "ip ftp username", "ip tftp source-interface", "Tftpd64", "tftpd-hpa", "macOS TFTP Server", "Cisco SCP kopieren", "TFTP 32MB Limit", "Mgmt-vrf copy"]
showToc: true
TocOpen: true
---

Jedes Cisco-Upgrade beginnt damit, eine Datei auf das Gerät zu bringen. Für ein 20 MB großes klassisches IOS-Image funktioniert fast alles. Für ein 1 GB großes IOS-XE-Image über eine WAN-Strecke entscheidet das Protokoll, ob die Kopie fünf Minuten dauert oder nach einer Stunde abbricht.

Dieser Leitfaden zeigt, welches Protokoll Sie wann verwenden, wie Sie den Server unter Windows, macOS und Linux einrichten und welche Befehle und Stolperfallen es auf dem Gerät gibt.

## Welches Protokoll?

| Protokoll | Port | Authentifizierung | Stärken | Schwächen |
| --- | --- | --- | --- | --- |
| TFTP | UDP 69 | Keine | Einfach, überall unterstützt, funktioniert aus dem ROMMON | Langsam, über WAN unzuverlässig, Größenlimits bei alten Servern |
| FTP | TCP 21 (+ Daten) | Benutzer und Passwort | Schnell und zuverlässig für große Images | Klartext, Datenkanal braucht Firewall-Anpassung |
| SCP | TCP 22 | SSH | Verschlüsselt, nutzt vorhandenen SSH-Zugang | Auf manchen Plattformen langsamer als FTP |
| HTTP(S) | TCP 80/443 | Optional | Schnell, einfach zu hosten | Auf älteren IOS-Versionen nicht verfügbar |

Meine Regel aus der Praxis:

- **FTP** für normale Upgrades über das Netzwerk. Schnell und zuverlässig für große IOS-XE-Images.
- **TFTP**, wenn das Gerät im ROMMON ist. Der ROMMON kann nur TFTP. Siehe [Cisco ROMMON Recovery](/de/posts/cisco-rommon-recovery/).
- **SCP**, wenn die Sicherheitsrichtlinie keine Klartextprotokolle erlaubt.

## Server einrichten

### Windows: Tftpd64

Tftpd64 ist ein kostenloses Tool, das TFTP-Server, DHCP-Server und Syslog-Server kombiniert.

1. Tftpd64 installieren und starten.
2. **Current Directory** auf den Ordner mit Ihren Images setzen.
3. **Server interface** wählen, also die IP-Adresse des Netzwerkadapters zu den Geräten.
4. Tftpd64 in der Windows-Firewall freigeben. Das ist der häufigste Grund für Timeouts.

Für FTP unter Windows ist FileZilla Server eine verbreitete kostenlose Wahl.

### macOS: Eingebauter TFTP-Server

macOS bringt einen TFTP-Server mit. Er liefert Dateien aus `/private/tftpboot`:

```
sudo mkdir -p /private/tftpboot
sudo cp <image>.bin /private/tftpboot/
sudo chmod 644 /private/tftpboot/<image>.bin
sudo launchctl load -F /System/Library/LaunchDaemons/tftp.plist
```

Beenden mit `sudo launchctl unload -F /System/Library/LaunchDaemons/tftp.plist`. Ist die macOS-Firewall aktiv, erlauben Sie eingehende Verbindungen.

### Linux: tftpd-hpa und vsftpd

Unter Debian und Ubuntu:

```
sudo apt install tftpd-hpa
```

Die Konfiguration liegt in `/etc/default/tftpd-hpa`. Das Standardverzeichnis ist `/srv/tftp`:

```
TFTP_DIRECTORY="/srv/tftp"
TFTP_OPTIONS="--secure"
```

Ergänzen Sie `--create` in `TFTP_OPTIONS` nur, wenn Geräte Dateien hochladen sollen, zum Beispiel Konfigurations-Backups.

Für FTP reicht `vsftpd` mit einem lokalen Benutzer:

```
sudo apt install vsftpd
sudo adduser netops
```

Legen Sie die Images ins Home-Verzeichnis des Benutzers oder in ein gemeinsames Verzeichnis wie `/tftpboot/images`.

## Auf dem Gerät: Image kopieren

### TFTP

```
copy tftp://192.0.2.10/<image>.bin flash:
```

### FTP

Zugangsdaten können in der URL stehen oder einmal konfiguriert werden:

```
configure terminal
ip ftp username netops
ip ftp password <passwort>
end
copy ftp://192.0.2.10/images/<image>.bin bootflash:
```

**Der doppelte Schrägstrich.** In einer FTP-URL behandelt IOS den Pfad relativ zum Home-Verzeichnis des FTP-Benutzers. Liegen die Images in einem absoluten Pfad außerhalb des Home-Verzeichnisses, verwenden Sie nach der Serveradresse zwei Schrägstriche:

```
copy ftp://192.0.2.10//tftpboot/images/<image>.bin bootflash:
```

`ftp://server/images/datei` bedeutet `<home>/images/datei`. `ftp://server//tftpboot/images/datei` bedeutet `/tftpboot/images/datei`. Dieses Detail erklärt viele „File not found“-Fehler.

### SCP

Eine Datei von einem SCP-Server holen:

```
copy scp://netops@192.0.2.10/images/<image>.bin flash:
```

Eine Datei vom Laptop auf das Gerät schieben setzt den SCP-Server auf dem Gerät voraus:

```
configure terminal
ip scp server enable
end
```

Dann vom Laptop:

```
scp <image>.bin admin@<geraete-ip>:flash:<image>.bin
```

Deaktivieren Sie `ip scp server enable` nach der Übertragung wieder, wenn Ihre Richtlinie das verlangt.

### Immer prüfen

```
verify /md5 flash:<image>.bin
```

Vergleichen Sie den Wert mit der MD5-Prüfsumme auf der Cisco-Download-Seite. Eine Datei, die ohne Fehler kopiert wurde, kann trotzdem unvollständig sein.

## Management-Port und VRF

Bei Catalyst 9000 Switches liegt der dedizierte Management-Port (GigabitEthernet0/0) in einem eigenen VRF namens `Mgmt-vrf`. Bei ISR-4000- und Catalyst-8000-Routern liegt der Management-Port im VRF `Mgmt-intf`. Eine Kopie ohne VRF nutzt die globale Routing-Tabelle und schlägt fehl, wenn der Server nur über das Management-Netz erreichbar ist.

Sagen Sie dem Gerät, welches Interface als Quelle dient:

```
configure terminal
ip tftp source-interface GigabitEthernet0/0
ip ftp source-interface GigabitEthernet0/0
end
```

Bei ISR-4000-Routern heißt der Management-Port `GigabitEthernet0`. Prüfen Sie den Namen mit `show ip interface brief`.

## Fehlersuche

### Timeout oder „Connection refused“

- Den Server vom Gerät aus anpingen, mit dem richtigen Quell-Interface oder VRF.
- Firewall auf dem Server prüfen. Windows und macOS blockieren eingehende Verbindungen standardmäßig.
- Bei FTP: Der Datenkanal nutzt zusätzliche Ports. Sitzt eine Firewall zwischen Gerät und Server, sind Probleme mit dem Passive Mode häufig.

### „File not found“

- Pfad relativ zum Root-Verzeichnis des Servers (TFTP) oder zum Home-Verzeichnis des Benutzers (FTP) prüfen. Denken Sie an den doppelten Schrägstrich.
- Groß- und Kleinschreibung prüfen. Auf Linux- und macOS-Servern sind Dateinamen case-sensitive.
- Prüfen, ob der Server-Benutzer die Datei lesen darf.

### Kopie bricht bei 32 MB ab (TFTP)

Klassisches TFTP verwendet 512-Byte-Blöcke und einen 16-Bit-Blockzähler. Das begrenzt eine Übertragung auf etwa 32 MB, außer beide Seiten unterstützen größere Blöcke oder das Überlaufen der Blocknummer. Alte oder minimale TFTP-Server haben dieses Limit noch. IOS-XE-Images sind viel größer.

- Verwenden Sie FTP oder SCP für große Images.
- Muss es TFTP sein, nehmen Sie einen aktuellen Server und erhöhen die Blockgröße auf dem Gerät:

```
configure terminal
ip tftp blocksize 8192
end
```

### Sehr langsame Übertragung

TFTP wartet nach jedem Block auf eine Bestätigung. Über eine WAN-Strecke mit hoher Latenz wird es dadurch extrem langsam. Verwenden Sie über große Entfernungen FTP oder SCP, oder stellen Sie einen Server in die Nähe des Geräts.

## Verwandte Artikel

- [Cisco IOS und IOS-XE Upgrade-Leitfaden](/de/posts/cisco-ios-xe-upgrade-guide/)
- [Cisco ROMMON Recovery: Start aus Flash, über TFTP oder USB](/de/posts/cisco-rommon-recovery/)
- [Cisco Nexus NX-OS Software-Upgrade-Leitfaden](/de/posts/cisco-nexus-nxos-upgrade-guide/)
- [SecureCRT und SuperPuTTY für Netzwerk-Engineers](/de/technology/securecrt-superputty/)
