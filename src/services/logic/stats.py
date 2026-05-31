"""
Analiza i monitorowanie.
Odpowiada za:
- Obliczanie danych do górnych kart pulpitu nawigacyjnego (suma sprzedaży, liczba klientów).
- Wykrywanie produktów o niskim stanie magazynowym (niedobór).
- Tworzenie raportów dziennych.
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
            (df_logs['Akcja'].str.contains("Sprzedaż", case=False, na=False))
            ]

        return len(today_sales)
    except Exception as e:
        print(f"Błąd statystyk sprzedaży: {e}")
        return 0
