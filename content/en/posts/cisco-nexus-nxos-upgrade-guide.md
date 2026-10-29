---
title: "Cisco Nexus NX-OS Software Upgrade Guide: Field-Tested Step by Step"
seoTitle: "Cisco Nexus NX-OS Upgrade Path & Matrix: Step-by-Step Upgrade Guide"
description: "How to check the Cisco NX-OS upgrade path with the Nexus Upgrade and ISSU Matrix, then upgrade a Nexus 9000, 3000 or 7000 step by step: install all, MD5, rollback and ROMMON recovery."
date: 2025-12-30
draft: false

cover:
  image: "/img/postimages/nexus-nxos-upgrade-cover.webp"
  alt: "Cisco Nexus NX-OS Software Upgrade Guide"
  relative: false

tags: ["Cisco", "Nexus", "NX-OS", "Network", "Upgrade", "Data Center"]
categories: ["Network Operations"]
keywords: ["Cisco Nexus upgrade", "NX-OS upgrade guide", "Nexus software update", "NX-OS ROMMON recovery", "Nexus upgrade path", "Cisco Nexus rollback", "NX-OS install all", "Nexus bootflash upgrade", "Cisco data center upgrade", "NX-OS MD5 verification"]
showToc: true
TocOpen: true
---

This guide covers the **Cisco Nexus NX-OS software upgrade process** in a practical, step-by-step manner — including **rollback and recovery scenarios**. The goal is to minimize service disruption and ensure the device can always be recovered in case of failure.

Most upgrade failures are not caused by the upgrade itself — they are caused by skipping preparation steps. This guide treats preparation as seriously as execution.

{{< figure src="/img/postimages/nexus-nxos-upgrade-cover.webp" title="Cisco Nexus NX-OS Upgrade Process" >}}

> For out-of-band access during upgrade failures, see: [The Backdoor of the Network: Next-Gen Console Server Architecture](/en/posts/next-gen-console-server-architecture/)

## 1. Pre-Upgrade Checks

Before starting the software upgrade, you must complete the preparation steps below. This phase is the most commonly skipped — and the most common source of problems.

### Configuration Backup

- Take a **backup of the current configuration** before anything else.
- Store the backup on your own computer or an **external location** such as FTP/SFTP — not on the switch itself.
- If the upgrade fails or a rollback is needed, this backup is critical.

### Verify Switch Model and Current Software Version

Check the switch model and the running NX-OS version with these commands:

```bash
show version
show module
show inventory
```

Example output (abbreviated, values are placeholders):

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

These outputs are required to select the correct NX-OS image, determine the upgrade path, and verify hardware compatibility.

## 2. Download the Software Image

