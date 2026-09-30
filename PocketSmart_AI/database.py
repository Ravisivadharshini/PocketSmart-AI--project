import sqlite3
from pathlib import Path
from datetime import datetime
import hashlib, os

DB_PATH = Path(__file__).resolve().parent / "pocketsmart.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        budget REAL NOT NULL,
        request_json TEXT NOT NULL,
        response_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    salt = os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), 120_000
    ).hex()
    return f"{salt}${digest}"

def verify_password(password: str, stored: str) -> bool:
    try:
        salt, digest = stored.split("$", 1)
        check = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt.encode(), 120_000
        ).hex()
        return check == digest
    except ValueError:
        return False

def create_user(name, email, password):
    conn = get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO users(name,email,password_hash,created_at) VALUES(?,?,?,?)",
            (name, email.lower().strip(), hash_password(password), datetime.utcnow().isoformat())
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()

def get_user_by_email(email):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM users WHERE email=?", (email.lower().strip(),)
    ).fetchone()
    conn.close()
    return row

def get_user_by_id(user_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()
    return row

def add_history(user_id, category, budget, request_json, response_json):
    conn = get_conn()
    conn.execute(
        """INSERT INTO history(user_id,category,budget,request_json,response_json,created_at)
           VALUES(?,?,?,?,?,?)""",
        (user_id, category, budget, request_json, response_json, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

def get_history(user_id):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM history WHERE user_id=? ORDER BY id DESC", (user_id,)
    ).fetchall()
    conn.close()
    return rows
