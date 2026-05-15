import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from gui.fonts import *
from gui.theme import *


def build_topbar(parent, role):
    topbar = tk.Frame(parent, height=80)
    topbar.pack(side="top", fill="x")
    topbar.pack_propagate(False)
    topbar.configure(bg=COLORS["bg_topbar"])

    # Логотип
    logo_frame = tk.Frame(topbar)
    logo_frame.pack(side="left", padx=16)
    logo_frame.configure(bg=COLORS["bg_topbar"])

    pharma = tk.Label(logo_frame, text="Pharma", font=FONT_LOGO)
    pharma.pack(side="left")
    pharma.configure(fg=COLORS["accent"], bg=COLORS["bg_topbar"])

    care = tk.Label(logo_frame, text="Care", font=FONT_LOGO)
    care.pack(side="left")
    care.configure(fg=COLORS["text"], bg=COLORS["bg_topbar"])

    # Кнопка роли справа
    role_frame = tk.Frame(topbar)
    role_frame.pack(side="right", padx=16)
    role_frame.configure(bg=COLORS["bg_topbar"])

    tb.Button(
        role_frame,
        text=role.upper(),
        bootstyle=SUCCESS,
        padding=(12, 4)
    ).pack()

    return topbar