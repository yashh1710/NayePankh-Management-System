import sqlite3

DB_NAME = "database/foundation.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS volunteers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        skills TEXT,
        join_date TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS beneficiaries(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        education TEXT,
        location TEXT,
        program TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        donor_name TEXT,
        amount REAL,
        date TEXT,
        purpose TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name TEXT,
        date TEXT,
        location TEXT,
        description TEXT
    )
    """)

    conn.commit()
    conn.close()