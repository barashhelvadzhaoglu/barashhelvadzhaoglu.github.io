---
title: "Firewall Selection and Capacity Planning: What the Datasheets Don't Tell You"
description: "Enterprise firewall selection — throughput reality, SSL inspection impact, and vendor trade-offs across Fortinet, Palo Alto, Cisco, and Check Point."
date: 2026-04-06
draft: false

cover:
  image: "/img/postimages/firewall-selection-capacity-cover.webp"
  alt: "Enterprise Firewall Selection and Capacity Planning"
  relative: false

tags: ["Firewall", "NGFW", "Fortinet", "Palo Alto", "Cisco Firepower", "Check Point", "Network Security", "Capacity Planning", "SSL Inspection"]
categories: ["Technology"]
keywords:
  - enterprise firewall selection guide
  - firewall capacity planning
  - Fortinet vs Palo Alto vs Cisco vs Check Point
  - NGFW SSL inspection throughput
  - firewall throughput real world
  - enterprise firewall comparison
  - Palo Alto App-ID architecture
  - Fortinet FortiGate high throughput
  - Cisco Firepower IPS
  - Check Point firewall management

showToc: true
TocOpen: true
---

# Firewall Selection and Capacity Planning: What the Datasheets Don't Tell You

Firewall selection conversations usually go one of two ways. Either the decision is made based on brand familiarity — "we've always used vendor X" — or it's made based on datasheet throughput numbers without understanding what those numbers actually mean in production. Both approaches lead to either overpaying for capacity you won't use or undersizing for the traffic you'll actually run.

After deploying hundreds of Fortinet firewalls across banking and manufacturing environments, and working extensively with Palo Alto and Cisco in production infrastructure, I want to share what the selection process actually looks like when you're responsible for the result — not just the recommendation.

 For the architectural context behind firewall placement decisions, see: [Switch, Firewall, AP — Why Choosing the Right Products Is Not Enough](/en/architecture/core-network-is-not-a-product-list/)

---

## The Number That Misleads Everyone: Firewall Throughput

Every firewall datasheet leads with a throughput number. 10 Gbps. 40 Gbps. 100 Gbps. These numbers are real — in the specific conditions under which they were measured.

Those conditions are not your production environment.

Datasheet throughput is typically measured with:
- Large packet sizes (1518 bytes) — real traffic mixes in much smaller packets
- No security features enabled — no IPS, no application control, no SSL inspection
- Synthetic test traffic — not the mixed, bursty, irregular traffic of a real network

What actually consumes firewall capacity in production:

**PPS (Packets Per Second):** Small packets are more expensive than large packets. A firewall moving 1 Gbps of 64-byte packets processes roughly 20× more packets per second than 1 Gbps of 1500-byte packets. Environments with high transaction rates (banking, trading, database replication) stress PPS limits long before bandwidth limits.

**Concurrent Sessions:** Every tracked connection occupies memory in the state table. A firewall with 2 million concurrent session capacity does not mean "2 million users" — a single user can have dozens of sessions open simultaneously. High-concurrency environments (web servers behind the firewall, database clusters, microservices architectures) exhaust session tables faster than bandwidth.

**New Session Rate:** How many new connections per second the firewall can establish. Under SYN flood conditions or during peak traffic periods, new session rate becomes the binding constraint.

**SSL/TLS Inspection:** This is where most capacity planning goes wrong. When SSL inspection is enabled — decrypting HTTPS traffic, inspecting it, re-encrypting it — throughput drops significantly on most platforms. The degree of impact varies by vendor and model.

---

## The SSL Inspection Reality

The majority of enterprise traffic today is HTTPS. If your firewall is not inspecting SSL, it is not inspecting most of your traffic. But enabling SSL inspection has a direct, significant performance cost.

