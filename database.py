import sqlite3

# Returns a connection to the database file
def get_connection():
    return sqlite3.connect("bank.db")

# Creates all necessary tables if they don't exist
def connect_db():
    conn = get_connection()
    c = conn.cursor()

    # Table: users
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            account_number TEXT UNIQUE,
            balance INTEGER
        )
    """)

    # Table: transactions
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            receiver TEXT,
            amount INTEGER,
            date TEXT
        )
    """)

    # Table: loans
    c.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT,
            amount INTEGER,
            status TEXT,
            request_date TEXT
        )
    """)

    conn.commit()
    conn.close()
