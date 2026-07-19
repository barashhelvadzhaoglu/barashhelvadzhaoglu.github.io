---
title: "IT Security Obligations for Small Businesses in Bavaria — and How Digitalbonus Bayern Covers Up to 50% of the Costs"
seoTitle: "GDPR IT Security SME Bavaria | Digitalbonus 2026 — Firewall, VLAN, Backup, Email"
description: "Which IT security measures are legally required in Bavaria? Firewall, network separation, email protection, backup — with legal references and grants up to €7,500."
date: 2026-04-17
draft: false
showToc: true
TocOpen: false
tags:
  - Digitalbonus Bayern
  - GDPR
  - BSI IT-Grundschutz
  - Network Security
  - IT Security
  - SME Munich
keywords:
  - Digitalbonus Bayern 2026
  - GDPR IT Security Obligation
  - BSI IT-Grundschutz SME
  - Firewall obligation small businesses
  - VLAN separation GDPR
  - Network segmentation Bavaria
  - Email security GDPR
  - Backup obligation companies
  - IT funding Bavaria 2026
---

# IT Security Obligations for Small Businesses — and How Digitalbonus Bayern Covers Up to 50%

Many small businesses in Bavaria believe that IT security is a topic for large corporations. The reality is different: The GDPR applies to **everyone** who processes personal data — from retailers and medical practices to hotels. And the requirements are concrete, binding, and enforced with fines.

The good news: The **Digitalbonus Bayern** reimburses up to **50% of the investment costs** — for firewalls, network separation, email security, backup, and more. The program runs until December 2027.

