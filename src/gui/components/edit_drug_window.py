import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import pandas as pd
import os

DRUGS_FILE = "database/drugs.xlsx"


def open_edit_drug_window(parent, drug_data, on_refresh_callback):
    top = tb.Toplevel(parent)
    top.title(f"Edycja: {drug_data[1]}")
    top.geometry("400x450")
    top.grab_set()

    container = tb.Frame(top, padding=20)
    container.pack(fill=BOTH, expand=True)

    tk.Label(container, text=f"Lek: {drug_data[1]}", font=("Arial", 12, "bold")).pack(pady=(0, 20))


    tk.Label(container, text="Zmień cenę:").pack(anchor=W)
    ent_price = tb.Entry(container)

    initial_price = str(drug_data[3]).replace(" zł", "").replace(",", ".").strip()
    ent_price.insert(0, initial_price)
    ent_price.pack(fill=X, pady=5)


    tk.Label(container, text=f"Zmień ilość (obecnie: {drug_data[4]}):").pack(anchor=W, pady=(10, 0))
    ent_qty = tb.Entry(container)
    ent_qty.insert(0, str(drug_data[4]).strip())
    ent_qty.pack(fill=X, pady=5)

    def save_changes():
        try:
            price_val = ent_price.get().replace(",", ".").replace("zł", "").strip()
            qty_val = ent_qty.get().strip()

            if not price_val or not qty_val:
                messagebox.showwarning("Uwaga", "Pola nie mogą być puste!")
                return

            final_price = float(price_val)
            final_qty = int(qty_val)

            if not os.path.exists(DRUGS_FILE):
                messagebox.showerror("Błąd", "Nie znaleziono pliku bazy danych XLSX!")
                return

            df = pd.read_excel(DRUGS_FILE)

            target_id = str(drug_data[0])

            idx = df[df['id'].astype(str) == target_id].index

            if not idx.empty:
                df.at[idx[0], 'price'] = final_price
                df.at[idx[0], 'quantity'] = final_qty

                df.to_excel(DRUGS_FILE, index=False)

                messagebox.showinfo("Sukces", "Dane w pliku XLSX zostały zaktualizowane!")
                top.destroy()
                if on_refresh_callback:
                    on_refresh_callback()
            else:
                messagebox.showerror("Błąd", f"ID {target_id} nie znaleziono!")

        except ValueError as e:
            messagebox.showerror("Błąd danych", f"Wprowadź liczby!\nSzczegóły: {e}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Problem z plikiem Excel: {e}")

    btn_frame = tb.Frame(container)
    btn_frame.pack(fill=X, pady=20)

    tb.Button(btn_frame, text="Zapisz", style='my.TButton', command=save_changes).pack(side=LEFT, fill=X, expand=True, padx=5)
    tb.Button(btn_frame, text="Anulowanie", style='my.TButton', command=top.destroy).pack(side=LEFT, fill=X, expand=True, padx=5)

    return top