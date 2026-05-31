import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.widgets.tableview import Tableview

from src.gui.theme import *
from src.services.backend.customer_manager import load_customers
from src.gui.components.customer_profile_window import open_customer_profile


def build_customer_table(parent):
    """
    Tworzy komponent tabeli klientów z polem wyszukiwania.
    """
    table_wrap = tk.Frame(parent)
    table_wrap.pack(fill=BOTH, expand=True)
    table_wrap.configure(bg=COLORS["bg_main"])

    search_frame = tk.Frame(table_wrap, bg=COLORS["bg_main"])
    search_frame.pack(fill=X, padx=10, pady=(10,0), expand=False)

    tb.Label(search_frame, text="Wyszukiwanie klienta:", style="tip.TLable").pack(side=LEFT, padx=(0, 10))

    search_ent = tb.Entry(search_frame, bootstyle=PRIMARY, width=35)
    search_ent.pack(side=LEFT)
    search_ent.insert(0, "")

    tb.Label(search_frame, text="(Wpisz ID, imię lub nazwę użytkownika i naciśnij klawisz Enter)", style="tip.TLable").pack(side=LEFT, padx=10)

    columns: list = [
        {"text": "ID", "stretch": False, "width": 70},
        {"text": "Imię", "stretch": True},
        {"text": "Nazwisko", "stretch": True},
        {"text": "Login", "stretch": True},
        {"text": "Rola", "stretch": False, "width": 100},
    ]

    table = Tableview(
        master=table_wrap,
        coldata=columns,
        rowdata=[],
        bootstyle=PRIMARY,
        stripecolor=(COLORS["bg_sidebar"], None),
        paginated=True,
        pagesize=35,
        autofit=True
    )
    table.pack(fill=BOTH, expand=True, padx=8, pady=(0,8))

    def update_table(_event=None):
        """Logika filtrowania i aktualizacji danych w tabeli."""
        query = search_ent.get().strip().lower()
        df = load_customers()

        if df.empty:
            table.build_table_data(columns, [])
            return "break"

        if query:
            mask = (
                    df['id'].astype(str).str.contains(query, case=False, na=False) |
                    df['name'].astype(str).str.lower().str.contains(query, na=False) |
                    df['surname'].astype(str).str.lower().str.contains(query, na=False) |
                    df['login'].astype(str).str.lower().str.contains(query, na=False)
            )
            filtered_df = df[mask]
        else:
            filtered_df = df

        formatted_rows = []
        for _, row in filtered_df.iterrows():
            formatted_rows.append((
                row.get('id', ''),
                row.get('name', ''),
                row.get('surname', ''),
                row.get('login', ''),
                row.get('role', '')
            ))

        table.build_table_data(coldata=columns, rowdata=formatted_rows)
        search_ent.focus_set()
        return "break"

    search_ent.bind("<Return>", update_table)

    def on_row_double_click(_event):
        selected_item = table.view.focus()
        if not selected_item:
            return

        row_values = table.view.item(selected_item)['values']
        if row_values:
            customer_id = row_values[0]
            open_customer_profile(parent, customer_id, on_delete_callback=update_table)

    table.view.bind("<Double-1>", on_row_double_click)

    update_table()

    return table_wrap