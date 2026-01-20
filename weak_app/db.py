import sqlite3
import os

# Get the directory of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "app.db")

def get_db():
    return sqlite3.connect(DB_PATH)
