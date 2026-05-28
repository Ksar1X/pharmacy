from src.gui.screens.admin.dashboard  import build_admin_dashboard
from src.gui.screens.admin.drugs      import render_admin_drugs
from src.gui.screens.admin.customers  import render_admin_customers
from src.gui.screens.admin.stats      import build_stats_screen

from src.gui.screens.cashier.dashboard import build_cashier_dashboard
from src.gui.screens.cashier.purchase  import build_purchase_screen
from src.gui.screens.cashier.search    import build_search_screen

from src.gui.screens.customer.dashboard import build_customer_dashboard
from src.gui.screens.customer.catalog   import build_catalog_screen
from src.gui.screens.customer.cart      import build_cart_screen
from src.gui.screens.customer.history   import build_history_screen


ROUTES = {
    "admin": {
        "Dashboard":    build_admin_dashboard,
        "Leki":         render_admin_drugs,
        "Klienci":      render_admin_customers,
        "Statystyki":   build_stats_screen,
    },
    "cashier": {
        "Dashboard":    build_cashier_dashboard,
        "Zakupy":       build_purchase_screen,
        "Szukaj":       build_search_screen,
    },
    "customer": {
        "Dashboard":    build_customer_dashboard,
        "Katalog":      build_catalog_screen,
        "Koszyk":       build_cart_screen,
        "Historia":     build_history_screen,
    }
}


def route(section, content_frame, role):
    """
    Czysta ramkę content_frame i rysuje odpowiedni ekran.

    :param section: nazwa sekcji (np. „Leki”)
    :param content_frame: ramka, w której rysujemy ekran
    :param role: rola użytkownika (admin / kasjer / klient)
    """
    # Очищаем текущий контент
    for widget in content_frame.winfo_children():
        widget.destroy()

    print(f"wywołano funkcję route: section='{section}', role='{role}'")
    # Находим нужный builder
    builder = ROUTES.get(role, {}).get(section)

    print(f"znaleziono builder: {builder}")

    if builder:
        builder(content_frame)
    else:
        import tkinter as tk
        from src.gui.theme import COLORS
        from src.gui.fonts import FONT_TITLE

        lbl = tk.Label(
            content_frame,
            text=f"Sekcja '{section}' w trakcie opracowywania...",
            font=FONT_TITLE
        )
        lbl.pack(expand=True)
        lbl.configure(bg=COLORS["bg_main"], fg=COLORS["muted"])

