
import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"


def load_transactions():
    transactions = []

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append(row)

    return transactions


def save_transactions(transactions):
    fields = ["date", "type", "category", "amount"]

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(transactions)


def add_transaction(transactions):
    kind = input("Enter type (income/expense): ").strip().lower()

    if kind not in ["income", "expense"]:
        print("Enter income or expense.")
        return

    category = input("Enter category: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    try:
        amount = float(input("Enter amount in rupees: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

    except ValueError:
        print("Please enter a valid amount.")
        return

    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()

    if not date:
        date = datetime.today().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")
            return

    transactions.append({
        "date": date,
        "type": kind,
        "category": category,
        "amount": f"{amount:.2f}"
    })

    save_transactions(transactions)
    print("Transaction saved successfully!")


def view_transactions(transactions):
    if not transactions:
        print("No transactions found.")
        return

    print("\n--- All Transactions ---")

    for item in transactions:
        print(
            item["date"],
            "|", item["type"],
            "|", item["category"],
            "| Rs.", item["amount"]
        )


def monthly_summary(transactions):
    month = input("Enter month (YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format.")
        return

    income = 0.0
    expenses = 0.0

    for item in transactions:
        if item["date"].startswith(month):
            amount = float(item["amount"])

            if item["type"] == "income":
                income += amount
            else:
                expenses += amount

    print("\n--- Monthly Summary ---")
    print("Month:", month)
    print(f"Total income: Rs. {income:.2f}")
    print(f"Total expenses: Rs. {expenses:.2f}")
    print(f"Balance: Rs. {income - expenses:.2f}")


def export_csv(transactions):
    if not transactions:
        print("No transactions to export.")
        return

    export_file = "expense_export.csv"
    fields = ["date", "type", "category", "amount"]

    with open(export_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(transactions)

    print("Export completed:", export_file)


def main():
    transactions = load_transactions()

    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Monthly Summary")
        print("4. Export CSV")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            view_transactions(transactions)
        elif choice == "3":
            monthly_summary(transactions)
        elif choice == "4":
            export_csv(transactions)
        elif choice == "5":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Select 1 to 5.")


if __name__ == "__main__":
    main()