import tkinter as tk
from src.gui.theme import *


def build_stat_card(parent, title, value, color):
    card = tk.Frame(parent)
    card.pack(side="left", fill="both", expand=True, padx=(0, 8))
    card.configure(bg=COLORS["bg_sidebar"],highlightbackground=COLORS["border"],highlightthickness=1)

    inner = tk.Frame(card)
    inner.pack(fill="both", expand=True, padx=16, pady=14)
    inner.configure(bg=COLORS["bg_sidebar"])

    title_lbl = tk.Label(inner, text=title, font=FONT_SMALL)
    title_lbl.pack(anchor="w")
    title_lbl.configure(bg=COLORS["bg_sidebar"], fg=COLORS["muted"])

    value_lbl = tk.Label(inner, text=value, font=FONT_TITLE)
    value_lbl.pack(anchor="w", pady=(6, 0))
    value_lbl.configure(bg=COLORS["bg_sidebar"], fg=color)

    return card