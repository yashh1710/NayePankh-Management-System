import tkinter as tk
from tkinter import messagebox
import pandas as pd

from database import get_connection


class ReportFrame(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        title = tk.Label(
            self,
            text="Report Generation",
            font=("Arial", 18, "bold")
        )

        title.pack(pady=20)

        tk.Button(
            self,
            text="Export Volunteers CSV",
            width=30,
            command=self.export_volunteers_csv
        ).pack(pady=5)

        tk.Button(
            self,
            text="Export Beneficiaries CSV",
            width=30,
            command=self.export_beneficiaries_csv
        ).pack(pady=5)

        tk.Button(
            self,
            text="Export Donations CSV",
            width=30,
            command=self.export_donations_csv
        ).pack(pady=5)

        tk.Button(
            self,
            text="Export Events CSV",
            width=30,
            command=self.export_events_csv
        ).pack(pady=5)

        tk.Label(
            self,
            text="Excel Reports",
            font=("Arial", 14, "bold")
        ).pack(pady=20)

        tk.Button(
            self,
            text="Export Volunteers Excel",
            width=30,
            command=self.export_volunteers_excel
        ).pack(pady=5)

        tk.Button(
            self,
            text="Export Beneficiaries Excel",
            width=30,
            command=self.export_beneficiaries_excel
        ).pack(pady=5)

        tk.Button(
            self,
            text="Export Donations Excel",
            width=30,
            command=self.export_donations_excel
        ).pack(pady=5)

        tk.Button(
            self,
            text="Export Events Excel",
            width=30,
            command=self.export_events_excel
        ).pack(pady=5)

    # ==========================
    # CSV EXPORTS
    # ==========================

    def export_volunteers_csv(self):

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM volunteers",
            conn
        )

        df.to_csv(
            "reports/volunteers.csv",
            index=False
        )

        conn.close()

        messagebox.showinfo(
            "Success",
            "Volunteer CSV Exported"
        )

    def export_beneficiaries_csv(self):

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM beneficiaries",
            conn
        )

        df.to_csv(
            "reports/beneficiaries.csv",
            index=False
        )

        conn.close()

        messagebox.showinfo(
            "Success",
            "Beneficiary CSV Exported"
        )

    def export_donations_csv(self):

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM donations",
            conn
        )

        df.to_csv(
            "reports/donations.csv",
            index=False
        )

        conn.close()

        messagebox.showinfo(
            "Success",
            "Donations CSV Exported"
        )

    def export_events_csv(self):

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM events",
            conn
        )

        df.to_csv(
            "reports/events.csv",
            index=False
        )

        conn.close()

        messagebox.showinfo(
            "Success",
            "Events CSV Exported"
        )

    # ==========================
    # EXCEL EXPORTS
    # ==========================

    def export_volunteers_excel(self):

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM volunteers",
            conn
        )

        df.to_excel(
            "reports/volunteers.xlsx",
            index=False
        )

        conn.close()

        messagebox.showinfo(
            "Success",
            "Volunteer Excel Exported"
        )

    def export_beneficiaries_excel(self):

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM beneficiaries",
            conn
        )

        df.to_excel(
            "reports/beneficiaries.xlsx",
            index=False
        )

        conn.close()

        messagebox.showinfo(
            "Success",
            "Beneficiary Excel Exported"
        )

    def export_donations_excel(self):

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM donations",
            conn
        )

        df.to_excel(
            "reports/donations.xlsx",
            index=False
        )

        conn.close()

        messagebox.showinfo(
            "Success",
            "Donations Excel Exported"
        )

    def export_events_excel(self):

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM events",
            conn
        )

        df.to_excel(
            "reports/events.xlsx",
            index=False
        )

        conn.close()

        messagebox.showinfo(
            "Success",
            "Events Excel Exported"
        )