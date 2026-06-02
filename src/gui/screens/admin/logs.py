import ttkbootstrap as tb
import tkinter as tk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from src.services.backend.logger import load_logs

from src.gui.theme import *

def render_admin_logs(parent, **kwargs):
    container = tk.Frame(parent)
    container.pack(fill="both", expand=True, padx=24, pady=20)
    container.configure(bg=COLORS["bg_main"])

    tb.Label(container, text="Historia aktywności systemu", style="high.TLabel").pack(pady=(0, 20))

    btn_refresh = tb.Button(container, text="Odśwież logi", bootstyle="secondary-outline", style="my.TButton" ,command=lambda: refresh_logs())
    btn_refresh.pack(anchor=E, pady=5)

    columns: list = [
        {"text": "Data i Godzina", "stretch": False, "width": 180},
        {"text": "Użytkownik", "stretch": False, "width": 120},
        {"text": "Poziom", "stretch": False, "width": 100},
        {"text": "Opis zdarzenia", "stretch": True}
    ]

    table = Tableview(
        master=container,
        coldata=columns,
        rowdata=[],
        paginated=True,
        pagesize=20,
        bootstyle=SECONDARY
    )
    table.pack(fill=BOTH, expand=True)

    def refresh_logs():
        df = load_logs()
        if not df.empty:
            df = df.sort_values(by="Data", ascending=False)
            rows = df.values.tolist()
            table.build_table_data(columns, rows)

    refresh_logs()
    return container