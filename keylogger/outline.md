# Keylogger Lab – Project Outline

🧠 **Repo:** `keylogger_lab`  
📅 **Date Started:** 2025-04-02  
📂 **Project Type:** Ethical Hacking Lab  
⚠️ **Disclaimer:** This project is for educational use only. Unauthorized access to systems or data is illegal and unethical.

---

## 🧪 Goal

Build and deploy a basic Python-based keylogger inside a virtual lab. This project simulates a post-exploitation scenario where a keylogger is manually installed on a compromised machine. The goal is to develop a functional tool, understand how data exfiltration works, and showcase ethical red team techniques.

This lab lives in the `dark_arts_lab` GitHub repo and is designed to show real, usable skills.

---

## 🛠️ Project Flow

### 1. Keylogger Build (Python)
- Build a Python script using the `keyboard` module
- Logs output to `keystrokes.log`
- Will be kept intentionally simple for clarity and realism

---

### 2. Virtual Lab Setup
- Environment: VMware Workstation or VirtualBox
- Machines:
  - **Attacker:** Kali Linux
  - **Target:** Metasploitable2
- Network: Isolated Host-Only or Internal Network
- Optional: Assign static IPs for consistency

---

### 3. Recon & Exploitation
- Use `nmap` to scan Meta2 from Kali
- Identify vulnerable services (e.g., FTP, Tomcat)
- Launch Metasploit and exploit the chosen service
- Get a Meterpreter or shell session
- Escalate to root (if not already)

---

### 4. Deploy the Keylogger
- Transfer the Python script to the target
- Run as root or sudo
- Log activity to `keystrokes.log`
- Validate functionality

---

### 5. Exfiltrate Logs
- Transfer `keystrokes.log` to Kali using:
  - `scp`
  - `netcat`
  - Simple file transfer tricks
- Read and interpret contents

---

### 6. Optional Cleanup
- Delete the script and log
- Clear shell history
- Demonstrate basic OPSEC hygiene

---

## 💡 Notes

- This project is being built from scratch to demonstrate real ability, not just copied scripts.
- Screenshots will be taken throughout key phases and stored in `/screenshots/`
- Once the lab is completed, files will be committed and pushed to GitHub for reference

---

## 🔮 Future Enhancements (Challenge Goals as Skills Develop)

- Run the keylogger as a background daemon
- Add log encryption or obfuscation
- Send logs to a remote host in real-time
- Build a stealthy version using Python packaging tricks
- Add persistence using crontab or init.d
