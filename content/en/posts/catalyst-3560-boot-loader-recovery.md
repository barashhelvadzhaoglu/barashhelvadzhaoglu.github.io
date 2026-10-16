---
title: "When a Catalyst 3560 Won't Boot: Recovery from the Boot Loader"
description: "Recovering a Cisco Catalyst 3560 stuck at the switch: prompt — boot loader variables, booting a different image, and transferring a new IOS image over the console with Xmodem."
date: 2026-10-16
draft: false

tags: ["Cisco", "Catalyst", "Switch", "Boot Loader", "IOS", "Recovery"]
categories: ["Network Operations"]
keywords: ["Catalyst 3560 boot loader", "Cisco switch prompt recovery", "copy xmodem flash", "Cisco switch boot loop", "set BOOT variable Cisco", "MANUAL_BOOT", "Cisco 3560 no IOS image", "Cisco switch xmodem baud rate"]
showToc: true
TocOpen: true
---

Sooner or later every network engineer sees it: after a reload, the switch does not come back. On the console there is only a `switch:` prompt. The IOS image is missing, corrupted, or the boot variable points to a file that does not exist.

This is not a reason to replace the switch. The Catalyst 3560 boot loader has everything you need to get IOS running again, even when the image in flash is gone. This guide covers:

- How to read the boot loader environment and why the switch stopped there
- How to boot an image that is already in flash
- How to transfer a new image over the console with **Xmodem** when flash is empty
- How to make the fix permanent

> **Lab note:** I am testing these scenarios on my own Catalyst 3560 8-port PoE switch. Console outputs and transfer times from that lab will be added to this guide.

## Why the Switch Stops at the Boot Loader

The boot loader starts IOS from the image listed in the `BOOT` variable. If that fails, or if no `BOOT` variable is set and the boot loader cannot find a bootable image itself, the switch stops at the `switch:` prompt. Typical causes:

- The upgrade went wrong: a typo in `boot system`, or the image was deleted before the new one was in place.
- The image file is corrupted, for example after an interrupted copy.
- The `MANUAL_BOOT` variable is set to `yes`, so the switch always waits at the prompt.
- The flash file system is damaged.

Another symptom is a **boot loop**: the switch starts loading IOS, crashes and reboots again and again. To break the loop, interrupt the boot process with the Mode button. The procedure is described in the [password recovery guide](/en/posts/catalyst-3560-password-recovery/).

## Step 1: Look Around

Initialize flash and look at what is there:

```
switch: flash_init
switch: dir flash:
```

Then show the boot loader environment variables:

```
switch: set
```

The most important variables:

| Variable | Meaning |
| --- | --- |
| `BOOT` | Image(s) the switch tries to boot, separated by semicolons |
| `MANUAL_BOOT` | `yes` = always stop at the boot loader prompt |
| `BAUD` | Console speed. Default is 9600 when the variable is not set |
| `CONFIG_FILE` | Configuration file name, default `config.text` |

Use `help` to see which commands your boot loader version supports.

## Step 2: Boot an Image That Is Already in Flash

If `dir flash:` shows a valid IOS image, you can boot it directly. Images installed with `archive download-sw` are in a subdirectory, so check the full path:

```
switch: dir flash:c3560-ipservicesk9-mz.<version>
switch: boot flash:c3560-ipservicesk9-mz.<version>/c3560-ipservicesk9-mz.<version>.bin
```

If `MANUAL_BOOT` was the problem, fix it:

```
switch: set MANUAL_BOOT no
```

When IOS is running, fix the boot variable permanently:

```
Switch# configure terminal
Switch(config)# boot system flash:<path>/<image>.bin
Switch(config)# end
Switch# copy running-config startup-config
Switch# show boot
```

## Step 3: Flash Is Empty: Transfer an Image with Xmodem

If there is no usable image in flash, you need to bring one in. On the classic Catalyst 3560, the boot loader has no network stack and the switch has no USB storage port, so the console is the way in. The protocol is **Xmodem**, which every serious terminal program supports.

### Prepare the Image

Use the `.bin` file, not the `.tar` file. Xmodem transfers a single file and the boot loader cannot extract archives. Check the MD5 checksum on your PC before you start, because the transfer is long and you do not want to repeat it.

### Increase the Console Speed

At 9600 baud, transferring an IOS image of this size takes several hours. Increase the speed first:

```
switch: set BAUD 115200
```

The console output becomes unreadable immediately. Change your terminal program to 115200 baud and press Enter until the `switch:` prompt comes back.

### Start the Transfer

```
switch: copy xmodem: flash:c3560-ipservicesk9-mz.<version>.bin
```

The switch waits for the file. In your terminal program, start an Xmodem send:

- **SecureCRT:** Transfer > Send Xmodem
- **Tera Term:** File > Transfer > XMODEM > Send
- **minicom / screen:** use `sx` from the `lrzsz` package

At 115200 baud, expect a transfer time in the range of half an hour to an hour, depending on the image size and the terminal program. Do not touch the console session during the transfer.

### Boot the New Image

```
switch: dir flash:
switch: boot flash:c3560-ipservicesk9-mz.<version>.bin
```

## Step 4: Clean Up

When IOS is running:

1. Verify the image: `verify /md5 flash:<image>.bin`
2. Set `boot system` to the new image and save, as in Step 2.
3. **Reset the console speed.** If you leave the boot loader `BAUD` at 115200, the console stays at that speed. Anyone who connects at the default 9600 baud later will see only garbage. Set it back in the boot loader (`set BAUD 9600`) or make sure the console line speed in IOS matches what your team expects.
4. Reload once to confirm that the switch boots without help.

## What About TFTP and USB?

On newer Catalyst platforms the boot loader can do more. Some models have a USB storage port (`usbflash0:`) or can boot an image over the network from the management port. That is much faster than Xmodem. On the classic 3560, these options are not available, so Xmodem is the only path when flash is empty. Run `help` at the `switch:` prompt to see what your platform supports.

The same idea, booting from TFTP or USB when the device does not start, is covered for data center switches in the [Nexus NX-OS upgrade guide](/en/posts/cisco-nexus-nxos-upgrade-guide/).

## Prevention

- Keep a copy of the current and the previous image on a TFTP server you can reach.
- Verify the MD5 checksum before every reload after an upgrade.
- Check `show boot` before every planned reload.
- Have console access ready for every upgrade. A console server makes this possible remotely: [Next-Gen Console Server Architecture](/en/posts/next-gen-console-server-architecture/).

## Related Articles

- [Cisco Catalyst 3560 Password Recovery: Two Methods](/en/posts/catalyst-3560-password-recovery/)
- [Catalyst 3560 IOS Upgrade: Two Methods and Verification](/en/posts/catalyst-3560-ios-upgrade/)
- [Cisco Nexus NX-OS Software Upgrade Guide](/en/posts/cisco-nexus-nxos-upgrade-guide/)