> 💬 **Free IT Analysis:** [WhatsApp](https://wa.me/4916098665971) or [Email](mailto:info@barashhelvadzhaoglu.com)
> We check your infrastructure free of charge — no contract, no product sales.

---

## The Legal Basis: What is Actually Mandatory?

### GDPR Article 32 — Security of Processing

**Source:** [Art. 32 GDPR](https://gdpr.eu/article-32-security-of-processing/)

> „The controller and the processor shall implement appropriate technical and organisational measures to ensure a level of security appropriate to the risk."

This means: Every company that processes personal data — i.e., names, email addresses, health data, booking information — must set up **technical protection measures**. Not as a recommendation, but as a **legal obligation**.

### BSI IT-Grundschutz — The Technical Standard

**Source:** [BSI IT-Grundschutz Compendium](https://www.bsi.bund.de/grundschutz)

The Federal Office for Information Security (BSI) defines in the IT-Grundschutz specifically what "appropriate technical measures" mean in the sense of the GDPR. German courts and data protection authorities use this standard as a guide during audits.

**Does BSI IT-Grundschutz apply to small businesses?**
Formally, it is voluntary — but: The GDPR prescribes the "state of the art." In Germany, this corresponds to the BSI IT-Grundschutz. Those who do not comply may have to prove during an audit why their alternative measures are equivalent.

---

## What is Specifically Required — Measure by Measure

### 1. Firewall — Mandatory according to BSI NET.3.2

**Legal Basis:** BSI IT-Grundschutz, Building Block [NET.3.2 Firewall](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/Kompendium/Bausteine/Infrastruktur/NET_3_2_Firewall.pdf)

BSI NET.3.2.A2 stipulates:
> „A rule set for the firewall must be created. No data traffic may automatically pass from the external to the internal network."

BSI NET.3.2.A9 adds:
> „The firewall must log all important events."

**What this means in practice:**
- A simple DSL router is **not** a firewall in the sense of the BSI.
- A UTM firewall (e.g., Fortinet FortiGate, Palo Alto) is required.
- The firewall must sit between **all** network zones — not just between the internet and the internal network.

**Eligible for Digitalbonus:** ✅ Yes — Hardware and configuration services.

---

### 2. Network Segmentation (VLANs) — Mandatory according to BSI NET.1.1 and GDPR Art. 25

**Legal Basis:**
- BSI IT-Grundschutz, Building Block [NET.1.1 Network Architecture and Design](https://www.bsi.bund.de/grundschutz)
- GDPR Art. 25 — Data protection by design and by default (Privacy by Design)

> „Personal data must be processed in such a way that only persons who need it for their tasks have access."

**What this means in practice:**

The following device classes must be operated in **separate networks (VLANs)**:

| Network Segment | What belongs in it | Risk without separation |
|---|---|---|
| **Employee Net** | PCs, Laptops | Access to customer data |
| **Server / NAS** | File server, Backup system | Data loss during attack |
| **IoT Devices** | Printers, IP Cameras, Smart TV, UPS | Known security gaps, no updates |
| **Guest WLAN** | Customers, Patients, Hotel guests | Access to internal systems |
| **POS / Checkout** | Card terminal, Checkout system | PCI DSS obligation, payment data |

**Why printers are dangerous:**
IP printers often have outdated firmware and no automatic security updates. A compromised printer on the same network as the accounting PC gives attackers direct access to all data.

**Why IP cameras are dangerous:**
Cheap IP cameras (Hikvision, Dahua) are regularly misused in international hacker attacks — as an entry point into the company network.

**Eligible for Digitalbonus:** ✅ Yes — Managed switches, Access Points, configuration services.

---

### 3. Guest WLAN with Captive Portal and Log Storage

**Legal Basis:**
- GDPR Art. 32 — Technical protection measures
- § 100 TKG (Telecommunications Act) — Traffic data
- BSI IT-Grundschutz NET.2.2 — WLAN usage

**What is required:**

**a) Complete Isolation:**
The guest WLAN must have **no** access to internal systems. A hotel guest or patient in the waiting room must not be able to access booking systems, printers, or employee files.

**b) Connection Logs — 12-month storage obligation:**
Anyone offering public WLAN must keep connection data (IP address, connection time, connection duration) for **12 months** — for possible official inquiries.

**c) Captive Portal with GDPR Consent:**
Upon login, the guest must be informed about data processing and actively consent.

**Technical Implementation:**
The connection logs are captured by the firewall (e.g., FortiGate) and automatically transferred to a NAS device — stored there for 12 months.

**Eligible for Digitalbonus:** ✅ Yes — WLAN hardware and configuration.

---

### 4. Email Security — Mandatory according to BSI APP.5.3 and GDPR Art. 32

**Legal Basis:**
- BSI IT-Grundschutz, Building Block [APP.5.3 General Email Client and Server](https://www.bsi.bund.de/grundschutz)
- GDPR Art. 32 — Protection against unauthorized access and data loss

BSI APP.5.3.A1 stipulates:
> „Protective measures must be taken against malware in emails. Incoming and outgoing emails must be checked for malware."

**What this means in practice:**
A simple email mailbox at Ionos or Strato without additional protection is **not sufficient**.

What is required:
- **Spam Filtering:** Blocking of unsolicited bulk emails.
- **Malware Protection:** Detection of harmful attachments (Ransomware, Trojans).
- **Phishing Protection:** Detection of forged sender addresses (Business Email Compromise).
- **Logging:** Proof of all filtered emails.

**Technical Solution:**
A cloud-based Email Security Gateway (e.g., Hornetsecurity, FortiMail Cloud) routes all incoming emails through a security filter before they reach the recipient. Works with any existing email system — Office 365, Google Workspace, or simple webmail.

**Eligible for Digitalbonus:** ✅ Yes — as an IT security software license (up to 18 months).

---

### 5. Endpoint Protection (Antivirus / EDR) — Mandatory according to BSI SYS.2.1 and GDPR Art. 32

**Legal Basis:**
- BSI IT-Grundschutz, Building Block [SYS.2.1 General Client](https://www.bsi.bund.de/grundschutz)
- GDPR Art. 32 — Protection against data loss through malware

BSI SYS.2.1.A6 stipulates:
> „A virus protection program must be installed and activated on clients. The virus protection program must be updated regularly."

BSI SYS.2.1.A7 adds:
> „Security-relevant events must be logged and checked for anomalies."

**What this means in practice:**

A single antivirus program on each PC — without central management — does **not** comply with the BSI standard. What is required:

- **Central Management:** An administrator sees the protection status of all devices at a glance.
- **Real-time Protection:** Threats are detected before they cause damage.
- **Ransomware Protection:** File encryption by malware is blocked.
- **Logging:** All security events are recorded — for potential audits.
- **Monthly Reports:** Proof of active protective measures.

**Technical Solution:**
Centrally managed EDR solutions like Bitdefender GravityZone or ESET Protect enable the management of all devices via a central dashboard.

**Eligible for Digitalbonus:** ✅ Yes — Software licenses and setup services.

---

### 6. Data Backup — Mandatory according to BSI CON.3 and GoBD

**Legal Basis:**
- BSI IT-Grundschutz, Building Block [CON.3 Data Backup Concept](https://www.bsi.bund.de/grundschutz)
- GoBD (Principles of Proper Bookkeeping) — legal retention obligations
- GDPR Art. 32 — Recoverability of personal data

BSI CON.3.A7 stipulates:
> „The backed-up data must be restored regularly to check the functionality of the data backup."

**The 3-2-1 Rule — Industry Standard:**
- **3** Copies of the data
- **2** Different storage media (e.g., NAS + Cloud)
- **1** Copy off-site (e.g., AWS Frankfurt)

**What this means in practice:**
A single external hard drive that is occasionally manually loaded does **not** comply with the BSI standard. What is required:

- **Automatic daily backup** — no manual intervention.
- **Encryption** — data is protected even if the backup medium is stolen.
- **External copy** — in case of fire or burglary, the backup remains preserved.
- **Regular restoration tests** — proof that the backup works.
- **GoBD Compliance** — retention periods of 6–10 years for accounting data.

**Technical Solution:**
NAS device (e.g., Synology) with automatic encrypted synchronization to AWS S3 Frankfurt — EU data center, GDPR compliant.

**Eligible for Digitalbonus:** ✅ Yes — NAS hardware and Cloud backup setup.

---

## Real Fines — Triggered by Complaints, Not Inspections

The BayLDA does **not carry out regular routine audits**. Fines arise through:

- **Customer Complaints** — a dissatisfied patient, guest, or employee.
- **Data Breaches** — hacker attack, data loss, accidental disclosure.
- **Competitor Complaints** — competitors file a report.

The Bavarian State Office for Data Protection Supervision (BayLDA) imposed the highest number of fines in 2023 since the introduction of the GDPR. Real examples: Dental practice in Bavaria €3,500, retail trade €1,200 — triggered by individual customer complaints.

**Important:** Ignorance is no excuse. The GDPR has been in force since 2018 — every company had time to adapt.

---

## What the Digitalbonus Bayern Funds

**Program:** [Digitalbonus Bayern](https://www.digitalbonus.bayern)
**Funding Rate:** 50% of eligible costs
**Maximum:** €7,500 (Digitalbonus Standard) — once for each funding area (IT Security and Digitalization)
**Duration:** until December 31, 2027
**Application:** Exclusively digital via ELSTER business account

| Measure | Eligible |
|---|---|
| Firewall (Hardware + License + Configuration) | ✅ Yes |
| Managed Switch for VLAN separation | ✅ Yes |
| WLAN Access Points | ✅ Yes |
| NAS + encrypted Cloud backup | ✅ Yes |
| Email security license (up to 18 months) | ✅ Yes |
| Antivirus/EDR licenses (up to 18 months) | ✅ Yes |
| Installation and configuration services | ✅ Yes |
| Maintenance contract (up to 18 months) | ✅ Yes |
| Consulting services (up to 50% of total costs) | ✅ Yes |
| Standard PCs, Laptops, Printers | ❌ No |
| Standard office software (Office, Windows) | ❌ No |

**Important Condition:** The application must be submitted **before** the start of the project. Neither the order nor the verbal assignment may take place before receipt of the application confirmation.

---

## Example Calculation: Small Hotel (10 rooms, 5 employees)

| Measure | Costs | After Funding (50%) |
|---|---|---|
| FortiGate Firewall + 1-year license | €1,000 | €500 |
| Managed Switch (VLAN-capable) | €500 | €250 |
| 3× WLAN Access Points | €900 | €450 |
| NAS + AWS Backup setup | €500 | €250 |
| Email Security (18 months) | €400 | €200 |
| Antivirus/EDR 5 devices (18 months) | €300 | €150 |
| Installation & Configuration | €1,000 | €500 |
| 18 months maintenance | €900 | €450 |
| **Total** | **€5,500** | **€2,750** |

The hotel pays **€2,750** — the Free State of Bavaria takes over **€2,750**.

---

## For Whom is This Relevant?

- **Hotels & Guesthouses** — guest WLAN, camera systems, booking data, POS terminals
- **Medical & Therapy Practices** — patient data, professional secrecy, GDPR + §75b SGB V
- **Law Firms** — client confidentiality, strict GDPR obligations
- **Cafés & Restaurants** — guest WLAN, checkout system, reservation data
- **Language Schools** — student WLAN, administration data, teacher data
- **Small Offices (2–20 people)** — without their own IT department

---

## What We Offer: Independent Consulting — No Product Sales

We do not sell products. You choose your own providers and products — we help with planning, installation, configuration, and documentation.

As a **Senior Network Security Engineer with 11+ years of experience** in banking, industry, and hospitality (including Hilton, Marriott, Crown Hotel Group, Wyndham Grand Europa), we offer:

1. **Free IT Infrastructure Analysis** — we look at your current situation and show where the gaps are.
2. **Independent Product Recommendation** — we recommend what suits you, not what is the most expensive.
3. **Technical Implementation** — VLAN configuration, firewall setup, backup setup, email security.
4. **Digitalbonus Application Preparation** — we help with the documentation of the eligible measures.
5. **Ongoing Maintenance** — monthly monitoring, updates, point of contact for problems.

---

## Next Step: Free Analysis

**📱 WhatsApp:** [wa.me/4916098665971](https://wa.me/4916098665971)

**📧 Email:** [info@barashhelvadzhaoglu.com](mailto:info@barashhelvadzhaoglu.com)

*Free analysis. No assignment without your consent. No product sales — only consulting and technical expertise.*

---

## Further Links

- [Digitalbonus Bayern — Official Funding Program](https://www.digitalbonus.bayern)
- [GDPR Article 32 — Security of Processing](https://gdpr.eu/article-32-security-of-processing/)
- [BSI IT-Grundschutz Compendium](https://www.bsi.bund.de/grundschutz)
- [BayLDA — Bavarian State Office for Data Protection Supervision](https://www.lda.bayern.de)
- [GoBD — Principles of Bookkeeping](https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Weitere_Steuerthemen/Abgabenordnung/2019-11-28-GoBD.pdf)