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
│   ├── __init__.py         - Package initialization
│   ├── app.py              - Main Flask application
│   ├── db.py               - Database connection and configuration
│   ├── data/               - Database and file storage
│   │   └── app.db          - SQLite database (created at runtime)
│   ├── logs/               - Access logs and audit trails
│   │   └── access.log      - Request logging
│   ├── routes/             - Route blueprints
│   │   ├── __init__.py
│   │   ├── login.py        - Login route with SQL injection
│   │   └── search.py       - Search route with SQL injection
│   ├── static/             - CSS assets
│   │   └── index.css
│   └── templates/          - HTML templates
│       ├── index.html
│       ├── login.html
│       ├── search.html
│       ├── comment.html
│       └── upload.html
├── readme.md               - This documentation
├── requirements.txt        - Python dependencies
└── injection_commands.md   - Example injection payloads
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

### Database Configuration
The `db.py` module handles database connectivity:
```python
# weak_app/db.py
from weak_app.db import get_db

# Get a database connection
conn = get_db()
cur = conn.cursor()
cur.execute("SELECT * FROM users")
```

Database path is automatically resolved relative to the `weak_app` module directory for consistent operation regardless of the working directory.

### Running the Application
```bash
# Run as a module (recommended)
python3 -m weak_app.app

# Or from the project directory
cd /mnt/OldVolume/New_projects/FINAL
python3 -m weak_app.app
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
