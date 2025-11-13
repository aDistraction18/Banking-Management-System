import customtkinter as ctk
from tkinter import messagebox
from database import connect_db
from user_manager import add_user, get_user, update_balance
from transaction_graph import TransactionGraph
from loan_manager import LoanManager

connect_db()
tg = TransactionGraph()
lm = LoanManager()
lm.ensure_table_exists()
lm.load_pending_loans()


ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Smart Banking System")
app.geometry("1000x600")
app.resizable(False, False)


left_panel = ctk.CTkFrame(app, width=700, height=600, corner_radius=0)
left_panel.pack(side="left", fill="both")
dashboard_label = ctk.CTkLabel(left_panel, text="Smart Banking System Dashboard",
                                font=("Arial", 20))
dashboard_label.place(relx=0.5, rely=0.5, anchor="center")


right_panel = ctk.CTkFrame(app, width=300, fg_color="#f0f0f0")
right_panel.pack(side="right", fill="y")
ctk.CTkLabel(right_panel, text="Control Panel", font=("Helvetica", 16, "bold"),
             text_color="black").pack(pady=20)


def add_user_ui():
    win = ctk.CTkToplevel(app)
    win.title("Add User")
    win.geometry("300x300")
    win.focus()
    win.grab_set()

    name_var = ctk.StringVar()
    acc_var = ctk.StringVar()
    bal_var = ctk.StringVar()

    ctk.CTkLabel(win, text="Name").pack(pady=5)
    ctk.CTkEntry(win, textvariable=name_var).pack()
    ctk.CTkLabel(win, text="Account Number").pack(pady=5)
    ctk.CTkEntry(win, textvariable=acc_var).pack()
    ctk.CTkLabel(win, text="Initial Balance").pack(pady=5)
    ctk.CTkEntry(win, textvariable=bal_var).pack()

    def submit():
        try:
            if add_user(name_var.get(), acc_var.get(), int(bal_var.get())):
                messagebox.showinfo("Success", "User added.")
                win.destroy()
            else:
                messagebox.showerror("Error", "Account already exists.")
        except:
            messagebox.showerror("Error", "Invalid input.")

    ctk.CTkButton(win, text="Submit", command=submit).pack(pady=15)

def transfer_ui():
    win = ctk.CTkToplevel(app)
    win.title("Transfer Money")
    win.geometry("300x300")
    win.grab_set()

    from_var = ctk.StringVar()
    to_var = ctk.StringVar()
    amount_var = ctk.StringVar()

    ctk.CTkLabel(win, text="From Account").pack(pady=5)
    ctk.CTkEntry(win, textvariable=from_var).pack()
    ctk.CTkLabel(win, text="To Account").pack(pady=5)
    ctk.CTkEntry(win, textvariable=to_var).pack()
    ctk.CTkLabel(win, text="Amount").pack(pady=5)
    ctk.CTkEntry(win, textvariable=amount_var).pack()

    def submit():
        try:
            sender, receiver = from_var.get(), to_var.get()
            amount = int(amount_var.get())
            s_user, r_user = get_user(sender), get_user(receiver)

            if not s_user or not r_user:
                messagebox.showerror("Error", "Invalid account(s)")
                return
            if s_user[3] < amount:
                messagebox.showerror("Error", "Insufficient balance")
                return

            update_balance(sender, s_user[3] - amount)
            update_balance(receiver, r_user[3] + amount)
            tg.add_transaction(sender, receiver, amount)
            messagebox.showinfo("Success", "Transaction successful.")
            win.destroy()
        except:
            messagebox.showerror("Error", "Invalid input")

    ctk.CTkButton(win, text="Transfer", command=submit).pack(pady=15)

def request_loan_ui():
    win = ctk.CTkToplevel(app)
    win.title("Request Loan")
    win.geometry("300x250")
    win.grab_set()

    acc_var = ctk.StringVar()
    amt_var = ctk.StringVar()

    ctk.CTkLabel(win, text="Account Number").pack(pady=5)
    ctk.CTkEntry(win, textvariable=acc_var).pack()
    ctk.CTkLabel(win, text="Loan Amount").pack(pady=5)
    ctk.CTkEntry(win, textvariable=amt_var).pack()

    def submit():
        acc, amt = acc_var.get(), int(amt_var.get())
        if not get_user(acc):
            messagebox.showerror("Error", "Account doesn't exist")
            return
        lm.request_loan(acc, amt)
        messagebox.showinfo("Success", "Loan request submitted.")
        win.destroy()

    ctk.CTkButton(win, text="Submit", command=submit).pack(pady=15)

def process_loan_ui():
    result = lm.process_loan()
    if result:
        acc, amt = result
        messagebox.showinfo("Loan Approved", f"₹{amt} approved for account {acc}.")
    else:
        messagebox.showinfo("No Pending Loans", "No loan requests available.")

def view_loans_ui():
    win = ctk.CTkToplevel(app)
    win.title("Loan Records")
    win.geometry("400x300")
    win.grab_set()
    for loan in lm.get_all_loans():
        text = f"Account: {loan[0]} | Amount: ₹{loan[1]} | Status: {loan[2]} | Date: {loan[3]}"
        ctk.CTkLabel(win, text=text, anchor="w").pack(fill="x", padx=5)

def detect_cycle_ui():
    if tg.detect_cycles():
        messagebox.showwarning("Cycle Detected", "Circular transaction found!")
    else:
        messagebox.showinfo("No Cycle", "No cycles detected.")


button_style = {"width": 220, "corner_radius": 10}
ctk.CTkButton(right_panel, text="Add User", command=add_user_ui, **button_style).pack(pady=8)
ctk.CTkButton(right_panel, text="Transfer Money", command=transfer_ui, **button_style).pack(pady=8)
ctk.CTkButton(right_panel, text="Request Loan", command=request_loan_ui, **button_style).pack(pady=8)
ctk.CTkButton(right_panel, text="Process Loan", command=process_loan_ui, **button_style).pack(pady=8)
ctk.CTkButton(right_panel, text="View Loans", command=view_loans_ui, **button_style).pack(pady=8)
ctk.CTkButton(right_panel, text="Detect Cycle", command=detect_cycle_ui, **button_style).pack(pady=8)
ctk.CTkButton(right_panel, text="Exit", command=app.quit, fg_color="#d9534f", hover_color="#c9302c", **button_style).pack(pady=15)


app.mainloop()