- Download the correct NX-OS image for your switch model from Cisco's official portal:
  [https://software.cisco.com/download/home](https://software.cisco.com/download/home)
- A valid **Cisco account with the appropriate entitlements** is required.
- After downloading, **note the MD5 hash value** — you will need it to verify file integrity after transfer.

> MD5 verification confirms the file was not corrupted during download. This step is not optional.

## 3. Verify the Upgrade Path (NX-OS Upgrade Matrix)

A direct upgrade from your current NX-OS version to the target version is **not always supported**. Some combinations need one or more intermediate releases, and some are only possible as a disruptive (cold boot) upgrade instead of ISSU. Cisco publishes the validated paths in its upgrade matrix tools.

**Nexus 9000 and 3000:** use the [Cisco Nexus 9000 and 3000 Upgrade and ISSU Matrix](https://www.cisco.com/c/en/us/td/docs/dcn/tools/nexus-9k3k-issu-matrix/index.html).

1. Select your **current** NX-OS release and the **target** release.
2. Read the result: whether a **direct** path exists, which **intermediate releases** are required, and whether the path supports **ISSU** (non-disruptive) or only a **disruptive** upgrade.
3. Check the listed **caveats** and the supported hardware (PIDs) for your exact switch model.

**Nexus 7000:** Cisco provides a separate ISSU and cold boot support matrix. Both tools are listed in Cisco's [Nexus Upgrade Matrix Tools](https://www.cisco.com/c/en/us/support/docs/ios-nx-os-software/nx-os-software/217715-nexus-upgrade-matrix-tools.pdf) note.

On the switch itself, check the impact before you start, once the target image is in bootflash:

```
show install all impact nxos bootflash:<target-image>.bin
show incompatibility-all nxos bootflash:<target-image>.bin
```

Example output (abbreviated, values are placeholders):

```
switch# show install all impact nxos bootflash:nxos.9.3.10.bin
...
Compatibility check is done:
Module  bootable          Impact  Install-type  Reason
------  --------  --------------  ------------  ------
     1       yes      disruptive         reset  Default upgrade is not hitless

Images will be upgraded according to following table:
Module       Image   Running-Version(pri:alt)   New-Version   Upg-Required
------  ----------  -------------------------  ------------  ------------
     1        nxos                     9.3(8)        9.3(10)           yes

switch# show incompatibility-all nxos bootflash:nxos.9.3.10.bin
No incompatible configurations
```

`show install all impact` tells you whether the upgrade will be disruptive for each module. `show incompatibility-all` lists configuration that the target release does not support.

> If multiple upgrade steps are required, download **all intermediate images** before starting, and verify each one with MD5.

## 4. Copy the Software File to the Switch

### Option A: FTP Transfer

FTP is one of the most common methods. Note that NX-OS images can be close to 2 GB, so transfer time depends on network speed.

Example:

```bash
copy ftp://<user>@10.10.10.5/nxos.9.3.10.bin bootflash: vrf management
```

If multiple VRFs are configured on the Nexus, you will be asked which VRF to use for the transfer. Since the management interface typically uses the management VRF, select management VRF.

### Option B: USB Transfer (Recommended)

USB transfer is my preferred method when:

- No FTP server is readily available
- You have time constraints
- You want to avoid any network transfer risk

```bash
copy usb1:nxos.9.3.10.bin bootflash:
```

Ensure the USB filesystem format is supported by the Nexus device before proceeding.

### MD5 Hash Verification

After the transfer, verify file integrity:

```bash
show file bootflash:nxos.9.3.10.bin md5sum
```

Example output (abbreviated, values are placeholders):

```
switch# show file bootflash:nxos.9.3.10.bin md5sum
<32-character MD5 value of the file>
```

Compare this value with the MD5 hash on the Cisco download page.

The output must exactly match the MD5 hash from the Cisco download portal.

## 5. Run the Upgrade

Once all checks are complete, start the upgrade:

```bash
install all nxos bootflash:nxos.9.3.10.bin
```

Example output (abbreviated, values are placeholders):

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

- The switch automatically saves the current configuration before installation.
- You will be prompted for confirmation before the reboot.
- After confirmation, the device reboots and the upgrade begins.

Upgrade duration varies depending on the device model and software size.

## 6. Rollback and Recovery Scenarios

{{< figure src="/img/postimages/nexus-upgrade-rollback.webp" title="Nexus Upgrade Rollback and Recovery Path" >}}

### ROMMON Mode Entry

If the installation fails or the device does not boot:

- During device startup, press **CTRL + L** or **CTRL + C** via console connection to enter **ROMMON mode**.

### Option 1: The Image Is Still in Bootflash

If the image is in bootflash but the boot variable is wrong, boot it directly:

```
loader > dir
loader > boot bootflash:nxos.9.3.10.bin
```

When NX-OS is up, fix the boot variable as shown at the end of this section.

### Option 2: Boot the Image over TFTP

If the image is missing but bootflash itself is fine, boot the full image from a TFTP server through the management port. The switch IP and the TFTP server are two different addresses, and you must give the full path to the image:

```
loader > set ip 10.10.10.20 255.255.255.0
loader > set gw 10.10.10.1
loader > boot tftp://10.10.10.5/tftpboot/nxos.9.3.10.bin
```

Example output (abbreviated, values are placeholders):

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

The image runs from memory only. When NX-OS is up, copy it to bootflash and verify it:

```
copy tftp://10.10.10.5/tftpboot/nxos.9.3.10.bin bootflash: vrf management
show file bootflash:nxos.9.3.10.bin md5sum
```

### Option 3: Boot from USB

```
loader > dir usb1:
loader > boot usb1:nxos.9.3.10.bin
```

When NX-OS is up, copy the image to bootflash with `copy usb1:nxos.9.3.10.bin bootflash:` and verify the MD5.

### Option 4: Bootflash Is Corrupted (Recovery Mode)

Use this only when bootflash itself is damaged. **`init system` reformats the file system of the device.** Make sure you have a configuration backup before you run it.

```
loader > set ip 10.10.10.20 255.255.255.0
loader > set gw 10.10.10.1
loader > cmdline recoverymode=1
loader > boot tftp://10.10.10.5/tftpboot/nxos.9.3.10.bin
switch(boot)# init system
switch(boot)# load-nxos
```

`cmdline recoverymode=1` stops the boot at the `switch(boot)#` prompt. `load-nxos` then completes loading NX-OS. Afterwards copy the image to bootflash and restore the configuration. Source: [Cisco Nexus 9000 NX-OS Troubleshooting Guide](https://www.cisco.com/c/en/us/td/docs/dcn/nx-os/nexus9000/102x/Troubleshooting/cisco-nexus-9000-series-nx-os-troubleshooting-guide-release-102x/m-troubleshooting-installations-upgrades-and-reboots.html).

### Fix the Boot Variable

```bash
configure terminal
  boot nxos bootflash:/nxos.9.3.10.bin
end
copy running-config startup-config
show boot
```

Example output (abbreviated, values are placeholders):

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

## Critical Warning

During the software upgrade:

- **Do not interrupt the network connection**
- **Do not interrupt the power supply**

Either condition can render the device unrecoverable without physical intervention.

---

## FAQ

**How do I find the NX-OS upgrade path for my Nexus switch?**
Use Cisco's Nexus 9000 and 3000 Upgrade and ISSU Matrix (or the Nexus 7000 ISSU matrix). Enter your current and target release. The tool shows whether a direct upgrade is supported, which intermediate releases you need and whether ISSU is possible.

**Can I upgrade NX-OS directly to the latest release?**
Not always. Large jumps between major releases often need one or more intermediate releases. Always check the matrix for your exact combination instead of assuming a direct path.

**What is the difference between ISSU and a disruptive upgrade?**
ISSU (In-Service Software Upgrade) upgrades the software while the switch keeps forwarding traffic. A disruptive (cold boot) upgrade reloads the switch and interrupts traffic. `show install all impact` tells you which one applies before you start.

**What do I do if the Nexus switch boots into loader or ROMMON after the upgrade?**
Boot the image from bootflash, TFTP or USB as described in the rollback section above, then fix the boot variables.

---

## Related Articles

**Architecture & Operations**
- 🛠️ [The Backdoor of the Network: Next-Gen Console Server Architecture](/en/posts/next-gen-console-server-architecture/) — Out-of-band access when IP management is lost
- 📊 [Monitoring Done Right: How to Build a Proactive IT Operations Culture](/en/architecture/monitoring-not-just-seeing/) — Catching problems before they escalate
- 🏗️ [Switch, Firewall, AP — Why Choosing the Right Products Is Not Enough](/en/architecture/core-network-is-not-a-product-list/) — Architecture-first core network design
- 🎯 [Network Infrastructure Product Selection: Strategic Criteria](/en/architecture/network-product-selection-strategy/) — Evaluating vendors strategically

**Practical Engineering**
- 🛡️ [Network Packet Broker (NPB) Masterclass](/en/posts/network-packet-broker-masterclass/) — Traffic visibility and security strategy
- 🔐 [802.1X Field Deployment Guide](/en/technology/identity-based-microsegmentation-8021x/) — Identity-based network access control