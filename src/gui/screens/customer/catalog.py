import tkinter as tk
from src.gui.fonts import *
from src.gui.theme import *

def build_catalog_screen(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)
    frame.configure(bg=COLORS["bg_main"])

    lbl = tk.Label(frame, text="📋 Katalog leków", font=FONT_TITLE)
    lbl.pack(expand=True)
    lbl.configure(bg=COLORS["bg_main"], fg=COLORS["accent"])

    return frame