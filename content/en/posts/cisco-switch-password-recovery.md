---
title: "Cisco Switch and Router Password Recovery: Catalyst 9000, 2960, 3560 and ISR"
description: "Recover a lost enable or console password on Cisco devices without losing the configuration — classic Catalyst (2960, 3560, 3750), Catalyst 9000 and 3850 with SWITCH_IGNORE_STARTUP_CFG, ISR routers with confreg 0x2142, and what to do when password recovery is disabled."
date: 2026-10-22
draft: false
aliases:
  - "/en/posts/catalyst-3560-password-recovery/"

tags: ["Cisco", "Password Recovery", "ROMMON", "IOS", "IOS-XE", "Catalyst 9300", "Catalyst 9200", "Catalyst 2960", "Catalyst 3560", "ISR 4000"]
categories: ["Network Operations"]
keywords: ["Cisco password recovery", "Cisco switch password reset", "Catalyst 9300 password recovery", "SWITCH_IGNORE_STARTUP_CFG", "no system ignore startupconfig switch all", "flash_init config.text", "confreg 0x2142", "no service password-recovery", "Cisco 2960 password recovery", "ISR 4331 password recovery"]
showToc: true
TocOpen: true
---

You inherit a device without documentation, or a lab switch comes back from storage and asks for a password nobody knows. On Cisco switches and routers you can recover from this without losing the configuration, as long as you have physical access and a console cable.

The principle is the same everywhere: interrupt the boot, start IOS **without** loading the startup configuration, then put the configuration back and set new passwords. Only the way you tell the device to skip the configuration differs:

| Platform | Typical models | How the configuration is skipped |
| --- | --- | --- |
| Classic Catalyst | 2960, 2960-X, 3560, 3750 | Rename `config.text` in the boot loader |
| IOS-XE Catalyst | 3650, 3850, 9200, 9300, 9400, 9500 | `SWITCH_IGNORE_STARTUP_CFG=1` |
| Routers | ISR 4000, ISR 1100, Catalyst 8000, ISR G2 | Configuration register `0x2142` |

## What You Need

- Physical access to the device, or a console server. Password recovery is deliberately not possible over the network. See [Next-Gen Console Server Architecture](/en/posts/next-gen-console-server-architecture/).
- A console cable and a terminal program. Settings: **9600 baud, 8 data bits, no parity, 1 stop bit, no flow control**.
- A maintenance window. The device reboots and does not forward traffic during the procedure.

## Switches: Get to the switch: Prompt

On Catalyst switches you interrupt the boot with the **Mode** button:

1. Connect the console and open the terminal session.
2. Unplug the power.
3. Hold the **Mode** button on the front panel and reconnect the power.
4. Keep holding until the console shows that the boot was interrupted, about 10 to 15 seconds, then release.

You are now at the `switch:` prompt.

On a Catalyst 9400 with two supervisors, Cisco recommends removing the secondary supervisor before you start.

## Classic Catalyst (2960, 3560, 3750): Rename config.text

```
switch: flash_init
switch: dir flash:
switch: rename flash:config.text flash:config.text.old
switch: boot
```

Some older boot loaders also need `load_helper` after `flash_init`. Do **not** delete `config.text`. Renaming is enough, and you need the contents later.

The switch boots without configuration. Answer **no** to the initial configuration dialog, then:

```
Switch> enable
Switch# rename flash:config.text.old flash:config.text
Switch# copy flash:config.text system:running-config
```

Continue with the section "Set New Passwords and Save" below.

## Catalyst 9000 and 3850: SWITCH_IGNORE_STARTUP_CFG

IOS-XE switches do not need the rename. A boot loader variable tells IOS to ignore the startup configuration:

```
switch: SWITCH_IGNORE_STARTUP_CFG=1
switch: boot flash:packages.conf
```

Use `boot flash:<image>.bin` if the switch runs in bundle mode. After the boot, answer **no** to the initial configuration dialog, then load the configuration:

```
Switch> enable
Switch# copy startup-config running-config
```

**Important:** reset the variable from IOS. Otherwise the switch ignores its configuration at every reload:

```
Switch# configure terminal
Switch(config)# no system ignore startupconfig switch all
Switch(config)# end
```

Continue with the next section, then save.

## Routers (ISR 4000, ISR 1100, Catalyst 8000): confreg 0x2142

Routers do not have a Mode button. Interrupt the boot by sending a **Break** from the terminal program during the first seconds after power-on. You land at the `rommon 1 >` prompt.

```
rommon 1 > confreg 0x2142
rommon 2 > reset
```

The value `0x2142` tells the router to ignore the startup configuration. After the boot, answer **no** to the initial configuration dialog:

```
Router> enable
Router# copy startup-config running-config
Router# configure terminal
Router(config)# config-register 0x2102
```

Setting the register back to `0x2102` is essential. Otherwise the router ignores its configuration at every reload.

## Set New Passwords and Save

You are now in privileged mode with the original configuration loaded. Set new credentials to match how authentication was set up before:

```
configure terminal
enable secret <new-enable-secret>
username admin privilege 15 secret <new-password>
line con 0
 login local
line vty 0 15
 login local
end
```

If the device uses TACACS+ or RADIUS, check that the local fallback account works.

Copying a configuration into the running configuration merges it. Interfaces may stay administratively down, especially VLAN interfaces (SVIs) on switches. Check and fix:

```
show ip interface brief
```

Bring up interfaces that should be up with `no shutdown`. Then save and test:

```
write memory
reload
```

Log in with the new credentials after the reload to confirm that the configuration and the passwords survive.

## When Password Recovery Is Disabled

If `no service password-recovery` is configured, the procedure behaves differently. The device does not let you skip the configuration. Instead it says that password recovery is disabled and asks whether to reset to the factory default configuration.

- **Yes:** the configuration (and on switches the VLAN database) is deleted. The device boots with default settings. The IOS image stays.
- **No:** the device boots normally with the current configuration, and you are back at the password prompt.

This is the purpose of the feature. Someone with physical access cannot read the configuration, but you lose it too. Before you answer yes, make sure you have a recent configuration backup from another source. After the reset, restore the configuration and recreate the VLANs if the backup does not contain them.

`no service password-recovery` makes sense for devices in public or unlocked locations, as long as the configuration is backed up somewhere else.

## Common Mistakes

- **Deleting `config.text` instead of renaming it.** Only a backup helps then.
- **Forgetting `no system ignore startupconfig switch all` or `config-register 0x2102`.** The device boots without configuration at the next reload.
- **Not saving after setting the passwords.** The old passwords come back at the next reload.
- **SVIs left shut down after the merge.** Management access over the network fails although the configuration looks correct.

## Related Articles

- [Cisco ROMMON Recovery: Boot from Flash, TFTP or USB](/en/posts/cisco-rommon-recovery/)
- [Cisco IOS and IOS-XE Upgrade Guide](/en/posts/cisco-ios-xe-upgrade-guide/)
- [Next-Gen Console Server Architecture](/en/posts/next-gen-console-server-architecture/)

Source: [Cisco: Troubleshoot Bootloader and Password Recovery on Catalyst 9000](https://cisco.com/c/en/us/support/docs/switches/catalyst-9300-series-switches/216944-troubleshoot-bootloader-rommon-and-pas.html)
