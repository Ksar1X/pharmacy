"""
Moduł narzędziowy (utils).
Zawiera funkcje do generowania ID, haszowania haseł, pobierania aktualnego czasu
oraz dekorator do logowania akcji (wymaganie projektowe).
"""
import hashlib
import random
from datetime import datetime
from functools import wraps

def generate_id() -> str:
    """Generuje losowy, unikalny 4-cyfrowy numer ID dla klienta."""
    return str(random.randint(1000, 9999))

def hash_password(password: str) -> str:
    """Szyfruje hasło algorytmem SHA-256 w celu bezpiecznego przechowywania w bazie."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def check_password(password: str, hashed: str) -> bool:
    """Weryfikuje, czy podane hasło w postaci jawnej odpowiada zapisanemu haszowi."""
    return hash_password(password) == hashed

def get_current_datetime() -> str:
    """Zwraca aktualną datę i czas w formacie YYYY-MM-DD HH:MM:SS."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_action(func):
    """
    Dekorator (wymaganie projektowe).
    Loguje do konsoli wywołania funkcji oraz ewentualne wyjątki.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("[{}] Wywołanie funkcji '{}'".format(get_current_datetime(), func.__name__))
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("[{}] Błąd w funkcji '{}': {}".format(get_current_datetime(), func.__name__, e))
            raise
    return wrapper
