import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import pandas as pd
import os

# Импорт путей и метода удаления из твоего менеджера
from src.customer_manager import remove_customer, CUSTOMER_FILE, ADDRESS_FILE


def open_customer_profile(parent, c_id, on_delete_callback=None):
    """Окно профиля клиента с адресом и историей."""
    top = tb.Toplevel(parent)
    top.title(f"Профиль клиента #{c_id}")
    top.geometry("550x700")
    top.grab_set()

    # --- ЛОГИКА ЗАГРУЗКИ ДАННЫХ ---

    # 1. Загрузка адреса
    address_info = "Данные об адресе не найдены."
    try:
        if os.path.exists(ADDRESS_FILE):
            df_addr = pd.read_csv(ADDRESS_FILE)
            # Ищем совпадение ID в первой колонке (обычно это id или customer_id)
            row = df_addr[df_addr.iloc[:, 0].astype(str) == str(c_id)]
            if not row.empty:
                r = row.iloc[0]
                # Берем данные по индексам колонок: 1-город, 2-улица, 3-индекс
                address_info = f"Город: {r.iloc[1]}\nУлица: {r.iloc[2]}\nИндекс: {r.iloc[3]}"
    except Exception as e:
        address_info = f"Ошибка загрузки адреса: {e}"

    # 2. Загрузка истории
    history_text = "История покупок пуста."
    history_path = os.path.join("database", "customer_history", f"{c_id}.txt")
    if os.path.exists(history_path):
        try:
            with open(history_path, 'r', encoding='utf-8') as f:
                history_text = f.read()
        except Exception as e:
            history_text = f"Ошибка чтения истории: {e}"

    # --- ИНТЕРФЕЙС ---
    container = tb.Frame(top, padding=20)
    container.pack(fill=BOTH, expand=True)

    tb.Label(container, text=f"Карточка клиента #{c_id}", font=("Arial", 18, "bold")).pack(pady=(0, 20))

    # Блок адреса (LabelFrame БЕЗ параметра padding)
    addr_group = tb.LabelFrame(container, text=" Адресная информация ")
    addr_group.pack(fill=X, pady=10)
    tb.Label(addr_group, text=address_info, font=("Arial", 11), justify=LEFT).pack(padx=15, pady=15, anchor=W)

    # Блок истории
    hist_group = tb.LabelFrame(container, text=" История операций ")
    hist_group.pack(fill=BOTH, expand=True, pady=10)

    history_box = tk.Text(hist_group, font=("Consolas", 10), bg="#f8f9fa", padx=10, pady=10)
    # Важно: Сначала вставляем, потом выключаем редактирование
    history_box.insert("1.0", history_text)
    history_box.config(state=DISABLED)
    history_box.pack(fill=BOTH, expand=True, padx=5, pady=5)

    # Кнопки
    btn_frame = tb.Frame(container)
    btn_frame.pack(fill=X, pady=(20, 0))

    def handle_delete():
        if messagebox.askyesno("Удаление", f"Удалить клиента #{c_id} и его адрес?"):
            if remove_customer(by_id=c_id):
                messagebox.showinfo("Успех", "Клиент удален.")
                top.destroy()
                if on_delete_callback:
                    on_delete_callback()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить.")

    tb.Button(btn_frame, text="Удалить", bootstyle=(DANGER, OUTLINE), command=handle_delete).pack(side=LEFT)
    tb.Button(btn_frame, text="Закрыть", bootstyle=SECONDARY, command=top.destroy).pack(side=RIGHT)