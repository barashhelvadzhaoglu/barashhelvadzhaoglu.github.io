---
title: "TFTP, FTP and SCP Servers for Cisco Upgrades: Setup and Troubleshooting"
description: "How to set up a TFTP, FTP or SCP server for Cisco IOS and IOS-XE image transfers on Windows, macOS and Linux — device-side commands, the management VRF, the FTP double-slash path, file size limits and firewall issues."
date: 2026-10-22
draft: false

tags: ["Cisco", "TFTP", "FTP", "SCP", "IOS", "IOS-XE", "Upgrade"]
categories: ["Network Operations"]
keywords: ["Cisco TFTP server setup", "copy tftp flash", "copy ftp bootflash", "ip ftp username", "ip tftp source-interface", "Tftpd64", "tftpd-hpa", "macOS tftp server", "Cisco scp copy", "TFTP 32MB limit", "Mgmt-vrf copy"]
showToc: true
TocOpen: true
---

Every Cisco upgrade starts with getting a file onto the device. For a 20 MB classic IOS image, almost anything works. For a 1 GB IOS-XE image over a WAN link, the choice of protocol decides whether the copy takes five minutes or fails after an hour.

This guide covers which protocol to use, how to set up the server on Windows, macOS and Linux, and the device-side commands and pitfalls.

## Which Protocol?

| Protocol | Port | Authentication | Strengths | Weaknesses |
| --- | --- | --- | --- | --- |
| TFTP | UDP 69 | None | Simple, supported everywhere, works from ROMMON | Slow, unreliable over WAN, size limits on old servers |
| FTP | TCP 21 (+ data) | User and password | Fast and reliable for large images | Clear text, needs firewall handling for the data channel |
| SCP | TCP 22 | SSH | Encrypted, uses existing SSH access | Slower than FTP on some platforms |
| HTTP(S) | TCP 80/443 | Optional | Fast, easy to host | Not available on older IOS versions |

My rule in practice:

- **FTP** for normal upgrades over the network. It is fast and reliable for large IOS-XE images.
- **TFTP** when the device is in ROMMON. ROMMON can only do TFTP. See [Cisco ROMMON Recovery](/en/posts/cisco-rommon-recovery/).
- **SCP** when the security policy does not allow clear-text protocols.

## Server Setup

### Windows: Tftpd64

Tftpd64 is a free tool that combines a TFTP server, a DHCP server and a syslog server.

1. Install Tftpd64 and start it.
2. Set the **Current Directory** to the folder that contains your images.
3. Select the **Server interface**, the IP address of the network adapter that faces the devices.
4. Allow Tftpd64 in the Windows firewall. This is the most common reason why transfers time out.

For FTP on Windows, FileZilla Server is a common free choice.

### macOS: Built-in TFTP Server

macOS has a TFTP server on board. It serves files from `/private/tftpboot`:

```
sudo mkdir -p /private/tftpboot
sudo cp <image>.bin /private/tftpboot/
sudo chmod 644 /private/tftpboot/<image>.bin
sudo launchctl load -F /System/Library/LaunchDaemons/tftp.plist
```

Stop it again with `sudo launchctl unload -F /System/Library/LaunchDaemons/tftp.plist`. If the macOS firewall is active, allow incoming connections.

### Linux: tftpd-hpa and vsftpd

On Debian and Ubuntu:

```
sudo apt install tftpd-hpa
```

The configuration is in `/etc/default/tftpd-hpa`. The default directory is `/srv/tftp`:

```
TFTP_DIRECTORY="/srv/tftp"
TFTP_OPTIONS="--secure"
```

Add `--create` to `TFTP_OPTIONS` only if devices should be able to upload files, for example configuration backups.

For FTP, `vsftpd` with a local user is enough:

```
sudo apt install vsftpd
sudo adduser netops
```

Put the images in the user's home directory or in a shared directory such as `/tftpboot/images`.

## Device Side: Copying the Image

### TFTP

```
copy tftp://192.0.2.10/<image>.bin flash:
```

### FTP

Credentials can be part of the URL, or configured once:

```
configure terminal
ip ftp username netops
ip ftp password <password>
end
copy ftp://192.0.2.10/images/<image>.bin bootflash:
```

**The double slash.** In an FTP URL, IOS treats the path as relative to the FTP user's home directory. If the images are in an absolute path outside the home directory, use two slashes after the server address:

```
copy ftp://192.0.2.10//tftpboot/images/<image>.bin bootflash:
```

`ftp://server/images/file` means `<home>/images/file`. `ftp://server//tftpboot/images/file` means `/tftpboot/images/file`. This detail explains many "file not found" errors.

### SCP

Pulling a file from an SCP server:

```
copy scp://netops@192.0.2.10/images/<image>.bin flash:
```

Pushing a file to the device from your laptop requires the SCP server on the device:

```
configure terminal
ip scp server enable
end
```

Then from the laptop:

```
scp <image>.bin admin@<device-ip>:flash:<image>.bin
```

Disable `ip scp server enable` again after the transfer if your policy requires it.

### Always Verify

```
verify /md5 flash:<image>.bin
```

Compare the value with the MD5 checksum on the Cisco download page. A file that copied without errors can still be incomplete.

## The Management Port and VRF

On Catalyst 9000 switches, the dedicated management port (GigabitEthernet0/0) sits in its own VRF called `Mgmt-vrf`. On ISR 4000 and Catalyst 8000 routers, the management port is in the VRF `Mgmt-intf`. A copy without a VRF uses the global routing table and fails if the server is only reachable through the management network.

Tell the device which interface to use as the source:

```
configure terminal
ip tftp source-interface GigabitEthernet0/0
ip ftp source-interface GigabitEthernet0/0
end
```

The router management port is named `GigabitEthernet0` on ISR 4000 routers. Check the name with `show ip interface brief`.

## Troubleshooting

### Timeout or "Connection refused"

- `ping` the server from the device, with the right source interface or VRF.
- Check the firewall on the server. Windows and macOS block incoming connections by default.
- For FTP: the data channel uses additional ports. If a firewall sits between device and server, passive mode problems are common.

### "File not found"

- Check the path relative to the server's root directory (TFTP) or the user's home directory (FTP). Remember the double slash.
- Check upper and lower case. File names are case-sensitive on Linux and macOS servers.
- Check that the server user can read the file.

### Copy Stops at 32 MB (TFTP)

Classic TFTP uses 512-byte blocks and a 16-bit block counter. That limits a transfer to about 32 MB unless both sides support larger blocks or block number rollover. Old or minimal TFTP servers still have this limit. IOS-XE images are much larger.

- Use FTP or SCP for large images.
- If you must use TFTP, use a current server and increase the block size on the device:

```
configure terminal
ip tftp blocksize 8192
end
```

### Very Slow Transfer

TFTP waits for an acknowledgment after every block. Over a WAN link with high latency, that makes it extremely slow. Use FTP or SCP over long distances, or place a server close to the device.

## Related Articles

- [Cisco IOS and IOS-XE Upgrade Guide](/en/posts/cisco-ios-xe-upgrade-guide/)
- [Cisco ROMMON Recovery: Boot from Flash, TFTP or USB](/en/posts/cisco-rommon-recovery/)
- [Cisco Nexus NX-OS Software Upgrade Guide](/en/posts/cisco-nexus-nxos-upgrade-guide/)
- [SecureCRT and SuperPuTTY for Network Engineers](/en/technology/securecrt-superputty/)
