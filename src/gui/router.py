# gui/router.py
from src.gui.screens.admin.dashboard  import build_admin_dashboard
from src.gui.screens.admin.drugs      import render_admin_drugs
from src.gui.screens.admin.customers  import build_customers_screen
from src.gui.screens.admin.stats      import build_stats_screen

from src.gui.screens.cashier.dashboard import build_cashier_dashboard
from src.gui.screens.cashier.purchase  import build_purchase_screen
from src.gui.screens.cashier.search    import build_search_screen

from src.gui.screens.customer.dashboard import build_customer_dashboard
from src.gui.screens.customer.catalog   import build_catalog_screen
from src.gui.screens.customer.cart      import build_cart_screen
from src.gui.screens.customer.history   import build_history_screen

# Маршруты для каждой роли
ROUTES = {
    "admin": {
        "Dashboard":    build_admin_dashboard,
        "Leki":         render_admin_drugs,
        "Klienci":      build_customers_screen,
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
    Очищает content_frame и отрисовывает нужный экран.

    :param section: название раздела (например "Leki")
    :param content_frame: фрейм в который рисуем экран
    :param role: роль пользователя (admin / cashier / customer)
    """
    # Очищаем текущий контент
    for widget in content_frame.winfo_children():
        widget.destroy()

    print(f"route вызван: section='{section}', role='{role}'")
    # Находим нужный builder
    builder = ROUTES.get(role, {}).get(section)

    print(f"builder найден: {builder}")

    if builder:
        builder(content_frame)
    else:
        # Если маршрут не найден — показываем заглушку
        import tkinter as tk
        from src.gui.theme import COLORS
        from src.gui.fonts import FONT_TITLE

        lbl = tk.Label(
            content_frame,
            text=f"Раздел '{section}' в разработке...",
            font=FONT_TITLE
        )
        lbl.pack(expand=True)
        lbl.configure(bg=COLORS["bg_main"], fg=COLORS["muted"])