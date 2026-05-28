import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import pandas as pd
import os

# Путь теперь к XLSX
DRUGS_FILE = "database/drugs.xlsx"


def open_edit_drug_window(parent, drug_data, on_refresh_callback):
    top = tb.Toplevel(parent)
    top.title(f"Редактирование: {drug_data[1]}")
    top.geometry("400x450")
    top.grab_set()

    container = tb.Frame(top, padding=20)
    container.pack(fill=BOTH, expand=True)

    tk.Label(container, text=f"Препарат: {drug_data[1]}", font=("Arial", 12, "bold")).pack(pady=(0, 20))

    # Поле цены
    tk.Label(container, text="Изменить цену:").pack(anchor=W)
    ent_price = tb.Entry(container)
    # Очистка входящих данных
    initial_price = str(drug_data[3]).replace(" zł", "").replace(",", ".").strip()
    ent_price.insert(0, initial_price)
    ent_price.pack(fill=X, pady=5)

    # Поле количества
    tk.Label(container, text=f"Изменить количество (сейчас: {drug_data[4]}):").pack(anchor=W, pady=(10, 0))
    ent_qty = tb.Entry(container)
    ent_qty.insert(0, str(drug_data[4]).strip())
    ent_qty.pack(fill=X, pady=5)

    def save_changes():
        try:
            # Очистка ввода
            price_val = ent_price.get().replace(",", ".").replace("zł", "").strip()
            qty_val = ent_qty.get().strip()

            if not price_val or not qty_val:
                messagebox.showwarning("Внимание", "Поля не могут быть пустыми!")
                return

            final_price = float(price_val)
            final_qty = int(qty_val)

            if not os.path.exists(DRUGS_FILE):
                messagebox.showerror("Ошибка", "Файл базы данных XLSX не найден!")
                return

            # Читаем Excel
            df = pd.read_excel(DRUGS_FILE)

            target_id = str(drug_data[0])
            # Находим строку по ID
            idx = df[df['id'].astype(str) == target_id].index

            if not idx.empty:
                df.at[idx[0], 'price'] = final_price
                df.at[idx[0], 'quantity'] = final_qty

                # Сохраняем в Excel
                df.to_excel(DRUGS_FILE, index=False)

                messagebox.showinfo("Успех", "Данные в XLSX обновлены!")
                top.destroy()
                if on_refresh_callback:
                    on_refresh_callback()
            else:
                messagebox.showerror("Ошибка", f"ID {target_id} не найден!")

        except ValueError as e:
            messagebox.showerror("Ошибка данных", f"Введите числа!\nДетали: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Проблема с Excel файлом: {e}")

    # Кнопки
    btn_frame = tb.Frame(container)
    btn_frame.pack(fill=X, pady=20)

    tb.Button(btn_frame, text="Сохранить", bootstyle=SUCCESS, command=save_changes).pack(side=LEFT, fill=X, expand=True,
                                                                                         padx=5)
    tb.Button(btn_frame, text="Отмена", bootstyle=SECONDARY, command=top.destroy).pack(side=LEFT, fill=X, expand=True,
                                                                                       padx=5)

    return top