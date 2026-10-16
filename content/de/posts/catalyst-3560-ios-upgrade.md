---
title: "Cisco Catalyst 3560 IOS-Upgrade: Zwei Methoden und Verifizierung"
description: "IOS-Upgrade auf einem Cisco Catalyst 3560 — archive download-sw oder manuelles Kopieren mit boot system, Flash-Speicher, MD5-Prüfung und Rollback."
date: 2026-10-16
draft: false

tags: ["Cisco", "Catalyst", "Switch", "IOS", "Upgrade"]
categories: ["Netzwerkbetrieb"]
keywords: ["Catalyst 3560 IOS Upgrade", "archive download-sw", "Cisco Switch Software Update", "boot system flash", "verify md5 Cisco", "Cisco 3560 TFTP Upgrade", "Cisco Switch Flash Speicher", "Cisco IOS Rollback"]
showToc: true
TocOpen: true
---

Ein IOS-Upgrade auf einem Catalyst 3560 ist nicht kompliziert, aber die Details zählen: welches Dateiformat Sie herunterladen, wie viel Platz im Flash frei ist und ob die Boot-Variable auf das richtige Image zeigt. Ein Fehler an einer dieser Stellen, und der Switch startet in den Boot Loader statt in IOS.

Es gibt zwei Wege:

- **Methode A: `archive download-sw` mit einer `.tar`-Datei.** Der Switch entpackt das Image und die Web-Device-Manager-Dateien und setzt die Boot-Variable selbst.
- **Methode B: Manuelles Upgrade mit einer `.bin`-Datei.** Sie kopieren das Image, prüfen es, setzen `boot system` und starten neu.

> **Lab-Hinweis:** Ich aktualisiere meinen eigenen Catalyst 3560 mit 8 PoE-Ports mit beiden Methoden. Konsolenausgaben und Zeiten aus diesem Lab werden ergänzt.

## 1. Vorbereitung

### Konfiguration sichern

```
Switch# copy running-config startup-config
Switch# copy startup-config tftp:
```

Bewahren Sie das Backup außerhalb des Switches auf: auf Ihrem Laptop, einem TFTP- oder SCP-Server oder in Ihrem Konfigurationsmanagement.

### Modell, Version und Feature Set ermitteln

```
Switch# show version
Switch# show inventory
```

Notieren Sie drei Dinge:

- **Genaues Modell**, zum Beispiel `WS-C3560-8PC-S`. Das Image muss zur Plattform passen.
- **Aktuelle IOS-Version**.
- **Feature Set**, zum Beispiel IP Base (`ipbasek9`) oder IP Services (`ipservicesk9`). Wählen Sie für das neue Image dasselbe Feature Set, außer Sie wollen es bewusst ändern.

### Boot-Einstellungen und Flash-Speicher prüfen

```
Switch# show boot
Switch# dir flash:
```

`show boot` zeigt, welches Image der Switch beim nächsten Neustart lädt. `dir flash:` zeigt die Dateien und ganz unten den freien Speicher. Kompakte Switches wie der 3560 mit 8 Ports haben wenig Flash. Oft reicht der Platz nicht für zwei Images gleichzeitig.

### Image herunterladen

Laden Sie das Image über Cisco Software Download herunter. Dafür ist ein Servicevertrag nötig. Sie finden zwei Dateitypen:

| Datei | Inhalt | Verwendung |
| --- | --- | --- |
| `.tar` | IOS-Image plus Web-Device-Manager-Dateien | `archive download-sw` (Methode A) |
| `.bin` | Nur das IOS-Image | Manuelles Kopieren und `boot system` (Methode B) |

Notieren Sie die **MD5-Prüfsumme** von der Download-Seite. Sie vergleichen sie später auf dem Switch.

Der klassische Catalyst 3560 ist End of Life. Das neueste Release auf der Download-Seite ist also das letzte für diese Plattform.

## 2. Methode A: archive download-sw

Das ist die von Cisco empfohlene Methode für diese Switch-Familie. Ein Befehl überträgt die `.tar`-Datei, entpackt sie in ein neues Verzeichnis im Flash, aktualisiert die Boot-Variable und startet bei Bedarf neu.

```
Switch# archive download-sw /overwrite /reload tftp://192.0.2.10/c3560-ipservicesk9-tar.<version>.tar
```

Die wichtigsten Optionen:

| Option | Wirkung |
| --- | --- |
| `/overwrite` | Ersetzt das aktuelle Image, wenn nicht genug Platz für beide ist |
| `/leave-old-sw` | Behält das alte Image (nur wenn der Flash für beide reicht) |
| `/reload` | Startet den Switch nach erfolgreichem Download neu |
| `/imageonly` | Installiert nur das IOS-Image ohne Web-Device-Manager-Dateien |

