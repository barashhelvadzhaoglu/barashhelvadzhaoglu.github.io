---
title: "DDoS Protection Strategies: ISP Scrubbing, On-Premise Appliances, and Cloud Services"
description: "DDoS protection guide — attack types, ISP scrubbing, on-premise appliances, cloud services, and how to choose the right combination for your organization."
date: 2026-03-30
draft: false

cover:
  image: "/img/postimages/ddos-protection-strategies-cover.webp"
  alt: "DDoS Protection Strategies — ISP Scrubbing, On-Premise, Cloud"
  relative: false

tags: ["DDoS", "Network Security", "Arbor", "Cloudflare", "AWS Shield", "ISP Scrubbing", "On-Premise", "Cloud Security"]
categories: ["Technology"]
keywords:
  - DDoS protection strategies
  - ISP DDoS scrubbing
  - on-premise DDoS appliance
  - cloud DDoS protection
  - Cloudflare DDoS
  - AWS Shield
  - Arbor DDoS
  - Radware DefensePro
  - hybrid DDoS protection
  - DDoS mitigation comparison

showToc: true
TocOpen: false
---

# DDoS Protection Strategies: ISP Scrubbing, On-Premise Appliances, and Cloud Services

A DDoS (Distributed Denial of Service) attack doesn't need to compromise your systems. It just needs to make them unreachable. And unlike most security threats, the damage is instant and fully visible — your application stops working, customers can't reach you, and revenue stops.

What makes DDoS uniquely difficult is that the attack traffic looks legitimate at the packet level. Millions of valid TCP SYN packets, millions of valid DNS queries, millions of valid HTTP requests — all perfectly formed, all completely intentional. Your network processes them the same way it processes real traffic, and that's exactly the problem.

After working in banking infrastructure where DDoS protection was a regulatory requirement — not just a best practice — I want to walk through how organizations actually protect themselves: what the three main approaches are, what each one can and cannot do, and how they combine in practice.

---

## Understanding the Attack Surface

Before choosing a protection strategy, it's worth being precise about what you're protecting against. DDoS attacks fall into three categories, and they require fundamentally different mitigation approaches.

### Volumetric Attacks (Layer 3/4)

The most visible type. The goal is simple: saturate your internet link with more traffic than it can carry.

Common techniques:
- **UDP flood** — send massive volumes of UDP packets to random ports. The target sends ICMP "port unreachable" responses, consuming both inbound and outbound bandwidth.
- **ICMP flood (Ping flood)** — overwhelm with ping requests.
- **Amplification attacks** — the most dangerous variant. Attacker sends small requests to misconfigured third-party servers (DNS resolvers, NTP servers, memcached instances) using your IP as the source. Those servers send large responses to you. DNS amplification can achieve 50–70× amplification; memcached amplification has reached 51,000×.

**Scale:** Modern volumetric attacks routinely exceed 1 Tbps. A 10 Gbps internet link is irrelevant against this — you're flooded before a single packet reaches your firewall.

**Key insight:** You cannot mitigate volumetric attacks on your own premises if the attack volume exceeds your ISP uplink. The traffic must be filtered upstream — at the ISP or cloud level — before it reaches your connection.

### Protocol Attacks (Layer 3/4)

Exhaust network device resources rather than bandwidth.

- **SYN flood** — send millions of TCP SYN packets without completing the handshake. The target allocates memory for each half-open connection until the connection table fills and legitimate connections are rejected.
- **Fragmented packet attacks** — send malformed or overlapping IP fragments that overwhelm reassembly buffers.
- **Smurf attack** — ICMP broadcast amplification using forged source IPs.

**Scale:** Measured in packets per second (Mpps), not bandwidth. A 100 Mbps SYN flood at small packet sizes can exceed the connection table capacity of a mid-range firewall.

**Key insight:** Protocol attacks can be mitigated on-premise by dedicated DDoS hardware with FPGA-based packet processing — but only if the volume doesn't saturate your upstream link first.

### Application Layer Attacks (Layer 7)

The hardest to detect and mitigate. Traffic is legitimate HTTP/HTTPS — it's the intent that's malicious.

- **HTTP flood** — millions of HTTP GET or POST requests targeting resource-intensive endpoints (search, login, report generation).
- **Slowloris** — open many connections and send HTTP headers very slowly, keeping connections open without completing requests. Exhausts the server's connection pool.
- **RUDY (R-U-Dead-Yet)** — similar to Slowloris but for POST bodies. Sends data one byte at a time.
- **SSL exhaustion** — initiate TLS handshakes but never complete them, or complete handshakes and immediately renegotiate. CPU-intensive for servers without hardware SSL acceleration.

