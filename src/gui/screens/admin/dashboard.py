import tkinter as tk
from gui.fonts import *
from gui.theme import *

def build_admin_dashboard(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)
    frame.configure(bg=COLORS["bg_main"])

    lbl = tk.Label(frame, text="Admin Dashboard", font=FONT_TITLE)
    lbl.pack(expand=True)
    lbl.configure(bg=COLORS["bg_main"], fg=COLORS["text"])

    return frame