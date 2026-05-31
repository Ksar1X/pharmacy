import tkinter as tk
from src.gui.theme import *


def build_topbar(parent, role, on_nav=None):

    topbar = tk.Frame(parent, height=80)
    topbar.pack(side="top", fill="x")
    topbar.pack_propagate(False)
    topbar.configure(bg=COLORS["bg_topbar"])

    logo_frame = tk.Frame(topbar)
    logo_frame.pack(side="left", padx=16)
    logo_frame.configure(bg=COLORS["bg_topbar"])

    pharma = tk.Label(logo_frame, text="Pharma", font=FONT_LOGO)
    pharma.pack(side="left")
    pharma.configure(fg=COLORS["accent"], bg=COLORS["bg_topbar"])

    care = tk.Label(logo_frame, text="Care", font=FONT_LOGO)
    care.pack(side="left")
    care.configure(fg=COLORS["text"], bg=COLORS["bg_topbar"])

    if on_nav:
        dash_btn = tk.Button(
            topbar,
            text="🏠 Dashboard",
            font=FONT_SMALL,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda: on_nav("Dashboard")
        )
        dash_btn.pack(side="left", padx=(24, 0))
        dash_btn.configure(bg=COLORS["bg_topbar"], fg=COLORS["muted"])

        dash_btn.bind("<Enter>", lambda e: dash_btn.configure(fg=COLORS["text"]))
        dash_btn.bind("<Leave>", lambda e: dash_btn.configure(fg=COLORS["muted"]))

    role_frame = tk.Frame(topbar)
    role_frame.pack(side="right", padx=16)
    role_frame.configure(bg=COLORS["bg_topbar"])

    tb.Button(role_frame, text=role.upper(), style="my.TButton", padding=(12, 4)).pack()

    return topbar