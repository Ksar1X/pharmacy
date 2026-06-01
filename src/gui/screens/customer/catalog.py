import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from src.services.logic.stats import get_available_drugs
from src.services.logic.cart import add_to_cart
from ttkbootstrap.dialogs import Messagebox


def render_customer_shop(parent):
    container = tb.Frame(parent, padding=20)
    container.pack(fill=BOTH, expand=True)

    header_frame = tb.Frame(container)
    header_frame.pack(fill=X, pady=(0, 20))

    tb.Label(header_frame, text="🛍️ Katalog Leków", font=("Arial", 20, "bold")).pack(side=LEFT)
    tb.Label(header_frame, text="Wszystkie leki dostępne bez recepty", font=("Arial", 10), bootstyle=SECONDARY).pack(
        side=LEFT, padx=15, pady=(10, 0))

    columns = [
        {"text": "Nazwa", "stretch": True},
        {"text": "Kategoria", "stretch": True},
        {"text": "Cena", "stretch": False, "width": 120},
        {"text": "Dostępność", "stretch": False, "width": 120},
    ]

    rows = get_available_drugs()

    table = Tableview(
        master=container,
        coldata=columns,
        rowdata=rows,
        paginated=True,
        pagesize=10,
        bootstyle=PRIMARY,
        searchable=True
    )
    table.pack(fill=BOTH, expand=True)

    action_frame = tb.Frame(container, padding=(0, 20, 0, 0))
    action_frame.pack(fill=X)

    def handle_add_to_cart():
        selected = table.view.focus()
        if not selected:
            Messagebox.show_warning("Wybierz produkt, który chcesz dodać do koszyka.", "Brak wyboru")
            return

        values = table.view.item(selected)['values']
        drug_id = values[0]
        name = values[1]
        price_str = str(values[3]).replace(' zł', '').replace(',', '.')

        add_to_cart(drug_id, name, price_str)

        Messagebox.show_info(f"Produkt {name} został dodany do koszyka!", "Koszyk")

    btn_buy = tb.Button(
        action_frame,
        text="➕ Dodaj do koszyka",
        bootstyle=SUCCESS,
        command=handle_add_to_cart,
        width=20
    )
    btn_buy.pack(side=RIGHT)

    return container