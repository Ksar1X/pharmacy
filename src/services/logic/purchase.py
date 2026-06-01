import pandas as pd
import os
from datetime import datetime

HISTORY_DIR = 'database/customer_history'
HISTORY_FILE = 'database/history.txt'
ARCHIVE_FILE = 'database/base_of_recipes.xlsx'


def save_to_history(user_id, items, total_price):
    """Zapisuje zakup w pliku tekstowym klienta."""
    file_path = os.path.join(HISTORY_DIR, f"{user_id}.txt")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    products_list = ", ".join([f"{item['name']} (x{item['qty']})" for item in items])

    entry = f"{now} | {products_list} | {total_price:.2f} zł\n"

    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(entry)


def get_user_history(user_id):
    """Odczytuje plik tekstowy i przekształca go w listę do tabeli."""
    file_path = os.path.join(HISTORY_DIR, f"{user_id}.txt")

    if not os.path.exists(file_path):
        return []

    history_rows = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in reversed(lines):
                if "|" in line:
                    parts = [p.strip() for p in line.split("|")]
                    history_rows.append(parts)
        return history_rows
    except Exception as e:
        print(f"Ошибка чтения истории: {e}")
        return []


def add_to_recipe_archive(recipe_id, patient_id, total_refund):
    """Dodaje wpis dotyczący zrealizowanej recepty do archiwum XLSX NFZ."""

    new_data = {
        "Date of transaction": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Number of recipe": [recipe_id],
        "Surname and name of client": [f"ID: {patient_id}"],
        "Cost": [round(total_refund, 2)]
    }

    df_new = pd.DataFrame(new_data)

    if not os.path.exists(ARCHIVE_FILE):
        df_new.to_excel(ARCHIVE_FILE, index=False, engine='openpyxl')
    else:
        try:
            with pd.ExcelWriter(ARCHIVE_FILE, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                try:
                    existing_df = pd.read_excel(ARCHIVE_FILE)
                    start_row = len(existing_df) + 1
                    df_new.to_excel(writer, index=False, header=False, startrow=start_row)
                except:
                    df_new.to_excel(writer, index=False)
        except Exception as e:
            print(f"Błąd zapisu do Excel: {e}")