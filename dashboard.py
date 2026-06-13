import tkinter as tk
from database import get_connection

class DashboardFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.configure(bg="white")

        title = tk.Label(
            self,
            text="NayePankh Foundation Dashboard",
            font=("Arial",20,"bold"),
            bg="white"
        )
        title.pack(pady=20)

        self.stats_frame = tk.Frame(self,bg="white")
        self.stats_frame.pack()

        self.refresh_dashboard()

    def get_count(self, table):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]

        conn.close()

        return count

    def get_total_donations(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT IFNULL(SUM(amount),0) FROM donations"
        )

        total = cursor.fetchone()[0]

        conn.close()

        return total

    def refresh_dashboard(self):

        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        stats = [
            ("Volunteers", self.get_count("volunteers")),
            ("Beneficiaries", self.get_count("beneficiaries")),
            ("Events", self.get_count("events")),
            ("Donations", self.get_count("donations")),
            ("Total Amount", f"₹{self.get_total_donations()}")
        ]

        for title,value in stats:

            card = tk.Frame(
                self.stats_frame,
                bg="#f5f5f5",
                bd=2,
                relief="ridge"
            )

            card.pack(
                side="left",
                padx=10,
                pady=10
            )

            tk.Label(
                card,
                text=title,
                font=("Arial",14,"bold"),
                bg="#f5f5f5"
            ).pack(padx=20,pady=10)

            tk.Label(
                card,
                text=value,
                font=("Arial",16),
                bg="#f5f5f5"
            ).pack(pady=10)