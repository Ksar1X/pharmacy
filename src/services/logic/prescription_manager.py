"""
Moduł zarządzania receptami (NFZ).
Odpowiada za zapisywanie i wczytywanie historii zrealizowanych recept.
Wymagane do celów raportowych i kontroli państwowej.
"""
import pandas as pd
import os
from src.utils import get_current_datetime, log_action

PRESCRIPTIONS_FILE = 'database/base_of_recipes.xlsx'


def load_prescription_history():
    """
    Wczytuje historię zrealizowanych recept z pliku XLSX.
    Zwraca DataFrame z kolumnami wymaganymi przez NFZ.
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