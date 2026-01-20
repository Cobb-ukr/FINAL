from flask import Blueprint, request, render_template
from weak_app.db import get_db

search_bp = Blueprint('search', __name__)

@search_bp.route("/search", methods=["GET"])
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
