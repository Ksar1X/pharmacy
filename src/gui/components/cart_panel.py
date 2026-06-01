import ttkbootstrap as tb
from ttkbootstrap.constants import *
from src.services.logic.cart import *
from ttkbootstrap.dialogs import Messagebox, Querybox
from src.services.logic.purchase import *



def render_cart_side_panel(parent, current_user, refresh_shop_callback):
    tb.Label(parent, text="🛒 Twoje zamówienie", style='high.TLabel').pack(pady=10)

    columns = ("name", "qty", "price")
    tree = tb.Treeview(parent, columns=columns, show="headings", height=15, bootstyle=SECONDARY)
    tree.heading("name", text="Lek")
    tree.heading("qty", text="Szt.")
    tree.heading("price", text="Suma")

    tree.column("name", width=120)
    tree.column("qty", width=50, anchor=CENTER)
    tree.column("price", width=80, anchor=E)
    tree.pack(fill=BOTH, expand=True, padx=5)

    total_lbl = tb.Label(parent, text="Suma: 0.00 zł", style="low.TLabel")
    total_lbl.pack(pady=15)

    def handle_remove():
        selected = tree.selection()
        if not selected:
            Messagebox.show_warning("Wybierz produkt do usunięcia", "Brak wyboru")
            return

        item_data = tree.item(selected)['values']
        item_name = item_data[0]
        current_qty = int(item_data[1])

        amount = Querybox.get_integer(
            prompt=f"Ile sztuk '{item_name}' usunąć?",
            title="Usuwanie",
            initialvalue=1,
            minvalue=1,
            maxvalue=current_qty
        )

        if amount:
            cart_content = get_cart_content()
            drug_id = next((i['id'] for i in cart_content if i['name'] == item_name), None)

            if drug_id:
                remove_from_cart(drug_id, amount)
                update_ui()
                refresh_shop_callback()

    btn_remove = tb.Button(parent, text="🗑️ Usuń z koszyka", style='delete.TButton', command=handle_remove, width=20)
    btn_remove.pack(pady=5)

    def update_ui():
        for item in tree.get_children():
            tree.delete(item)

        for item in get_cart_content():
            tree.insert("", END, values=(item['name'], item['qty'], f"{item['price'] * item['qty']:.2f}"))

        total_lbl.config(text=f"Suma: {get_cart_total():.2f} zł")

    def handle_checkout():
        success, msg = checkout(current_user)
        if success:
            Messagebox.show_info(msg, "Sukces")
            update_ui()
            refresh_shop_callback()
        else:
            Messagebox.show_error(msg, "Błąd")

    btn_pay = tb.Button(parent, text="Kupuję i Płacę", style='my.TButton', command=handle_checkout)
    btn_pay.pack(fill=X, padx=10, pady=5)

    return update_ui