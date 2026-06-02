"""
Moduł zarządzania receptami.
Odpowiada za zapisywanie i wczytywanie historii zrealizowanych recept.
Wymagane do celów raportowych i kontroli państwowej.
"""
import datetime

import pandas as pd
import os

from src.services.backend.drug_manager import load_drugs
from src.utils import get_current_datetime, log_action

PRESCRIPTIONS_FILE = 'database/base_of_recipes.xlsx'


def load_prescription_history():
    """
    Wczytuje historię zrealizowanych recept z pliku XLSX.
    Zwraca DataFrame z kolumnami wymaganymi przez NFZ.
    :return:
    """
    try:
        return pd.read_excel(PRESCRIPTIONS_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            'transaction_date',
            'prescription_number',
            'patient_name',
            'refund_amount'
        ])
    except Exception as e:
        print("Błąd podczas wczytywania historii recept: {}".format(e))
        return pd.DataFrame()


@log_action
def save_prescription_record(prescription_number, patient_name, refund_amount):
    """
    Zapisuje nową zrealizowaną receptę do bazy danych (plik XLSX).
    """
    date_str = get_current_datetime()

    df = load_prescription_history()

    new_record = {
        'transaction_date': date_str,
        'prescription_number': prescription_number,
        'patient_name': patient_name,
        'refund_amount': refund_amount
    }

    df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)

    try:
        df.to_excel(PRESCRIPTIONS_FILE, index=False)
        print("Sukces: Recepta nr {} dla pacjenta {} została zrealizowana. (Refundacja NFZ: {} PLN)".format(
            prescription_number, patient_name, refund_amount
        ))
        return True
    except PermissionError:
        print("Błąd: Plik {} jest otwarty w innym programie. Zamknij go!".format(PRESCRIPTIONS_FILE))
        return False
    except Exception as e:
        print("Krytyczny błąd podczas zapisu recepty: {}".format(e))
        return False


def verify_prescription(prescription_id):
    """Sprawdza, czy numer recepty znajduje się w bazie danych."""
    if not os.path.exists(PRESCRIPTIONS_FILE):
        return False, "Baza recept nie istnieje."

    try:
        df = pd.read_excel(PRESCRIPTIONS_FILE)
        prescription_id = str(prescription_id).strip()

        recipe_row = df[df['id'].astype(str) == prescription_id]

        if not recipe_row.empty:
            return True, "Recepta poprawna."
        return False, "Nie znaleziono recepty o tym numerze."
    except Exception as e:
        return False, f"Błąd bazy: {e}"


def is_drug_prescription_required(drug_id):
    """Sprawdza, czy na lek potrzebna jest recepta (szuka wartości „Tak”)."""
    df = load_drugs()
    drug = df[df['id'].astype(str) == str(drug_id)]

    if not drug.empty:
        val = str(drug.iloc[0].get('requires_recipe', 'Nie')).strip().capitalize()
        return val == "Tak"
    return False


def save_recipe_to_archive(recipe_number, customer_name, total_price):
    """
    Po prostu zapisuje dane w pliku XLSX: data, numer, imię i nazwisko, cena.
    """
    new_entry = {
        "Data transakcji": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Numer recepty": [recipe_number],
        "Imię i Nazwisko": [customer_name],
        "Cena (PLN)": [f"{total_price:.2f}"]
    }

    df_new = pd.DataFrame(new_entry)

    try:
        if not os.path.exists(PRESCRIPTIONS_FILE):
            df_new.to_excel(PRESCRIPTIONS_FILE, index=False, engine='openpyxl')
        else:
            with pd.ExcelWriter(PRESCRIPTIONS_FILE, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                existing_df = pd.read_excel(PRESCRIPTIONS_FILE)
                df_new.to_excel(writer, index=False, header=False, startrow=len(existing_df) + 1)
        return True
    except Exception as e:
        print(f"Błąd archiwum: {e}")
        return False