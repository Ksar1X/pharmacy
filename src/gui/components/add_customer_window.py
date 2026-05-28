import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from src.customer_manager import register_customer


def open_add_customer_window(parent, on_refresh_callback):
    """Otwiera okno modalne służące do rejestracji nowego klienta z funkcją sprawdzania poprawności danych."""

    window = tb.Toplevel(parent)
    window.title("Rejestracja nowego klienta")
    window.geometry("450x900")
    window.resizable(False, False)
    window.grab_set()

    form = tb.Frame(window, padding=30)
    form.pack(fill=BOTH, expand=True)

    tb.Label(form, text="Nowy klient", font=("Arial", 20, "bold")).pack(pady=(0, 20))

    def create_field(label_text, is_password=False):
        tb.Label(form, text=label_text, font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        entry = tb.Entry(form, show="*" if is_password else "")
        entry.pack(fill=X, pady=5)
        return entry

    ent_name = create_field("Imię:")
    ent_surname = create_field("Nazwisko:")
    ent_login = create_field("Login:")
    ent_password = create_field("Hasło:", is_password=True)

    password_hint = tb.Label(
        form,
        text="Co najmniej 6 znaków, 1 wielka litera, 1 cyfra",
        font=("Arial", 8),
        foreground="gray"
    )
    password_hint.pack(anchor=W)

    tb.Separator(form, bootstyle=SECONDARY).pack(pady=15)
    tb.Label(form, text="Adres zamieszkania", font=("Arial", 10, "bold")).pack(anchor=W)

    ent_city = create_field("Miasto:")
    ent_street = create_field("Ulica:")
    ent_zip = create_field("Kod pocztowy:")

    def validate_password(pwd):
        """Sprawdza hasło i zwraca listę błędów."""
        errors = []
        if len(pwd) < 6:
            errors.append("krótki")
        if not any(char.isdigit() for char in pwd):
            errors.append("brak cyfry")
        if not any(char.isupper() for char in pwd):
            errors.append("brak wielkiej litery")
        return errors

    def check_live(event):
        """Odświeża podpowiedź przy każdym naciśnięciu klawisza."""
        pwd = ent_password.get()
        if not pwd:
            password_hint.config(text="Co najmniej 6 znaków, 1 wielka litera, 1 cyfra", foreground="gray")
            return

        errors = validate_password(pwd)
        if errors:
            password_hint.config(text="Słabe hasło: " + ", ".join(errors), foreground="orange")
        else:
            password_hint.config(text="Świetne hasło!", foreground="green")

    ent_password.bind("<KeyRelease>", check_live)

    def handle_submit():
        name = ent_name.get().strip()
        surname = ent_surname.get().strip()
        login = ent_login.get().strip()
        pwd = ent_password.get().strip()
        city = ent_city.get().strip()
        street = ent_street.get().strip()
        zip_code = ent_zip.get().strip()

        if not all([name, surname, login, pwd, city, street, zip_code]):
            messagebox.showwarning("Uwaga", "Wszystkie pola muszą zostać wypełnione!")
            return

        pwd_errors = validate_password(pwd)
        if pwd_errors:
            messagebox.showerror("Błąd", "Hasło nie spełnia wymagań!")
            password_hint.config(foreground="red")
            return

        try:
            result = register_customer(
                name, surname, login, pwd, "customer",
                city, street, zip_code
            )

            if result:
                messagebox.showinfo("Sukces", f"Klient został zarejestrowany!\nID: {result}")
                window.destroy()
                if on_refresh_callback:
                    on_refresh_callback()
            else:
                messagebox.showerror("Błąd", "Nazwa użytkownika jest już zajęta lub wystąpił błąd bazy danych.")
        except Exception as e:
            messagebox.showerror("Błąd krytyczny", f"Nie udało się zapisać: {e}")

    btn_submit = tb.Button(
        form,
        text="Zarejestruj klienta",
        bootstyle=SUCCESS,
        command=handle_submit
    )
    btn_submit.pack(fill=X, pady=25)

    tb.Button(
        form,
        text="Anulowanie",
        bootstyle=(SECONDARY, OUTLINE),
        command=window.destroy
    ).pack(fill=X)

    return window