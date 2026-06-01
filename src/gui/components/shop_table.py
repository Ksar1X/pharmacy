import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.widgets.tableview import Tableview

from src.gui.theme import COLORS
from src.services.logic.stats import get_available_drugs


def render_shop_table(parent, on_add_callback):
    """
    Компонент магазина с работающим поиском по логике из drug_table.
    """
    # 1. Основной контейнер (table_wrp)
    table_wrp = tk.Frame(parent)
    table_wrp.pack(fill=BOTH, expand=True)
    table_wrp.configure(bg=COLORS["bg_main"])

    search_frame = tk.Frame(table_wrp, bg=COLORS["bg_main"])
    search_frame.pack(fill=X, padx=10, pady=(10, 5))

    tb.Label(search_frame, text="Wyszukaj lek:", style="tip.TLabel").pack(side=LEFT, padx=(0, 10))

    search_ent = tb.Entry(search_frame, bootstyle=PRIMARY, width=35)
    search_ent.pack(side=LEFT)

    tb.Label(search_frame, text="(wpisz nazwę и naciśnij Enter ⏎)", font=("Arial", 8), foreground="gray").pack(
        side=LEFT, padx=10)

    columns = [
        {"text": "ID", "stretch": False, "width": 60},
        {"text": "Nazwa", "stretch": True},
        {"text": "Kategoria", "stretch": True},
        {"text": "Cena", "stretch": False, "width": 100},
        {"text": "Dostępność", "stretch": False, "width": 100},
    ]

    table = Tableview(
        master=table_wrp,
        coldata=columns,
        rowdata=[],
        bootstyle=PRIMARY,
        paginated=True,
        pagesize=15,
        autofit=True,
    )
    table.pack(fill=BOTH, expand=True, padx=8, pady=5)

    btn_add = tb.Button(
        table_wrp,
        text="➕ Dodaj wybrany lek do koszyka",
        style='my.TButton',
        command=lambda: on_add_callback(table)
    )
    btn_add.pack(pady=10, fill=X, padx=8)

    def search_drugs(_event=None):
        """Фильтрация данных магазина."""
        query = search_ent.get().strip().lower()
        all_available = get_available_drugs()

        if query:
            filtered_rows = [
                row for row in all_available
                if query in str(row[1]).lower() or query in str(row[2]).lower()
            ]
        else:
            filtered_rows = all_available

        table.build_table_data(coldata=columns, rowdata=filtered_rows)
        search_ent.focus_set()
        return "break"

    search_ent.bind("<Return>", search_drugs)

    def refresh_shop():
        search_ent.delete(0, END)
        search_drugs()

    search_drugs()

    return table, refresh_shop