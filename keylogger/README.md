## Keylogger Lab

A hands-on cybersecurity lab simulating a post-exploitation scenario in which a keylogger is manually deployed on a compromised Linux machine. Built and tested entirely in a virtual lab environment using Kali Linux and Metasploitable2.

⚠️ **This project is for educational use only. Unauthorized access to systems is illegal and unethical.**

---

## Overview

This lab was created to learn and demonstrate real-world skills in Python scripting, red team tactics, and ethical hacking workflows. It is part of the `dark_arts_lab` repo series and focuses on developing a simple but functional keylogger, exploiting a target machine using Metasploit, and exfiltrating captured keystroke logs.

---

##  Tools & Environment

- **Attacker VM:** Kali Linux
- **Target VM:** Metasploitable2
- **Network Type:** Host-only / Internal (isolated)
- **Tech Stack:**
  - Python 3
  - `keyboard` module
  - Metasploit Framework
  - `nmap`, `scp`, `netcat`
- I use Vmware Workstation Pro for these labs, your setup might different depending on the hypervisor you're using  

---

## Full Outline

See [`outline.md`](./outline.md) for a complete breakdown of each phase, future improvements, and structure.