A firewall marketed at 10 Gbps throughput might deliver 2–4 Gbps with full SSL inspection enabled, depending on the platform. This is not a bug or a vendor shortcoming — SSL decryption is computationally expensive, and hardware SSL acceleration (available on higher-end models) is what separates entry-level from mid-range platforms in practice.

**The calculation that matters:**

When sizing a firewall, the question is not "how much bandwidth do I have?" but "how much of that bandwidth will be SSL-inspected?" For most organizations:
- Internet-bound traffic: nearly 100% HTTPS → all SSL inspected
- Internal segmentation traffic: mix of encrypted and unencrypted application traffic
- Server-to-server traffic: increasingly TLS for compliance reasons

If you have 2 Gbps of internet bandwidth and plan to inspect all of it, size the firewall for 2 Gbps of SSL inspection throughput — not 2 Gbps of raw throughput. These are often very different numbers.

---

## Multi-Firewall Architecture: One Size Does Not Fit All

In many production environments, a single firewall handling all roles is a design compromise rather than a design choice. Different traffic types have different requirements:

```
Internet Edge Firewall:
  → High SSL inspection throughput (most traffic is HTTPS)
  → VPN termination capacity
  → IPS for internet-sourced threats
  → Moderate session count

Internal Segmentation Firewall (East-West):
  → High PPS (internal traffic is often small packets)
  → Very high concurrent session count
  → Lower SSL inspection requirements (internal traffic often unencrypted)
  → High new session rate

Data Center / Server Firewall:
  → Extreme session counts (servers have many concurrent connections)
  → Low latency (application performance sensitive)
  → High throughput for bulk data transfers
  → IPS tuned for server-side exploits
```

Using the same firewall model for all three roles means compromising on at least one. The internet edge firewall optimized for SSL inspection is often wrong for east-west segmentation. The high-session-count DC firewall is often over-engineered for a branch office.

This is not theoretical — I've seen networks where the internet edge firewall was saturating at 30% of its rated throughput because the session count limit was reached, while the DC firewall had plenty of throughput headroom but was dropping packets due to PPS limits.

---

## Vendor Field Notes

What follows is based on direct production experience. These are operational observations, not benchmark comparisons. Vendor capabilities evolve with software releases and new hardware generations — validate current specifications for any active project.

### Fortinet FortiGate

Fortinet is where most of my production firewall experience is concentrated — across small branch deployments, banking headquarters, and large manufacturing environments.

**Where FortiGate genuinely excels:**

High-throughput environments with moderate security inspection requirements. Fortinet's custom NP (Network Processor) and CP (Content Processor) ASICs offload specific functions to hardware — packet processing, IPsec VPN, and some inspection tasks run on dedicated silicon rather than general-purpose CPUs. At high bandwidth, this hardware acceleration makes a meaningful difference.

For environments needing to move large volumes of traffic — server-to-server, large file transfers, high-bandwidth branch connectivity — FortiGate delivers throughput that software-based architectures struggle to match at equivalent price points.

The Fortinet Security Fabric is a genuine operational advantage for organizations running FortiGate alongside FortiSwitch, FortiAP, FortiAnalyzer, and FortiManager. Policy, logging, and management are unified in a way that reduces the integration work that multi-vendor environments require.

**Where FortiGate has limitations:**

Deep inspection at scale. When IPS, application control, SSL inspection, and antivirus are all enabled simultaneously on high-traffic links, throughput can drop substantially compared to the headline numbers. Fortinet publishes "threat protection" throughput figures that reflect this — but these numbers are still often optimistic compared to what you'll see with your specific traffic mix and full feature activation.

For environments where the primary requirement is maximum inspection depth with minimum performance compromise — high-security environments inspecting all traffic including encrypted internal communications — the capacity math can work against FortiGate at mid-range model tiers.

