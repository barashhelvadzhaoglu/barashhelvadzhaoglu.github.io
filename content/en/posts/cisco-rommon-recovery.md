---
title: "Cisco ROMMON Recovery: Boot a Switch or Router from Flash, TFTP or USB"
description: "Cisco switch or router stuck at the switch: or rommon prompt? Recovery scenarios for Catalyst 9300, 9200, 3850, 2960, 3560 and ISR 4000 — boot from flash, set ROMMON network variables, boot over TFTP or USB, and fix an outdated ROMMON."
date: 2026-10-22
draft: false
aliases:
  - "/en/posts/catalyst-3560-boot-loader-recovery/"

tags: ["Cisco", "ROMMON", "Boot Loader", "Recovery", "IOS-XE", "Catalyst 9300", "Catalyst 9200", "Catalyst 3850", "Catalyst 2960", "Catalyst 3560", "ISR 4000"]
categories: ["Network Operations"]
keywords: ["Cisco ROMMON recovery", "Cisco switch stuck in rommon", "switch: prompt recovery", "rommon boot tftp", "IP_ADDRESS DEFAULT_GATEWAY rommon", "boot usbflash0", "emergency-install", "Cisco rommon too old", "Catalyst 9300 bootloader recovery", "ISR 4331 rommon"]
showToc: true
TocOpen: true
---

After a reload, the device does not come back. On the console you see only `switch:` (Catalyst switches) or `rommon 1 >` (routers). This is ROMMON, also called the boot loader: the small program that starts IOS. It stopped because it could not find or start a valid image.

This is not a hardware failure in most cases, and you do not need to replace the device. Which way out you take depends on one question: **is a good image still in flash?**

| Scenario | Situation | Way out |
| --- | --- | --- |
| 1 | The correct image is in flash | Boot it, fix the boot variable |
| 2 | The image is missing or corrupted | Boot over TFTP or from USB, then copy the image to flash |
| 3 | The image is there, but ROMMON is too old for it | Boot an older image, upgrade ROMMON, then upgrade |

## Before You Start: Console Access

ROMMON is only reachable over the console. In a branch office that means a laptop and a console cable. In a data center, where you are rarely next to the rack, a console server is what makes recovery possible at all: [Next-Gen Console Server Architecture](/en/posts/next-gen-console-server-architecture/).

Look at the environment first:

```
switch: dir flash:
switch: set
```

On routers:

```
rommon 1 > dir bootflash:
rommon 2 > set
```

`set` shows the boot loader variables. The important ones are `BOOT` (which image to start) and, on some switches, `MANUAL_BOOT` (if `yes`, the switch always stops at the prompt). On routers, also check the configuration register with `confreg`. A value of `0x2100` keeps the router in ROMMON. The normal value is `0x2102`.

`help` or `?` lists the commands your ROMMON version supports.

## Scenario 1: The Correct Image Is in Flash

The image is there, but the boot variable is wrong: a typo after an upgrade, a deleted file name, or `MANUAL_BOOT=yes`.

### Boot It Manually

Catalyst 9000 and other IOS-XE switches in install mode:

```
switch: boot flash:packages.conf
```

In bundle mode, or on classic Catalyst switches:

```
switch: boot flash:<image>.bin
```

On classic Catalyst switches, images installed with `archive download-sw` are in a subdirectory. Check the full path with `dir flash:<directory>`.

Routers:

```
rommon 1 > boot bootflash:<image>.bin
```

If the router stayed in ROMMON because of the configuration register:

```
rommon 1 > confreg 0x2102
rommon 2 > reset
```

### Fix the Boot Variable in IOS

Once IOS is running, make the fix permanent, otherwise the problem returns at the next reload:

```
configure terminal
no boot system
boot system flash:packages.conf
end
write memory
show boot
```

Use the `.bin` file name instead of `packages.conf` in bundle mode, and `bootflash:` on routers.

## Scenario 2: The Image Is Missing or Corrupted

The image was deleted by mistake, the copy was interrupted, or flash is empty. You need to bring an image to the device from outside. There are two practical ways.

| | TFTP from ROMMON | USB |
| --- | --- | --- |
| Needs someone on site | No | Yes |
| Works over a console server | Yes | Only if someone inserts the stick |
| Speed | Depends on the network | Fast |
| Typical use | Data center, remote sites | Branch office, lab |

### Option A: Boot over TFTP from ROMMON

If you are connected remotely through a console server and the network around the device works, TFTP is the most practical option. The hard part is the network configuration in ROMMON, because ROMMON has no IOS, no routing and no DHCP. You set everything by hand.

**Requirements:**

- The **management port** is connected and reachable. On Catalyst 9000 switches that is the dedicated management port (Gi0/0). ROMMON does not use the front-panel ports.
- A TFTP server with the image is reachable from the management network. Setup and firewall rules: [TFTP, FTP and SCP Servers for Cisco Upgrades](/en/posts/tftp-ftp-server-cisco-upgrades/).

**Catalyst 9000 switches:**

```
switch: set IP_ADDRESS 192.0.2.50
switch: set IP_SUBNET_MASK 255.255.255.0
switch: set DEFAULT_GATEWAY 192.0.2.1
switch: ping 192.0.2.10
switch: boot tftp://192.0.2.10/cat9k_iosxe.<version>.SPA.bin
```

Test with `ping` first. If the ping fails, there is no point starting the boot. Check the cable on the management port, the gateway and the firewall on the TFTP server.

