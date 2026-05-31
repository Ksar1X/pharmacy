import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from src.services.backend.drug_manager import remove_drug


def open_delete_drug_window(parent, refresh_callback):
    delete_win = tb.Toplevel(master=parent)
    delete_win.title("Usuwanie")
    delete_win.geometry("300x200")
    delete_win.resizable(False, False)
    delete_win.grab_set()  # Модальное окно

    container = tb.Frame(delete_win, padding=20)
    container.pack(fill=BOTH, expand=True)

    tb.Label(container, text="Podaj ID leku do usunięcia:", font=("Arial", 10)).pack(pady=10)

    id_entry = tb.Entry(container)
    id_entry.pack(fill=X, pady=5)
    id_entry.focus_set()

    def handle_delete():
        did = id_entry.get().strip()
        if not did:
            return

        if messagebox.askyesno("Potwierdzenie", f"Czy na pewno usunąć lek o ID: {did}?"):
            if remove_drug(by_id=did):
                messagebox.showinfo("Sukces", "Lek usunięty.")
                refresh_callback()
                delete_win.destroy()
            else:
                messagebox.showerror("Błąd", "Nie znaleziono leku.")

    btn_del = tb.Button(container, text="Usuń", bootstyle="danger", command=handle_delete)
    btn_del.pack(fill=X, pady=10)