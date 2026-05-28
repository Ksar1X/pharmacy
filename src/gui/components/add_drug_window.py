import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from src.drug_manager import add_or_update_drug


def open_add_drug_window(parent, on_refresh_callback):
    top = tb.Toplevel(parent)
    top.title("Podanie leku")
    top.geometry("400x550")
    top.grab_set()

    container = tb.Frame(top, padding=20)
    container.pack(fill=BOTH, expand=True)

    tb.Label(container, text="Informacje o preparacie", font=("Arial", 14, "bold")).pack(pady=(0, 20))

    def create_field(label):
        tb.Label(container, text=label).pack(anchor=W, pady=(5, 0))
        entry = tb.Entry(container)
        entry.pack(fill=X, pady=5)
        return entry

    ent_name = create_field("Nazwa leku")
    ent_cat = create_field("Kategoria (tabletki, syrop itp.)")
    ent_price = create_field("Cena za sztukę")
    ent_qty = create_field("Ilość")

    recipe_var = tk.BooleanVar()
    tb.Checkbutton(container, text="Potrzebny jest przepis", variable=recipe_var, bootstyle="round-toggle").pack(pady=10,
                                                                                                           anchor=W)

    def handle_submit():
        name = ent_name.get()
        cat = ent_cat.get()
        price = ent_price.get()
        qty = ent_qty.get()
        is_recipe = "Tak" if recipe_var.get() else "Nie"

        if not all([name, cat, price, qty]):
            messagebox.showwarning("Błąd", "Wypełnij wszystkie pola!")
            return

        try:
            success, msg = add_or_update_drug(name, cat, price, qty, is_recipe)
            if success:
                messagebox.showinfo("Sukces", msg)
                top.destroy()
                on_refresh_callback()  # Обновляем таблицу лекарств
        except Exception as e:
            messagebox.showerror("Błąd", f"Nieprawidłowe dane: {e}")

    # Кнопки
    btn_save = tb.Button(container, text="Potwierdź", bootstyle=SUCCESS, command=handle_submit)
    btn_save.pack(fill=X, pady=(20, 5))

    tb.Button(container, text="Anulowanie", bootstyle=SECONDARY, command=top.destroy).pack(fill=X)