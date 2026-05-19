# gui/screens/admin/dashboard.py
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from datetime import datetime

from src.gui.fonts import *
from src.gui.theme import *
from src.gui.components.stat_card import build_stat_card
from src.gui.components.drug_table import build_drug_table


def build_admin_dashboard(parent):

    # ── Основной фрейм ────────────────────────────────
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=24, pady=20)
    frame.configure(bg=COLORS["bg_main"])

    # ── ЗАГОЛОВОК ─────────────────────────────────────
    header = tk.Frame(frame)
    header.pack(fill="x", pady=(0, 20))
    header.configure(bg=COLORS["bg_main"])

    # Левая часть — заголовок и дата
    left = tk.Frame(header)
    left.pack(side="left")
    left.configure(bg=COLORS["bg_main"])

    title_lbl = tk.Label(left, text="Dzień dobry!", font=FONT_TITLE)
    title_lbl.pack(anchor="w")
    title_lbl.configure(bg=COLORS["bg_main"], fg=COLORS["text"])

    now = datetime.now()
    date_str = now.strftime("%A, %d %B %Y · Ostatnia aktualizacja: %H:%M")
    date_lbl = tk.Label(left, text=date_str, font=FONT_SMALL)
    date_lbl.pack(anchor="w", pady=(2, 0))
    date_lbl.configure(bg=COLORS["bg_main"], fg=COLORS["muted"])

    # Правая часть — кнопки
    right = tk.Frame(header)
    right.pack(side="right", anchor="center")
    right.configure(bg=COLORS["bg_main"])

    tb.Button(
        right,
        text="+ Dodaj lek",
        bootstyle=(SUCCESS, OUTLINE),
        padding=(12, 6)
    ).pack(side="left", padx=(0, 8))

    tb.Button(
        right,
        text="+ Nowy klient",
        bootstyle=SUCCESS,
        padding=(12, 6)
    ).pack(side="left")

    # ── КАРТОЧКИ СТАТИСТИКИ ───────────────────────────
    stats = tk.Frame(frame)
    stats.pack(fill="x", pady=(0, 20))
    stats.configure(bg=COLORS["bg_sidebar"])

    build_stat_card(stats, "Dostępne leki", "148", COLORS["accent"])
    build_stat_card(stats, "Klienci",       "312", COLORS["accent2"])
    build_stat_card(stats, "Zakupy dziś",   "47",  COLORS["warn"])
    build_stat_card(stats, "Niski stan",    "12",  COLORS["danger"])

    stats.winfo_children()[-1].pack_configure(padx=0)

    # ── ТАБЛИЦА ───────────────────────────────────────
    rows = [
        ("#0021", "Apap Forte 500mg",  "12,99 zł", "240", "Bez recepty", "Dostępny"),
        ("#0034", "Amoxicillin 875mg", "34,50 zł", "56",  "Na receptę",  "Dostępny"),
        ("#0057", "Voltaren Emulgel",  "24,99 zł", "8",   "Bez recepty", "Niski stan"),
        ("#0062", "Metformin 1000mg",  "18,75 zł", "0",   "Na receptę",  "Brak"),
        ("#0078", "Rutinoscorbin",      "9,49 zł",  "180", "Bez recepty", "Dostępny"),
    ]

    build_drug_table(frame, rows)

    return frame