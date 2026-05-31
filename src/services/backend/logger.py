import pandas as pd
import datetime
import os

LOG_FILE = 'database/logs.csv'


def log_event(action, user="Admin", level="INFO"):
    """
    Zapisuje zdarzenie w pliku dziennika.
    poziom: INFO, WARNING, ERROR
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_log = {
        "Data": now,
        "Użytkownik": user,
        "Poziom": level,
        "Akcja": action
    }

    df_new = pd.DataFrame([new_log])

    if not os.path.exists(LOG_FILE):
        df_new.to_csv(LOG_FILE, index=False, encoding='utf-8-sig')
    else:
        df_new.to_csv(LOG_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')


def load_logs():
    """Pobiera wszystkie logi w celu wyświetlenia ich w tabeli."""
    if not os.path.exists(LOG_FILE):
        return pd.DataFrame(columns=["Data", "Użytkownik", "Poziom", "Akcja"])
    try:
        return pd.read_csv(LOG_FILE, encoding='utf-8-sig')
    except:
        return pd.DataFrame()