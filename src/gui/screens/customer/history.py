import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from src.services.logic.purchase import get_user_history
from src.gui.theme import COLORS


def build_history_screen(parent, user_id):
    """Ekran historii zakupów klienta.."""

    frame = tk.Frame(parent)
    frame.pack(fill=BOTH, expand=True)
    frame.configure(bg=COLORS["bg_main"])

    header_label = tb.Label(
        frame,
        text="📜 Moja Historia Zakupów",
        style="high.TLabel",
    )
    header_label.pack(pady=(0, 20))

    columns = [
        {"text": "Data i Godzina", "stretch": False, "width": 200},
        {"text": "Zakupione Produkty", "stretch": True},
        {"text": "Kwota", "stretch": False, "width": 120},
    ]

    rows = get_user_history(user_id)

    table = Tableview(
        master=frame,
        coldata=columns,
        rowdata=rows,
        paginated=True,
        pagesize=15,
        bootstyle=PRIMARY,
        autoalign=True
    )
    table.pack(fill=BOTH, expand=True)

    if not rows:
        no_data_lbl = tb.Label(
            frame,
            text="Nie masz jeszcze żadnych zapisanych zakupów.",
            font=("Arial", 12),
            foreground="gray"
        )
        no_data_lbl.pack(pady=20)

    return frame