import ttkbootstrap as tb
from ttkbootstrap.constants import *
from src.gui.components.shop_table import render_shop_table
from src.gui.components.cart_panel import render_cart_side_panel
from src.services.logic.cart import add_to_cart, get_cart_content, checkout
from src.services.backend.prescription_manager import is_drug_prescription_required
from src.services.logic.purchase import add_to_recipe_archive
from ttkbootstrap.dialogs import Querybox, Messagebox


def build_cashier_dashboard(parent, user_id):
    main_frame = tb.Frame(parent, padding=15)
    main_frame.pack(fill=BOTH, expand=True)

    right_panel = tb.Labelframe(main_frame, text=" 🛒 Koszyk Klienta ", padding=10, style="low.TLabel", width=350)
    right_panel.pack(side=RIGHT, fill=Y, padx=(10, 0))
    right_panel.pack_propagate(False)

    def handle_cashier_checkout():
        cart_items = get_cart_content()
        if not cart_items:
            Messagebox.show_error("Koszyk jest pusty!")
            return

        customer_full_name = Querybox.get_string("Podaj Imię i Nazwisko pacjenta:", "Dane Pacjenta")
        if not customer_full_name: return

        needs_recipe = any(is_drug_prescription_required(item['id']) for item in cart_items)

        recipe_no = None
        if needs_recipe:
            recipe_no = Querybox.get_string("Wymagana RECEPTA. Podaj numer:", "NFZ Rejestracja")
            if not recipe_no:
                Messagebox.show_error("Błąd: Nie można sprzedać leków na receptę bez numeru!")
                return

        total_sum = sum(item['price'] * item['qty'] for item in cart_items)
        success, msg = checkout(user_id)

        if success:
            if recipe_no:
                add_to_recipe_archive(recipe_no, customer_full_name, total_sum)

            Messagebox.show_info("Sprzedaż zakończona i zarchiwizowana!")
            refresh_cart()
            refresh_shop()

    def handle_add_event(table_obj):
        selected = table_obj.view.focus()
        if selected:
            values = table_obj.view.item(selected)['values']
            drug_id, name, price = values[0], values[1], values[3]
            clean_price = float(str(price).replace(' zł', '').replace(',', '.'))

            amount = Querybox.get_integer(f"Ile sztuk '{name}'?", "Ilość", 1, minvalue=1)
            if amount:
                if add_to_cart(drug_id, name, clean_price, amount):
                    refresh_cart()
                else:
                    Messagebox.show_error("Brak на stanie!")

    left_panel = tb.Frame(main_frame)
    left_panel.pack(side=LEFT, fill=BOTH, expand=True)

    shop_table, refresh_shop = render_shop_table(left_panel, handle_add_event, show_all=True)
    refresh_cart = render_cart_side_panel(right_panel, user_id, refresh_shop)

    btn_final = tb.Button(right_panel, text="✅ Finalizuj i Archiwizuj", style='my.TButton',
                          command=handle_cashier_checkout)
    btn_final.pack(side=BOTTOM, fill=X, pady=10)

    return main_frame