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

    row1 = tk.Frame(frame)
    row1.configure(bg=COLORS["bg_main"])
    row1.pack(fill=X, pady=10)

    today_rev = get_today_revenue()
    build_stat_card(row1, "Utarg dzisiejszy", f"{today_rev:.2f} zł", COLORS['accent']).pack(side=LEFT, fill=X, expand=True,
                                                                                   padx=5)

    avg_check = get_average_purchase_value_today()
    build_stat_card(row1, "Średni koszyk (dziś)", f"{avg_check:.2f} zł", COLORS['accent2']).pack(side=LEFT, fill=X, expand=True,
                                                                                    padx=5)

    avg_daily = get_average_daily_revenue(30)
    build_stat_card(row1, "Średni utarg (30 dni)", f"{avg_daily:.2f} zł", COLORS['accent']).pack(side=LEFT, fill=X,
                                                                                          expand=True, padx=5)

    row2 = tk.Frame(frame)
    row2.configure(bg=COLORS["bg_main"])
    row2.pack(fill=X, pady=10)

    total_val = get_total_value() or 0
    build_stat_card(row2, "Wartość magazynu", f"{total_val:,.2f} zł", COLORS['accent']).pack(side=LEFT, fill=X, expand=True,
                                                                                    padx=5)

    new_users = get_new_users_today_count()
    build_stat_card(row2, "Nowi klienci (dziś)", str(new_users), COLORS['accent']).pack(side=LEFT, fill=X, expand=True, padx=5)


    low_stock = out_of_stock_drugs() or 0
    build_stat_card(row2, "Braki (<= 5 szt.)", str(low_stock), COLORS['danger']).pack(side=LEFT, fill=X, expand=True, padx=5)

    row3 = tk.Frame(frame)
    row3.configure(bg=COLORS["bg_main"])
    row3.pack(fill=X, pady=10)

    prescr_count = get_number_of_drugs_with_prescription() or 0
    build_stat_card(row3, "Leki na receptę", str(prescr_count), COLORS['accent']).pack(side=LEFT, fill=X, expand=True, padx=5)

    total_drugs = get_count_of_drugs() or 0
    build_stat_card(row3, "Liczba pozycji", str(total_drugs), COLORS['warn']).pack(side=LEFT, fill=X, expand=True, padx=5)

    total_clients = get_count_of_clients() or 0
    build_stat_card(row3, "Suma klientów", str(total_clients), COLORS['accent2']).pack(side=LEFT, fill=X, expand=True, padx=5)

    return frame