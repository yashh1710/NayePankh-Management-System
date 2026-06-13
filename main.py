import tkinter as tk

from modules.beneficiaries import BeneficiaryFrame

from database import initialize_database
from dashboard import DashboardFrame
from modules.volunteer import VolunteerFrame
from modules.donation import DonationFrame
from modules.event import EventFrame
from modules.report import ReportFrame



initialize_database()

root = tk.Tk()

root.title("NayePankh Foundation Management System")
root.geometry("1300x750")
root.configure(bg="white")

# ==========================
# HEADER
# ==========================

header = tk.Label(
    root,
    text="NayePankh Foundation Management System",
    font=("Arial", 22, "bold"),
    bg="#2C3E50",
    fg="white",
    pady=15
)

header.pack(fill="x")

# ==========================
# MAIN CONTAINER
# ==========================

main_container = tk.Frame(root)
main_container.pack(fill="both", expand=True)

# ==========================
# SIDEBAR
# ==========================

sidebar = tk.Frame(
    main_container,
    bg="#34495E",
    width=220
)

sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

# ==========================
# CONTENT AREA
# ==========================

content = tk.Frame(
    main_container,
    bg="white"
)

content.pack(side="right", fill="both", expand=True)

# ==========================
# FRAME SWITCHER
# ==========================

current_frame = None

def show_frame(frame_class):

    global current_frame

    if current_frame:
        current_frame.destroy()

    current_frame = frame_class(content)
    current_frame.pack(fill="both", expand=True)

# ==========================
# SIDEBAR BUTTONS
# ==========================

btn_style = {
    "font": ("Arial", 12, "bold"),
    "bg": "#34495E",
    "fg": "white",
    "activebackground": "#2C3E50",
    "activeforeground": "white",
    "bd": 0,
    "pady": 12
}

dashboard_btn = tk.Button(
    sidebar,
    text="Dashboard",
    command=lambda: show_frame(DashboardFrame),
    **btn_style
)

dashboard_btn.pack(fill="x")

volunteer_btn = tk.Button(
    sidebar,
    text="Volunteers",
    command=lambda: show_frame(VolunteerFrame),
    **btn_style
)

volunteer_btn.pack(fill="x")

# Future Modules

beneficiary_btn = tk.Button(
    sidebar,
    text="Beneficiaries",
    command=lambda: show_frame(BeneficiaryFrame),
    **btn_style
)

beneficiary_btn.pack(fill="x")

donation_btn = tk.Button(
    sidebar,
    text="Donations",
    command=lambda: show_frame(DonationFrame),
    **btn_style
)

donation_btn.pack(fill="x")

event_btn = tk.Button(
    sidebar,
    text="Events",
    command=lambda: show_frame(EventFrame),
    **btn_style
)

event_btn.pack(fill="x")

report_btn = tk.Button(
    sidebar,
    text="Reports",
    command=lambda: show_frame(ReportFrame),
    **btn_style
)

report_btn.pack(fill="x")

exit_btn = tk.Button(
    sidebar,
    text="Exit",
    command=root.destroy,
    **btn_style
)

exit_btn.pack(fill="x")

# Default Page

show_frame(DashboardFrame)

root.mainloop()