**Hardware generation update (2024–2025):** Fortinet's newer appliance series have improved SSL inspection capacity significantly. The FortiGate 700G series, validated by Keysight in 2025, achieves up to 14 Gbps of SSL deep inspection throughput — a meaningful improvement over equivalent mid-range models from earlier generations. Cisco, Palo Alto, and others have similarly released hardware with improved SSL inspection capacity. When sizing, always use the datasheet figures for the specific model and generation you're evaluating, not generic estimates.

**Practical guidance:** When sizing FortiGate for full SSL inspection deployments, I use 20–30% of the SSL inspection throughput figure from the datasheet as my working estimate for production traffic. This sounds conservative, but it accounts for traffic mix, concurrent connections, and logging overhead. If the math works at that figure, you have appropriate headroom.

---

### Palo Alto Networks

Palo Alto's architecture is fundamentally different from traditional firewalls, and understanding this is essential for both appreciating its strengths and planning for its constraints.

**The App-ID architecture:**

Palo Alto identifies traffic by application before deciding what to do with it. Every session is analyzed to determine what application it represents — not just what port it uses. HTTP on port 80, port 8080, or a custom port is all identified as the specific application running on it.

This is architecturally powerful for security: policy is based on "allow Salesforce from the sales team" rather than "allow TCP 443 from subnet X." Unknown applications — traffic that doesn't match any known application signature — are treated as potentially suspicious by default. You must explicitly permit unrecognized traffic if you want it to pass.

**The security advantage this creates:**

In environments where the threat model requires full application visibility — financial services, regulated industries, environments with strict compliance requirements — Palo Alto's approach creates genuine security depth. The policy model forces explicit decisions about every traffic type. Nothing passes unexamined. For security-focused organizations with mature security teams, this is a significant advantage.

**The operational trade-off:**

The same architecture that makes Palo Alto powerful in security-focused environments creates friction in others. Unknown or unusual applications require investigation and explicit policy decisions. For organizations without dedicated security teams or for environments with diverse, evolving application sets, the operational overhead of maintaining an application-based policy model can be significant.

For small and medium organizations, or for environments where the primary requirement is connectivity with reasonable security rather than maximum security depth, this trade-off may not be worth it. The operational model assumes a level of security maturity that not every organization has.

**Panorama:**

Centralized management of Palo Alto firewalls through Panorama is substantially more capable than managing individual devices. For multi-firewall environments, Panorama is effectively required to operate Palo Alto at scale. The management overhead without Panorama is disproportionate relative to the alternatives.

**SASE leadership (2025 update):** Palo Alto's cloud security platform (Prisma SASE) has become one of their strongest growth areas — named Gartner SASE Leader three consecutive years through 2025, with $1.3 billion ARR growing at 35% year-over-year. For organizations moving toward cloud-delivered security and hybrid workforce models, Palo Alto's SASE offering is among the most mature in the market. This doesn't change the on-premise firewall evaluation, but it's relevant if your organization is evaluating a broader security platform rather than just a perimeter firewall.

---

### Cisco Firepower (Now Cisco Secure Firewall)

Cisco's NGFW story has a history worth understanding. The original ASA (Adaptive Security Appliance) was a strong stateful firewall — reliable, widely deployed, but limited in next-generation capabilities. Cisco's response was to acquire Sourcefire, whose IPS technology (Snort-based) was and remains genuinely strong, and build the Firepower platform on top of the ASA architecture.

**Where Firepower is strong:**

The IPS capability is real. Sourcefire's threat intelligence and detection, now Cisco Talos (one of the largest threat intelligence organizations in the world), powers Firepower's IPS with a detection quality that is broadly respected. For environments where IPS is the primary security requirement, Cisco brings serious capability.

Integration with Cisco's broader ecosystem — ISE, Umbrella, Stealthwatch (now Secure Network Analytics), SecureX — is increasingly coherent and has improved substantially in recent years.

**The management challenge:**

Cisco Firepower has historically been criticized for management complexity. Running Firepower without Firepower Management Center (FMC) means accepting significant limitations on visibility and policy management. FMC itself has a learning curve that is steeper than the alternatives. For teams without Cisco-specific expertise, the ramp-up time is real.

