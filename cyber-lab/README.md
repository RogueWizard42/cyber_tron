## 🛡️ Pentest Forge

---

## Overview

**Author’s Note:**  
Welcome to the Pentest Forge project — a guided build of a complete virtual cybersecurity lab. This project is designed to learn, experiment and build skills. It aims at **Blue Team skills** gaining hands-on **Red Team** exposure and building **Purple Team** monitoring skills.

I'll be working on **VMware Workstation Pro 17.x**, using a powerful home system to simulate an enterprise-style network with segmented subnets, firewall controls, intrusion detection, and log aggregation. Everything here is built using **free tools**, and every step focuses not just on *how*, but on *why* — this is about building a real foundation.

---

##  Lab Architecture & Network Design

I'm simulating a small business or enterprise-style network. To do that, I’ll segment the lab into **three subnets** behind a firewall/router, using **host-only virtual networks** in VMware (no expensive managed switches needed):

#### 🔴 Red Team Subnet (192.168.10.0/24)

- Home of the **Kali Linux attacker machine**
- Used to simulate external attacks (penetration testing, vulnerability scans, etc.)

#### 🔵 Blue Team Subnet (192.168.20.0/24)

- Target systems live here: **Metasploitable2**, **Ubuntu Server**, and **Windows 10**
- This is the internal "company" network I'm defending and monitoring

#### 🟣 Purple Team Subnet (192.168.30.0/24)

- Monitoring and logging live here — **Splunk** will aggregate data from pfSense, Ubuntu, and other systems

---

### 🔥 pfSense Firewall/Router

pfSense is the heart of this lab:
- Routes traffic between subnets
- Controls access via firewall rules
- Hosts **Snort** (IDS/IPS) for detecting suspicious behavior
- Connected to a **WAN (NAT)** adapter for internet access

---

## 🧰 Tools and Virtual Machines

#### 🔸 pfSense (Firewall/Router)
- FreeBSD-based open-source firewall/router
- Will have 4 NICs: WAN, Red, Blue, Purple
- Includes Snort for IDS/IPS

#### 🔸 Kali Linux (Attacker VM)
- Red Team system
- Comes preloaded with tools: `nmap`, `Metasploit`, `Hydra`, etc.
- I’ll also install **Nessus Essentials** (free vulnerability scanner)

#### 🔸 Metasploitable2 (Linux Target VM)
- Intentionally vulnerable VM for exploitation practice
- Will be scanned, probed, and likely broken
- Default creds: `msfadmin:msfadmin`

#### 🔸 Windows 10 (Target VM)
- Represents an internal user workstation
- Optional future target for exploitation and log forwarding
- Evaluation ISO will be used if necessary

#### 🔸 Ubuntu Server (Target + Logging)
- Hosts SSH service for brute-force/hardening exercises
- Sends logs to Splunk for analysis

#### 🔸 Splunk (SIEM VM)
- Installed in **free mode** (500MB/day indexing)
- Gathers logs from pfSense, Ubuntu, and potentially Windows
- Our central dashboard for Purple Team operations

#### 🔸 Wireshark (Traffic Analysis)
- Not a dedicated VM
- Used inside Kali or the host OS to capture packets
- Great for troubleshooting, recon, and deep traffic inspection

---

## 💡 Why This Lab?

- Designed to reinforce **Security+ domains** with practical labs
- Also builds foundational Linux skills in preparation for **Linux+**
- Created for repetition, fundamentals, and real-world job readiness
- Every step will be **documented, version-controlled**, and include clear notes for learning and showcasing on GitHub

---

## 🧭 Network Layout (Diagram Placeholder)
