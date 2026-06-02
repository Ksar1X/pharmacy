"""
Analiza i monitorowanie.
Odpowiada za:
- Obliczanie danych do gĂłrnych kart pulpitu nawigacyjnego (suma sprzedaĹĽy, liczba klientĂłw).
- Wykrywanie produktĂłw o niskim stanie magazynowym (niedobĂłr).
- Tworzenie raportĂłw dziennych.
"""
from datetime import datetime
import os

import pandas as pd

from src.services.backend.customer_manager import load_customers
from src.services.backend.drug_manager import load_drugs

LOG_FILE = "database/logs.csv"

def get_total_value():
    df = load_drugs()
    if df.empty:
        return None
    total_value = (df['price'] * df['quantity']).sum()
    return total_value

def get_count_of_drugs():
    df = load_drugs()
    if df.empty:
        return None
    return len(df)

def out_of_stock_drugs():
    df = load_drugs()
    if df.empty:
        return None
    return len(df[df['quantity'] <= 5])

def get_count_of_clients():
    df = load_customers()
    if df.empty:
        return None
    return len(df)

def get_number_of_drugs_with_prescription():
    df = load_drugs()
    if df.empty:
        return None

    if 'requires_recipe' in df.columns:
        prescription_needed = len(df[df['requires_recipe'].astype(str).str.lower() == 'tak'])
    else:
        prescription_needed = 0

    return prescription_needed


def get_purchases_today_count():
    if not os.path.exists(LOG_FILE):
        return 0

    try:
        df_logs = pd.read_csv(LOG_FILE, encoding='utf-8-sig')

        today = datetime.now().strftime("%Y-%m-%d")
        df_logs['Data'] = pd.to_datetime(df_logs['Data'])

        today_sales = df_logs[
            (df_logs['Data'].dt.date == today) &
            (df_logs['Akcja'].str.contains("SprzedaĹĽ", case=False, na=False))
            ]

        return len(today_sales)
    except Exception as e:
        print(f"BĹ‚Ä…d statystyk sprzedaĹĽy: {e}")
        return 0


def _load_logs_for_stats():
    """Wczytuje logi bezpiecznie i normalizuje typy kolumn do analiz."""
    if not os.path.exists(LOG_FILE):
        return pd.DataFrame(columns=["Data", "Akcja"])

    try:
        df_logs = pd.read_csv(LOG_FILE, encoding='utf-8-sig')
    except Exception:
        try:
            df_logs = pd.read_csv(LOG_FILE, encoding='utf-8')
        except Exception as e:
            print("Błąd podczas wczytywania logów: {}".format(e))
            return pd.DataFrame(columns=["Data", "Akcja"])

    if 'Data' not in df_logs.columns or 'Akcja' not in df_logs.columns:
        return pd.DataFrame(columns=["Data", "Akcja"])

    df_logs = df_logs.copy()
    parsed_dates = pd.to_datetime(df_logs['Data'], errors='coerce')
    df_logs = df_logs.assign(Data=parsed_dates)
    df_logs = df_logs[parsed_dates.notna()].copy()
    df_logs = df_logs.assign(Akcja=df_logs['Akcja'].fillna('').astype(str))
    return df_logs


def _is_sale_action(action):
    action_lower = str(action).strip().lower()
    return ('sprzeda' in action_lower) or ('zakup' in action_lower)


def _extract_revenue_from_action(action):
    """Próbuje wyciągnąć kwotę przychodu z tekstu akcji."""
    import re

    text = str(action).lower().replace(',', '.')
    values = []

    patterns = [
        r"(\d+(?:\.\d{1,2})?)\s*(?:zł|zl|pln)",
        r"(?:kwota|suma|wartość|wartosc|za|total)\s*[:=]?\s*(\d+(?:\.\d{1,2})?)"
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            try:
                values.append(float(match.group(1)))
            except (ValueError, TypeError):
                continue

    return max(values) if values else 0.0


def get_average_daily_revenue(days=30):
    """Średnia wyreczka dzienna za ostatnie N dni (domyślnie 30)."""
    try:
        from datetime import date, timedelta

        period_days = int(days)
        if period_days <= 0:
            return 0.0

        df_logs = _load_logs_for_stats()
        if df_logs.empty:
            return 0.0

        start_day = date.today() - timedelta(days=period_days - 1)
        df_period = df_logs[df_logs['Data'].dt.date >= start_day]

        sales = df_period[df_period['Akcja'].apply(_is_sale_action)]
        if sales.empty:
            return 0.0

        total_revenue = sales['Akcja'].apply(_extract_revenue_from_action).sum()
        return round(float(total_revenue) / period_days, 2)
    except Exception as e:
        print("Błąd średniej wyreczki dziennej: {}".format(e))
        return 0.0


def get_new_users_today_count():
    """Liczba nowych użytkowników dodanych dzisiaj."""
    try:
        from datetime import date

        df_logs = _load_logs_for_stats()
        if df_logs.empty:
            return 0

        today = date.today()
        new_users_today = df_logs[
            (df_logs['Data'].dt.date == today) &
            (df_logs['Akcja'].str.contains('Dodano nowy klient|zarejestrowano|rejestracj', case=False, na=False, regex=True))
        ]
        return len(new_users_today)
    except Exception as e:
        print("Błąd statystyki nowych użytkowników: {}".format(e))
        return 0


def get_today_revenue():
    """Suma przychodu ze sprzedaży dla bieżącego dnia."""
    try:
        from datetime import date

        df_logs = _load_logs_for_stats()
        if df_logs.empty:
            return 0.0

        today = date.today()
        today_sales = df_logs[
            (df_logs['Data'].dt.date == today) &
            (df_logs['Akcja'].apply(_is_sale_action))
        ]

        if today_sales.empty:
            return 0.0

        revenue = today_sales['Akcja'].apply(_extract_revenue_from_action).sum()
        return round(float(revenue), 2)
    except Exception as e:
        print("Błąd obliczania dzisiejszej wyreczki: {}".format(e))
        return 0.0


def get_average_purchase_value_today():
    """Średnia wartość pojedynczego zakupu dla bieżącego dnia."""
    try:
        from datetime import date

        df_logs = _load_logs_for_stats()
        if df_logs.empty:
            return 0.0

        today = date.today()
        today_sales = df_logs[
            (df_logs['Data'].dt.date == today) &
            (df_logs['Akcja'].apply(_is_sale_action))
        ]

        purchases = len(today_sales)
        if purchases <= 0:
            return 0.0

        today_revenue = float(today_sales['Akcja'].apply(_extract_revenue_from_action).sum())
        return round(today_revenue / purchases, 2)
    except Exception as e:
        print("Błąd średniej wartości zakupu: {}".format(e))
        return 0.0