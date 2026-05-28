import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import pandas as pd
import os

from src.customer_manager import remove_customer, ADDRESS_FILE


def open_customer_profile(parent, c_id, on_delete_callback=None):
    """Okno profilu klienta zawierające adres i historię."""
    top = tb.Toplevel(parent)
    top.title(f"Profil klienta #{c_id}")
    top.geometry("550x700")
    top.grab_set()

    address_info = "Nie znaleziono danych dotyczących adresu."
    try:
        if os.path.exists(ADDRESS_FILE):
            df_addr = pd.read_csv(ADDRESS_FILE)
            row = df_addr[df_addr.iloc[:, 0].astype(str) == str(c_id)]
            if not row.empty:
                r = row.iloc[0]
                address_info = f"Miasto: {r.iloc[1]}\nUlica: {r.iloc[2]}\nIndeks: {r.iloc[3]}"
    except Exception as e:
        address_info = f"Błąd podczas ładowania adresu: {e}"

    history_text = "Historia zakupów jest pusta."
    history_path = os.path.join("database", "customer_history", f"{c_id}.txt")
    if os.path.exists(history_path):
        try:
            with open(history_path, 'r', encoding='utf-8') as f:
                history_text = f.read()
        except Exception as e:
            history_text = f"Błąd podczas odczytywania historii: {e}"

    container = tb.Frame(top, padding=20)
    container.pack(fill=BOTH, expand=True)

    tb.Label(container, text=f"Karta klienta #{c_id}", font=("Arial", 18, "bold")).pack(pady=(0, 20))

    addr_group = tb.LabelFrame(container, text=" Dane adresowe ")
    addr_group.pack(fill=X, pady=10)
    tb.Label(addr_group, text=address_info, font=("Arial", 11), justify=LEFT).pack(padx=15, pady=15, anchor=W)

    hist_group = tb.LabelFrame(container, text=" Historia operacji ")
    hist_group.pack(fill=BOTH, expand=True, pady=10)

    history_box = tk.Text(hist_group, font=("Consolas", 10), bg="#f8f9fa", padx=10, pady=10)
    history_box.insert("1.0", history_text)
    history_box.config(state=DISABLED)
    history_box.pack(fill=BOTH, expand=True, padx=5, pady=5)

    btn_frame = tb.Frame(container)
    btn_frame.pack(fill=X, pady=(20, 0))

    def handle_delete():
        if messagebox.askyesno("Usunięcie", f"Usuń klienta #{c_id} oraz jego adres?"):
            if remove_customer(by_id=c_id):
                messagebox.showinfo("Sukces", "Klient został usunięty.")
                top.destroy()
                if on_delete_callback:
                    on_delete_callback()
            else:
                messagebox.showerror("Błąd", "Nie udało się usunąć.")

    tb.Button(btn_frame, text="Usuń", bootstyle=(DANGER, OUTLINE), command=handle_delete).pack(side=LEFT)
    tb.Button(btn_frame, text="Zamknij", bootstyle=SECONDARY, command=top.destroy).pack(side=RIGHT)