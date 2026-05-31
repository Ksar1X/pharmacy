import tkinter as tk
from ttkbootstrap.constants import *
from src.gui.theme import *
from src.services.logic.stats import *
from src.gui.components.stat_card import build_stat_card


def build_stats_screen(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=24, pady=20)
    frame.configure(bg=COLORS["bg_main"])

    header = tb.Label(frame, text="Statystyki Systemowe", style="high.TLabel")
    header.pack(pady=(0, 20), anchor=W)

    stats = tk.Frame(frame)
    stats.pack(fill="x", pady=(0, 20))
    stats.configure(bg=COLORS["bg_main"])

    build_stat_card(stats,"Całkowita Wartość",f"{get_total_value()} zł",COLORS["accent"])
    build_stat_card(stats,"Liczba Produktów",get_count_of_drugs(),COLORS["accent2"])
    build_stat_card(stats,"Niski stan", out_of_stock_drugs(),COLORS["danger"])
    build_stat_card(stats,"Leki na Receptę",get_number_of_drugs_with_prescription(),COLORS["warn"])

    return frame