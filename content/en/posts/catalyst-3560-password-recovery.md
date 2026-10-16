---
title: "Cisco Catalyst 3560 Password Recovery: Two Methods, Step by Step"
description: "How to recover a lost enable or console password on a Cisco Catalyst 3560 — keep the configuration with the boot loader method, or reset when password recovery is disabled."
date: 2026-10-16
draft: false

tags: ["Cisco", "Catalyst", "Switch", "Password Recovery", "Boot Loader", "IOS"]
categories: ["Network Operations"]
keywords: ["Catalyst 3560 password recovery", "Cisco switch password reset", "flash_init", "config.text rename", "no service password-recovery", "Cisco boot loader switch prompt", "Cisco 3560 mode button", "recover enable secret Cisco switch"]
showToc: true
TocOpen: true
---

You inherit a switch, the documentation is gone, and nobody knows the enable password. Or a lab switch comes back from storage and the console asks for a password you never set. On a Cisco Catalyst 3560 you can recover from both without losing the configuration, as long as you have physical access and a console cable.

This guide covers the two situations you will meet in practice:

- **Method 1: keep the configuration.** The switch boots without loading its startup configuration, you reset the passwords, and you put the original configuration back.
- **Method 2: password recovery is disabled.** Someone configured `no service password-recovery`. You can still get the switch back, but only by resetting it to factory defaults.

> **Lab note:** I am running these procedures on my own Catalyst 3560 8-port PoE switch. Console outputs from that lab will be added to this guide.

## What You Need

- Physical access to the switch. Password recovery is deliberately impossible remotely.
- A console cable (RJ-45 rollover or USB-to-serial) and a terminal program such as SecureCRT, PuTTY or `screen`.
- Terminal settings: **9600 baud, 8 data bits, no parity, 1 stop bit, no flow control**.
- A maintenance window. The switch reboots twice and does not forward traffic during the procedure.

For console access from a distance, a console server is the professional answer. See [Next-Gen Console Server Architecture](/en/posts/next-gen-console-server-architecture/).

## How the Recovery Works

The Catalyst 3560 stores its startup configuration as a file called `config.text` in flash. When the switch boots normally, IOS loads that file. Password recovery interrupts the boot process before IOS starts and gives you the **boot loader**, a small environment with the `switch:` prompt.

In the boot loader you can access the flash file system. If `config.text` is renamed, IOS boots without a configuration, which means without passwords. You then log in, restore the configuration manually and set new passwords.

## Method 1: Recover the Password and Keep the Configuration

### Step 1: Interrupt the Boot Process

1. Connect the console cable and open your terminal session.
2. Unplug the power cable.
3. Press and hold the **Mode** button on the front panel.
4. Reconnect the power while still holding Mode.
5. Release the button after about 15 seconds, when the console shows that the system was interrupted before the flash file system was initialized.

You should now see the `switch:` prompt. If the switch boots normally instead, power off and try again, holding the button a little longer.

### Step 2: Initialize Flash

The flash file system is not mounted yet. Initialize it:

```
switch: flash_init
```

On some older boot loader versions you also need to load helper files:

```
switch: load_helper
```

Then list the contents of flash:

```
switch: dir flash:
```

You should see the IOS image (or a directory containing it), `config.text`, `vlan.dat` and possibly `private-config.text`.

### Step 3: Rename the Configuration File

```
switch: rename flash:config.text flash:config.text.old
```

Do **not** delete `config.text`. Renaming it is enough to stop IOS from loading it, and you still need its contents later.

### Step 4: Boot IOS Without the Configuration

```
switch: boot
```

The switch boots with an empty configuration. When it asks whether you want to enter the initial configuration dialog, answer **no**.

### Step 5: Restore the Original Configuration

```
Switch> enable
Switch# rename flash:config.text.old flash:config.text
Switch# copy flash:config.text system:running-config
```

The switch now runs your original configuration, including the hostname, VLANs, interfaces and the old passwords. You are still in privileged mode because you entered it before the configuration was loaded.

### Step 6: Set New Passwords

```
Switch# configure terminal
Switch(config)# enable secret <new-enable-secret>
Switch(config)# username admin privilege 15 secret <new-password>
Switch(config)# line con 0
Switch(config-line)# login local
Switch(config-line)# line vty 0 15
Switch(config-line)# login local
Switch(config-line)# end
```

Adjust this to how authentication was set up before. If the switch used TACACS+ or RADIUS, check that the local fallback account still works.

### Step 7: Check Interfaces and Save

Copying a configuration into the running configuration merges it. It does not reproduce every interface state. Check for interfaces that are administratively down, especially VLAN interfaces (SVIs):

```
Switch# show ip interface brief
```

Bring up any interface that should be up with `no shutdown`. Then save:

```
Switch# copy running-config startup-config
```

Reload once and log in with the new credentials to confirm that everything survives a reboot.

## Method 2: When Password Recovery Is Disabled

If the switch was configured with `no service password-recovery`, the Mode button procedure behaves differently. You cannot access the flash file system from the boot loader. Instead, the switch tells you that password recovery has been disabled and asks whether you want to reset the system to its default configuration.

- If you answer **yes**, the switch deletes the configuration file and the VLAN database and boots with factory defaults. The IOS image stays in flash.
- If you answer **no**, the switch boots normally with its current configuration, and you are back at the password prompt.

This is the intended trade-off of the feature. An attacker with physical access cannot read the configuration, but you lose it too.

Before you reset, make sure you have a recent backup of the configuration from another source, for example a configuration management tool, a TFTP server or an archived `show running-config`. After the reset:

1. Log in without a password and set new credentials.
2. Restore the configuration from your backup.
3. Recreate the VLANs if your backup does not include them. The VLAN database (`vlan.dat`) is deleted too.
4. Decide whether `no service password-recovery` should be enabled again. It makes sense for switches in public or unlocked locations, as long as the configuration is backed up somewhere else.

## Newer Boot Loaders: Ignoring the Startup Configuration

Newer Catalyst models and boot loader versions offer a cleaner alternative to renaming `config.text`: a boot loader variable that tells IOS to ignore the startup configuration for one boot. Whether your switch supports it depends on the model and boot loader version. Run `set` at the `switch:` prompt to see the variables your boot loader knows.

I will document what the 3560 boot loader offers once I have the lab outputs.

## Common Mistakes

- **Deleting `config.text` instead of renaming it.** The configuration is gone, and your only option is a backup.
- **Forgetting to rename the file back.** The switch boots without configuration at the next reload.
- **Using `copy startup-config running-config` before renaming.** The startup configuration does not exist under its normal name at that point.
- **Not saving after changing the passwords.** The old passwords come back at the next reload.
- **Shut down SVIs after the merge.** Management access over the network fails even though the configuration looks correct.

## Related Articles

- [Catalyst 3560 IOS Upgrade: Two Methods and Verification](/en/posts/catalyst-3560-ios-upgrade/)
- [When a Catalyst 3560 Won't Boot: Recovery from the Boot Loader](/en/posts/catalyst-3560-boot-loader-recovery/)
- [Cisco Nexus NX-OS Software Upgrade Guide](/en/posts/cisco-nexus-nxos-upgrade-guide/)
- [Next-Gen Console Server Architecture](/en/posts/next-gen-console-server-architecture/)
