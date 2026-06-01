import ttkbootstrap as tb
from ttkbootstrap.constants import *
from src.gui.components.shop_table import render_shop_table
from src.gui.components.cart_panel import render_cart_side_panel
from src.services.logic.cart import add_to_cart

from ttkbootstrap.dialogs import Querybox, Messagebox


def build_customer_dashboard(parent, user_id):
    """
    Разделенный экран: Слева каталог, Справа корзина.
    current_user: логин текущего пользователя для истории и логов.
    """
    main_frame = tb.Frame(parent, padding=15)
    main_frame.pack(fill=BOTH, expand=True)

    right_panel = tb.Labelframe(
        main_frame,
        text=" 🛒 Twój Koszyk ",
        padding=10,
        bootstyle=PRIMARY,
        width=350
    )

    right_panel.pack(side=RIGHT, fill=Y, padx=(10, 0), expand=False)
    right_panel.pack_propagate(False)


    def handle_add_event(table_obj):
        """Эту функцию вызовет кнопка из компонента таблицы."""
        selected = table_obj.view.focus()
        if selected:
            values = table_obj.view.item(selected)['values']
            drug_id, name, price = values[0], values[1], values[3]

            amount = Querybox.get_integer(
                prompt=f"Ile sztuk '{name}' dodać?",
                title="Ilość",
                initialvalue=1,
                minvalue=1
            )
            if amount:  # Если пользователь не нажал "Отмена"
                if add_to_cart(drug_id, name, price, amount):
                    refresh_cart()
                    refresh_shop()
                else:
                    Messagebox.show_error("Brak wystarczającej ilości na stanie!", "Błąd")

    left_panel = tb.Frame(main_frame)
    left_panel.pack(side=LEFT, fill=BOTH, expand=True)

    shop_table, refresh_shop = render_shop_table(left_panel, handle_add_event)
    refresh_cart = render_cart_side_panel(right_panel, current_user, refresh_shop)

    return main_frame