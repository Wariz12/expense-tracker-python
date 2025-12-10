import tkinter as tk
from gui import ExpenseTrackerGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()