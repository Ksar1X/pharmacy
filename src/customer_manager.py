"""
Moduł obsługi klienta.
Odpowiada za rejestrację, wczytywanie i usuwanie danych klientów (plik CSV).
Zaimplementowano tu m.in. funkcję zagnieżdżoną oraz funkcję wielu zmiennych.
"""
import pandas as pd
import csv
import os
from src.utils import generate_id, hash_password

CUSTOMER_FILE = 'database/customer.csv'
ADDRESS_FILE = 'database/address.csv'
HISTORY_DIR = 'database/customer_history/'

# Tworzenie folderu na historię, jeśli nie istnieje
os.makedirs(HISTORY_DIR, exist_ok=True)


def load_customers():
    """Wczytuje bazę klientów z pliku CSV. Posiada obsługę wyjątków (brak pliku)."""
    try:
        return pd.read_csv(CUSTOMER_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=['id', 'name', 'surname', 'login', 'password_hash', 'role'])


def register_customer(name, surname, login, password, role="customer", *address_args):
    """
    Rejestracja nowego klienta.
    Spełnia wymagania: funkcja wielu zmiennych wejściowych (*address_args) oraz funkcja zagnieżdżona.
    """
    df = load_customers()
    if login in df['login'].values:
        print("Błąd: Użytkownik o podanym loginie już istnieje.")
        return None

    customer_id = generate_id()
    hashed_pw = hash_password(password)

    # --- FUNKCJA ZAGNIEŻDŻONA ---
    def _save_address(c_id, args):
        """Zapisuje adres klienta. Oczekuje dokładnie 3 argumentów (city, street, zip_code)."""
        if len(args) != 3:
            raise ValueError("Dla adresu wymagane są dokładnie 3 argumenty: city, street, zip_code")
        try:
            with open(ADDRESS_FILE, 'a', newline='', encoding='utf-8') as f:
                csv.writer(f).writerow([c_id, args[0], args[1], args[2]])
        except IOError as e:
            print("Błąd podczas zapisu adresu: {}".format(e))

    # ----------------------------

    try:
        # 1. Zapis klienta do bazy
        with open(CUSTOMER_FILE, 'a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow([customer_id, name, surname, login, hashed_pw, role])

        # 2. Wywołanie funkcji zagnieżdżonej (zapis adresu)
        _save_address(customer_id, address_args)

        # 3. Utworzenie unikalnego pliku tekstowego z historią (wymaganie projektowe)
        history_path = os.path.join(HISTORY_DIR, "{}.txt".format(customer_id))
        with open(history_path, 'w', encoding='utf-8') as hf:
            hf.write("Historia zakupów klienta: {} {} (ID: {})\n".format(name, surname, customer_id))
            hf.write("=" * 50 + "\n")

        print("Sukces! Klient {} został zarejestrowany. Przydzielono ID: {}".format(login, customer_id))
        return customer_id
    except Exception as e:
        print("Krytyczny błąd podczas rejestracji klienta: {}".format(e))
        return None


def remove_customer(by_id=None, by_name=None):
    """Usuwanie danych klienta z bazy. Opcje: względem ID lub Imienia (NAME)."""
    df = load_customers()
    initial_len = len(df)

    if by_id is not None:
        df = df[df['id'].astype(str) != str(by_id)]
    elif by_name is not None:
        df = df[df['name'] == by_name]
    else:
        print("Błąd: Należy określić parametr by_id lub by_name.")
        return False

    if len(df) < initial_len:
        df.to_csv(CUSTOMER_FILE, index=False)
        print("Dane klienta zostały pomyślnie usunięte.")
        return True

    print("Nie znaleziono klienta w bazie.")
    return False
