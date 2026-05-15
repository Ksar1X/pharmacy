# gui/router.py
from gui.screens.admin.dashboard  import build_admin_dashboard
from gui.screens.admin.drugs      import build_drugs_screen
from gui.screens.admin.customers  import build_customers_screen
from gui.screens.admin.stats      import build_stats_screen

from gui.screens.cashier.dashboard import build_cashier_dashboard
from gui.screens.cashier.purchase  import build_purchase_screen
from gui.screens.cashier.search    import build_search_screen

from gui.screens.customer.dashboard import build_customer_dashboard
from gui.screens.customer.catalog   import build_catalog_screen
from gui.screens.customer.cart      import build_cart_screen
from gui.screens.customer.history   import build_history_screen

# Маршруты для каждой роли
ROUTES = {
    "admin": {
        "Dashboard":    build_admin_dashboard,
        "Leki":         build_drugs_screen,
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

    # Находим нужный builder
    builder = ROUTES.get(role, {}).get(section)

    if builder:
        builder(content_frame)
    else:
        # Если маршрут не найден — показываем заглушку
        import tkinter as tk
        from gui.theme import COLORS
        from gui.fonts import FONT_TITLE

        lbl = tk.Label(
            content_frame,
            text=f"Раздел '{section}' в разработке...",
            font=FONT_TITLE
        )
        lbl.pack(expand=True)
        lbl.configure(bg=COLORS["bg_main"], fg=COLORS["muted"])