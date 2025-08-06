# HTB Starting Point Lab Walkthrough: Explosion (Windows Box)

## Executive Summary

- **Lab Objective**: Enumerate and exploit an RDP service on the target machine to gain administrative access and retrieve a flag, simulating basic remote desktop reconnaissance.
- **Target IP**: 10.129.92.86
- **Key Findings**: Identified an open RDP service (Microsoft Terminal Services) on port 3389, allowing login as `Administrator` with a blank password. This granted full desktop access and retrieval of a sensitive file (`flag.txt`).
- **Impact**: In a real-world scenario, unauthenticated RDP access could lead to complete system compromise, including data theft and unauthorized command execution.
- **Recommendations**: Enforce strong passwords for all accounts, restrict RDP to trusted networks, and consider disabling RDP if not required.
- **Completion Date**: July 9, 2025
- **Tools Used**: Nmap, xfreerdp (on Kali Linux)

## Methodology and Scope

This walkthrough follows a standard reconnaissance and access process for the HTB Starting Point lab "Explosion." The scope was limited to port scanning, RDP service enumeration, and file access via remote desktop on the provided target IP. No advanced exploitation or privilege escalation was required.

Steps were performed in a controlled lab environment using default Kali tools. Assumptions: Target is a Windows machine running Microsoft Terminal Services.

## Findings

### Finding 1: RDP Service Identification

- **Description**: RDP (Remote Desktop Protocol) is a protocol for remote graphical access to Windows systems, running on port 3389. A scan identified the service as `ms-wbt-server` (Microsoft Terminal Services).
- **Severity**: Informational (baseline enumeration).
- **Steps to Reproduce**:
    1. Perform a targeted port scan with version detection using Nmap:
        
        ```bash
        nmap -sV -p 3389 10.129.92.86
        ```
        
        Output:
        
        ```bash
        Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-09 19:33 EDT
        Nmap scan report for 10.129.92.86
        Host is up (0.021s latency).
        PORT     STATE SERVICE       VERSION
        3389/tcp open  ms-wbt-server Microsoft Terminal Services
        Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
        Nmap done: 1 IP address (1 host up) scanned in 6.38 seconds
        ```
        
- **Impact**: Confirms RDP is active, enabling further access attempts.
- **Evidence**: Nmap scan results above.
- **Remediation**: N/A (informational).

### Finding 2: Unauthenticated RDP Access as Administrator

- **Description**: The RDP service allows login as the `Administrator` user with a blank password, granting immediate access to the remote desktop.
- **Severity**: Critical (unauthenticated administrative access).
- **Steps to Reproduce**:
    1. Connect to the target via RDP using xfreerdp with the `/v:` switch for the IP and `/u:` for the username, leaving the password empty:
        
        ```bash
        xfreerdp /v:10.129.92.86 /u:Administrator /p:""
        ```
        
        Output: Successful connection to the Windows desktop.
- **Impact**: Unauthenticated administrative access allows full control of the system, including file access, modification, and execution of arbitrary commands, equivalent to a total system compromise.
- **Evidence**: Successful desktop projection via xfreerdp.
- **Remediation**: Enforce strong, complex passwords for all accounts; disable accounts with blank passwords; restrict RDP access via firewall rules.

### Finding 3: File Retrieval via RDP

- **Description**: After gaining Administrator access via RDP, located a sensitive file (`flag.txt`) on the desktop of the target machine.
- **Severity**: Critical (successful data exfiltration).
- **Steps to Reproduce**:
    1. Connect to the RDP session (as above).
    2. Navigate to the desktop and locate `flag.txt`.
    3. Open the file to retrieve the flag contents (manually viewed on the desktop).
- **Impact**: Access to sensitive files demonstrates the ability to extract critical data, simulating a real-world data breach.
- **Evidence**: Flag file (`flag.txt`) found on the desktop.
- **Remediation**: Remove unnecessary sensitive files from accessible locations; implement strict file permissions; monitor for unauthorized access.

## Recommendations

- Disable RDP if not required, or restrict access to specific IP ranges using firewalls.
- Enforce strong password policies for all accounts, especially privileged ones like Administrator.
- Regularly scan for open RDP ports and misconfigurations using tools like Nmap or RDP-specific scripts (e.g., `rdp-enum-encryption.nse`).
- For labs like this, practice enumerating RDP with tools like Hydra or Metasploit’s `rdp_login` module to explore credential-based attacks.

## Appendices

- **Raw Notes/Logs**: (Optional—attach full session logs if sharing.)
- **Screenshots**: (Add here if available, e.g., desktop capture showing `flag.txt`.)