import tkinter as tk
import ttkbootstrap as tb

from src.gui.components import build_drug_table
from src.gui.fonts import *
from src.gui.theme import *

def build_drugs_screen(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)
    frame.configure(bg=COLORS["bg_main"])

    header = tk.Frame(frame)
    header.pack(fill="x", pady=(0, 20))
    header.configure(bg=COLORS["bg_main"])

    title = tk.Label(header, text="💊 Leki", font=FONT_TITLE)
    title.pack(side="left", anchor="w")
    title.configure(bg=COLORS["bg_main"], fg=COLORS["accent"])

    tb.Button(
        header,
        text="+ Dodaj lek",
        bootstyle="accent",
        padding=(12, 6)
    ).pack(side="right")

    rows = [
        ("#0021", "Apap Forte 500mg", "12,99 zł", "240", "Bez recepty", "Dostępny"),
        ("#0034", "Amoxicillin 875mg", "34,50 zł", "56", "Na receptę", "Dostępny"),
        ("#0057", "Voltaren Emulgel", "24,99 zł", "8", "Bez recepty", "Niski stan"),
        ("#0062", "Metformin 1000mg", "18,75 zł", "0", "Na receptę", "Brak"),
        ("#0078", "Rutinoscorbin", "9,49 zł", "180", "Bez recepty", "Dostępny"),
    ]

    build_drug_table(frame, rows)

    return frame