**Scale:** Can be devastatingly effective at low traffic volumes — a few thousand requests per second targeting the right endpoint can bring down a web server that handles millions of normal requests.

**Key insight:** Layer 7 attacks require application-aware mitigation. A volumetric scrubbing service cannot distinguish a malicious HTTP flood from legitimate traffic — it needs WAF or behavioral analysis capabilities.

---

## The Three Protection Approaches

No single protection approach covers all attack types at all scales. Organizations with serious DDoS exposure typically combine two or three of these layers.

---

## 1. ISP-Based Scrubbing Services

### How It Works

Your ISP (or a specialist scrubbing provider with upstream network agreements) diverts your traffic to a **scrubbing center** during an attack. In the scrubbing center, attack traffic is filtered and only clean traffic is forwarded to your network:

```
Normal operation:
  Internet → ISP → Your Network

During attack:
  Internet → ISP → Scrubbing Center → Clean traffic → Your Network
                        │
                   Attack traffic dropped
```

Traffic diversion is typically triggered in two ways:
- **On-demand:** You contact the ISP when an attack is detected. Manual process, response time depends on the provider.
- **Always-on:** Traffic is continuously routed through scrubbing. No detection delay, but adds latency.

### What ISP Scrubbing Protects Against

ISP scrubbing is designed specifically for **volumetric attacks**. It operates at the network layer, upstream of your infrastructure. An attack that would saturate your 10 Gbps link is absorbed by the provider's 10 Tbps+ capacity before it reaches you.

Major scrubbing providers (Telia, Lumen, GTT, Zayo, and others) operate globally distributed scrubbing centers with aggregate capacities in the tens of Tbps.

### What ISP Scrubbing Does Not Do

- **Layer 7 protection:** ISP scrubbing operates at L3/L4. It cannot analyze HTTP request content. A sophisticated application-layer attack using legitimate-looking HTTP traffic will pass through scrubbing untouched.
- **Low-and-slow attacks:** Slowloris, RUDY, and SSL exhaustion are not volumetric — they don't trigger volume-based scrubbing activation.
- **Instant response:** On-demand scrubbing has an activation delay — typically 15–30 minutes while traffic is diverted. During this window, the attack continues unmitigated.

### When ISP Scrubbing Makes Sense

- Your primary threat is volumetric attacks (the most common type targeting infrastructure)
- Your ISP link is 10 Gbps or less (almost any volumetric attack exceeds this)
- You have regulatory requirements for DDoS protection but cannot justify hardware costs
- You want a cost-effective baseline protection layer

**Cost model:** Typically a monthly retainer plus per-GB or per-event fees during active mitigation. Generally more cost-effective than on-premise hardware for pure volumetric protection.

---

## 2. On-Premise DDoS Appliances

### How It Works

A dedicated hardware device (or virtual appliance) sits inline in your network, upstream of your firewall:

```
Internet → [ISP Router] → [DDoS Appliance] → [NGFW] → Internal Network
```

The appliance analyzes all traffic in real time and drops attack packets before they reach your firewall or servers. Unlike software-based solutions, purpose-built DDoS appliances use **FPGA (Field Programmable Gate Array)** hardware for packet processing — enabling line-rate analysis at 40–100 Gbps without impacting legitimate traffic.

### Leading On-Premise Solutions

**NETSCOUT Arbor (Peakflow / Sightline / TMS)**
The dominant enterprise solution, particularly in banking and telco. Arbor is widely considered the industry standard for on-premise DDoS protection. The platform combines:
- **Sightline:** Traffic analysis and attack detection using flow data (NetFlow, sFlow, IPFIX) and BGP
- **Threat Mitigation System (TMS):** Hardware-based scrubbing appliance deployed inline or out-of-band
- Integration with Arbor's global threat intelligence network (ATLAS)

**Radware DefensePro**
Strong in financial services. Features behavioral-based detection that creates a dynamic baseline of normal traffic and detects anomalies — effective against zero-day DDoS attacks that don't match known signatures.

**Fortinet FortiDDoS**
Integrated with the Fortinet ecosystem. Suitable for organizations already running FortiGate firewalls who want consistent management.

**F5 BIG-IP AFM (Advanced Firewall Manager)**
As discussed in the F5 series — AFM provides DDoS mitigation capabilities as part of the BIG-IP platform. Most suitable for environments already running F5 for application delivery, where adding DDoS protection to existing hardware is cost-effective.

### What On-Premise Appliances Protect Against

