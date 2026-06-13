import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from database import get_connection


class EventFrame(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.selected_id = None

        title = tk.Label(
            self,
            text="Event Management",
            font=("Arial", 18, "bold")
        )

        title.pack(pady=10)

        # ======================
        # FORM
        # ======================

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Event Name").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(form, text="Date").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(form, text="Location").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(form, text="Description").grid(row=3, column=0, padx=5, pady=5)

        self.event_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.description_var = tk.StringVar()

        tk.Entry(form, textvariable=self.event_var, width=40).grid(row=0, column=1)
        tk.Entry(form, textvariable=self.date_var, width=40).grid(row=1, column=1)
        tk.Entry(form, textvariable=self.location_var, width=40).grid(row=2, column=1)
        tk.Entry(form, textvariable=self.description_var, width=40).grid(row=3, column=1)

        # ======================
        # BUTTONS
        # ======================

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Add Event",
            command=self.add_event
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Update Event",
            command=self.update_event
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Delete Event",
            command=self.delete_event
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Clear",
            command=self.clear_fields
        ).pack(side="left", padx=5)

        # ======================
        # SEARCH
        # ======================

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
            command=self.search_event
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
                "Event Name",
                "Date",
                "Location",
                "Description"
            ),
            show="headings"
        )

        columns = [
            "ID",
            "Event Name",
            "Date",
            "Location",
            "Description"
        ]

        for col in columns:
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

    # ======================
    # LOAD
    # ======================

    def load_data(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM events")

        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        conn.close()

    # ======================
    # ADD
    # ======================

    def add_event(self):

        if not self.event_var.get():

            messagebox.showerror(
                "Error",
                "Event Name Required"
            )
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO events
            (event_name,date,location,description)
            VALUES(?,?,?,?)
            """,
            (
                self.event_var.get(),
                self.date_var.get(),
                self.location_var.get(),
                self.description_var.get()
            )
        )

        conn.commit()
        conn.close()

        self.load_data()
        self.clear_fields()

    # ======================
    # UPDATE
    # ======================

    def update_event(self):

        if self.selected_id is None:
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE events
            SET
            event_name=?,
            date=?,
            location=?,
            description=?
            WHERE id=?
            """,
            (
                self.event_var.get(),
                self.date_var.get(),
                self.location_var.get(),
                self.description_var.get(),
                self.selected_id
            )
        )

        conn.commit()
        conn.close()

        self.load_data()

    # ======================
    # DELETE
    # ======================

    def delete_event(self):

        selected = self.tree.selection()

        if not selected:
            return

        event_id = self.tree.item(
            selected[0]
        )["values"][0]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM events WHERE id=?",
            (event_id,)
        )

        conn.commit()
        conn.close()

        self.load_data()

    # ======================
    # SEARCH
    # ======================

    def search_event(self):

        keyword = self.search_var.get()

        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM events
            WHERE event_name LIKE ?
            """,
            (f"%{keyword}%",)
        )

        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        conn.close()

    # ======================
    # SELECT
    # ======================

    def select_record(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        row = self.tree.item(
            selected[0]
        )["values"]

        self.selected_id = row[0]

        self.event_var.set(row[1])
        self.date_var.set(row[2])
        self.location_var.set(row[3])
        self.description_var.set(row[4])

    # ======================
    # CLEAR
    # ======================

    def clear_fields(self):

        self.selected_id = None

        self.event_var.set("")
        self.date_var.set("")
        self.location_var.set("")
        self.description_var.set("")