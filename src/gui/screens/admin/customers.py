import tkinter as tk
from ttkbootstrap.constants import *
from src.gui.theme import *
from src.gui.components.customer_table import build_customer_table
from src.gui.components.add_customer_window import open_add_customer_window

def render_admin_customers(parent, **kwargs):
    """
    Ekran zarządzania listą klientów dla administratora.
    """
    container = tk.Frame(parent)
    container.pack(fill=BOTH, expand=True, padx=30, pady=30)
    container.configure(bg=COLORS["bg_main"])

    header_frame = tk.Frame(container)
    header_frame.pack(fill=X, pady=(0, 20))
    header_frame.configure(bg=COLORS["bg_main"])

    title_label = tb.Label(header_frame, text="Baza klientów", style="high.TLabel")
    title_label.pack(side=LEFT)

    def refresh_customers():
        for widget in table_container.winfo_children():
            widget.destroy()
        build_customer_table(table_container)

    btn_add = tb.Button(header_frame, text="+ Dodaj klienta", style="my.TButton", command=lambda: open_add_customer_window(parent, refresh_customers))
    btn_add.pack(side=RIGHT)

    table_container = tk.Frame(container)
    table_container.pack(fill=BOTH, expand=True)
    table_container.configure(bg=COLORS["bg_main"])

    build_customer_table(table_container)

    return container