import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview

from src.gui.fonts import *
from src.gui.theme import *
from src.drug_manager import load_drugs


def get_formatted_rows(df):
    """Преобразует DataFrame в список кортежей для отображения в таблице."""
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
            f"{float(drug.get('price', 0)):.2f} zł",
            qty,
            drug.get('requires_recipe', ''),
            status
        ))
    return rows


def build_drug_table(parent):
    """Создает компонент таблицы с поиском."""
    table_wrap = tk.Frame(parent)
    table_wrap.pack(fill="both", expand=True)
    table_wrap.configure(
        bg=COLORS["bg_sidebar"],
        highlightbackground=COLORS["border"],
        highlightthickness=1
    )

    t_header = tk.Frame(table_wrap, bg=COLORS["bg_sidebar"])
    t_header.pack(fill="x", padx=16, pady=(14, 8))

    t_title = tk.Label(
        t_header,
        text="Lista Leków",
        font=FONT_HEADING,
        bg=COLORS["bg_sidebar"],
        fg=COLORS["text"]
    )
    t_title.pack(side="left")

    search_ent = tb.Entry(t_header, bootstyle=SECONDARY, width=25)
    search_ent.pack(side="right")
    search_ent.insert(0, "")

    columns = [
        {"text": "ID", "stretch": False, "width": 70},
        {"text": "Nazwa", "stretch": True},
        {"text": "Category", "stretch": True},
        {"text": "Cena", "stretch": False, "width": 100},
        {"text": "Ilość", "stretch": False, "width": 80},
        {"text": "Recepta", "stretch": False, "width": 100},
        {"text": "Status", "stretch": False, "width": 110},
    ]

    table = Tableview(
        master=table_wrap,
        coldata=columns,
        rowdata=[],
        bootstyle=DARK,
        stripecolor=(COLORS["bg_main"], None),
        paginated=True,
        pagesize=45,
        autofit=True
    )
    table.pack(fill="both", expand=True, padx=8, pady=8)

    def search_drugs(event=None):
        """Логика фильтрации данных."""
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

        t_title.config(text=f"Leki ({len(new_rows)})")

        search_ent.focus_set()
        return "break"

    search_ent.bind("<Return>", search_drugs)

    search_drugs()

    return table_wrap