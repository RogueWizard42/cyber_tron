# HTB Starting Point Lab Walkthrough: Appointment (Linux Box)

## Executive Summary

- **Lab Objective**: Enumerate and exploit a web application on the target machine to bypass authentication via SQL injection and retrieve a flag.
- **Target IP**: 10.129.89.238
- **Key Findings**: Identified an Apache 2.4.38 web server on port 80 hosting a login form vulnerable to SQL injection. Using the input `admin' #` bypassed password authentication, granting access to an admin page with the flag.
- **Impact**: In a real-world scenario, SQL injection could allow unauthorized access to sensitive data or functionality, potentially leading to full system compromise.
- **Recommendations**: Sanitize user inputs, use prepared statements, and regularly audit web applications for injection vulnerabilities.
- **Completion Date**: July 20, 2025
- **Tools Used**: Nmap, web browser (on Kali Linux)

## Methodology and Scope

This walkthrough follows a standard reconnaissance and exploitation process for the HTB Starting Point lab "Appointment." The scope was limited to port scanning, web application enumeration, and exploitation of a login form on the provided target IP. No directory brute-forcing or advanced exploitation was required.

Steps were performed in a controlled lab environment using default Kali tools and a web browser. Assumptions: Target is a Linux machine running an Apache web server. The lab emphasized SQL injection, leveraging the `#` comment character to bypass authentication.

## Findings

### Finding 1: Web Service Identification

- **Description**: An HTTP service running on Apache httpd 2.4.38 was identified on port 80, hosting a web application.
- **Severity**: Informational (baseline enumeration).
- **Steps to Reproduce**:
    1. Perform a targeted port scan with version detection using Nmap:
        
        ```bash
        nmap -sV -p 80 10.129.89.238
        ```
        
        **Flag Explanation**: `-sV` enables version detection; `-p 80` targets the specific port.  
        Output:
        
        ```bash
        Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-20 18:19 EDT
        Nmap scan report for 10.129.89.238
        Host is up (0.025s latency).
        PORT   STATE SERVICE VERSION
        80/tcp open  http    Apache httpd 2.4.38
        Service Info: Host: 127.0.0.1
        Nmap done: 1 IP address (1 host up) scanned in 32.49 seconds
        ```
        
- **Impact**: Confirms an active web server, enabling targeted enumeration of web vulnerabilities.
- **Evidence**: Nmap scan results above.
- **Remediation**: N/A (informational).

### Finding 2: SQL Injection in Login Form

- **Description**: The web application on port 80 hosts a login form vulnerable to SQL injection. Using the input `admin' #` in the username field bypasses password authentication by commenting out the password check, granting access to an admin page.
- **Severity**: Critical (authentication bypass).
- **Steps to Reproduce**:
    1. Access the login page in a browser:
        
        ```bash
        http://10.129.89.238
        ```
        
    2. Enter `admin' #` as the username and leave the password blank.
    3. Submit the form to access the admin page, which displays "Congratulations" and the flag: `e3d0796d002a446c0e622226f42e9672`.
- **Impact**: SQL injection allows unauthorized access to restricted areas, potentially exposing sensitive data or enabling further system compromise. This vulnerability is classified as A03:2021-Injection in the OWASP Top 10.
- **Evidence**: Successful login with `admin' #`, revealing the flag and admin page content.
- **Remediation**: Implement input sanitization and prepared statements in the application’s SQL queries; validate all user inputs.

## Recommendations

- Use prepared statements or parameterized queries to prevent SQL injection.
- Regularly audit web applications for vulnerabilities using tools like SQLmap or Burp Suite.
- Restrict access to port 80 to trusted networks via firewall rules.
- For labs like this, practice identifying SQL injection points with manual testing or automated tools to understand query manipulation.

## Appendices

- **Raw Notes/Logs**: (Optional—attach full session logs if sharing.)
- **Screenshots**: (Add here if available, e.g., browser captures of login page or flag.)
- **Key Takeaway**: Clues in the lab questions (e.g., SQL comment character `#`) and understanding SQL syntax were critical to identifying the injection point. External guidance (e.g., Shadownet) helped clarify the `admin' #` payload.