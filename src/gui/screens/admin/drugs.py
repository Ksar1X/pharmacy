import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview

from src.gui.theme import COLORS
from src.drug_manager import load_drugs
# Импортируем окна для добавления и редактирования
from src.gui.components.add_drug_window import open_add_drug_window
from src.gui.components.edit_drug_window import open_edit_drug_window


def render_admin_drugs(parent):
    """
    Экран управления складом медикаментов.
    """
    # Основной контейнер
    container = tk.Frame(parent, bg=COLORS["bg_main"])
    container.pack(fill=BOTH, expand=True, padx=30, pady=30)

    # --- 1. ВЕРХНЯЯ ПАНЕЛЬ ---
    header_frame = tk.Frame(container, bg=COLORS["bg_main"])
    header_frame.pack(fill=X, pady=(0, 20))

    # Используем tk.Label, так как нам нужен кастомный фон из COLORS
    tk.Label(
        header_frame,
        text="Склад медикаментов",
        font=("Arial", 24, "bold"),
        bg=COLORS["bg_main"],
        fg=COLORS["text"]
    ).pack(side=LEFT)

    # Функция обновления данных
    def refresh_table():
        update_table_data()

    # Кнопка добавления НОВОГО лекарства
    tb.Button(
        header_frame,
        text="+ Новый товар",
        bootstyle=SUCCESS,
        command=lambda: open_add_drug_window(parent, refresh_table)
    ).pack(side=RIGHT)

    # --- 2. ПОИСК ---
    search_frame = tk.Frame(container, bg=COLORS["bg_main"])
    search_frame.pack(fill=X, pady=(0, 10))

    tk.Label(search_frame, text="Поиск:", bg=COLORS["bg_main"], fg=COLORS["text"]).pack(side=LEFT, padx=(0, 10))

    search_ent = tb.Entry(search_frame, width=40)
    search_ent.pack(side=LEFT)

    tk.Label(
        search_frame,
        text=" (двойной клик по строке для изменения цены/кол-ва)",
        font=("Arial", 9, "italic"),
        bg=COLORS["bg_main"],
        fg="gray"
    ).pack(side=LEFT, padx=10)

    # --- 3. ТАБЛИЦА ---
    columns = [
        {"text": "ID", "stretch": False, "width": 60},
        {"text": "Название", "stretch": True},
        {"text": "Категория", "stretch": True},
        {"text": "Цена", "stretch": False, "width": 100},
        {"text": "Кол-во", "stretch": False, "width": 80},
        {"text": "Рецепт", "stretch": False, "width": 100},
    ]

    table = Tableview(
        master=container,
        coldata=columns,
        rowdata=[],
        bootstyle=PRIMARY,
        paginated=True,
        pagesize=15,
        stripecolor=(COLORS["bg_sidebar"], None),
    )
    table.pack(fill=BOTH, expand=True)

    def update_table_data(event=None):
        """Загрузка данных из CSV и фильтрация по поиску."""
        query = search_ent.get().strip().lower()
        df = load_drugs()

        if query:
            mask = (df['name'].str.lower().str.contains(query)) | \
                   (df['category'].str.lower().str.contains(query))
            filtered_df = df[mask]
        else:
            filtered_df = df

        rows = []
        for _, r in filtered_df.iterrows():
            rows.append((
                r['id'],
                r['name'],
                r['category'],
                f"{r['price']} zł",
                r['quantity'],
                r['requires_recipe']
            ))

        table.build_table_data(columns, rows)
        return "break"

    # --- 4. СОБЫТИЯ ---

    # Поиск при нажатии Enter
    search_ent.bind("<Return>", update_table_data)

    # Двойной клик для редактирования
    def on_row_double_click(event):
        selected_item = table.view.focus()
        if not selected_item:
            return

        row_values = table.view.item(selected_item)['values']
        if row_values:
            # Открываем окно редактирования (передаем данные строки и функцию обновления)
            open_edit_drug_window(parent, row_values, refresh_table)

    table.view.bind("<Double-1>", on_row_double_click)

    # Начальная загрузка
    update_table_data()

    return container