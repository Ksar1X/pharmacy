import tkinter as tk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets.tableview import Tableview

from src.gui.theme import *
from src.services.backend.drug_manager import load_drugs
from src.gui.components.edit_drug_window import open_edit_drug_window


def get_formatted_rows(df):
    """Przekształca DataFrame w listę krotek w celu wyświetlenia w tabeli."""
    rows = []
    if df.empty:
        return rows

    for _, drug in df.iterrows():
        qty = drug.get('quantity', 0)
        status = "Dostępny" if qty > 0 else "Brak"

        rows.append((
            drug.get('id', ''),
            drug.get('name', ''),
            drug.get('category', ''),
            drug.get('price', ''),
            qty,
            drug.get('requires_recipe', ''),
            status
        ))
    return rows


def build_drug_table(parent):
    """Tworzy komponent tabeli z funkcją wyszukiwania."""

    table_wrp = tk.Frame(parent)
    table_wrp.pack(fill=BOTH, expand=True)
    table_wrp.configure(bg=COLORS["bg_main"])

    search_frame = tk.Frame(table_wrp, bg=COLORS["bg_main"])
    search_frame.pack(fill=X, padx=10, pady=(10,0), expand=False)

    tb.Label(search_frame, text="Wyszukiwanie:", style="tip.TLable").pack(side=LEFT, padx=(0, 10))

    search_ent = tb.Entry(search_frame, bootstyle=PRIMARY, width=35)
    search_ent.pack(side=LEFT)
    search_ent.insert(0, "")

    tb.Label(search_frame, text=" (kliknij dwukrotnie w wiersz, aby zmienić cenę/ilość)", style="tip.TLable").pack(side=LEFT, padx=10)

    columns: list = [
        {"text": "ID", "stretch": False, "width": 70},
        {"text": "Nazwa", "stretch": True},
        {"text": "Kategoria", "stretch": True},
        {"text": "Cena", "stretch": False, "width": 100},
        {"text": "Ilość", "stretch": False, "width": 80},
        {"text": "Recepta", "stretch": False, "width": 100},
        {"text": "Status", "stretch": False, "width": 110},
    ]

    table = Tableview(
        master=table_wrp,
        coldata=columns,
        rowdata=[],
        bootstyle=PRIMARY,
        stripecolor=(COLORS["bg_sidebar"], None),
        paginated=True,
        pagesize=35,
        autofit=True,
    )
    table.pack(fill=BOTH, expand=True, padx=8, pady=(0,8))

    def update_table_data(_event=None):
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
                r['price'],
                r['quantity'],
                r['requires_recipe']
            ))

        table.build_table_data(columns, rows)
        return "break"

    search_ent.bind("<Return>", update_table_data)

    def search_drugs(_event=None):
        """Logika filtrowania danych."""
        query = search_ent.get().strip().lower()
        df = load_drugs()

        if query:
            mask = (df['id'].astype(str).str.contains(query, case=False, na=False)) | \
                   (df['name'].astype(str).str.lower().str.contains(query, case=False, na=False))
            filtered_df = df[mask]
        else:
            filtered_df = df

        new_rows = get_formatted_rows(filtered_df)
        table.build_table_data(coldata=columns, rowdata=new_rows)

        search_ent.focus_set()
        return "break"

    search_ent.bind("<Return>", search_drugs)

    search_drugs()

    def refresh_table():
        update_table_data()

    def on_row_double_click(_event):
        selected_item = table.view.focus()
        if not selected_item:
            return

        row_values = table.view.item(selected_item)['values']
        if row_values:
            open_edit_drug_window(parent, row_values, refresh_table)

    table.view.bind("<Double-1>", on_row_double_click)

    update_table_data()

    return table_wrp