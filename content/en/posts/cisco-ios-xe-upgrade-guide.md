---
title: "Cisco IOS and IOS-XE Upgrade Guide: Catalyst Switches and ISR Routers"
description: "Step-by-step Cisco IOS and IOS-XE software upgrade for Catalyst switches (2960, 3560, 3850, 9200, 9300, 9500) and routers (ISR 4000, ISR 1100, Catalyst 8000) — flash checks, ROMMON, install mode, bundle mode, MD5 and rollback."
date: 2026-10-22
draft: false
aliases:
  - "/en/posts/catalyst-3560-ios-upgrade/"

tags: ["Cisco", "IOS", "IOS-XE", "Upgrade", "Catalyst 9300", "Catalyst 9200", "Catalyst 9500", "Catalyst 3850", "Catalyst 2960", "Catalyst 3560", "ISR 4000", "ISR 1100", "Catalyst 8000"]
categories: ["Network Operations"]
keywords: ["Cisco IOS upgrade", "Cisco IOS XE upgrade", "install add file activate commit", "Catalyst 9300 upgrade", "ISR 4331 upgrade", "Cisco ROMMON upgrade", "upgrade rom-monitor filename", "bundle mode to install mode", "Cisco verify md5", "archive download-sw", "packages.conf", "install remove inactive"]
showToc: true
TocOpen: true
---

Most Cisco upgrades fail before the first command is typed: the wrong image for the platform, too little space in flash, a ROMMON that is too old for the target release, or a boot variable that points nowhere. This guide puts the checks first and the commands second.

It covers both families you meet in practice:

| Family | Typical models | Software | File system | Upgrade method |
| --- | --- | --- | --- | --- |
| Classic Catalyst switches | 2960, 2960-X, 3560, 3750 | IOS | `flash:` | `archive download-sw` or `.bin` + `boot system` |
| IOS-XE Catalyst switches | 3650, 3850, 9200, 9300, 9400, 9500 | IOS-XE | `flash:` (on some models `bootflash:`) | Install mode (`packages.conf`) |
| IOS-XE routers | ISR 4000, ISR 1100, Catalyst 8200/8300, Catalyst 8000V | IOS-XE | `bootflash:` | Install mode or bundle mode |
| Classic IOS routers | ISR G2, C900 | IOS | `flash:` | `.bin` + `boot system` |

The commands are the ones I use in the field on Catalyst switches and ISR routers. IP addresses and paths in the examples are placeholders.

## 1. Check the Platform Before Anything Else

### File System: flash: or bootflash:?

Do not assume. Ask the device:

```
show file systems
dir
```

Classic Catalyst switches and Catalyst 9200/9300 use `flash:`. ISR and Catalyst 8000 routers use `bootflash:`. On many IOS-XE platforms one name is an alias for the other. Use whatever the device shows. Every command in this guide works with either name.

### Model, Version and Boot Mode

```
show version
show inventory
show boot            ! switches
show bootvar         ! routers
show install summary ! IOS-XE only
```

Write down:

- **Exact model and platform family.** An image for an ISR 4300 does not boot on an ISR 4400. The platform family is in the file name, for example `isr4300-universalk9`, `c1100-universalk9`, `cat9k_iosxe`.
- **Current version.**
- **Boot mode on IOS-XE.** If the boot variable points to `packages.conf`, the device runs in **install mode**. If it points to a `.bin` file, it runs in **bundle mode**.

### Free Space

`dir` shows the free bytes at the bottom. An IOS-XE image is large, and install mode needs extra space to extract the packages. If space is tight, clean up first:

```
install remove inactive   ! IOS-XE install mode: removes unused packages
delete flash:<old-image>.bin
```

## 2. Read the Release Notes: Upgrade Path and ROMMON

Two things in the release notes decide whether the upgrade works:

- **Upgrade path.** Some jumps are not supported directly. Cisco documents, for example, that Catalyst 9500 switches in bundle mode should go from 16.x to 17.x through an intermediate release, while install mode supports the direct jump.
- **Minimum ROMMON version.** Every IOS-XE release needs a minimum ROMMON (boot loader) version. If the device has an older ROMMON, the new image may not boot and the device stops at the `rommon` prompt.

Check the current ROMMON version:

```
show rom-monitor r0          ! ISR 4000 and similar routers
show version | include ROM   ! most platforms
```

### Does ROMMON Need a Separate Upgrade?

- **Catalyst 9000:** Usually not by hand. When a new release contains a newer ROMMON, the switch upgrades its primary ROMMON automatically at the first boot. The golden (backup) ROMMON is upgraded manually with the `upgrade rom-monitor capsule golden` command. The exact arguments differ by model, so check the upgrade guide for your platform.
- **ISR 4000 and similar routers:** Check it every time. A well-known case is ISR 4000 routers that need ROMMON 16.12(2r) before they boot 17.x releases.

### Upgrading ROMMON on an ISR 4000

ROMMON is upgraded from the running IOS-XE, not from the ROMMON prompt. Copy the ROMMON package, verify it, then:

```
copy ftp://192.0.2.10/images/isr4200_4300_rommon_1612_2r_SPA.pkg bootflash:
verify /md5 bootflash:isr4200_4300_rommon_1612_2r_SPA.pkg
upgrade rom-monitor filename bootflash:isr4200_4300_rommon_1612_2r_SPA.pkg R0
reload
show rom-monitor r0
```

Do the ROMMON upgrade **before** the software upgrade. If you get it wrong and the device no longer boots, see [Cisco ROMMON Recovery](/en/posts/cisco-rommon-recovery/).

