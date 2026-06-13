import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from database import get_connection


class DonationFrame(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.selected_id = None

        title = tk.Label(
            self,
            text="Donation Management",
            font=("Arial", 18, "bold")
        )

        title.pack(pady=10)

        # =====================
        # FORM
        # =====================

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Donor Name").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(form, text="Amount").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(form, text="Date").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(form, text="Purpose").grid(row=3, column=0, padx=5, pady=5)

        self.donor_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.purpose_var = tk.StringVar()

        tk.Entry(form, textvariable=self.donor_var, width=30).grid(row=0, column=1)
        tk.Entry(form, textvariable=self.amount_var, width=30).grid(row=1, column=1)
        tk.Entry(form, textvariable=self.date_var, width=30).grid(row=2, column=1)
        tk.Entry(form, textvariable=self.purpose_var, width=30).grid(row=3, column=1)

        # =====================
        # BUTTONS
        # =====================

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Add Donation",
            command=self.add_donation
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Update Donation",
            command=self.update_donation
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Delete Donation",
            command=self.delete_donation
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Clear",
            command=self.clear_fields
        ).pack(side="left", padx=5)

        # =====================
        # SEARCH
        # =====================

        search_frame = tk.Frame(self)
        search_frame.pack()

        self.search_var = tk.StringVar()

        tk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=30
        ).pack(side="left")

        tk.Button(
            search_frame,
            text="Search",
            command=self.search_donation
        ).pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="Show All",
            command=self.load_data
        ).pack(side="left")

        # =====================
        # TOTAL DONATIONS
        # =====================

        self.total_label = tk.Label(
            self,
            text="Total Donations: ₹0",
            font=("Arial", 12, "bold")
        )

        self.total_label.pack(pady=10)

        # =====================
        # TABLE
        # =====================

        self.tree = ttk.Treeview(
            self,
            columns=(
                "ID",
                "Donor",
                "Amount",
                "Date",
                "Purpose"
            ),
            show="headings"
        )

        cols = [
            "ID",
            "Donor",
            "Amount",
            "Date",
            "Purpose"
        ]

        for col in cols:
            self.tree.heading(col, text=col)

        self.tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_record
        )

        self.load_data()

    # =====================
    # LOAD DATA
    # =====================

    def load_data(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM donations"
        )

        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        cursor.execute(
            "SELECT IFNULL(SUM(amount),0) FROM donations"
        )

        total = cursor.fetchone()[0]

        self.total_label.config(
            text=f"Total Donations: ₹{total}"
        )

        conn.close()

    # =====================
    # ADD
    # =====================

    def add_donation(self):

        if not self.donor_var.get():

            messagebox.showerror(
                "Error",
                "Donor Name Required"
            )
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO donations
            (donor_name,amount,date,purpose)
            VALUES (?,?,?,?)
            """,
            (
                self.donor_var.get(),
                self.amount_var.get(),
                self.date_var.get(),
                self.purpose_var.get()
            )
        )

        conn.commit()
        conn.close()

        self.load_data()
        self.clear_fields()

    # =====================
    # UPDATE
    # =====================

    def update_donation(self):

        if self.selected_id is None:
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE donations
            SET
            donor_name=?,
            amount=?,
            date=?,
            purpose=?
            WHERE id=?
            """,
            (
                self.donor_var.get(),
                self.amount_var.get(),
                self.date_var.get(),
                self.purpose_var.get(),
                self.selected_id
            )
        )

        conn.commit()
        conn.close()

        self.load_data()

    # =====================
    # DELETE
    # =====================

    def delete_donation(self):

        selected = self.tree.selection()

        if not selected:
            return

        donation_id = self.tree.item(
            selected[0]
        )["values"][0]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM donations WHERE id=?",
            (donation_id,)
        )

        conn.commit()
        conn.close()

        self.load_data()

    # =====================
    # SEARCH
    # =====================

    def search_donation(self):

        keyword = self.search_var.get()

        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM donations
            WHERE donor_name LIKE ?
            """,
            (f"%{keyword}%",)
        )

        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        conn.close()

    # =====================
    # SELECT RECORD
    # =====================

    def select_record(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        row = self.tree.item(
            selected[0]
        )["values"]

        self.selected_id = row[0]

        self.donor_var.set(row[1])
        self.amount_var.set(row[2])
        self.date_var.set(row[3])
        self.purpose_var.set(row[4])

    # =====================
    # CLEAR
    # =====================

    def clear_fields(self):

        self.selected_id = None

        self.donor_var.set("")
        self.amount_var.set("")
        self.date_var.set("")
        self.purpose_var.set("")