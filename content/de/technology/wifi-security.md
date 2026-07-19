---
title: "WiFi Security: WPA3, 802.1X, Rogue AP Detection, and Site Survey"
description: "Enterprise-WLAN-Sicherheit — WPA3 vs. WPA2, 802.1X-Authentifizierung, Rogue-AP-Erkennung und Ekahau Site Survey Methodik."
date: 2026-04-27
draft: false

cover:
  image: "/img/postimages/wifi-security-wpa3-cover.webp"
  alt: "WiFi Security — WPA3, 802.1X, Rogue AP Detection, Ekahau Site Survey"
  relative: false

tags: ["WiFi", "WPA3", "802.1X", "Wireless Security", "Rogue AP", "Ekahau", "Site Survey", "RADIUS", "WPA2 Enterprise"]
categories: ["Technology"]
keywords:
  - WPA3 enterprise WiFi security
  - 802.1X wireless authentication
  - rogue AP detection wireless
  - Ekahau site survey methodology
  - WiFi security WPA2 vs WPA3
  - wireless RADIUS authentication
  - enterprise WiFi security best practices
  - WiFi intrusion detection
  - wireless site survey process
  - 802.11 security protocols

showToc: true
TocOpen: true
---

# WiFi Security: WPA3, 802.1X, Rogue AP Detection, and Site Survey

This article is part of the Enterprise WiFi series.

> **New to enterprise wireless?** Start with the overview: [Enterprise WiFi Architecture: From Standards to Deployment](/en/technology/enterprise-wifi-architecture-complete-guide/)

---

## Why WiFi Security Is Different

Wired network security benefits from physical access control — a device must be physically connected to the network to communicate on it. WiFi removes this constraint. Anyone within RF range of your access point can attempt to connect. Your network's perimeter is literally invisible and extends beyond your walls.

This makes WiFi security fundamentally different from wired security, and it makes the authentication and encryption choices on a wireless network more critical than most teams treat them.

---

## Encryption: From WEP to WPA3

### The History That Explains the Present

**WEP (1997):** The original WiFi encryption. Completely broken. RC4 stream cipher with catastrophically weak key reuse. WEP encryption can be cracked in minutes with freely available tools. If you see WEP anywhere, treat it as unencrypted.

**WPA (2003):** Introduced TKIP (Temporal Key Integrity Protocol) as a WEP replacement. Better than WEP but still vulnerable. Not acceptable in any current deployment.

**WPA2 (2004):** Introduced CCMP with AES-128 encryption. WPA2 with a strong PSK or WPA2-Enterprise (802.1X) remains secure for most environments. The KRACK vulnerability (2017) required patching but was mitigated by OS updates.

**WPA3 (2018):** The current standard. Two security improvements matter:

### WPA3: What Actually Changed

**SAE (Simultaneous Authentication of Equals)** replaces WPA2's PSK handshake:

In WPA2-PSK, the 4-way handshake can be captured passively. An attacker captures the handshake and performs offline brute-force attack — testing millions of password combinations against the captured data without any interaction with your network. A weak password can be cracked in hours.

WPA3-SAE eliminates offline brute-force: each authentication attempt requires active interaction with the AP. Dictionary attacks are impractical. Even if an attacker captures the SAE handshake, they cannot use it for offline cracking.

**Forward Secrecy:** WPA3's most important security improvement. In WPA2, if an attacker captures encrypted traffic and later obtains the network password, they can decrypt all previously captured traffic. WPA3's SAE generates a unique key for each session — obtaining the password does not compromise past sessions.

**WPA3-Enterprise:** Adds 192-bit security mode (GCMP-256 encryption, BIP-GMAC-256 management frame protection) for environments with higher security requirements — financial services, government, healthcare.

### Management Frame Protection (802.11w)

WiFi management frames (probe requests, authentication, de-authentication, beacon) were historically unencrypted and unauthenticated — any device could send a forged de-authentication frame and disconnect clients from the network.

802.11w (Protected Management Frames, PMF) encrypts and authenticates management frames:
- Prevents de-authentication attacks (a common WiFi denial-of-service technique)
- Required for WPA3; optional but recommended for WPA2

Enable PMF in "required" mode for WPA3 networks. For WPA2 networks, "optional" mode provides protection for clients that support it while remaining compatible with older devices.

---

## Authentication Architecture: PSK vs. 802.1X

