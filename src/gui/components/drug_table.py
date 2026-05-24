import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview

from src.gui.fonts import *
from src.gui.theme import *
from src.drug_manager import load_drugs


def get_formatted_rows(df):
    """Преобразует DataFrame в список кортежей для отображения в таблице."""
    rows = []
    if df.empty:
        return rows

    for _, drug in df.iterrows():
        # Статус наличия
        qty = drug.get('quantity', 0)
        status = "Dostępny" if qty > 0 else "Brak"

        # Формируем строку (порядок должен совпадать с coldata)
        rows.append((
            drug.get('id', ''),
            drug.get('name', ''),
            drug.get('category', ''),
            f"{float(drug.get('price', 0)):.2f} zł",
            qty,
            "Tak" if str(drug.get('requires_recipe')).lower() == 'true' else "Nie",
            status
        ))
    return rows


def build_drug_table(parent):
    """Создает компонент таблицы с поиском."""
    table_wrap = tk.Frame(parent)
    table_wrap.pack(fill="both", expand=True)
    table_wrap.configure(
        bg=COLORS["bg_sidebar"],
        highlightbackground=COLORS["border"],
        highlightthickness=1
    )

    # --- Шапка таблицы ---
    t_header = tk.Frame(table_wrap, bg=COLORS["bg_sidebar"])
    t_header.pack(fill="x", padx=16, pady=(14, 8))

    t_title = tk.Label(
        t_header,
        text="Lista Leków",
        font=FONT_HEADING,
        bg=COLORS["bg_sidebar"],
        fg=COLORS["text"]
    )
    t_title.pack(side="left")

    # --- Поле поиска ---
    search_ent = tb.Entry(t_header, bootstyle=SECONDARY, width=25)
    search_ent.pack(side="right")
    search_ent.insert(0, "")  # Пустое поле по умолчанию

    # --- Определение колонок ---
    columns = [
        {"text": "ID", "stretch": False, "width": 70},
        {"text": "Nazwa", "stretch": True},
        {"text": "Category", "stretch": True},
        {"text": "Cena", "stretch": False, "width": 100},
        {"text": "Ilość", "stretch": False, "width": 80},
        {"text": "Recepta", "stretch": False, "width": 100},
        {"text": "Status", "stretch": False, "width": 110},
    ]

    # --- Создание таблицы ---
    table = Tableview(
        master=table_wrap,
        coldata=columns,
        rowdata=[],  # Загрузим через search_drugs() ниже
        bootstyle=DARK,
        stripecolor=(COLORS["bg_main"], None),
        paginated=True,
        pagesize=10,
        autofit=True
    )
    table.pack(fill="both", expand=True, padx=8, pady=8)

    def search_drugs(event=None):
        """Логика фильтрации данных."""
        query = search_ent.get().strip().lower()
        df = load_drugs()

        if query:
            # Фильтрация по id или name
            mask = (df['id'].astype(str).str.contains(query, case=False, na=False)) | \
                   (df['name'].astype(str).str.lower().str.contains(query, case=False, na=False))
            filtered_df = df[mask]
        else:
            filtered_df = df

        # Обновление данных в таблице
        new_rows = get_formatted_rows(filtered_df)
        table.build_table_data(coldata=columns, rowdata=new_rows)

        # Обновляем заголовок с количеством
        t_title.config(text=f"Leki ({len(new_rows)})")

        # Возвращаем фокус и блокируем стандартный Enter
        search_ent.focus_set()
        return "break"

    # Привязка клавиши Enter
    search_ent.bind("<Return>", search_drugs)

    # Первичная загрузка данных
    search_drugs()

    return table_wrap