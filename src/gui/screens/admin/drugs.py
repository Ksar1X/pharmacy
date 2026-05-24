import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from src.gui.fonts import *
from src.gui.theme import *
from src.gui.components.drug_table import build_drug_table

def render_admin_drugs(parent):
    """
    Отрисовка экрана управления лекарствами для администратора.
    """
    container = tk.Frame(parent)
    container.pack(fill=BOTH, expand=True, padx=30, pady=30)
    container.configure(bg=COLORS["bg_main"])

    header_frame = tk.Frame(container)
    header_frame.pack(fill=X, pady=(0, 20))
    header_frame.configure(bg=COLORS["bg_main"])

    title_label = tk.Label(
        header_frame,
        text="Leki",
        font=("Arial", 24, "bold"),
        fg=COLORS["text"]
    )
    title_label.config(bg=COLORS["bg_main"])
    title_label.pack(side=LEFT)

    btn_add = tb.Button(
        header_frame,
        text="+ Добавить лекарство",
        bootstyle=SUCCESS,
        command=lambda: print("Открыть окно добавления")
    )
    btn_add.pack(side=RIGHT, padx=5)

    drug_table_view = build_drug_table(container)
    drug_table_view.pack(fill=BOTH, expand=True)

    return container