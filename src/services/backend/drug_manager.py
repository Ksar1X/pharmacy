"""
Moduł zarządzania zasobami apteki (lekami).
Odpowiada za operacje CRUD na pliku Excel (drugs.xlsx).
"""
import pandas as pd
from src.utils import log_action
from src.services.backend.logger import log_event

DRUGS_FILE = 'database/drugs.xlsx'


def load_drugs():
    """Wczytuje bazę leków z pliku Excel. Posiada obsługę wyjątków."""
    try:
        return pd.read_excel(DRUGS_FILE, engine='openpyxl')
    except FileNotFoundError:
        print("Uwaga: Plik {} nie istnieje. Tworzenie pustej struktury.".format(DRUGS_FILE))
        return pd.DataFrame(columns=['id', 'name', 'category', 'price', 'quantity', 'requires_recipe'])
    except Exception as e:
        print("Błąd podczas wczytywania bazy leków: {}".format(e))
        return pd.DataFrame()


def save_drugs(df):
    """Zapisuje zmodyfikowany DataFrame z powrotem do pliku Excel."""
    try:
        df.to_excel(DRUGS_FILE, index=False, engine='openpyxl')
    except PermissionError:
        print("Błąd: Brak dostępu. Zamknij plik {} przed wykonaniem operacji.".format(DRUGS_FILE))


def list_drugs():
    """Zwraca listę wszystkich leków jako listę słowników (records)."""
    df = load_drugs()
    if df.empty:
        return None
    return df.to_dict(orient='records')


def find_drug_by_id(drug_id):
    """Wyszukuje lek po ID. Zwraca słownik z danymi leku lub None."""
    df = load_drugs()
    if df.empty:
        return None
    # Konwertujemy ID do jednego typu dla bezpieczeństwa porównania
    result = df[df['id'].astype(str) == str(drug_id)]
    if not result.empty:
        return result.iloc[0].to_dict()
    print("Błąd: Lek o ID {} nie istnieje.".format(drug_id))
    return None


def find_drug_by_name(name):
    """Wyszukuje lek po nazwie. Zwraca słownik z danymi leku lub None."""
    df = load_drugs()
    if df.empty:
        return None

    target_name = str(name).strip().lower()
    result = df[df['name'].astype(str).str.lower() == target_name]
    if not result.empty:
        return result.iloc[0].to_dict()
    print("Błąd: Lek o nazwie '{}' nie istnieje.".format(name))
    return None


@log_action
def add_new_drug(name, category, price, quantity, requires_recipe):
    """
    Dodaje nowy lek lub aktualizuje ilość istniejącego.
    """

    existing_drug = find_drug_by_name(name)
    if existing_drug:
        msg = "Lek o takiej nazwie już istnieje!"
        return False, msg

    df = load_drugs()
    name_lower = name.strip().lower()
    existing_index = df[df['name'].str.lower() == name_lower].index

    if not existing_index.empty:
        idx = existing_index[0]
        df.at[idx, 'quantity'] = int(df.at[idx, 'quantity']) + int(quantity)
        df.at[idx, 'price'] = float(price)
        df.at[idx, 'category'] = category
        df.at[idx, 'requires_recipe'] = requires_recipe
        message = "Liczba zaktualizowana"
    else:
        new_id = int(df['id'].max() + 1) if not df.empty else 1
        new_row = {
            'id': new_id,
            'name': name.strip(),
            'category': category.strip(),
            'price': float(price),
            'quantity': int(quantity),
            'requires_recipe': requires_recipe
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        message = "Dodano nowy lek"

    df.to_excel(DRUGS_FILE, index=False)
    log_event(f"Dodano nowy lek: {name}", level="INFO")
    return True, message


@log_action
def remove_drug(by_id=None, by_name=None):
    """Usuwanie leku z bazy. Opcje: względem ID lub Nazwy."""

    if not find_drug_by_id(by_id) or find_drug_by_name(by_name):
        print("Nie znaleziono leku w bazie.")
        return False

    df = load_drugs()
    if df.empty:
        return None
    initial_len = len(df)

    if by_id is not None:
        target_id = str(by_id).strip()
        df = df[df['id'].astype(str) != str(by_id)]
        df = df[df['id'] != target_id]
    elif by_name is not None:
        target_name = str(by_name).strip().lower()
        df = df[df['name'].str.strip().str.lower() != str(by_name).strip().lower()]
        df = df[df['name'] != target_name]
    else:
        print("Błąd: Należy podać parametr by_id lub by_name.")
        return False

    if len(df) < initial_len:
        save_drugs(df)
        print("Lek został pomyślnie usunięty z bazy.")
        log_event(f"Usunięto lek: ID {by_id}", level="WARNING")
        return True

    print("Nie znaleziono leku w bazie.")
    return False


def update_drug_quantity(drug_id, delta):
    """Aktualizuje stan magazynowy leku po dokonaniu zakupu."""
    df = load_drugs()
    if df.empty:
        return None
    if drug_id not in df['id'].values:
        raise ValueError("Nie znaleziono leku o ID {}.".format(drug_id))

    current_quantity = df.loc[df['id'] == drug_id, 'quantity'].values[0]
    new_quantity = current_quantity + delta

    if new_quantity < 0:
        raise ValueError("Niewystarczająca ilość leku w magazynie!")

    df.loc[df['id'] == drug_id, 'quantity'] = new_quantity
    save_drugs(df)
    return True