### Secure Boot and Signed Images

IOS-XE images are signed. The `.SPA` in the file name stands for a signed production image. The device verifies the signature at boot. An image for the wrong platform or a corrupted file fails this check and does not boot. Only use images from Cisco Software Download and always verify the checksum.

## 3. Copy the Image and Verify It

FTP is faster and more reliable than TFTP for large IOS-XE images:

```
copy ftp://192.0.2.10/images/isr4300-universalk9.17.12.08.SPA.bin bootflash:
copy ftp://192.0.2.10/images/c1100-universalk9.17.12.08.SPA.bin bootflash:
copy tftp://192.0.2.10/cat9k_iosxe.<version>.SPA.bin flash:
```

Setting up the server, credentials, the double slash in FTP paths and the management VRF are covered in [TFTP, FTP and SCP Servers for Cisco Upgrades](/en/posts/tftp-ftp-server-cisco-upgrades/).

Verify the MD5 checksum against the value on the Cisco download page:

```
verify /md5 bootflash:c1100-universalk9.17.12.08.SPA.bin
```

If the values differ, delete the file and copy it again. Never install an image that failed verification.

## 4. Upgrade in Install Mode (IOS-XE)

Install mode is the recommended mode for Catalyst 9000 switches and current ISR and Catalyst 8000 routers. One command adds, activates and commits the new software:

```
install add file bootflash:isr4300-universalk9.17.12.08.SPA.bin activate commit
```

The device asks whether it may reload. Answer `y`. After the reload:

```
show version
show install summary
install remove inactive
```

`show install summary` should show the new version as `Committed`. `install remove inactive` removes the old packages and frees space.

On Catalyst 9000 switches the command is the same, with the switch file system:

```
install add file flash:cat9k_iosxe.<version>.SPA.bin activate commit
```

### Several Hops in a Row

If the release notes require an intermediate release, repeat the sequence per hop: copy, verify, `install add ... activate commit`, check, `install remove inactive`. For example 17.9 first, then 17.12. Clean up between the hops so there is room for the next image.

### From Bundle Mode to Install Mode

A device in bundle mode boots a `.bin` file directly. To switch to install mode:

1. Run `install add file <image>.bin activate commit` as above. This extracts the packages and creates `packages.conf`.
2. Make sure the boot variable points to `packages.conf`:

```
configure terminal
no boot system
boot system flash:packages.conf
end
write memory
show boot
```

On routers, use `bootflash:packages.conf`.

## 5. Bundle Mode and Classic IOS

### IOS-XE in Bundle Mode, ISR G2, C900

```
configure terminal
no boot system
boot system bootflash:<image>.bin
end
write memory
show bootvar
reload
```

On classic IOS routers like the C900 series, the file system is `flash:` and the image name has the old format, for example `c900-universalk9-mz.SPA.<version>.bin`.

### Classic Catalyst Switches (2960, 3560, 3750)

These switches offer `archive download-sw`. It transfers a `.tar` file, extracts it, sets the boot variable and can reload:

```
archive download-sw /overwrite /reload tftp://192.0.2.10/c3560-ipservicesk9-tar.<version>.tar
```

- `/overwrite` replaces the current image when flash has room for only one.
- `/leave-old-sw` keeps the old image when there is room for both. Rollback is then just a boot variable change.

Alternatively, copy the `.bin` file, verify it and set `boot system flash:<image>.bin` as above.

## 6. After the Upgrade

```
show version
show install summary          ! IOS-XE install mode
show interfaces status        ! switches
show ip interface brief
show power inline             ! PoE switches
show logging
```

On stacks and redundant systems, check every member: `show switch` on Catalyst stacks, `show redundancy` on dual-supervisor systems.

## 7. Rollback

- **Install mode:** `show install rollback` lists the rollback points.
- **Bundle mode and classic IOS:** point `boot system` back to the old image, if it is still in flash, and reload.
- **Device stops at ROMMON or the `switch:` prompt:** see [Cisco ROMMON Recovery](/en/posts/cisco-rommon-recovery/).

## Common Mistakes

- **Image for the wrong platform family.** It fails signature or platform checks and does not boot.
- **ROMMON not checked.** The new image needs a newer ROMMON, and the device stops at the `rommon` prompt.
- **No space for install mode.** The extraction fails halfway. Run `install remove inactive` first.
- **Boot variable still points to the old `.bin` after moving to install mode.** The device boots the old version in bundle mode.
- **No console access during the reload.** A console server makes this possible remotely: [Next-Gen Console Server Architecture](/en/posts/next-gen-console-server-architecture/).

## Related Articles

- [Cisco ROMMON Recovery: Boot from Flash, TFTP or USB](/en/posts/cisco-rommon-recovery/)
- [TFTP, FTP and SCP Servers for Cisco Upgrades](/en/posts/tftp-ftp-server-cisco-upgrades/)
- [Cisco Switch and Router Password Recovery](/en/posts/cisco-switch-password-recovery/)
- [Cisco Nexus NX-OS Software Upgrade Guide](/en/posts/cisco-nexus-nxos-upgrade-guide/)

Sources: [Cisco: Upgrading Catalyst 9500 Switches](https://www.cisco.com/c/en/us/support/docs/switches/catalyst-9500-series-switches/222279-upgrading-catalyst-9500-switches.html) · [Cisco: Upgrading Catalyst 9300 Switches](https://www.cisco.com/c/de_de/support/docs/switches/catalyst-9300-series-switches/222280-upgrading-catalyst-9300-switches.html)
