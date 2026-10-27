# CodeAlpha_SecureCodingReview
# CodeAlpha Cyber Security Internship – Task 3

## Secure Coding Review

### Project Overview
This project focuses on reviewing a Python-based authentication system to identify security vulnerabilities and demonstrate secure coding practices.

It contains two applications:
- **Vulnerable Application:** Demonstrates common security weaknesses.
- **Secure Application:** Implements security improvements to reduce those weaknesses.

### Technologies Used
- Python
- SQLite
- Bandit Security Scanner
- PyCharm

### Vulnerabilities Identified
The vulnerable application contains the following security issues:

1. **Hardcoded Password (B105):** An administrator password is stored directly in the source code.
2. **Potential SQL Injection (B608):** SQL queries are constructed using string concatenation.
3. **Weak Password Validation:** Short and weak passwords are accepted.
4. **Unlimited Login Attempts:** Repeated incorrect login attempts are allowed.
5. **Insecure Password Storage:** Passwords are stored without secure hashing.

### Security Improvements
The secure application implements the following protections:

- PBKDF2-HMAC-SHA256 password hashing
- Random salt generation
- Parameterized SQL queries
- Minimum password length validation
- Login attempt limiting
- Temporary account lockout
- Hidden password input
- Generic authentication error messages

### Bandit Security Scan Results

| Metric        | Vulnerable Application | Secure Application |
| Lines Scanned |  83                    |       223          |
| Low Severity Issues | 1                |       0            |
| Medium Severity Issues | 1             |       0            |
| High Severity Issues | 0               |       0             |
| Total Issues | 2 | 0 |

The vulnerable application scan identified a hardcoded password and a potential SQL injection issue. The secure application scan reported no detectable issues.

**Note:** Zero Bandit findings do not guarantee that an application is completely secure. Manual inspection and functional testing are also required.

### Project Files
- `vulnerabilities_app.py` — Intentionally vulnerable application
- `main.py` — Secure authentication application
- `vulnerable_scan.txt` — Bandit scan results for the vulnerable application
- `secure_scan.txt` — Bandit scan results for the secure application
- `Security_Review_Report.pdf` — Security review report
- `screenshots/` — Testing and scan evidence

### How to Run

**1. Run the vulnerable application**

```bash
python vulnerabilities_app.py
```

**2. Run the secure application**

```bash
python main.py
```

**3. Install Bandit**

```bash
python -m pip install bandit
```

**4. Scan the applications**

```bash
python -m bandit vulnerabilities_app.py
python -m bandit main.py
```

### Testing
The applications were tested for weak password acceptance and repeated failed login attempts.

The vulnerable application accepted weak passwords and allowed repeated login attempts. The secure application rejected short passwords and temporarily locked accounts after repeated failed attempts.

### Conclusion
This project demonstrates the importance of secure password handling, SQL query parameterization, password validation, and login attempt controls. Comparing the vulnerable and secure implementations helps illustrate how secure coding practices can reduce common application security risks.

### Disclaimer
The vulnerable application is intended strictly for educational purposes and authorized local security testing.

**Internship:** CodeAlpha Cyber Security Internship  
**Task:** Secure Coding Review
