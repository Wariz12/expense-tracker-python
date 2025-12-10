import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from data_manager import ExpenseManager
import csv
from datetime import datetime

class ExpenseTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("700x650")

        self.manager = ExpenseManager()

        # ------------------------------
        # THEME COLORS
        # ------------------------------
        BG = "#F1F7F5"         # Soft mint background
        CARD = "#FFFFFF"       # White panels/cards
        ACCENT = "#6C9987"     # Teal accent
        BUTTON = "#8CC4B9"     # Light teal buttons
        TEXT = "#000000"       # Black text
        # ------------------------------

        self.root.configure(bg=BG)

        style = ttk.Style()
        style.theme_use("clam")

        # Frame styling
        style.configure("Card.TFrame", background=CARD)
        style.configure("Main.TFrame", background=BG)

        # Label styling
        style.configure("Title.TLabel", font=("Arial", 16, "bold"), background=CARD, foreground=ACCENT)
        style.configure("TLabel", background=CARD)

        # Entry styling
        style.configure("TEntry", fieldbackground="white", background="white")

        # Button styling
        style.configure("TButton",
                        font=("Arial", 11, "bold"),
                        padding=6)
        
        # ------------------------------
        # MAIN AREA
        # ------------------------------
        self.main_frame = ttk.Frame(root, style="Main.TFrame", padding=20)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Card container
        self.card = ttk.Frame(self.main_frame, style="Card.TFrame", padding=20)
        self.card.grid(row=0, column=0, sticky="nsew")

        # Title
        ttk.Label(self.card, text="Add New Expense", style="Title.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Input fields
        ttk.Label(self.card, text="Date (MM/DD):").grid(row=1, column=0, sticky="w")
        self.date_entry = ttk.Entry(self.card)
        self.date_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.card, text="Category:").grid(row=2, column=0, sticky="w")
        self.category_entry = ttk.Entry(self.card)
        self.category_entry.grid(row=2, column=1, pady=5)

        ttk.Label(self.card, text="Amount:").grid(row=3, column=0, sticky="w")
        self.amount_entry = ttk.Entry(self.card)
        self.amount_entry.grid(row=3, column=1, pady=5)

        ttk.Label(self.card, text="Notes:").grid(row=4, column=0, sticky="w")
        self.notes_entry = ttk.Entry(self.card)
        self.notes_entry.grid(row=4, column=1, pady=5)

        # Add button
        self.add_button = ttk.Button(self.card, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=5, column=0, columnspan=2, pady=15)

        # Expense List Title
        ttk.Label(self.card, text="Expense List", style="Title.TLabel").grid(row=6, column=0, columnspan=2, pady=20)

        # Treeview
        columns = ("date", "category", "amount", "notes")
        self.tree = ttk.Treeview(self.card, columns=columns, show="headings", height=10)

        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=130)

        self.tree.grid(row=7, column=0, columnspan=2, pady=(0, 10))

        self.load_tree()

        # Buttons row
        self.button_frame = ttk.Frame(self.card, style="Card.TFrame")
        self.button_frame.grid(row=8, column=0, columnspan=2, pady=10)

        # Delete button
        ttk.Button(self.button_frame, text="Delete Selected", command=self.delete_selected).grid(row=0, column=0, padx=5)

        # Analysis button
        ttk.Button(self.button_frame, text="Show Analysis", command=self.show_analysis).grid(row=0, column=1, padx=5)

        # Export button
        ttk.Button(self.button_frame, text="Export to CSV", command=self.export_csv).grid(row=0, column=2, padx=5)

    # ----------------------------------
    # LOAD TREEVIEW
    # ----------------------------------
    def load_tree(self):
        for exp in self.manager.expenses:
            self.tree.insert("", "end", values=(exp["date"], exp["category"], exp["amount"], exp["notes"]))

    # ----------------------------------
    # ADD EXPENSE
    # ----------------------------------
    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        notes = self.notes_entry.get()

        success, msg = self.manager.add_expense(date, category, amount, notes)

        if not success:
            messagebox.showerror("Error", msg)
            return

        self.tree.insert("", "end", values=(date, category, amount, notes))
        messagebox.showinfo("Success", "Expense added!")

        self.date_entry.delete(0, "end")
        self.category_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")
        self.notes_entry.delete(0, "end")

    # ----------------------------------
    # DELETE
    # ----------------------------------
    def delete_selected(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showerror("Error", "No item selected.")
            return

        index = self.tree.index(selected[0])
        ok = self.manager.delete_expense(index)

        if ok:
            self.tree.delete(selected[0])
            messagebox.showinfo("Deleted", "Expense deleted.")
        else:
            messagebox.showerror("Error", "Unable to delete.")

    # ----------------------------------
    # ANALYSIS
    # ----------------------------------
    def show_analysis(self):
        totals = self.manager.get_category_totals()
        total_spent = self.manager.get_total_spent()
        largest = self.manager.get_largest_expense()

        message = "Category Totals:\n"
        for cat, amount in totals.items():
            message += f"- {cat}: ${amount:.2f}\n"

        message += f"\nTotal Spent: ${total_spent:.2f}"

        if largest:
            message += f"\n\nLargest Expense:\n{largest['category']} - ${largest['amount']:.2f}"

        messagebox.showinfo("Analysis", message)

    # ----------------------------------
    # EXPORT CSV
    # ----------------------------------
    def export_csv(self):
        filename = f"expenses_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=filename,
            filetypes=[("CSV Files", "*.csv")]
        )

        if not filepath:
            return

        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Category", "Amount", "Notes"])

            for exp in self.manager.expenses:
                writer.writerow([exp["date"], exp["category"], exp["amount"], exp["notes"]])

        messagebox.showinfo("Exported", f"Saved to:\n{filepath}")