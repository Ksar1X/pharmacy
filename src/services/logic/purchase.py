import pandas as pd
import os
from datetime import datetime

HISTORY_DIR = 'database/customer_history'


def save_to_history(user_id, items, total_price):
    """Сохраняет покупку в текстовый файл клиента."""
    file_path = os.path.join(HISTORY_DIR, f"{user_id}.txt")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    products_list = ", ".join([f"{item['name']} (x{item['qty']})" for item in items])

    entry = f"{now} | {products_list} | {total_price:.2f} zł\n"

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(entry)


def get_user_history(user_id):
    """Читает текстовый файл и превращает его в список для таблицы."""
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