The platform has matured significantly, and Cisco has invested heavily in improving the management experience. In 2024, Cisco rebranded Cisco Defense Orchestrator as **Security Cloud Control** — an AI-embedded cloud management platform that unifies FMC, ASA, and other Cisco security products under one interface. It now includes an AI Assistant for policy rule creation, AIOps insights for proactive recommendations, and cloud-delivered FMC that reduces the on-premise infrastructure burden. This is a meaningful improvement over the older FMC-only model. Teams coming from simpler firewall platforms will still face an adjustment period, but the gap has narrowed compared to a few years ago.

**Architecture context:**

Cisco tends to be strongest in environments already deeply invested in the Cisco ecosystem — where ISE provides identity, Catalyst provides switching, and the DNA Center / Catalyst Center provides centralized management. In those environments, Firepower fits coherently. In multi-vendor environments, the integration story is more work.

---

### Check Point

Check Point is one of the original enterprise firewall vendors — the company that made firewall technology mainstream in the 1990s. Their architecture reflects that heritage: mature, security-focused, and built around an operating system (Gaia, based on Linux) that gives administrators significant control but requires corresponding expertise.

**Where Check Point is strong:**

Security policy depth and inspection quality. Check Point's policy model is granular, and their inspection capabilities are mature. In environments where security policy complexity is high — many rules, many exceptions, detailed logging requirements — Check Point's management infrastructure (SmartConsole, management server, log server separation) handles scale well.

For organizations with security operations teams who know the platform, Check Point is a capable and well-regarded choice.

**The operational reality:**

Check Point's management model is different from other vendors. Management is separated from enforcement — the management server, the Security Management Server (SMS), is distinct from the enforcement gateways. Understanding and working with this separation, the policy installation process, and the underlying Gaia OS requires genuine expertise.

From a network engineer's perspective, Check Point is not the most operationally transparent platform. Familiarity with Linux administration helps significantly. Policy management without a solid understanding of the object model and rule base structure leads to complexity that compounds over time.

The security policy model can become difficult to maintain as rule bases grow without disciplined hygiene. This is true of all firewalls, but Check Point's complexity means the technical debt accumulates faster when rule management discipline is absent.

---

## HA Architecture: Active-Standby vs Active-Active

Enterprise firewall deployments require high availability. The two models have different characteristics:

**Active-Standby:**
- One firewall handles all traffic; the standby monitors and takes over on failure
- Session state is synchronized to standby — failover is transparent to established connections
- Simpler to troubleshoot — all traffic through one device at any time
- Wastes 50% of hardware capacity in normal operation
- Standard choice for most enterprise edge deployments

**Active-Active:**
- Both firewalls handle traffic simultaneously, typically for different traffic flows or zones
- More complex to configure and troubleshoot — asymmetric routing must be avoided
- Utilizes both devices, but complicates state synchronization
- More appropriate for very high throughput requirements where one device is insufficient
- Requires careful traffic engineering — asymmetric flows (request through FW-1, response through FW-2) cause session drops

In practice, Active-Standby is the right choice for the majority of enterprise deployments. The throughput benefit of Active-Active doesn't justify the operational complexity unless you genuinely need more throughput than one device can provide with HA overhead accounted for.

---

## Policy Hygiene: The Problem That Builds Slowly

Firewall capacity is not only a hardware question. Firewall performance degrades as rule base complexity increases — particularly when rule bases grow without regular cleanup.

A rule base with 5,000 rules where most traffic matches in the first 50 rules performs very differently from a 5,000-rule base where traffic is distributed across hundreds of rules. Every packet traverses the rule base from top to bottom until it matches — or reaches the implicit deny.

**What rule hygiene means in practice:**

- Rules that are never matched (shadow rules, obsolete rules) should be identified and removed quarterly
- High-traffic rules should be positioned near the top of the rule base
- Overly broad rules (any/any permits with logging disabled) should be documented and reviewed
- Application-specific rules should replace port-based rules where the platform supports it

