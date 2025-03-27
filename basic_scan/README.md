## Project 1: Scanning and Enumerating a Local Network with Nmap on Kali Linux

🔍 nmap -sn 172.16.252.0/24

What it does:
A quick ping scan to see which hosts are online and in the subnet — no port scanning involved.

Findings:
IP Address	MAC Address	Notes
172.16.252.1	00:50:56:C0:00:01	VMware Gateway
172.16.252.20	00:0C:29:0F:00:6E	Windows 10 VM
172.16.252.40	00:0C:29:6C:B6:FD	Android VM
172.16.252.254	00:50:56:E1:16:36	VMware (DHCP or NAT service)
172.16.252.128	(No MAC shown)	Possibly a leftover/ghost VM or inactive system that replied briefly

✅ Summary

    The scan found 5 live hosts in the subnet.
    All expected VMs (Kali, Windows 10, Android) are online.
    Some additional VMware infrastructure showed up (likely gateway & DHCP services).

---

🔌 nmap -p 80 172.16.252.20 & 172.16.252.40
              
What it does:
Scans port 80 (HTTP)

Findings:
Windows 10 172.16.252.20 - Port 80 - closed
Android x86 172.16252.40 - Port 80 - filtered - no connection (I learned that Android VMs don't really behave as expected)

---


🧠 nmap -O 172.16.252.20 & 172.16.252.40
What it does: Tries to detmine the OS of the target
Windows 10 - 172.16.252.20 --> Microsoft Windows 1709 (21H2)
Android x86 - 172.16.252.40 --> failed to detect

---

🧪 nmap -sV 172.16.252.20

What it does:
Tries to find the version info for services running on open ports.
Windows 10 - Detected MSFT Windows RPC, NetBIOS
Android x86 - Nothing found - ports ignored

---

⚔️ nmap -A 172.16.252.20

What it does:
Runs an aggressive scan: combines OS detection, version detection, script scanning, and traceroute.

Findings:
✅ Windows 10 (172.16.252.20)

    Open Ports:

        135/tcp → msrpc (Microsoft RPC)

        139/tcp → netbios-ssn (NetBIOS Session Service)

        445/tcp → microsoft-ds (Windows file sharing)

    OS Detection:
    Detected as Microsoft Windows 10, version 1709 – 21H2

    Scripts Output:

        smb2-time: SMB time shows correct system time.

        smb2-security-mode: Message signing is enabled but not required.

        nbstat: Hostname and MAC detected correctly.

    Traceroute:
    1 hop → 172.16.252.20

✅ Android (172.16.252.40)

    Open Ports:
    None detected (all 1000 common ports are either closed or filtered).

    OS Detection:
    Not enough information to guess the OS.

    MAC Vendor:
    VMware detected, confirming it’s a virtual machine.

    Traceroute:
    1 hop → 172.16.252.40
