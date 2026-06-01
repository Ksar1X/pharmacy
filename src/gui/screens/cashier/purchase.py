import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Querybox, Messagebox

from src.services.backend.drug_manager import load_drugs
from src.services.logic.cart import add_to_cart, get_cart_content, clear_cart, checkout
from src.services.backend.prescription_manager import verify_prescription
from src.gui.theme import COLORS


def build_purchase_screen(parent):
    """Ekran obsługi sprzedaży przez kasjera."""

    main_frame = tb.Frame(parent, padding=10)
    main_frame.pack(fill=BOTH, expand=True)

    left_panel = tb.Frame(main_frame)
    left_panel.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

    tb.Label(left_panel, text="Dostępne leki", font=("Arial", 14, "bold")).pack(pady=5)

    columns = [
        {"text": "ID", "stretch": False, "width": 50},
        {"text": "Nazwa", "stretch": True},
        {"text": "Ilość", "stretch": False, "width": 80},
        {"text": "Cena", "stretch": False, "width": 100},
        {"text": "Recepta", "stretch": False, "width": 80},
    ]

    df = load_drugs()
    drug_data = []
    for _, row in df.iterrows():
        req = "TAK" if row.get('prescription_required', 0) == 1 else "NIE"
        drug_data.append([row['id'], row['name'], row['quantity'], f"{row['price']} zł", req])

    drug_table = Tableview(
        master=left_panel,
        coldata=columns,
        rowdata=drug_data,
        paginated=True,
        pagesize=15,
        bootstyle=PRIMARY,
    )
    drug_table.pack(fill=BOTH, expand=True)

    def on_add_click():
        selected = drug_table.view.focus()
        if not selected:
            return

        values = drug_table.view.item(selected)['values']
        d_id, d_name, d_price = values[0], values[1], values[3]

        amount = Querybox.get_integer("Ile sztuk dodać?", "Ilość", initialvalue=1, minvalue=1)
        if amount:
            if add_to_cart(d_id, d_name, d_price, amount):
                update_cart_ui()
            else:
                Messagebox.show_error("Brak wystarczającej ilości!", "Błąd")

    tb.Button(left_panel, text="➕ Dodaj do zamówienia", command=on_add_click, bootstyle=SUCCESS).pack(pady=10)

    right_panel = tb.Frame(main_frame, width=350, bootstyle=LIGHT)
    right_panel.pack(side=RIGHT, fill=BOTH, padx=5)
    right_panel.pack_propagate(False)

    tb.Label(right_panel, text="Zamówienie", font=("Arial", 14, "bold"), bootstyle="inverse-light").pack(pady=10)

    cart_tree = tb.Treeview(right_panel, columns=("name", "qty", "total"), show="headings", height=15)
    cart_tree.heading("name", text="Produkt")
    cart_tree.heading("qty", text="Szt.")
    cart_tree.heading("total", text="Suma")
    cart_tree.column("name", width=150)
    cart_tree.column("qty", width=50)
    cart_tree.column("total", width=80)
    cart_tree.pack(fill=X, padx=10)

    total_label = tb.Label(right_panel, text="Suma: 0.00 zł", font=("Arial", 12, "bold"), bootstyle="inverse-light")
    total_label.pack(pady=20)

    def update_cart_ui():
        for i in cart_tree.get_children():
            cart_tree.delete(i)

        cart_items = get_cart_content()
        grand_total = 0
        for item in cart_items:
            total = item['price'] * item['qty']
            grand_total += total
            cart_tree.insert("", END, values=(item['name'], item['qty'], f"{total:.2f}"))

        total_label.config(text=f"Suma: {grand_total:.2f} zł")

    def handle_checkout():
        cart_items = get_cart_content()
        if not cart_items:
            Messagebox.show_error("Koszyk jest pusty!", "Błąd")
            return

        customer_id = Querybox.get_string("Podaj ID Klienta (na kogo zarejestrować zakup):", "Dane Klienta")
        if not customer_id:
            return

        needs_recipe = False
        df_drugs = load_drugs()
        for item in cart_items:
            drug_info = df_drugs[df_drugs['id'].astype(str) == str(item['id'])]
            if not drug_info.empty and drug_info.iloc[0].get('prescription_required', 0) == 1:
                needs_recipe = True
                break

        recipe_id = None
        if needs_recipe:
            recipe_id = Querybox.get_string("W koszyku są leki na receptę. Podaj numer recepty:", "Weryfikacja")
            if not recipe_id:
                Messagebox.show_error("Brak numeru recepty! Sprzedaż niemożliwa.", "Błąd")
                return

            valid, msg = verify_prescription(recipe_id)
            if not valid:
                Messagebox.show_error(msg, "Błąd weryfikacji")
                return

        success, msg = checkout(customer_id)
        if success:
            if recipe_id:
                print(f"Sprzedaż zrealizowana na receptę: {recipe_id}")

            Messagebox.show_info("Sprzedaż zakończona pomyślnie!", "Sukces")
            update_cart_ui()
        else:
            Messagebox.show_error(msg, "Błąd")

    btn_frame = tb.Frame(right_panel, bootstyle=LIGHT)
    btn_frame.pack(fill=X, side=BOTTOM, pady=20, padx=10)

    tb.Button(btn_frame, text="✅ Finalizuj", bootstyle=SUCCESS, command=handle_checkout).pack(fill=X, pady=5)
    tb.Button(btn_frame, text="🗑️ Czyść", bootstyle=DANGER, command=lambda: [clear_cart(), update_cart_ui()]).pack(
        fill=X)

    update_cart_ui()
    return main_frame