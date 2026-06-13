import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from database import get_connection


class VolunteerFrame(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        title = tk.Label(
            self,
            text="Volunteer Management",
            font=("Arial", 18, "bold")
        )

        title.pack(pady=10)

        # ===================
        # FORM
        # ===================

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Name").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(form, text="Email").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(form, text="Phone").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(form, text="Skills").grid(row=3, column=0, padx=5, pady=5)
        tk.Label(form, text="Join Date").grid(row=4, column=0, padx=5, pady=5)

        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.skills_var = tk.StringVar()
        self.date_var = tk.StringVar()

        tk.Entry(form, textvariable=self.name_var).grid(row=0, column=1)
        tk.Entry(form, textvariable=self.email_var).grid(row=1, column=1)
        tk.Entry(form, textvariable=self.phone_var).grid(row=2, column=1)
        tk.Entry(form, textvariable=self.skills_var).grid(row=3, column=1)
        tk.Entry(form, textvariable=self.date_var).grid(row=4, column=1)

        # ===================
        # BUTTONS
        # ===================

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Add Volunteer",
            command=self.add_volunteer
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Delete Volunteer",
            command=self.delete_volunteer
        ).pack(side="left", padx=5)

        # ===================
        # SEARCH
        # ===================

        search_frame = tk.Frame(self)
        search_frame.pack()

        self.search_var = tk.StringVar()

        tk.Entry(
            search_frame,
            textvariable=self.search_var
        ).pack(side="left")

        tk.Button(
            search_frame,
            text="Search",
            command=self.search_volunteer
        ).pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="Show All",
            command=self.load_data
        ).pack(side="left")

        # ===================
        # TABLE
        # ===================

        self.tree = ttk.Treeview(
            self,
            columns=(
                "ID",
                "Name",
                "Email",
                "Phone",
                "Skills",
                "JoinDate"
            ),
            show="headings"
        )

        columns = [
            "ID",
            "Name",
            "Email",
            "Phone",
            "Skills",
            "JoinDate"
        ]

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.load_data()

    # ===================
    # LOAD DATA
    # ===================

    def load_data(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM volunteers")

        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        conn.close()

    # ===================
    # ADD
    # ===================

    def add_volunteer(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO volunteers
            (name,email,phone,skills,join_date)
            VALUES (?,?,?,?,?)
            """,
            (
                self.name_var.get(),
                self.email_var.get(),
                self.phone_var.get(),
                self.skills_var.get(),
                self.date_var.get()
            )
        )

        conn.commit()
        conn.close()

        self.load_data()

        messagebox.showinfo(
            "Success",
            "Volunteer Added Successfully"
        )

    # ===================
    # DELETE
    # ===================

    def delete_volunteer(self):

        selected = self.tree.selection()

        if not selected:
            return

        volunteer_id = self.tree.item(
            selected[0]
        )["values"][0]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM volunteers WHERE id=?",
            (volunteer_id,)
        )

        conn.commit()
        conn.close()

        self.load_data()

    # ===================
    # SEARCH
    # ===================

    def search_volunteer(self):

        keyword = self.search_var.get()

        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM volunteers
            WHERE name LIKE ?
            """,
            (f"%{keyword}%",)
        )

        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        conn.close()