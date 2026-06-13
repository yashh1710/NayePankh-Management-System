import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from database import get_connection


class VolunteerFrame(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.selected_id = None

        title = tk.Label(
            self,
            text="Volunteer Management",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        # ======================
        # FORM
        # ======================

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

        tk.Entry(form, textvariable=self.name_var, width=30).grid(row=0, column=1)
        tk.Entry(form, textvariable=self.email_var, width=30).grid(row=1, column=1)
        tk.Entry(form, textvariable=self.phone_var, width=30).grid(row=2, column=1)
        tk.Entry(form, textvariable=self.skills_var, width=30).grid(row=3, column=1)
        tk.Entry(form, textvariable=self.date_var, width=30).grid(row=4, column=1)

        # ======================
        # BUTTONS
        # ======================

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Add Volunteer",
            width=15,
            command=self.add_volunteer
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Update Volunteer",
            width=15,
            command=self.update_volunteer
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Delete Volunteer",
            width=15,
            command=self.delete_volunteer
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Clear",
            width=15,
            command=self.clear_fields
        ).pack(side="left", padx=5)

        # ======================
        # SEARCH
        # ======================

        search_frame = tk.Frame(self)
        search_frame.pack(pady=5)

        self.search_var = tk.StringVar()

        tk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=30
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

        # ======================
        # TABLE
        # ======================

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

        self.tree.column("ID", width=50)
        self.tree.column("Name", width=180)
        self.tree.column("Email", width=220)
        self.tree.column("Phone", width=120)
        self.tree.column("Skills", width=180)
        self.tree.column("JoinDate", width=120)

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

    # ======================
    # LOAD DATA
    # ======================

    def load_data(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM volunteers"
        )

        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        conn.close()

    # ======================
    # ADD
    # ======================

    def add_volunteer(self):

        if not self.name_var.get():

            messagebox.showerror(
                "Error",
                "Volunteer Name Required"
            )
            return

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
        self.clear_fields()

        messagebox.showinfo(
            "Success",
            "Volunteer Added Successfully"
        )

    # ======================
    # UPDATE
    # ======================

    def update_volunteer(self):

        if self.selected_id is None:

            messagebox.showerror(
                "Error",
                "Select a volunteer first"
            )
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE volunteers
            SET
            name=?,
            email=?,
            phone=?,
            skills=?,
            join_date=?
            WHERE id=?
            """,
            (
                self.name_var.get(),
                self.email_var.get(),
                self.phone_var.get(),
                self.skills_var.get(),
                self.date_var.get(),
                self.selected_id
            )
        )

        conn.commit()
        conn.close()

        self.load_data()

        messagebox.showinfo(
            "Success",
            "Volunteer Updated Successfully"
        )

    # ======================
    # DELETE
    # ======================

    def delete_volunteer(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showerror(
                "Error",
                "Select a volunteer first"
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete selected volunteer?"
        )

        if not confirm:
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
        self.clear_fields()

        messagebox.showinfo(
            "Deleted",
            "Volunteer Deleted Successfully"
        )

    # ======================
    # SEARCH
    # ======================

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

    # ======================
    # SELECT RECORD
    # ======================

    def select_record(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        row = self.tree.item(selected[0])["values"]

        self.selected_id = row[0]

        self.name_var.set(row[1])
        self.email_var.set(row[2])
        self.phone_var.set(row[3])
        self.skills_var.set(row[4])
        self.date_var.set(row[5])

    # ======================
    # CLEAR
    # ======================

    def clear_fields(self):

        self.selected_id = None

        self.name_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.skills_var.set("")
        self.date_var.set("")