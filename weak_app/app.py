from flask import Flask, request, render_template
import json
from datetime import datetime
import os

from .db import get_db, DB_PATH

app = Flask(__name__)

ACCESS_LOG = "logs/access.log"

# Import blueprints
from .routes.login import login_bp
from .routes.search import search_bp

# Register blueprints
app.register_blueprint(login_bp)
app.register_blueprint(search_bp)


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


# /login section:

#Main Hook
if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
