from flask import Flask, request, render_template
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__)

DB_PATH = "data/app.db"
ACCESS_LOG = "logs/access.log"

def get_db():
    return sqlite3.connect(DB_PATH)


# Log each request to a file and database
@app.before_request
def log_request():
    timestamp = datetime.utcnow().isoformat()
    source_ip = request.remote_addr
    method = request.method
    path = request.path
    query_string = request.query_string.decode(errors="ignore")
    headers = json.dumps(dict(request.headers))
    body = request.get_data(as_text=True)

    log_entry = f"""
[{timestamp}]
IP: {source_ip}
Method: {method}
Path: {path}
Query: {query_string}
Headers: {headers}
Body: {body}
-------------------------
"""

    with open(ACCESS_LOG, "a") as f:
        f.write(log_entry)

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO request_logs
        (timestamp, source_ip, method, path, query_string, headers, body)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (timestamp, source_ip, method, path, query_string, headers, body)
    )
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return "Vulnerable App Running"


#login section:
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form.get("username")
    password = request.form.get("password")

    query = f"""
    SELECT * FROM users
    WHERE username = '{username}'
    AND password = '{password}'
    """

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(query)
        user = cur.fetchone()
    except Exception as e:
        return f"SQL ERROR: {e}", 500
    
    conn.close()

    success = 1 if user else 0
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO auth_attempts
        (timestamp, source_ip, username, password, success)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            datetime.utcnow().isoformat(),
            request.remote_addr,
            username,
            password,
            success
        )
    )
    conn.commit()
    conn.close()

    if user:
        return "Login successful"
    else:
        return "Login failed"


# implementing /search endpoint

@app.route("/search", methods=["GET"])
def search():
    q = request.args.get("q", "")

    if q == "":
        return render_template("search.html", query=q, results=[])
    
    
    query = f"""
    SELECT id, username, password
    FROM users
    WHERE username LIKE '%{q}%'
    """

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(query)
        rows = cur.fetchall()
    except Exception as e:
        conn.close()
        return f"SQL Error: {e}", 500

    conn.close()
    return render_template("search.html", query=q, results=rows)


#Main Hook
if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