Wenn Platz für beide Images ist, verwenden Sie `/leave-old-sw` statt `/overwrite`. Ein Rollback ist dann nur eine Änderung der Boot-Variable.

Ohne `/reload` prüfen Sie das Ergebnis vor dem Neustart:

```
Switch# show boot
Switch# dir flash:
Switch# reload
```

## 3. Methode B: Manuelles Upgrade mit einer .bin-Datei

Die manuelle Methode gibt Ihnen volle Kontrolle über jeden Schritt. Sie ist nützlich, wenn Sie nur eine `.bin`-Datei haben oder das Image prüfen wollen, bevor Sie die Boot-Variable ändern.

### Image kopieren

```
Switch# copy tftp://192.0.2.10/c3560-ipservicesk9-mz.<version>.bin flash:
```

Reicht der Platz nicht, müssen Sie zuerst das alte Image löschen. Damit verlieren Sie die Rollback-Option auf dem Switch. Stellen Sie sicher, dass das alte Image auf Ihrem TFTP-Server liegt und eine Konsolenverbindung bereitsteht.

TFTP funktioniert für kleine Dateien, ist aber langsam und über große Entfernungen unzuverlässig. Wenn Ihre IOS-Version es unterstützt, sind SCP oder FTP schneller.

### Prüfsumme verifizieren

```
Switch# verify /md5 flash:c3560-ipservicesk9-mz.<version>.bin
```

Vergleichen Sie das Ergebnis mit dem MD5-Wert von der Cisco-Download-Seite. Stimmen sie nicht überein, löschen Sie die Datei und kopieren sie erneut. Starten Sie nie ein Image, dessen Prüfung fehlgeschlagen ist.

### Boot-Variable setzen und neu starten

```
Switch# configure terminal
Switch(config)# boot system flash:c3560-ipservicesk9-mz.<version>.bin
Switch(config)# end
Switch# copy running-config startup-config
Switch# show boot
Switch# reload
```

Prüfen Sie `show boot` vor dem Neustart. Die `BOOT path-list` muss auf das neue Image zeigen, mit korrektem Dateinamen und Pfad.

## 4. Nach dem Upgrade

```
Switch# show version
Switch# show interfaces status
Switch# show power inline
Switch# show logging
```

- `show version`: Die neue IOS-Version läuft.
- `show interfaces status`: Alle erwarteten Ports sind aktiv.
- `show power inline`: PoE-Geräte werden wieder versorgt.
- `show logging`: Keine Fehler beim Start.

Wenn die neue Version sicher funktioniert, löschen Sie das alte Image, um Platz zu schaffen, außer Sie wollen es für einen Rollback behalten.

## 5. Rollback

- **Altes Image noch im Flash:** Boot-Variable mit `boot system flash:<altes-image>` zurückstellen, speichern und neu starten.
- **Altes Image gelöscht:** Vom TFTP-Server zurückkopieren, MD5 prüfen und Boot-Variable setzen.
- **Switch startet IOS gar nicht:** Er bleibt am Prompt `switch:` stehen. Das behandelt der Artikel [Wenn ein Catalyst 3560 nicht startet: Wiederherstellung über den Boot Loader](/de/posts/catalyst-3560-boot-loader-recovery/).

## Häufige Fehler

- **Falsche Plattform oder falsches Feature Set.** Ein Image für ein anderes Modell startet nicht.
- **Altes Image löschen, bevor das neue geprüft ist.** Ist die Kopie beschädigt, gibt es nichts mehr zu starten.
- **Tippfehler in `boot system`.** Der Switch findet das Image nicht und bleibt im Boot Loader stehen.
- **Keine Konsolenverbindung während des Neustarts.** Wenn etwas schiefgeht, sehen Sie es nur über die Konsole.

## Verwandte Artikel

- [Cisco Catalyst 3560 Passwort-Wiederherstellung: Zwei Methoden](/de/posts/catalyst-3560-password-recovery/)
- [Wenn ein Catalyst 3560 nicht startet: Wiederherstellung über den Boot Loader](/de/posts/catalyst-3560-boot-loader-recovery/)
- [Cisco Nexus NX-OS Software-Upgrade-Leitfaden](/de/posts/cisco-nexus-nxos-upgrade-guide/)
- [SecureCRT und SuperPuTTY für Netzwerk-Engineers](/de/technology/securecrt-superputty/)
