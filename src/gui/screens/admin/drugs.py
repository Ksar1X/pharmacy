import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview

from src.gui.theme import COLORS
from src.gui.fonts import *
from src.services.backend.drug_manager import load_drugs

from src.gui.components.add_drug_window import open_add_drug_window
from src.gui.components.edit_drug_window import open_edit_drug_window


def render_admin_drugs(parent):
    """
    Ekran do zarządzania magazynem leków.
    """
    container = tk.Frame(parent)
    container.config(bg=COLORS["bg_main"])
    container.pack(fill=BOTH, expand=True, padx=30, pady=30)

    header_frame = tk.Frame(container, bg=COLORS["bg_main"])
    header_frame.config(bg=COLORS["bg_main"])
    header_frame.pack(fill=X, pady=(0, 20))

    tk.Label(header_frame,text="Magazyn leków",font=FONT_TITLE,bg=COLORS["bg_main"],fg=COLORS["text"]).pack(side=LEFT)


    def refresh_table():
        update_table_data()

    tb.Button(
        header_frame,
        text="+ Nowy produkt",
        bootstyle=SUCCESS,
        command=lambda: open_add_drug_window(parent, refresh_table)
    ).pack(side=RIGHT)

    search_frame = tk.Frame(container)
    search_frame.pack(fill=X, pady=(0, 10))

    tk.Label(search_frame, text="Wyszukiwanie:", font=FONT_SMALL ,bg=COLORS["bg_main"], fg=COLORS["text"]).pack(side=LEFT, padx=(0, 10))

    search_ent = tb.Entry(search_frame, width=40)
    search_ent.pack(side=LEFT)

    tk.Label(search_frame, text=" (kliknij dwukrotnie w wiersz, aby zmienić cenę/ilość)", font=FONT_SMALL, bg=COLORS["bg_main"], fg="gray").pack(side=LEFT, padx=10)

    columns = [
        {"text": "ID", "stretch": False, "width": 60},
        {"text": "Tytuł", "stretch": True},
        {"text": "Kategoria", "stretch": True},
        {"text": "Cena", "stretch": False, "width": 100},
        {"text": "Ilość", "stretch": False, "width": 80},
        {"text": "Przepis", "stretch": False, "width": 100},
    ]

    table = Tableview(master=container,coldata=columns,rowdata=[],bootstyle=PRIMARY,paginated=True,pagesize=15,stripecolor=(COLORS["bg_sidebar"], None),)
    table.pack(fill=BOTH, expand=True)

    def update_table_data(event=None):
        """Wczytywanie danych z pliku CSV i filtrowanie wyników wyszukiwania."""
        query = search_ent.get().strip().lower()
        df = load_drugs()

        if query:
            mask = (df['name'].str.lower().str.contains(query)) | \
                   (df['category'].str.lower().str.contains(query))
            filtered_df = df[mask]
        else:
            filtered_df = df

        rows = []
        for _, r in filtered_df.iterrows():
            rows.append((
                r['id'],
                r['name'],
                r['category'],
                f"{r['price']} zł",
                r['quantity'],
                r['requires_recipe']
            ))

        table.build_table_data(columns, rows)
        return "break"

    search_ent.bind("<Return>", update_table_data)

    def on_row_double_click(event):
        selected_item = table.view.focus()
        if not selected_item:
            return

        row_values = table.view.item(selected_item)['values']
        if row_values:
            open_edit_drug_window(parent, row_values, refresh_table)

    table.view.bind("<Double-1>", on_row_double_click)

    update_table_data()

    return container