Two limits apply, according to Cisco:

- The switch boots **in bundle mode** when you boot over TFTP.
- The image is **not copied to flash**. It only runs from memory. After the next reload, you are back at the prompt.

**ISR 4000 and other IOS-XE routers:**

```
rommon 1 > IP_ADDRESS=192.0.2.50
rommon 2 > IP_SUBNET_MASK=255.255.255.0
rommon 3 > DEFAULT_GATEWAY=192.0.2.1
rommon 4 > TFTP_SERVER=192.0.2.10
rommon 5 > TFTP_FILE=isr4300-universalk9.<version>.SPA.bin
rommon 6 > set
rommon 7 > boot tftp://192.0.2.10/isr4300-universalk9.<version>.SPA.bin
```

Variable names and the exact boot syntax differ between ROMMON versions. Check with `set` and `help`. Older routers (ISR G2) use the `tftpdnld` command instead, which writes the image directly to flash.

**After the device has booted over TFTP:** copy the image to flash, verify it and set it up properly, as described in the [upgrade guide](/en/posts/cisco-ios-xe-upgrade-guide/):

```
copy tftp://192.0.2.10/<image>.bin flash:
verify /md5 flash:<image>.bin
install add file flash:<image>.bin activate commit
```

On devices in bundle mode or classic IOS, set `boot system` to the copied file instead of `install add`.

### Option B: Boot from USB

When someone can insert a USB stick, this is the easiest and fastest way. Format the stick with FAT32 and copy the image to it.

```
switch: dir usbflash0:
switch: boot usbflash0:<image>.bin
```

On ISR routers the USB device is usually called `usb0:` (on some models `usb1:`):

```
rommon 1 > dir usb0:
rommon 2 > boot usb0:<image>.bin
```

When the device is up, copy the image from USB to flash and fix the boot variable:

```
copy usbflash0:<image>.bin flash:
verify /md5 flash:<image>.bin
```

Then install it or set `boot system` as in Scenario 1.

### Option C: emergency-install (Catalyst 9000)

Catalyst 9000 switches (except the 9200 series) have an `emergency-install` command in ROMMON. It installs an image from TFTP straight into flash:

```
switch: emergency-install tftp://192.0.2.10/cat9k_iosxe.<version>.SPA.bin
switch: boot flash:packages.conf
```

Warning: this **erases the entire flash file system**, including the configuration. Use it only when Options A and B are not possible, and only when you have a configuration backup.

### Option D: Xmodem over the Console (Classic Catalyst)

Classic Catalyst switches like the 2960 and 3560 have no network stack in the boot loader and often no USB port. The last resort is a transfer over the console with Xmodem:

```
switch: flash_init
switch: set BAUD 115200
switch: copy xmodem: flash:<image>.bin
```

After `set BAUD`, change your terminal program to 115200 baud. Even at this speed the transfer takes a long time. Reset the speed afterwards with `set BAUD 9600`, otherwise the next person connecting at 9600 baud sees only garbage.

## Scenario 3: ROMMON Is Too Old for the New Image

The image is in flash and correct, but the device still does not start it. On ISR 4000 routers this happens when the target release needs a newer ROMMON than the device has, for example 17.x releases that need ROMMON 16.12(2r).

As far as I know, ROMMON cannot be upgraded from the ROMMON prompt on these platforms. The upgrade runs from IOS-XE. The way out:

1. Boot an **older image** that works with the current ROMMON. From flash if you kept it, otherwise over TFTP or USB as in Scenario 2.
2. In IOS-XE, upgrade ROMMON: `upgrade rom-monitor filename bootflash:<rommon>.pkg R0`, then reload.
3. Check with `show rom-monitor r0`.
4. Now install the new image.

This is why the [upgrade guide](/en/posts/cisco-ios-xe-upgrade-guide/) puts the ROMMON check before the upgrade.

A related case: the boot variable points to an image for another platform family, for example an ISR 4300 image on an ISR 4400. The device stays in ROMMON. Boot the correct image manually and fix the boot variable.

## Prevention

- Keep the current and the previous image on a server you can reach from the management network.
- Check `show boot` (or `show bootvar`) and the ROMMON requirement before every planned reload.
- Connect and test the management port before you need it.
- Have console access ready for every upgrade: [Next-Gen Console Server Architecture](/en/posts/next-gen-console-server-architecture/).

## Related Articles

- [Cisco IOS and IOS-XE Upgrade Guide](/en/posts/cisco-ios-xe-upgrade-guide/)
- [TFTP, FTP and SCP Servers for Cisco Upgrades](/en/posts/tftp-ftp-server-cisco-upgrades/)
- [Cisco Switch and Router Password Recovery](/en/posts/cisco-switch-password-recovery/)
- [Cisco Nexus NX-OS Upgrade Guide (with ROMMON recovery)](/en/posts/cisco-nexus-nxos-upgrade-guide/)

Sources: [Cisco: Troubleshoot Bootloader and Password Recovery on Catalyst 9000](https://cisco.com/c/en/us/support/docs/switches/catalyst-9300-series-switches/216944-troubleshoot-bootloader-rommon-and-pas.html) · [Cisco: ISR 4000 Stuck in ROMMON](https://www.cisco.com/c/en/us/support/docs/routers/4000-series-integrated-services-routers/200678-Troubleshoot-Cisco-4000-Series-ISR-Stuck.html)
