import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from src.drug_manager import add_or_update_drug


def open_add_drug_window(parent, on_refresh_callback):
    top = tb.Toplevel(parent)
    top.title("Добавление медикамента")
    top.geometry("400x550")
    top.grab_set()

    container = tb.Frame(top, padding=20)
    container.pack(fill=BOTH, expand=True)

    tb.Label(container, text="Данные препарата", font=("Arial", 14, "bold")).pack(pady=(0, 20))

    # Поля ввода
    def create_field(label):
        tb.Label(container, text=label).pack(anchor=W, pady=(5, 0))
        entry = tb.Entry(container)
        entry.pack(fill=X, pady=5)
        return entry

    ent_name = create_field("Название лекарства")
    ent_cat = create_field("Категория (таблетки, сироп и т.д.)")
    ent_price = create_field("Цена за ед.")
    ent_qty = create_field("Количество")

    # Чекбокс для рецепта
    recipe_var = tk.BooleanVar()
    tb.Checkbutton(container, text="Требуется рецепт", variable=recipe_var, bootstyle="round-toggle").pack(pady=10,
                                                                                                           anchor=W)

    def handle_submit():
        name = ent_name.get()
        cat = ent_cat.get()
        price = ent_price.get()
        qty = ent_qty.get()
        is_recipe = "Да" if recipe_var.get() else "Нет"

        if not all([name, cat, price, qty]):
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        try:
            success, msg = add_or_update_drug(name, cat, price, qty, is_recipe)
            if success:
                messagebox.showinfo("Успех", msg)
                top.destroy()
                on_refresh_callback()  # Обновляем таблицу лекарств
        except Exception as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {e}")

    # Кнопки
    btn_save = tb.Button(container, text="Подтвердить", bootstyle=SUCCESS, command=handle_submit)
    btn_save.pack(fill=X, pady=(20, 5))

    tb.Button(container, text="Отмена", bootstyle=SECONDARY, command=top.destroy).pack(fill=X)