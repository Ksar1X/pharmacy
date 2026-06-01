from src.gui.screens.admin.dashboard  import build_admin_dashboard
from src.gui.screens.admin.drugs      import render_admin_drugs
from src.gui.screens.admin.customers  import render_admin_customers
from src.gui.screens.admin.stats      import build_stats_screen
from src.gui.screens.admin.logs       import render_admin_logs

from src.gui.screens.cashier.dashboard import build_cashier_dashboard
from src.gui.screens.cashier.purchase  import build_purchase_screen
from src.gui.screens.cashier.search    import build_search_screen

from src.gui.screens.customer.dashboard import build_customer_dashboard
from src.gui.screens.customer.history   import build_history_screen


ROUTES = {
    "admin": {
        "Dashboard":    build_admin_dashboard,
        "Leki":         render_admin_drugs,
        "Klienci":      render_admin_customers,
        "Statystyki":   build_stats_screen,
        "Logi":         render_admin_logs
    },
    "cashier": {
        "Dashboard":    build_cashier_dashboard,
        "Zakupy":       build_purchase_screen,
        "Szukaj":       build_search_screen,
    },
    "customer": {
        "Dashboard":    build_customer_dashboard,
        "Historia":     build_history_screen,
    }
}


def route(section, content_frame, role, user_id=None):
    """
    Czyści ramkę content_frame i rysuje odpowiedni ekran.
    """
    for widget in content_frame.winfo_children():
        widget.destroy()

    section_normalized = section.capitalize()
    print(f"wywołano funkcję route: section='{section}', role='{role}', user_id='{user_id}'")

    builder = ROUTES.get(role, {}).get(section_normalized)

    if builder:
        if role == "customer" and section in ["Dashboard", "Historia"]:
            builder(content_frame, user_id=user_id)
        else:
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

