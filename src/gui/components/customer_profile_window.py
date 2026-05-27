import tkinter as tk
from turtledemo.nim import COLOR

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import pandas as pd
import os

from src.gui.theme import *

from src.customer_manager import remove_customer, CUSTOMER_FILE, ADDRESS_FILE


def open_customer_profile(parent, c_id, on_delete_callback=None):
    """
    Окно профиля клиента: отображает данные из customer.csv, address.csv
    и историю из текстового файла.
    """
    top = tb.Toplevel(parent)
    top.title(f"Profil Klienta ID: {c_id}")
    top.geometry("550x900")
    top.grab_set()

    address_info = "Brak danych adresowych в базе."
    try:
        if os.path.exists(ADDRESS_FILE):
            df_addr = pd.read_csv(ADDRESS_FILE)
            # Проверь имя колонки в твоем CSV (customer_id или id)
            addr_col = 'customer_id' if 'customer_id' in df_addr.columns else 'id'
            row = df_addr[df_addr[addr_col].astype(str) == str(c_id)]
            if not row.empty:
                r = row.iloc[0]
                address_info = f"Miasto: {r.get('city', '-')}\nUlica: {r.get('street', '-')}\nKod: {r.get('zip', '-')}"
    except Exception as e:
        address_info = f"Błąd ładowania adresu: {e}"

    history_text = "Brak historii zakupów для данного клиента."
    history_path = f"database/customer_history/{c_id}.txt"
    if os.path.exists(history_path):
        try:
            with open(history_path, 'r', encoding='utf-8') as f:
                history_text = f.read()
        except Exception as e:
            history_text = f"Nie udało się odczytać historii: {e}"


    container = tb.Frame(top, padding=20)
    container.pack(fill=BOTH, expand=True)

    tb.Label(
        container,
        text=f"Szczegóły klienta #{c_id}",
        font=("Arial", 18, "bold"),
        bootstyle=SUCCESS,
    ).pack(pady=(0, 20))


    addr_group = tb.LabelFrame(container, text=" Informacja adresowa ", bootstyle=INFO)
    addr_group.pack(fill=X, pady=10)

    tb.Label(
        addr_group,
        text=address_info,
        font=("Arial", 11),
        justify=LEFT
    ).pack(padx=15, pady=15, anchor=W)

    hist_group = tb.LabelFrame(container, text=" Historia operacji ", bootstyle=SECONDARY)
    hist_group.pack(fill=BOTH, expand=True, pady=10)

    txt_scroll = tb.Scrollbar(hist_group)
    txt_scroll.pack(side=RIGHT, fill=Y)

    history_box = tk.Text(
        hist_group,
        font=("Consolas", 10),
        bg="#f8f9fa",
        fg="#333",
        yscrollcommand=txt_scroll.set,
        padx=10,
        pady=10,
        height=10
    )
    history_box.insert("1.0", history_text)
    history_box.config(state=DISABLED)
    history_box.pack(fill=BOTH, expand=True)
    txt_scroll.config(command=history_box.yview)

    btn_frame = tb.Frame(container)
    btn_frame.pack(fill=X, pady=(20, 0))

    def handle_delete():
        """Логика удаления клиента."""
        confirm = messagebox.askyesno(
            "Potwierdzenie",
            f"Czy na pewno chcesz usunąć klienta #{c_id}?\nOperacja jest nieodwracalna!"
        )
        if confirm:
            if remove_customer(by_id=c_id):
                messagebox.showinfo("Sukces", "Klient został usunięty.")
                top.destroy()
                if on_delete_callback:
                    on_delete_callback()  # Обновляем таблицу
            else:
                messagebox.showerror("Błąd", "Nie udało się usunąć klienta.")

    tb.Button(
        btn_frame,
        text="Usuń klienta",
        bootstyle=(DANGER, OUTLINE),
        command=handle_delete
    ).pack(side=LEFT)

    tb.Button(
        btn_frame,
        text="Zamknij",
        bootstyle=SECONDARY,
        command=top.destroy
    ).pack(side=RIGHT)

    return top