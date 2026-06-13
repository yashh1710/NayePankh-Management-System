import tkinter as tk
from tkinter import ttk

from database import get_connection


class DashboardFrame(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        title = tk.Label(
            self,
            text="Dashboard",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=10)

        tk.Button(
            self,
            text="Refresh Dashboard",
            command=self.refresh_dashboard
        ).pack(pady=5)

        self.stats_frame = tk.Frame(self)
        self.stats_frame.pack(pady=10)

        self.cards = {}

        self.create_cards()

        # Recent Donations

        donation_title = tk.Label(
            self,
            text="Recent Donations",
            font=("Arial", 14, "bold")
        )

        donation_title.pack(pady=5)

        self.donation_tree = ttk.Treeview(
            self,
            columns=("Donor", "Amount"),
            show="headings",
            height=5
        )

        self.donation_tree.heading("Donor", text="Donor")
        self.donation_tree.heading("Amount", text="Amount")

        self.donation_tree.pack(
            fill="x",
            padx=20
        )

        # Recent Events

        event_title = tk.Label(
            self,
            text="Recent Events",
            font=("Arial", 14, "bold")
        )

        event_title.pack(pady=10)

        self.event_tree = ttk.Treeview(
            self,
            columns=("Event", "Date"),
            show="headings",
            height=5
        )

        self.event_tree.heading("Event", text="Event")
        self.event_tree.heading("Date", text="Date")

        self.event_tree.pack(
            fill="x",
            padx=20
        )

        self.refresh_dashboard()

    def create_cards(self):

        labels = [
            "Volunteers",
            "Beneficiaries",
            "Events",
            "Donations",
            "Donation Amount"
        ]

        for text in labels:

            card = tk.Frame(
                self.stats_frame,
                bd=2,
                relief="ridge",
                padx=20,
                pady=10
            )

            card.pack(
                side="left",
                padx=10
            )

            tk.Label(
                card,
                text=text,
                font=("Arial", 12, "bold")
            ).pack()

            value_label = tk.Label(
                card,
                text="0",
                font=("Arial", 16)
            )

            value_label.pack()

            self.cards[text] = value_label

    def get_count(self, table):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        count = cursor.fetchone()[0]

        conn.close()

        return count

    def get_total_amount(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT IFNULL(SUM(amount),0)
            FROM donations
            """
        )

        total = cursor.fetchone()[0]

        conn.close()

        return total

    def load_recent_donations(self):

        for row in self.donation_tree.get_children():
            self.donation_tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT donor_name, amount
            FROM donations
            ORDER BY id DESC
            LIMIT 5
            """
        )

        rows = cursor.fetchall()

        for row in rows:
            self.donation_tree.insert(
                "",
                tk.END,
                values=row
            )

        conn.close()

    def load_recent_events(self):

        for row in self.event_tree.get_children():
            self.event_tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT event_name, date
            FROM events
            ORDER BY id DESC
            LIMIT 5
            """
        )

        rows = cursor.fetchall()

        for row in rows:
            self.event_tree.insert(
                "",
                tk.END,
                values=row
            )

        conn.close()

    def refresh_dashboard(self):

        self.cards["Volunteers"].config(
            text=self.get_count("volunteers")
        )

        self.cards["Beneficiaries"].config(
            text=self.get_count("beneficiaries")
        )

        self.cards["Events"].config(
            text=self.get_count("events")
        )

        self.cards["Donations"].config(
            text=self.get_count("donations")
        )

        self.cards["Donation Amount"].config(
            text=f"₹{self.get_total_amount()}"
        )

        self.load_recent_donations()
        self.load_recent_events()