### WPA2/WPA3-PSK: Where It's Acceptable and Where It Isn't

A Pre-Shared Key (PSK) is a single password shared by all users of an SSID. For consumer use and simple SMB deployments, PSK is operationally convenient. For enterprise environments, it has critical weaknesses:

- **No individual accountability:** You know someone connected with the PSK, but not who.
- **Revocation requires changing the password everywhere:** One departing employee means a password change for the entire organization.
- **No dynamic policy:** Every user gets identical access regardless of role or device.

**Where PSK is acceptable:**
- Guest networks (where accountability is lower priority and everyone gets the same access)
- IoT device networks (devices often don't support 802.1X)
- Small offices where IT overhead of 802.1X deployment is genuinely disproportionate

**Where PSK is not acceptable:**
- Any network carrying sensitive business data
- Any network where individual user accountability is required
- Any regulated industry where authentication logging is mandated

### 802.1X: Enterprise Authentication

802.1X provides port-based network access control — a client must authenticate before gaining network access. For wireless, "port" means the association with an AP.

The authentication flow:

```
1. Client (Supplicant) associates with AP
2. AP (Authenticator) blocks all traffic except EAPOL (authentication frames)
3. AP relays authentication exchange to RADIUS server (Authentication Server)
4. RADIUS authenticates against identity store (Active Directory, LDAP, certificate store)
5. RADIUS returns: Access-Accept + VLAN assignment + other attributes
6. AP grants network access, places client in assigned VLAN
```

**Components required:**
- **Supplicant:** 802.1X client software on the connecting device. Built into Windows, macOS, iOS, Android.
- **Authenticator:** The AP (or WLC in centralized architectures)
- **RADIUS server:** Windows NPS, Cisco ISE, Aruba ClearPass, FreeRADIUS
- **Identity store:** Active Directory, LDAP directory, certificate authority

### EAP Methods: Choosing the Right One

EAP (Extensible Authentication Protocol) defines the specific authentication exchange. The choice of EAP method determines security strength and deployment complexity:

**PEAP-MSCHAPv2 (Most Common):**
- Client authenticates with username/password
- Password is never sent in clear — it's used in an MS-CHAP exchange inside a TLS tunnel
- Server presents a certificate to the client (client must verify it)
- Simple to deploy — no client certificates required
- Weakness: password-based, still vulnerable to credential theft

**EAP-TLS (Strongest):**
- Both client and server authenticate with certificates
- No password involved — the certificate is the credential
- Even if a user's AD password is compromised, network access requires the certificate
- Requires PKI infrastructure (Active Directory Certificate Services or similar)
- Client certificates must be distributed to all managed devices (typically via GPO)
- Most secure wireless authentication method

**EAP-TTLS / EAP-FAST:**
- Alternatives to PEAP, less commonly deployed in enterprise environments
- EAP-FAST was designed by Cisco as a PEAP alternative; relevant in Cisco-heavy environments

**Field recommendation:** PEAP for most enterprise deployments — straightforward deployment with AD integration. EAP-TLS for environments with high security requirements (banking, healthcare, critical infrastructure) where certificate infrastructure already exists.

### Dynamic VLAN Assignment

One of 802.1X's most powerful features: the RADIUS server can assign clients to different VLANs based on identity, device type, or group membership:

```
User: john.smith (member of Finance group)
→ RADIUS assigns VLAN 30 (Finance VLAN)

User: jane.doe (member of HR group)
→ RADIUS assigns VLAN 40 (HR VLAN)

Device: MedDevice-001 (MAC auth bypass, device certificate)
→ RADIUS assigns VLAN 50 (Medical Device VLAN)

Unknown device (no certificate, no AD account)
→ RADIUS assigns VLAN 99 (Quarantine VLAN)
```

This eliminates manual VLAN assignment and ensures consistent policy regardless of which physical AP a user connects through.

---

## Rogue AP Detection and Containment

### What Is a Rogue AP?

A rogue AP is any unauthorized access point present in your RF environment. Categories:

**Malicious rogue:** Deliberately planted by an attacker. Often configured with the same SSID as your corporate network to capture credentials (evil twin attack). Provides internet connectivity to attract clients.

**Accidental rogue:** An employee connected a personal router or WiFi extender to the corporate network. Often well-intentioned but creates security bypass — devices connecting to this AP bypass corporate authentication and land directly on the corporate LAN.

**Neighboring AP:** An AP from an adjacent office or building, not connected to your network. Not a security threat, but contributes to interference.

Enterprise wireless controllers classify detected APs based on whether they are connected to the same wired network as your infrastructure.

### How Detection Works

Enterprise wireless controllers continuously scan the RF environment on all channels in addition to serving clients. This is called **off-channel scanning** or **background scanning**:

- APs briefly switch to neighboring channels to scan for other wireless devices
- Detected APs are reported to the controller with BSSID, SSID, signal strength, and channel
- The controller compares detected APs against the known AP database

**Wired-side detection:** When an AP is detected in the RF environment, the controller checks whether its BSSID appears in the wired network's ARP table or MAC address table. If a detected AP's MAC address is visible on your wired infrastructure, it is classified as a **rogue connected to your network** — a security incident.

### Containment (Rogue AP Mitigation)

When a rogue AP is classified as a threat, enterprise controllers can automatically contain it:

**Deauthentication containment:** The controller sends 802.11 de-authentication frames impersonating the rogue AP, instructing connected clients to disconnect. Clients attempting to connect are continuously deauthenticated. This prevents clients from maintaining connections to the rogue AP.

**Legal note:** Active containment (sending deauthentication frames) is legally restricted in many jurisdictions. If the rogue AP belongs to a neighboring business rather than being on your network, active containment may violate telecommunications regulations. Most enterprise controllers allow you to configure automatic containment for APs connected to your network and manual containment only for neighboring APs.

### Evil Twin Detection

An evil twin attack is a rogue AP configured with the same SSID as your corporate network, intended to capture credentials from users who connect to it.

Detection: Your controller sees an AP with your SSID but a different BSSID (MAC address). This is classified as an evil twin and should trigger immediate investigation and containment.

Mitigation beyond containment: 802.1X authentication makes evil twin attacks against credential capture much harder. Even if a user connects to the evil twin, EAP-TLS requires mutual authentication — the evil twin cannot present a valid server certificate from your CA, so the client's 802.1X supplicant will refuse to authenticate.

---

## Site Survey: Methodology and Process

### Why Site Survey Is Not Optional

A site survey is the only way to know — not assume, not estimate, but know — that your wireless deployment will meet its requirements before you rely on it. Skipping the survey is common. It's also the most common cause of "we deployed WiFi and now it doesn't work properly" situations.

What a site survey reveals:
- Actual RF coverage from each AP position
- Signal strength and data rate at every point in the space
- Channel utilization and interference from neighboring networks
- Roaming behavior between APs
- Coverage gaps that aren't visible on floor plans

### Survey Types

**Predictive Survey (Pre-Deployment):**
Uses RF simulation software to model coverage before installing APs. You provide a floor plan, specify wall materials and thickness, place virtual APs at proposed locations, and the software calculates expected coverage.

**Ekahau Site Survey** (now called Ekahau Pro) is the industry standard. Cisco and Aruba also have proprietary tools (Cisco DNA Spaces, Aruba Airwave) but Ekahau is vendor-neutral and widely used.

The predictive survey answers: How many APs do I need? Where should they be placed? What channels should they use? What will coverage look like?

**Validation Survey (Post-Deployment):**
After APs are installed, you walk the space with a laptop running Ekahau's survey software, collecting actual measurements. The software records your GPS location (based on walking path on the floor plan), the RSSI from every AP, channel utilization, noise floor, and roaming events.

Compare validation results against the predictive model:
- Coverage matches prediction → deployment is correct
- Coverage gaps exist → adjust AP placement or power levels
- Channel contention found → adjust channel assignments
- Roaming dead zones found → adjust AP placement or enable fast roaming protocols

### Running an Ekahau Survey: Process

**Step 1: Import floor plan**
Import an accurate floor plan (AutoCAD, PDF, image) into Ekahau. Set the scale — Ekahau needs to know the real-world dimensions to calculate RF propagation distances.

**Step 2: Define wall types**
Mark walls on the floor plan and assign attenuation values:
- Interior plasterboard/drywall: 3–5 dB per wall
- Brick/concrete: 12–15 dB per wall
- Glass: 2–3 dB per wall
- Metal (elevator shafts, equipment rooms): 20–30 dB

Accuracy here directly affects predictive survey quality.

**Step 3: Place virtual APs and run simulation**
Place virtual APs at proposed locations. Set AP model, antenna orientation, and power level. Run the simulation and review coverage heat maps.

Heat maps show:
- **Signal strength (RSSI):** Target -65 dBm or better for high-throughput clients; -70 dBm minimum for basic connectivity
- **Data rate:** Expected throughput at each point
- **Coverage overlap:** Percentage of the space covered by 2+ APs at threshold RSSI (important for roaming)

**Step 4: Iterate AP placement**
Adjust AP positions based on simulation results. Add APs in areas with inadequate coverage. Reduce power in areas where cells overlap too much (co-channel interference).

**Step 5: Validation walk**
After physical installation, walk the space in a systematic pattern using Ekahau's survey mode. Move slowly — Ekahau collects measurements continuously and correlates them with your position on the floor plan.

Pay special attention to:
- Room corners and edges (often weakest signal)
- Stairwells and elevator lobbies (transition areas, common roaming failure points)
- Conference rooms (high-density scenarios)
- Areas behind obstacles (server racks, large metal cabinets)

**Step 6: Review and remediate**
Compare validation heatmap against prediction. Document actual versus predicted performance. Adjust AP placement, power levels, or channel assignments for any areas that fall below requirements.

### Key Survey Metrics and Targets

| Metric | Minimum | Target |
|---|---|---|
| RSSI (signal strength) | -70 dBm | -65 dBm or better |
| SNR (signal-to-noise ratio) | 20 dB | 25 dB or better |
| Channel overlap | 15–20% | 20–25% (sufficient for roaming) |
| Co-channel interference | < -85 dBm from neighbors | < -90 dBm |
| Roaming transition time | < 150ms (voice) | < 50ms (best case with 802.11r) |

---

## Wireless Intrusion Detection (WIDS)

Beyond rogue AP detection, enterprise wireless platforms provide broader wireless intrusion detection:

- **De-authentication flood detection:** Alert when a burst of de-authentication frames is detected — indicates a potential WiFi DoS attack
- **Probe flood detection:** Unusual volume of probe requests may indicate scanning activity
- **Association flood:** Rapid connection attempts that could indicate a brute-force or credential stuffing attempt against the WiFi network
- **SSID spoofing:** Detect APs broadcasting SSIDs identical to your network (evil twin)
- **Adhoc network detection:** Client-to-client wireless connections that bypass your AP infrastructure

WIDS events should be integrated into your SIEM or monitoring platform for centralized visibility. An increase in de-authentication flood events alongside network performance degradation, for example, suggests a coordinated WiFi attack.

---

## Key Takeaways

- **WPA3 SAE** eliminates offline brute-force attacks on PSK networks. **WPA3-Enterprise** adds 192-bit security for high-assurance environments.
- **802.1X** provides individual accountability, dynamic VLAN assignment, and policy enforcement that PSK cannot deliver. Use PEAP for most deployments, EAP-TLS where certificate infrastructure exists.
- **Rogue AP detection** is built into enterprise wireless platforms — use it. Automatic containment for network-connected rogues, manual review for neighboring APs.
- **Evil twin attacks** are significantly mitigated by 802.1X with mutual authentication — clients won't authenticate to a rogue AP that can't present a valid server certificate.
- **Site survey is not optional.** Predictive survey before deployment, validation survey after. Ekahau is the industry standard tool.
- **WIDS** turns your wireless infrastructure into a sensor for wireless-layer attacks. Integrate events into your monitoring platform.

---

## This Series

- 📖 [Enterprise WiFi Architecture Overview](/en/technology/enterprise-wifi-architecture-complete-guide/) ← Start here
- 📡 [802.11 Standards Deep Dive](/en/technology/wifi-80211-standards-wifi4-wifi5-wifi6/)
- 🏢 [Enterprise Controller Architecture: Cisco and Aruba](/en/technology/enterprise-wifi-controller-architecture-cisco-aruba/)
- 🏨 [WiFi Design for SMB, Hotels, and Medical Practices](/en/technology/wifi-design-smb-hotel-medical/)

## Related Articles

- 🔐 [802.1X Identity-Based Architecture in the Field](/en/technology/identity-based-microsegmentation-8021x/) — Deep dive on 802.1X beyond wireless
- 🔐 [The Zero Trust Mindset: Engineering Security as an Architecture](/en/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — Where wireless security fits in Zero Trust
- 📊 [Monitoring Done Right](/en/architecture/monitoring-not-just-seeing/) — Integrating wireless events into proactive monitoring
