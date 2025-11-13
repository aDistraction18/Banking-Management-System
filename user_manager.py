from database import get_connection
import sqlite3

def add_user(name, account_number, balance):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, account_number, balance) VALUES (?, ?, ?)",
                  (name, account_number, balance))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

def get_user(account_number):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE account_number = ?", (account_number,))
    user = c.fetchone()
    conn.close()
    return user

def update_balance(account_number, new_balance):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE users SET balance = ? WHERE account_number = ?", (new_balance, account_number))
    conn.commit()
    conn.close()
