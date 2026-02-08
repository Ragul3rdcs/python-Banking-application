import sqlite3
from datetime import datetime

# Database connection
conn = sqlite3.connect("Bank.db")
cur = conn.cursor()

# Create tables
cur.execute("""
CREATE TABLE IF NOT EXISTS accounts(
    acc_no INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    balance REAL,
    pin INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    acc_no INTEGER,
    type TEXT,
    amount REAL,
    date TEXT
)
""")
conn.commit()


# Create account
def create_account():
    name = input("Enter Name: ")
    phone = input("Enter Phone: ")
    pin = int(input("Set 4-digit PIN: "))
    balance = float(input("Initial Deposit: "))

    cur.execute(
        "INSERT INTO accounts(name,phone,balance,pin) VALUES(?,?,?,?)",
        (name, phone, balance, pin)
    )
    conn.commit()
    acc_no=cur.lastrowid
    print("\n✅ Account created successfully!")
    print(f"Your Account number is:{acc_no}")


# Login
def login():
    acc_no = int(input("Enter Account Number: "))
    pin = int(input("Enter PIN: "))
    cur.execute("SELECT * FROM accounts WHERE acc_no=? AND pin=?", (acc_no, pin))
    user = cur.fetchone()
    if user:
        print("\n✅ Login successful")
        return acc_no
    else:
        print("\n❌ Invalid account number or PIN")
        return None


# Deposit
def deposit(acc_no):
    amount = float(input("Enter amount to deposit: "))
    cur.execute("UPDATE accounts SET balance = balance + ? WHERE acc_no=?", (amount, acc_no))
    cur.execute("INSERT INTO transactions(acc_no,type,amount,date) VALUES(?,?,?,?)",
                (acc_no, "Deposit", amount, datetime.now()))
    conn.commit()
    print("✅ Amount deposited successfully")


# Withdraw
def withdraw(acc_no):
    amount = float(input("Enter amount to withdraw: "))
    cur.execute("SELECT balance FROM accounts WHERE acc_no=?", (acc_no,))
    balance = cur.fetchone()[0]

    if amount <= balance:
        cur.execute("UPDATE accounts SET balance = balance - ? WHERE acc_no=?", (amount, acc_no))
        cur.execute("INSERT INTO transactions(acc_no,type,amount,date) VALUES(?,?,?,?)",
                    (acc_no, "Withdraw", amount, datetime.now()))
        conn.commit()
        print("✅ Withdrawal successful")
    else:
        print("❌ Insufficient balance")


# Balance enquiry
def check_balance(acc_no):
    cur.execute("SELECT balance FROM accounts WHERE acc_no=?", (acc_no,))
    balance = cur.fetchone()[0]
    print(f"💰 Current Balance: ₹{balance}")


# Transaction history
def transaction_history(acc_no):
    cur.execute("SELECT type, amount, date FROM transactions WHERE acc_no=?", (acc_no,))
    records = cur.fetchall()
    print("\n--- Transaction History ---")
    for r in records:
        print(r[0], "| ₹", r[1], "|", r[2])


# Main menu
while True:
    print("\n🏦 BANKING APPLICATION")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")

    choice = input("Choose option: ")

    if choice == "1":
        create_account()

    elif choice == "2":
        acc = login()
        if acc:
            while True:
                print("\n1. Deposit")
                print("2. Withdraw")
                print("3. Balance Enquiry")
                print("4. Transaction History")
                print("5. Logout")

                ch = input("Select option: ")

                if ch == "1":
                    deposit(acc)
                elif ch == "2":
                    withdraw(acc)
                elif ch == "3":
                    check_balance(acc)
                elif ch == "4":
                    transaction_history(acc)
                elif ch == "5":
                    break
                else:
                    print("Invalid choice")

    elif choice == "3":
        print("Thank you for using banking system")
        break

    else:
        print("Invalid option")