- **Protocol attacks:** SYN floods, fragmented packets, malformed headers — handled at hardware speed before reaching the firewall
- **Application layer attacks:** Advanced appliances with behavioral analysis can detect and mitigate HTTP floods, Slowloris, and SSL exhaustion
- **Zero-day behavioral attacks:** Rate-based and behavioral detection identifies attack patterns without requiring known signatures

### What On-Premise Cannot Do

**Volumetric attacks that exceed your ISP link:** An on-premise appliance at your data center cannot help when 500 Gbps of attack traffic is filling your 10 Gbps internet connection. The attack wins before a single packet reaches your appliance. This is the fundamental limitation.

This is why on-premise appliances and ISP scrubbing are **complementary, not competing** solutions.

### When On-Premise Makes Sense

- You need protection against protocol and application-layer attacks
- You have regulatory requirements for on-premise traffic inspection
- You're already running F5 or FortiGate and can leverage existing hardware
- You need granular visibility into attack traffic for forensics and compliance reporting
- Your internet link is large enough (100 Gbps+) that pure volumetric attacks are less of a risk

---

## 3. Cloud DDoS Protection Services

### How It Works

Cloud DDoS protection routes all your traffic through the provider's globally distributed network. Clean traffic is delivered to your origin servers; attack traffic is dropped at the edge:

```
Without cloud protection:
  User → Internet → Your Server

With cloud protection:
  User → [Cloudflare / Akamai / AWS edge] → Your Server
                    │
             Attack traffic dropped
             at the network edge
```

Traffic routing is typically achieved through:
- **DNS change:** Point your domain's DNS to the cloud provider's anycast network
- **BGP announcement:** The provider announces your IP prefixes from their network

### Leading Cloud Solutions

**Cloudflare**
The most widely known cloud DDoS provider. Cloudflare operates one of the world's largest anycast networks — 300+ PoPs globally, with aggregate capacity exceeding 230 Tbps. Key capabilities:
- Automatic DDoS mitigation without manual intervention
- Layer 3, 4, and 7 protection in a single platform
- WAF integration — application security and DDoS mitigation from the same provider
- Magic Transit for infrastructure-level protection (BGP-based, not just HTTP)
- Unmetered DDoS mitigation — no per-GB charges during attacks

**AWS Shield**
- **Shield Standard:** Automatically included for all AWS resources. Protects against common L3/L4 attacks.
- **Shield Advanced:** Paid tier with L7 protection, 24/7 DDoS Response Team access, cost protection (AWS credits for scaling costs during attacks), and integration with AWS WAF.
- Best suited for organizations with significant AWS infrastructure.

**Akamai Prolexic**
Enterprise-focused cloud scrubbing platform. Operates 20+ globally distributed scrubbing centers. Strong track record in financial services and media. Prolexic Routed provides always-on BGP-based protection for infrastructure (not just web applications).

**Azure DDoS Protection**
Microsoft's offering for Azure-hosted resources. Standard tier provides adaptive tuning, attack telemetry, and rapid response support. Most relevant for organizations running significant workloads in Azure.

### What Cloud Protection Covers

- **Volumetric attacks at any scale:** Cloud providers have multi-Tbps capacity at globally distributed edge locations. An attack that overwhelms ISP scrubbing capacity is distributed across hundreds of PoPs.
- **Application layer attacks:** Providers like Cloudflare combine DDoS mitigation with WAF, bot management, and rate limiting at the edge.
- **Always-on without configuration changes:** Once traffic is routed through the provider, protection is continuous with no activation delay.

### What Cloud Protection Adds

- **Latency:** All traffic passes through the provider's network. For most web applications, the latency added by edge PoPs is negligible or negative (edge caching actually reduces latency). For latency-sensitive applications (trading platforms, real-time communications), evaluate carefully.
- **Privacy/compliance considerations:** All traffic, including SSL-decrypted content, passes through the provider's infrastructure. In regulated industries (banking, healthcare), this requires careful review of the provider's data processing agreements.
- **DNS dependency:** DNS-based cloud protection can be bypassed if attackers discover your origin IP and attack it directly. Protect origin IPs carefully — restrict access at the firewall level to only the cloud provider's IP ranges.

### When Cloud Protection Makes Sense

- Your application is internet-facing and must remain available during large-scale volumetric attacks
- You want always-on protection without hardware investment
- You're already using cloud infrastructure (AWS, Azure) and want integrated protection
- You need global distribution to protect against geographically distributed attacks

---

## Comparing the Three Approaches

