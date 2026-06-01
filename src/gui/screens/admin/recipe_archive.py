import ttkbootstrap as tb
import tkinter as tk
from ttkbootstrap.tableview import Tableview
import pandas as pd
import os

from src.gui.theme import *

def build_recipe_archive_screen(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=24, pady=20)
    frame.configure(bg=COLORS["bg_main"])

    tb.Label(frame, text="Archiwum Recept (NFZ)", style="high.TLabel").pack(pady=10)

    columns = [
        {"text": "Data transakcji", "stretch": True},
        {"text": "Numer recepty", "stretch": True},
        {"text": "Pacjent", "stretch": True},
        {"text": "Refundacja", "stretch": False, "width": 120},
    ]

    file_path = 'database/base_of_recipes.xlsx'
    rows = []

    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
            rows = df.values.tolist()
        except Exception as e:
            print(f"Błąd ładowania Excel: {e}")

    table = Tableview(
        master=frame,
        coldata=columns,
        rowdata=rows,
        paginated=True,
        pagesize=15,
        bootstyle="secondary",
    )
    table.pack(fill="both", expand=True)

    return frame