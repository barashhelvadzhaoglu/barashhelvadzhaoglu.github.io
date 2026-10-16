---
title: "Cisco Catalyst 3560 IOS Upgrade: Two Methods and Verification"
description: "Upgrading IOS on a Cisco Catalyst 3560 — archive download-sw versus manual copy and boot system, flash space, MD5 verification and rollback."
date: 2026-10-16
draft: false

tags: ["Cisco", "Catalyst", "Switch", "IOS", "Upgrade"]
categories: ["Network Operations"]
keywords: ["Catalyst 3560 IOS upgrade", "archive download-sw", "Cisco switch software upgrade", "boot system flash", "verify md5 Cisco", "Cisco 3560 tftp upgrade", "Cisco switch flash space", "Cisco IOS rollback switch"]
showToc: true
TocOpen: true
---

Upgrading IOS on a Catalyst 3560 is not complicated, but the details matter: which file format you download, how much space is left in flash, and whether the boot variable points to the right image. A mistake in any of these leaves you with a switch that boots into the boot loader instead of IOS.

There are two ways to do it:

- **Method A: `archive download-sw` with a `.tar` file.** The switch extracts the image, the web device manager files and sets the boot variable itself.
- **Method B: manual upgrade with a `.bin` file.** You copy the image, verify it, set `boot system` and reload.

> **Lab note:** I am upgrading my own Catalyst 3560 8-port PoE switch with both methods. Console outputs and timings from that lab will be added to this guide.

## 1. Before You Start

### Back Up the Configuration

```
Switch# copy running-config startup-config
Switch# copy startup-config tftp:
```

Keep the backup off the switch: on your laptop, a TFTP or SCP server, or your configuration management tool.

### Identify the Model, Version and Feature Set

```
Switch# show version
Switch# show inventory
```

Write down three things:

- **Exact model**, for example `WS-C3560-8PC-S`. The image must match the platform.
- **Current IOS version**.
- **Feature set**, for example IP Base (`ipbasek9`) or IP Services (`ipservicesk9`). Choose the same feature set for the new image unless you deliberately change it.

### Check the Boot Settings and Flash Space

```
Switch# show boot
Switch# dir flash:
```

`show boot` shows which image the switch loads at the next reload. `dir flash:` shows the files and, at the bottom, the free space. Compact switches like the 8-port 3560 have little flash. Often there is not enough room for two images at the same time.

### Download the Image

Download the image from Cisco Software Download. A service contract is required. You will find two file types:

| File | Contents | Used with |
| --- | --- | --- |
| `.tar` | IOS image plus web device manager files | `archive download-sw` (Method A) |
| `.bin` | IOS image only | Manual copy and `boot system` (Method B) |

Note the **MD5 checksum** shown on the download page. You will compare it on the switch.

The classic Catalyst 3560 is end of life, so the latest release on the download page is the final one for this platform.

## 2. Method A: archive download-sw

This is the method Cisco recommends for this switch family. One command transfers the `.tar` file, extracts it into a new directory in flash, updates the boot variable and optionally reloads.

```
Switch# archive download-sw /overwrite /reload tftp://192.0.2.10/c3560-ipservicesk9-tar.<version>.tar
```

The most useful options:

| Option | Effect |
| --- | --- |
| `/overwrite` | Replaces the current image if there is not enough space for both |
| `/leave-old-sw` | Keeps the old image (only if flash has room for both) |
| `/reload` | Reloads the switch after a successful download |
| `/imageonly` | Installs only the IOS image, without the web device manager files |

If you have room for both images, use `/leave-old-sw` instead of `/overwrite`. Rollback is then just a boot variable change.

Without `/reload`, check the result before reloading:

```
Switch# show boot
Switch# dir flash:
Switch# reload
```

## 3. Method B: Manual Upgrade with a .bin File

The manual method gives you full control over each step. It is useful when you only have a `.bin` file, or when you want to verify the image before touching the boot variable.

### Copy the Image

```
Switch# copy tftp://192.0.2.10/c3560-ipservicesk9-mz.<version>.bin flash:
```

If there is not enough space, you must delete the old image first. That removes your rollback option on the switch, so make sure you have the old image on your TFTP server and a console connection ready.

TFTP works for small files but is slow and unreliable over long distances. If your IOS version supports it, SCP or FTP is faster.

### Verify the Checksum

```
Switch# verify /md5 flash:c3560-ipservicesk9-mz.<version>.bin
```

Compare the result with the MD5 value from the Cisco download page. If they differ, delete the file and copy it again. Never boot an image that failed verification.

### Set the Boot Variable and Reload

```
Switch# configure terminal
Switch(config)# boot system flash:c3560-ipservicesk9-mz.<version>.bin
Switch(config)# end
Switch# copy running-config startup-config
Switch# show boot
Switch# reload
```

Check `show boot` before the reload. The `BOOT path-list` must point to the new image, with the correct file name and path.

## 4. After the Upgrade

```
Switch# show version
Switch# show interfaces status
Switch# show power inline
Switch# show logging
```

- `show version`: the new IOS version is running.
- `show interfaces status`: all expected ports are up.
- `show power inline`: PoE devices are powered again.
- `show logging`: no errors during boot.

When you are sure the new version works, remove the old image to free up space, unless you want to keep it for rollback.

## 5. Rollback

- **Old image still in flash:** point the boot variable back to it with `boot system flash:<old-image>`, save and reload.
- **Old image deleted:** copy it back from your TFTP server, verify the MD5 and set the boot variable.
- **Switch does not boot IOS at all:** it stops at the `switch:` prompt. This is covered in [When a Catalyst 3560 Won't Boot: Recovery from the Boot Loader](/en/posts/catalyst-3560-boot-loader-recovery/).

## Common Mistakes

- **Wrong platform or feature set.** An image for another model does not boot.
- **Deleting the old image before the new one is verified.** If the copy is corrupted, you have nothing to boot.
- **A typo in `boot system`.** The switch cannot find the image and stops at the boot loader.
- **No console connection during the reload.** If something goes wrong, you can only see it from the console.

## Related Articles

- [Cisco Catalyst 3560 Password Recovery: Two Methods](/en/posts/catalyst-3560-password-recovery/)
- [When a Catalyst 3560 Won't Boot: Recovery from the Boot Loader](/en/posts/catalyst-3560-boot-loader-recovery/)
- [Cisco Nexus NX-OS Software Upgrade Guide](/en/posts/cisco-nexus-nxos-upgrade-guide/)
- [SecureCRT and SuperPuTTY for Network Engineers](/en/technology/securecrt-superputty/)