| | ISP Scrubbing | On-Premise Appliance | Cloud Service |
|---|---|---|---|
| Volumetric protection | ✅ | ❌ (limited by link) | ✅✅ |
| Protocol attack protection | ✅ | ✅✅ | ✅ |
| Application layer (L7) | ❌ | ✅ (advanced models) | ✅✅ |
| Activation time | Minutes (on-demand) | Immediate | Immediate |
| Traffic visibility | Limited | Full | Provider-dependent |
| Compliance / data residency | ✅ | ✅✅ | Requires review |
| CapEx | Low | High | None |
| OpEx | Medium | Medium | Medium–High |
| Scalability | ISP capacity | Fixed hardware | Near-unlimited |

---

## The Hybrid Model: How Serious Organizations Combine All Three

In high-risk environments — banking, payment processors, government infrastructure, large e-commerce — a single protection layer is never sufficient. The standard architecture combines all three:

```
Attack traffic
      │
      ▼
[Cloud / ISP Scrubbing]      ← Absorbs volumetric floods before they reach you
      │
   Clean(er) traffic
      │
      ▼
[On-Premise Appliance]       ← Catches protocol attacks and L7 anomalies
      │
      ▼
[NGFW + WAF]                 ← Application security and policy enforcement
      │
      ▼
[Application Servers]
```

**Layer 1 — Cloud or ISP scrubbing:** Absorbs volumetric attacks at scale. The upstream layer handles what on-premise hardware physically cannot.

**Layer 2 — On-premise appliance:** Catches protocol attacks and application-layer anomalies that slipped through scrubbing. Provides detailed forensic visibility for compliance and incident response.

**Layer 3 — NGFW + WAF:** Handles application security, policy enforcement, and the most sophisticated L7 attacks targeting specific application logic.

Each layer handles what the others cannot. The combination creates defense-in-depth that is resilient to the full spectrum of DDoS attack types.

### Real-World Example: Banking Sector

In the banking environment I worked in, the DDoS protection stack was:

- **Arbor TMS** on-premise — inline scrubbing for protocol attacks, real-time flow analysis for anomaly detection, integration with BGP for automated traffic diversion
- **ISP scrubbing contract** — activated when Arbor detected volumetric attack signatures that would saturate the uplink
- **Cloudflare Magic Transit** — for public-facing web applications, providing always-on cloud-level protection with WAF integration
- **F5 AFM** — additional L4 protection on the application delivery tier

This wasn't redundancy for its own sake — each layer handled attack types the others couldn't.

---

## DDoS Response Planning: The Non-Technical Part

Technology is only part of DDoS readiness. The other part is organizational:

**Runbooks:** Document exactly what to do when an attack starts. Who gets notified? Who activates ISP scrubbing? What's the escalation path? Under attack is the wrong time to figure this out.

**Contact lists:** ISP scrubbing activation, cloud provider support, upstream router access, on-call network engineers. All current, all tested.

**Thresholds and automation:** Define when automated mitigation activates vs. when human review is required. Fully manual responses are too slow for modern attack rates.

**Regular testing:** A DDoS protection stack that has never been tested is a DDoS protection stack you don't actually trust. Schedule periodic tests with your ISP and cloud provider.

**Post-incident review:** After every significant attack, review what worked, what didn't, and what the attack traffic looked like. DDoS tactics evolve — your protection strategy should too.

---

## Key Takeaways

- DDoS attacks come in three fundamentally different types — volumetric, protocol, and application layer — and each requires different mitigation.
- **No single protection layer covers all attack types.** Volumetric attacks require upstream scrubbing capacity; protocol attacks need hardware-speed packet processing; L7 attacks require application-aware analysis.
- **ISP scrubbing** is the only option for very large volumetric attacks — the attack must be absorbed before it reaches your link.
- **On-premise appliances** (Arbor, Radware, F5 AFM) provide granular visibility, compliance-friendly on-site processing, and effective protocol/L7 protection — but cannot handle attacks that exceed your ISP link capacity.
- **Cloud services** (Cloudflare, AWS Shield, Akamai) offer massive scale, global distribution, and always-on protection with no hardware investment — but introduce traffic routing through third-party infrastructure.
- In high-risk environments, all three layers work together. This isn't over-engineering — it's the architecture that serious organizations use in practice.

---

## Related Articles

- 🛡️ [F5 BIG-IP Platform Overview](/en/technology/f5-bigip-application-delivery-platform-overview/) — F5 AFM as part of DDoS defense in depth
- 🔐 [The Zero Trust Mindset: Engineering Security as an Architecture](/en/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — DDoS protection within a Zero Trust framework
- 🛡️ [Network Packet Broker (NPB) Masterclass](/en/posts/network-packet-broker-masterclass/) — Traffic visibility essential for DDoS forensics
- 📊 [Monitoring Done Right](/en/architecture/monitoring-not-just-seeing/) — Detecting DDoS early through proactive monitoring
