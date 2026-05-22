"""
Moduł zarządzania zasobami apteki (lekami).
Odpowiada za operacje CRUD na pliku Excel (drugs.xlsx).
"""
import pandas as pd
from src.utils import log_action

DRUGS_FILE = 'database/drugs.xlsx'


def load_drugs():
    """Wczytuje bazę leków z pliku Excel. Posiada obsługę wyjątków."""
    try:
        return pd.read_excel(DRUGS_FILE)
    except FileNotFoundError:
        print("Uwaga: Plik {} nie istnieje. Tworzenie pustej struktury.".format(DRUGS_FILE))
        return pd.DataFrame(columns=['id', 'name', 'category', 'price', 'quantity', 'requires_recipe'])
    except Exception as e:
        print("Błąd podczas wczytywania bazy leków: {}".format(e))
        return pd.DataFrame()


def save_drugs(df):
    """Zapisuje zmodyfikowany DataFrame z powrotem do pliku Excel."""
    try:
        df.to_excel(DRUGS_FILE, index=False)
    except PermissionError:
        print("Błąd: Brak dostępu. Zamknij plik {} przed wykonaniem operacji.".format(DRUGS_FILE))


def list_drugs():
    """Zwraca listę wszystkich leków jako listę słowników (records)."""
    df = load_drugs()
    return df.to_dict(orient='records')


def find_drug_by_id(drug_id):
    """Wyszukuje lek po ID. Zwraca słownik z danymi leku lub None."""
    df = load_drugs()
    # Konwertujemy ID do jednego typu dla bezpieczeństwa porównania
    result = df[df['id'].astype(str) == str(drug_id)]
    if not result.empty:
        return result.iloc[0].to_dict()
    print("Błąd: Lek o ID {} nie istnieje.".format(drug_id))
    return None


def find_drug_by_name(name):
    """Wyszukuje lek po nazwie. Zwraca słownik z danymi leku lub None."""
    df = load_drugs()
    result = df[df['name'].astype(str).str.lower() == str(name).lower()]
    if not result.empty:
        return result.iloc[0].to_dict()
    print("Błąd: Lek o nazwie '{}' nie istnieje.".format(name))
    return None


@log_action
def add_drug(name, category, price, quantity, requires_recipe):
    """Dodaje nowy lek do bazy. Zabezpieczone dekoratorem @log_action."""
    df = load_drugs()

    if not df.empty and name in df['name'].values:
        print("Błąd: Lek '{}' już znajduje się w bazie.".format(name))
        return False

    new_id = int(df['id'].max() + 1) if not df.empty else 1

    new_row = pd.DataFrame([{
        'id': new_id,
        'name': name,
        'category': category,
        'price': float(price),
        'quantity': int(quantity),
        'requires_recipe': bool(requires_recipe)
    }])

    df = pd.concat([df, new_row], ignore_index=True)
    save_drugs(df)
    print("Dodano nowy lek: {} (ID: {})".format(name, new_id))
    return True


@log_action
def remove_drug(by_id=None, by_name=None):
    """Usuwanie leku z bazy. Opcje: względem ID lub Nazwy."""
    df = load_drugs()
    initial_len = len(df)

    if by_id is not None:
        df = df[df['id'] != by_id]
    elif by_name is not None:
        df = df[df['name'] != by_name]
    else:
        print("Błąd: Należy podać parametr by_id lub by_name.")
        return False

    if len(df) < initial_len:
        save_drugs(df)
        print("Lek został pomyślnie usunięty z bazy.")
        return True

    print("Nie znaleziono leku w bazie.")
    return False


def update_drug_quantity(drug_id, delta):
    """Aktualizuje stan magazynowy leku po dokonaniu zakupu."""
    df = load_drugs()
    if drug_id not in df['id'].values:
        raise ValueError("Nie znaleziono leku o ID {}.".format(drug_id))

    current_quantity = df.loc[df['id'] == drug_id, 'quantity'].values[0]
    new_quantity = current_quantity + delta

    if new_quantity < 0:
        raise ValueError("Niewystarczająca ilość leku w magazynie!")

    df.loc[df['id'] == drug_id, 'quantity'] = new_quantity
    save_drugs(df)
    return True