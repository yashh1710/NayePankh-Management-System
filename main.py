import tkinter as tk

from database import initialize_database
from dashboard import DashboardFrame

initialize_database()

root = tk.Tk()

root.title(
    "NayePankh Foundation Management System"
)

root.geometry("1200x700")

root.configure(bg="white")

header = tk.Label(
    root,
    text="NayePankh Foundation Management System",
    font=("Arial",22,"bold"),
    bg="white"
)

header.pack(pady=15)

dashboard = DashboardFrame(root)
dashboard.pack(fill="both",expand=True)

root.mainloop()