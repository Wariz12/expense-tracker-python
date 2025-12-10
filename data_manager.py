import json
import os

class ExpenseManager:
    def __init__(self):
        self.filename = "expenses.json"
        self.expenses = []
        self.load_expenses()

    def add_expense(self, date, category, amount, notes):
        try:
            amount = float(amount)
        except:
            return False, "Amount must be a number."

        if date.strip() == "" or category.strip() == "":
            return False, "Date and Category are required."

        expense = {
            "date": date,
            "category": category,
            "amount": amount,
            "notes": notes
        }

        self.expenses.append(expense)
        self.save_expenses()
        return True, "Added"

    def delete_expense(self, index):
        if 0 <= index < len(self.expenses):
            del self.expenses[index]
            self.save_expenses()
            return True
        return False

    def save_expenses(self):
        with open(self.filename, "w") as f:
            json.dump(self.expenses, f, indent=4)

    def load_expenses(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.expenses = json.load(f)
        else:
            self.expenses = []

    def get_category_totals(self):
        totals = {}
        for e in self.expenses:
            cat = e["category"]
            totals[cat] = totals.get(cat, 0) + e["amount"]
        return totals

    def get_total_spent(self):
        return sum(e["amount"] for e in self.expenses)

    def get_largest_expense(self):
        if not self.expenses:
            return None
        return max(self.expenses, key=lambda x: x["amount"])