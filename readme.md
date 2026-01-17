# Intentionally Vulnerable Flask Application

**SECURITY WARNING** - This application contains deliberate security vulnerabilities

##  Important Security Notice
**This application contains deliberate security vulnerabilities** designed for:
- Security education and research
- Penetration testing practice
- Demonstration of common web vulnerabilities
- **NOT FOR PRODUCTION USE**

## Project Structure
```
FINAL/
├── weak_app/
│   ├── app.py              - Main vulnerable application
│   ├── test.py             - Simple calculator (unrelated to web app)
│   ├── data/               - Database and file storage
│   ├── logs/               - Access logs and audit trails
│   ├── static/             - CSS assets
│   └── templates/          - HTML templates
└── readme.md               - This documentation
```

## Key Vulnerabilities

### 1. SQL Injection (Login)
```python
# Vulnerable code in app.py
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
cur.execute(query)
```
- **Impact**: Full database compromise through authentication bypass
- **Test vector**: `' OR 1=1--`

### 2. SQL Injection (Search)
```python
# Vulnerable code in app.py
query = f"SELECT id, username, password FROM users WHERE username LIKE '%{q}%'"
cur.execute(query)
```
- **Impact**: Data extraction through blind SQLi vectors
- **Test vector**: `%' UNION SELECT 1,2,3--`

### 3. Credential Logging
- All login attempts (including passwords) stored in:
  - SQLite database (`data/app.db`)
  - Plaintext logs (`logs/access.log`)

## Getting Started

### Prerequisites
```bash
pip install -r requirements.txt
```

### Database Initialization
```python
# Run once to create tables
from weak_app.app import get_db
conn = get_db()
conn.executescript('''
    CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT, password TEXT);
    CREATE TABLE request_logs(...);
    CREATE TABLE auth_attempts(...);
''')
conn.commit()
```

### Running the Application
```bash
python weak_app/app.py
```
Access at: http://localhost:5000

## Core Endpoints

| Endpoint   | Method | Vulnerability        | Risk Level |
|------------|--------|----------------------|------------|
| `/login`   | POST   | SQL Injection        | Critical   |
| `/search`  | GET    | SQL Injection        | High       |
| `/`        | GET    | Information disclosure | Medium     |

## Security Controls (Intentionally Disabled)
-  Input sanitization
-  Parameterized queries
-  Error masking
-  Authentication hardening

## Production Warning
This application contains known vulnerabilities including:
- Clear-text credential storage
- Debug mode enabled
- Public exposure (0.0.0.0 binding)
- Unrestricted error disclosure

**DO NOT DEPLOY IN PRODUCTION ENVIRONMENTS**
