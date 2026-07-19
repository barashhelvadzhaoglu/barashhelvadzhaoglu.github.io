---
title: "Cisco Nexus NX-OS Software Upgrade Guide: Field-Tested Step by Step"
description: "Field-tested guide for upgrading Cisco Nexus NX-OS — preparation, upgrade path, file transfer, rollback, and ROMMON recovery scenarios."
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

These outputs are required to select the correct NX-OS image, determine the upgrade path, and verify hardware compatibility.

## 2. Download the Software Image

- Download the correct NX-OS image for your switch model from Cisco's official portal:
  [https://software.cisco.com/download/home](https://software.cisco.com/download/home)
- A valid **Cisco account with the appropriate entitlements** is required.
- After downloading, **note the MD5 hash value** — you will need it to verify file integrity after transfer.

> MD5 verification confirms the file was not corrupted during download. This step is not optional.

## 3. Verify the Upgrade Path

A direct upgrade from your current NX-OS version to the target version is **not always supported**. Some version combinations require intermediate steps.

Use Cisco's official tools to verify:

- **Nexus Upgrade Matrix Tools**
- Nexus 9000 / 3000 Series
- Nexus 7000 Series

> If multiple upgrade steps are required, download **all intermediate images** before starting the process.

## 4. Copy the Software File to the Switch

### Option A: FTP Transfer

FTP is one of the most common methods. Note that NX-OS images can be close to 2 GB, so transfer time depends on network speed.

Example:

```bash
copy ftp://user1:Qazwsx@10.10.10.5/nxos.9.3.10.bin bootflash:
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

The output must exactly match the MD5 hash from the Cisco download portal.

## 5. Run the Upgrade

Once all checks are complete, start the upgrade:

```bash
install all nxos bootflash:nxos.9.3.10.bin
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

### Boot via TFTP from ROMMON

```bash
set ip 10.10.10.2 255.255.255.0
set gw 10.10.10.1
cmdline recoverymode=1
boot tftp://10.10.10.2/tftpboot/nxos.9.3.10.bin
init system
reload-nxos
```

### Boot via USB from ROMMON

```bash
boot usb1:nxos.9.3.10.bin bootflash:
set ip 10.10.10.2 255.255.255.0
set gw 10.10.10.1
cmdline recoverymode=1
boot usb1:nxos.9.3.10.bin
init system
reload-nxos
```

After booting from TFTP or USB, verify and correct the boot settings:

```bash
show boot
```

```bash
configure terminal
  boot nxos bootflash:/nxos.9.3.10.bin
```

## Critical Warning

During the software upgrade:

- **Do not interrupt the network connection**
- **Do not interrupt the power supply**

Either condition can render the device unrecoverable without physical intervention.

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