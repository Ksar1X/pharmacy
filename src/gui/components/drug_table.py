import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview

from gui.fonts import *
from gui.theme import *


def build_drug_table(parent, rows):
    table_wrap = tk.Frame(parent)
    table_wrap.pack(fill="both", expand=True)
    table_wrap.configure(
        bg=COLORS["bg_card"],
        highlightbackground=COLORS["border"],
        highlightthickness=1
    )

    # Заголовок
    t_header = tk.Frame(table_wrap)
    t_header.pack(fill="x", padx=16, pady=(14, 8))
    t_header.configure(bg=COLORS["bg_card"])

    t_title = tk.Label(t_header, text=f"Leki ({len(rows)})", font=FONT_HEADING)
    t_title.pack(side="left")
    t_title.configure(bg=COLORS["bg_card"], fg=COLORS["text"])

    tb.Entry(t_header, bootstyle=SECONDARY, width=22).pack(side="right")

    # Разделитель
    sep = tk.Frame(table_wrap, height=1)
    sep.pack(fill="x")
    sep.configure(bg=COLORS["border"])

    columns = [
        {"text": "ID",      "stretch": False, "width": 70},
        {"text": "Nazwa",   "stretch": True},
        {"text": "Cena",    "stretch": False, "width": 90},
        {"text": "Ilość",   "stretch": False, "width": 80},
        {"text": "Recepta", "stretch": False, "width": 110},
        {"text": "Status",  "stretch": False, "width": 110},
    ]

    table = Tableview(
        table_wrap,
        coldata=columns,
        rowdata=rows,
        bootstyle=DARK,
        stripecolor=(COLORS["bg_main"], None),
        autofit=True,
        paginated=True,
        pagesize=10,
        searchable=False,
    )
    table.pack(fill="both", expand=True, padx=8, pady=8)

    return table_wrap