import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from database import get_connection


class BeneficiaryFrame(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.selected_id = None

        title = tk.Label(
            self,
            text="Beneficiary Management",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        # ======================
        # FORM
        # ======================

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Name").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(form, text="Age").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(form, text="Education").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(form, text="Location").grid(row=3, column=0, padx=5, pady=5)
        tk.Label(form, text="Program").grid(row=4, column=0, padx=5, pady=5)

        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.education_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.program_var = tk.StringVar()

        tk.Entry(form, textvariable=self.name_var, width=30).grid(row=0, column=1)
        tk.Entry(form, textvariable=self.age_var, width=30).grid(row=1, column=1)
        tk.Entry(form, textvariable=self.education_var, width=30).grid(row=2, column=1)
        tk.Entry(form, textvariable=self.location_var, width=30).grid(row=3, column=1)
        tk.Entry(form, textvariable=self.program_var, width=30).grid(row=4, column=1)

        # Buttons

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add", width=12,
                  command=self.add_beneficiary).pack(side="left", padx=5)

        tk.Button(btn_frame, text="Update", width=12,
                  command=self.update_beneficiary).pack(side="left", padx=5)

        tk.Button(btn_frame, text="Delete", width=12,
                  command=self.delete_beneficiary).pack(side="left", padx=5)

        tk.Button(btn_frame, text="Clear", width=12,
                  command=self.clear_fields).pack(side="left", padx=5)

        # Search

        search_frame = tk.Frame(self)
        search_frame.pack()

        self.search_var = tk.StringVar()

        tk.Entry(search_frame,
                 textvariable=self.search_var,
                 width=30).pack(side="left")

        tk.Button(search_frame,
                  text="Search",
                  command=self.search_beneficiary).pack(side="left", padx=5)

        tk.Button(search_frame,
                  text="Show All",
                  command=self.load_data).pack(side="left")

        # Table

        self.tree = ttk.Treeview(
            self,
            columns=(
                "ID",
                "Name",
                "Age",
                "Education",
                "Location",
                "Program"
            ),
            show="headings"
        )

        cols = [
            "ID",
            "Name",
            "Age",
            "Education",
            "Location",
            "Program"
        ]

        for col in cols:
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both",
                       expand=True,
                       padx=10,
                       pady=10)

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_record
        )

        self.load_data()

    def load_data(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM beneficiaries"
        )

        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        conn.close()

    def add_beneficiary(self):

        if not self.name_var.get():

            messagebox.showerror(
                "Error",
                "Name Required"
            )
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO beneficiaries
            (name,age,education,location,program)
            VALUES(?,?,?,?,?)
            """,
            (
                self.name_var.get(),
                self.age_var.get(),
                self.education_var.get(),
                self.location_var.get(),
                self.program_var.get()
            )
        )

        conn.commit()
        conn.close()

        self.load_data()
        self.clear_fields()

    def update_beneficiary(self):

        if self.selected_id is None:
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE beneficiaries
            SET
            name=?,
            age=?,
            education=?,
            location=?,
            program=?
            WHERE id=?
            """,
            (
                self.name_var.get(),
                self.age_var.get(),
                self.education_var.get(),
                self.location_var.get(),
                self.program_var.get(),
                self.selected_id
            )
        )

        conn.commit()
        conn.close()

        self.load_data()

    def delete_beneficiary(self):

        selected = self.tree.selection()

        if not selected:
            return

        beneficiary_id = self.tree.item(
            selected[0]
        )["values"][0]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM beneficiaries WHERE id=?",
            (beneficiary_id,)
        )

        conn.commit()
        conn.close()

        self.load_data()

    def search_beneficiary(self):

        keyword = self.search_var.get()

        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM beneficiaries
            WHERE name LIKE ?
            """,
            (f"%{keyword}%",)
        )

        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        conn.close()

    def select_record(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        row = self.tree.item(
            selected[0]
        )["values"]

        self.selected_id = row[0]

        self.name_var.set(row[1])
        self.age_var.set(row[2])
        self.education_var.set(row[3])
        self.location_var.set(row[4])
        self.program_var.set(row[5])

    def clear_fields(self):

        self.selected_id = None

        self.name_var.set("")
        self.age_var.set("")
        self.education_var.set("")
        self.location_var.set("")
        self.program_var.set("")