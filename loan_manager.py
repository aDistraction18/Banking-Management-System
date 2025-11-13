# =====================
# File: loan_manager.py (with pending loan loader)
# =====================
import heapq
from database import get_connection
from datetime import datetime

# Priority: lower values = higher priority (use urgency, amount, etc.)
class LoanManager:
    def __init__(self):
        self.loan_heap = []  # Min heap based on priority (amount or urgency)

    def request_loan(self, account_number, amount):
        # Here we use amount as priority (smaller amount, higher chance)
        heapq.heappush(self.loan_heap, (amount, account_number))
        self.save_loan_request(account_number, amount)

    def process_loan(self):
        if not self.loan_heap:
            return None
        amount, account_number = heapq.heappop(self.loan_heap)
        self.approve_loan(account_number, amount)
        return (account_number, amount)

    def save_loan_request(self, account_number, amount):
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number TEXT,
                amount INTEGER,
                status TEXT,
                request_date TEXT
            )
        """)
        c.execute("""
            INSERT INTO loans (account_number, amount, status, request_date)
            VALUES (?, ?, ?, ?)
        """, (account_number, amount, "Pending", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()

    def approve_loan(self, account_number, amount):
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
            UPDATE loans SET status = 'Approved' 
            WHERE account_number = ? AND amount = ? AND status = 'Pending'
        """, (account_number, amount))

        # Optional: Add loan amount to user balance
        c.execute("UPDATE users SET balance = balance + ? WHERE account_number = ?", (amount, account_number))
        conn.commit()
        conn.close()

    def get_all_loans(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT account_number, amount, status, request_date FROM loans")
        data = c.fetchall()
        conn.close()
        return data

    def load_pending_loans(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT account_number, amount FROM loans WHERE status = 'Pending'")
        rows = c.fetchall()
        conn.close()
        for account_number, amount in rows:
            heapq.heappush(self.loan_heap, (amount, account_number))
  
    def ensure_table_exists(self):
        conn = get_connection()
        c = conn.cursor()
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
