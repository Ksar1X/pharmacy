import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from src.gui.fonts import *
from src.gui.theme import *
from src.gui.components.customer_table import build_customer_table
from src.gui.components.add_customer_window import open_add_customer_window

def render_admin_customers(parent):
    """
    Экран управления списком клиентов для администратора.
    """
    container = tk.Frame(parent)
    container.pack(fill=BOTH, expand=True, padx=30, pady=30)
    container.configure(bg=COLORS["bg_main"])

    header_frame = tk.Frame(container)
    header_frame.pack(fill=X, pady=(0, 20))
    header_frame.configure(bg=COLORS["bg_main"])

    title_label = tk.Label(
        header_frame,
        text="База клиентов",
        font=("Arial", 24, "bold"),
        bg=COLORS["bg_main"],
        fg=COLORS["text"]
    )
    title_label.pack(side=LEFT)

    def refresh_customers():
        for widget in table_container.winfo_children():
            widget.destroy()
        build_customer_table(table_container)

    btn_add = tb.Button(
        header_frame,
        text="+ Добавить клиента",
        bootstyle=SUCCESS,
        command=lambda: open_add_customer_window(parent, refresh_customers)
    )
    btn_add.pack(side=RIGHT)

    table_container = tk.Frame(container)
    table_container.pack(fill=BOTH, expand=True)
    table_container.configure(bg=COLORS["bg_main"])

    build_customer_table(table_container)

    return container