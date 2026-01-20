from flask import Blueprint, request, render_template
from datetime import datetime
from weak_app.db import get_db

login_bp = Blueprint('login', __name__)

@login_bp.route("/login", methods=["GET", "POST"])
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
