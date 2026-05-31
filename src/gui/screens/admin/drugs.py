import tkinter as tk
from ttkbootstrap.constants import *

from src.gui.components import build_drug_table
from src.gui.components.delete_drug_window import open_delete_drug_window
from src.gui.theme import *
from src.gui.components.add_drug_window import open_add_drug_window


def render_admin_drugs(parent):
    """
    Ekran do zarządzania magazynem leków.
    """
    container = tk.Frame(parent)
    container.pack(fill=BOTH, expand=True, padx=30, pady=30)
    container.configure(bg=COLORS["bg_main"])

    header_frame = tk.Frame(container)
    header_frame.pack(fill=X, pady=(0, 20))
    header_frame.configure(bg=COLORS["bg_main"])

    title = tb.Label(header_frame, text="Magazyn leków", style="high.TLabel")
    title.pack(side=LEFT)

    def refresh_table():
        for widget in table_container.winfo_children():
            widget.destroy()
        build_drug_table(table_container)

    btn_add = tb.Button(header_frame, text="+ Dodaj lek", style="my.TButton", command=lambda: open_add_drug_window(parent, refresh_table))
    btn_add.pack(side=RIGHT)

    dlt_add = tb.Button(header_frame, text="- Usuń lek", style="my.TButton", command=lambda: open_delete_drug_window(parent, refresh_table))
    dlt_add.pack(side=RIGHT, padx=5)

    table_container = tk.Frame(container)
    table_container.pack(fill=BOTH, expand=True)
    table_container.configure(bg=COLORS["bg_main"])

    build_drug_table(table_container)

    return container