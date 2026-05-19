import tkinter as tk
from src.gui.fonts import *
from src.gui.theme import *

def build_stats_screen(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)
    frame.configure(bg=COLORS["bg_main"])

    lbl = tk.Label(frame, text="📊 Statystyki", font=FONT_TITLE)
    lbl.pack(expand=True)
    lbl.configure(bg=COLORS["bg_main"], fg=COLORS["warn"])

    return frame