---
title: "Supermarket Fridge Cyberattacks in Europe: How to Secure OT and IoT Devices"
description: "Refrigerators in European supermarkets were remotely heated in October and November 2026. What is known so far, why a fridge controller is reachable at all, and seven measures to secure OT and IoT devices in retail and SMB networks."
date: 2026-11-06
draft: false

tags: ["OT Security", "IoT Security", "Cyber Security", "Network Segmentation", "Remote Access", "Retail"]
categories: ["Network Architecture", "Cyber Security"]
keywords: ["supermarket fridge cyberattack", "refrigerator hack Europe", "Danfoss refrigeration cyberattack", "OT security retail", "IoT device security", "secure remote access OT", "network segmentation IoT", "building automation security"]
showToc: true
TocOpen: true
---

In October and November 2026, refrigerators and freezers in supermarkets across Europe were switched to temperatures that destroyed the food inside them. Nobody touched the devices physically. This article summarizes what is publicly known, explains why a refrigeration controller can be attacked over a network in the first place, and lists the measures that would have made such an attack much harder.

> **Status:** This is based on media reports and company statements up to 6 November 2026. The investigations are ongoing. Where something is not confirmed, I say so.

## What Happened

- **France, 12 October 2026:** Refrigerators in stores of Intermarché, Carrefour, Monoprix and Coopérative U were heated and food was spoiled. Intermarché's parent company expected losses of several million euros.
- **2 November 2026:** A second wave hit around 75 stores in Belgium (including Delhaize, Carrefour, Intermarché, Spar and an IKEA store), 13 SuperValu stores in Ireland, ICA and Coop stores in Sweden, and companies in the Netherlands, Estonia and Finland. In Stockholm, a freezer was reportedly heated to 50 °C.
- **Common element:** Some of the affected systems used refrigeration control software from Danfoss. According to Danfoss, the affected customers had not updated their software. Security researchers from Claroty had reported vulnerabilities in Danfoss refrigeration controllers in August, which Danfoss says it fixed with an update.
- **Mechanism:** The Belgian refrigeration service company Sabcobel said the units were switched into defrost mode, and that a software update alone is not enough: physical modifications are needed as well.

**Not confirmed so far:** how the attackers got access, whether the vulnerabilities reported in August were exploited, and who is behind the attacks. Belgium's federal prosecutor has opened an investigation. The EU agriculture commissioner called the attacks a deliberate attempt to disrupt the food supply chain.

## Why Is a Fridge on the Network at All?

Commercial refrigeration is not a household fridge. A supermarket runs dozens of cooling units that are controlled centrally: temperatures, defrost cycles, alarms and energy optimization. The service company needs to see alarms at night and adjust settings without driving to the store.

That is a legitimate need. The problem is how it is often solved:

- The controller or its web interface is **reachable directly from the internet**, sometimes with a port forward that someone set up years ago.
- It sits in the **same network** as the cash registers, the office PCs and the guest Wi-Fi.
- The service company uses a **permanent remote access** tool that nobody monitors.
- The software **has not been updated** since installation, because "it works".
- **Default passwords** were never changed.

None of these is specific to refrigeration. The same pattern exists for building automation, heating and ventilation, access control, cameras, PV inverters and production machines. That is why this incident matters beyond supermarkets.

## Seven Measures to Secure OT and IoT Devices

### 1. Know What You Have

You cannot protect devices you do not know about. Keep an inventory of every connected controller, gateway and sensor: vendor, model, software version, IP address, who manages it and how it is accessed remotely.

### 2. No Direct Exposure to the Internet

A management interface of an OT device should never be reachable from the internet. Check your firewall for port forwards and search for your public IP addresses in services such as Shodan to see what the outside world can reach.

### 3. Segment the Network

Put OT and IoT devices into their own VLAN or network segment. The firewall between the segments decides what may talk to what:

- The refrigeration controller talks only to its management server and to the vendor's cloud, if one is used.
- Cash registers, office PCs and guest Wi-Fi cannot reach the controller at all.

More on segmentation in industrial networks: [OT Networks: What an IT Engineer Actually Encounters on the Factory Floor](/en/technology/ot-network-security/).

### 4. Restrict Outbound Traffic

Many devices only need to reach a handful of destinations. Allow exactly those addresses and ports and block everything else. If a device is compromised, it cannot download tools or reach an attacker's server.

### 5. Secure Remote Access for Vendors

The service company needs access, but on your terms:

- Access through **IPsec VPN or ZTNA (Zero Trust Network Access)** with **multi-factor authentication**, never through an open port.
- Access only to the systems the vendor maintains, not to the whole network.
- Access **enabled when needed** and disabled afterwards, with logging of who connected when.

### 6. Updates and Credentials

Plan software updates for OT devices like you do for servers, coordinated with the vendor. Change all default passwords and use individual accounts instead of one shared login.

### 7. Safety Limits That Software Cannot Override

This is the lesson most specific to this incident. If a hacked controller can heat a freezer to 50 °C, the system has no independent safety limit. Physical or hardware-based limits and local alarms that work without the network ensure that a compromised controller cannot cause physical damage. Monitoring helps as well: unusual temperature changes or configuration changes at 3 a.m. should trigger an alarm immediately.

## Quick Checklist for Small Businesses

- Do we know which devices in our store are connected to the network?
- Can any of them be reached from the internet?
- Are they in a separate network from cash registers and guest Wi-Fi?
- How does our service company connect, and can we see when it does?
- When was the software last updated? Have the default passwords been changed?
- Is there an alarm that works even if the network or the controller is down?

If you cannot answer one of these questions, that is where to start.

## Related Articles

- [OT Networks: What an IT Engineer Actually Encounters on the Factory Floor](/en/technology/ot-network-security/)
- [The Zero Trust Mindset: Security as an Architecture, Not a Product](/en/architecture/zero-trust-architecture-behaviors/)
- [802.1X Projects: Deploying the Identity-Based Architecture in the Field](/en/technology/identity-based-microsegmentation-8021x/)
- [Firewall Selection and Capacity Planning](/en/technology/firewall-selection-capacity/)

## Sources

- [Euronews: Cyberattacks hit supermarket fridges and freezers in Europe](https://www.euronews.com/2026/11/02/cyberattack-hits-belgian-supermarket-fridges-and-freezers)
- [Forbes: New wave of refrigerator cyberattacks roils European supermarkets](https://www.forbes.com/sites/conormurray/2026/11/02/new-wave-of-refrigerator-cyberattacks-roils-european-supermarkets-everything-is-destroyed/)
- [Al Jazeera: Suspected cyberattacks trigger supermarket fridge failures across Europe](https://www.aljazeera.com/news/2026/11/2/freezers-in-sweden-belgium-overheat-following-possible-cyberattacks)
- [Axios: Europe's fridges are getting hacked](https://www.axios.com/2026/11/02/europe-supermarket-fridges-attacks-food)
