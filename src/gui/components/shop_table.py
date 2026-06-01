import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from src.services.backend.drug_manager import load_drugs


def render_shop_table(parent, on_add_callback, show_all=True):
    """
    Wyświetla tabelę produktów do zakupu.

    Args:
        parent: Ramka, w której będzie znajdować się tabela.
        on_add_callback: Funkcja wywoływana po naciśnięciu przycisku „Dodaj”.
        show_all: Jeśli True — pokazuje wszystkie produkty (dla kasjera).
                  Jeśli False — ukrywa produkty z receptury (dla klienta).
    """

    container = tb.Frame(parent)
    container.pack(fill=BOTH, expand=True)

    df = load_drugs()

    if not show_all:
        df = df[df['requires_recipe'].astype(str).str.capitalize() != 'Tak']


    columns = [
        {"text": "ID", "stretch": False, "width": 50},
        {"text": "Nazwa", "stretch": True},
        {"text": "Dostępność", "stretch": False, "width": 100},
        {"text": "Cena", "stretch": False, "width": 100},
        {"text": "Recepta", "stretch": False, "width": 80},
    ]

    row_data = []
    for _, row in df.iterrows():
        row_data.append([
            row['id'],
            row['name'],
            f"{row['quantity']} szt.",
            f"{row['price']} zł",
            row.get('requires_recipe', 'Nie')
        ])

    table = Tableview(
        master=container,
        coldata=columns,
        rowdata=row_data,
        paginated=True,
        pagesize=15,
        bootstyle=PRIMARY,
    )
    table.pack(fill=BOTH, expand=True, pady=10)

    btn_add = tb.Button(
        container,
        text="➕ Dodaj wybrane do koszyka",
        bootstyle=SUCCESS,
        command=lambda: on_add_callback(table)
    )
    btn_add.pack(pady=10)

    def refresh_shop():
        new_df = load_drugs()
        if not show_all:
            new_df = new_df[new_df['requires_recipe'].astype(str).str.capitalize() != 'Tak']

        new_rows = []
        for _, row in new_df.iterrows():
            new_rows.append([
                row['id'],
                row['name'],
                f"{row['quantity']} szt.",
                f"{row['price']} zł",
                row.get('requires_recipe', 'Nie')
            ])
        table.build_table_data(columns, new_rows)

    return table, refresh_shop