FortiManager, Panorama, and FMC all have rule usage statistics and shadow rule detection. Using these tools is part of responsible firewall operations — not a periodic cleanup exercise.

---

## Capacity Planning: The Practical Framework

When sizing a firewall, work through these metrics in order:

**1. Baseline traffic characterization**
- What is current peak bandwidth (not average)?
- What percentage is SSL/HTTPS?
- What is the concurrent session count at peak?
- What is the new session rate at peak?

**2. Growth projection**
- Add 40–50% headroom over expected peak for 3-year lifecycle
- Account for new applications and services that will be added

**3. Feature impact**
- Which security features will be enabled? (IPS, SSL inspection, App-ID, AV)
- Use vendor "threat protection" throughput figures, not raw throughput
- For SSL inspection specifically: validate with vendor sizing tools using your estimated HTTPS percentage

**4. HA overhead**
- Active-Standby: size each unit for 100% of traffic (standby must be able to handle full load)
- Do not plan to use standby capacity — it must be available for failover

**5. Management and logging**
- High logging rates consume CPU on the firewall itself
- External log management (FortiAnalyzer, Panorama, FMC) is not optional at scale

A simple sizing example:
```
Environment:
  Peak bandwidth: 2 Gbps
  SSL percentage: 80% (1.6 Gbps HTTPS)
  IPS + App-ID + SSL inspection: all enabled
  3-year growth headroom: 50%

Required SSL inspection throughput:
  1.6 Gbps × 1.5 (growth) = 2.4 Gbps

Select a model rated for ≥ 2.4 Gbps SSL inspection throughput
(not 2.4 Gbps raw throughput)
```

---

## Key Takeaways

- **Datasheet throughput is not production throughput.** SSL inspection, IPS, and application control reduce effective throughput significantly. Size based on threat protection or SSL inspection figures, not raw numbers.
- **SSL inspection capacity is the binding constraint** for most internet edge deployments. The majority of traffic is HTTPS, and inspecting it is expensive.
- **Fortinet** excels at high-throughput environments where hardware acceleration matters. Full deep inspection at scale requires careful model selection — throughput drops substantially with all features enabled.
- **Palo Alto** provides the deepest application visibility and most rigorous policy model. The architecture is powerful for security-mature organizations; it adds operational overhead for those without dedicated security teams. Panorama is effectively required for multi-device management.
- **Cisco Firepower** brings strong IPS (Talos intelligence) and Cisco ecosystem integration. Management complexity is real — FMC is required to realize the platform's value.
- **Check Point** is mature and security-focused with deep policy control. Requires Linux/Gaia OS familiarity and disciplined rule base management to operate effectively.
- **Multi-firewall architecture** — different firewalls for edge, internal segmentation, and DC — is often the right answer rather than one platform for everything.
- **Rule hygiene** is a performance and security issue, not just housekeeping. Neglected rule bases degrade both.

---

## Related Articles

- 🏗️ [Switch, Firewall, AP — Why Choosing the Right Products Is Not Enough](/en/architecture/core-network-is-not-a-product-list/) — Architectural context for firewall placement
- 🔐 [The Zero Trust Mindset: Engineering Security as an Architecture](/en/architecture/zero-trust-mindset-engineering-security-as-an-architecture-not-a-product/) — Policy philosophy behind firewall design
- 🛡️ [DDoS Protection Strategies](/en/technology/ddos-protection-strategies-isp-scrubbing-on-premise-cloud/) — What sits upstream of the firewall
- 🛡️ [F5 WAF Deep Dive](/en/technology/f5-waf-asm-advanced-waf-application-security/) — Layer 7 protection that complements firewall policy
- 📊 [Monitoring Done Right](/en/architecture/monitoring-not-just-seeing/) — Making firewall behavior visible
