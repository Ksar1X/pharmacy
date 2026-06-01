"""
Moduł obsługi klienta.
Odpowiada za rejestrację, wczytywanie, autoryzację i usuwanie danych klientów (pliki CSV).
"""
import pandas as pd
import csv
import os

from src.services.backend.logger import log_event
from src.utils import generate_id, hash_password, check_password


CUSTOMER_FILE = 'database/customer.csv'
ADDRESS_FILE = 'database/address.csv'
HISTORY_DIR = 'database/customer_history/'

os.makedirs(HISTORY_DIR, exist_ok=True)

def load_customers():
    """Wczytuje bazę klientów z pliku CSV. Obsługuje brak pliku."""
    try:
        return pd.read_csv(CUSTOMER_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=['id', 'name', 'surname', 'login', 'password_hash', 'role'])

def load_addresses():
    """Wczytuje bazę adresów z pliku CSV. Obsługuje brak pliku."""
    try:
        return pd.read_csv(ADDRESS_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=['customer_id', 'city', 'street', 'zip_code'])

def save_customers(df):
    """Zapisuje DataFrame z klientami do pliku CSV."""
    try:
        df.to_csv(CUSTOMER_FILE, index=False)
    except Exception as e:
        print("Błąd zapisu pliku klientów: {}".format(e))

def save_addresses(df):
    """Zapisuje DataFrame z adresami do pliku CSV."""
    try:
        df.to_csv(ADDRESS_FILE, index=False)
    except Exception as e:
        print("Błąd zapisu pliku adresów: {}".format(e))

def find_customer_by_id(customer_id):
    """Wyszukuje klienta po ID. Zwraca słownik lub None."""
    df = load_customers()
    if df.empty:
        return None
    result = df[df['id'].astype(str) == str(customer_id)]
    if not result.empty:
        return result.iloc[0].to_dict()
    print("Błąd: Nie znaleziono klienta o ID {}.".format(customer_id))
    return None

def find_customer_by_name(name, surname):
    """Wyszukuje klienta po imieniu i nazwisku. Zwraca słownik lub None."""
    df = load_customers()
    if df.empty:
        return None
    result = df[(df['name'].str.lower() == name.lower()) & (df['surname'].str.lower() == surname.lower())]
    if not result.empty:
        return result.iloc[0].to_dict()
    print("Błąd: Nie znaleziono klienta o danych {} {}.".format(name, surname))
    return None

def login_customer(login, password):
    """
    Autoryzuje klienta. Zwraca jego rolę (role) przy sukcesie,
    lub None przy błędnych danych logowania.
    """
    df = load_customers()
    if df.empty:
        return None
    user_row = df[df['login'] == login]

    if user_row.empty:
        print("Błąd: Nie znaleziono użytkownika o loginie '{}'.".format(login))
        return None

    hashed_from_db = user_row.iloc[0]['password_hash']
    user_role = user_row.iloc[0]['role']
    user_id = user_row.iloc[0]['id']

    if check_password(password, hashed_from_db):
        log_event(f"Użytkownik {user_role} zalogował się na swoje konto", level="INFO")
        return user_role, user_id
    else:
        print("Błąd: Niepoprawne hasło dla użytkownika '{}'.".format(login))
        return None

def register_customer(name, surname, login, password, role="customer", *address_args):
    """
    Rejestracja nowego klienta.
    Zawiera funkcję wielu zmiennych (*address_args) oraz funkcję zagnieżdżoną.
    """
    df = load_customers()
    if df.empty:
        return None
    if login in df['login'].values:
        print("Błąd: Użytkownik o podanym loginie już istnieje.")
        return None

    customer_id = generate_id()
    hashed_pw = hash_password(password)

    def _save_address(c_id, args):
        """Zapisuje adres klienta. Oczekuje dokładnie 3 argumentów (city, street, zip_code)."""
        if len(args) != 3:
            raise ValueError("Dla adresu wymagane są dokładnie 3 argumenty: city, street, zip_code")
        try:
            with open(ADDRESS_FILE, 'a', newline='', encoding='utf-8') as f:
                csv.writer(f).writerow([c_id, args[0], args[1], args[2]])
        except IOError as e:
            print("Błąd podczas zapisu adresu: {}".format(e))

    try:
        needs_newline = False
        if os.path.exists(CUSTOMER_FILE) and os.path.getsize(CUSTOMER_FILE) > 0:
            with open(CUSTOMER_FILE, 'rb+') as f_check:
                f_check.seek(-1, os.SEEK_END)
                last_char = f_check.read(1)
                if last_char != b'\n':
                    needs_newline = True

        with open(CUSTOMER_FILE, 'a', newline='', encoding='utf-8') as f:
            if needs_newline:
                f.write('\n')

            writer = csv.writer(f)
            writer.writerow([customer_id, name, surname, login, hashed_pw, role])

        _save_address(customer_id, address_args)

        history_path = os.path.join(HISTORY_DIR, "{}.txt".format(customer_id))
        with open(history_path, 'w', encoding='utf-8') as hf:
            hf.write("Historia zakupów klienta: {} {} (ID: {})\n".format(name, surname, customer_id))
            hf.write("=" * 50 + "\n")

        print("Sukces! Klient {} został zarejestrowany. Przydzielono ID: {}".format(login, customer_id))
        log_event(f"Dodano nowy klient: {name}", level="INFO")
        return customer_id
    except Exception as e:
        print("Krytyczny błąd podczas rejestracji klienta: {}".format(e))
        return None

def remove_customer(by_id=None, by_name=None):
    """
    Usuwanie danych klienta z OBU plików (customer.csv oraz address.csv).
    Opcje: względem ID lub Imienia (NAME).
    """
    df_cust = load_customers()
    df_addr = load_addresses()

    ids_to_remove = []

    if by_id is not None:
        ids_to_remove = [str(by_id)]
    elif by_name is not None:
        matched = df_cust[df_cust['name'].str.lower() == by_name.lower()]
        ids_to_remove = matched['id'].astype(str).tolist()
    else:
        print("Błąd: Należy określić parametr by_id lub by_name.")
        return False

    if not ids_to_remove:
        print("Nie znaleziono klienta spełniającego kryteria.")
        return False

    df_cust = df_cust[~df_cust['id'].astype(str).isin(ids_to_remove)]
    save_customers(df_cust)

    df_addr = df_addr[~df_addr['customer_id'].astype(str).isin(ids_to_remove)]
    save_addresses(df_addr)

    print("Dane klienta zostały pomyślnie usunięte z obu baz danych (customer i address).")
    log_event("Usunięto konto klienta", level="INFO")
    return True