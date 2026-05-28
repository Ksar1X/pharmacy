import json
import os

SETTINGS_FILE = "database/settings.json"

TRANSLATIONS = {
    "pl": {
        "dashboard": "Panel sterowania",
        "drugs": "Magazyn leków",
        "customers": "Klienci",
        "settings": "Ustawienia",
        "logout": "Wyloguj się",
        "search": "Szukaj",
        "add_item": "+ Nowy produkt",
        "language_select": "Wybierz język",
        "save": "Zapisz",
        "edit_drug": "Edycja leku",
        "price": "Cena",
        "quantity": "Ilość"
    },
    "ru": {
        "dashboard": "Дашборд",
        "drugs": "Склад лекарств",
        "customers": "Клиенты",
        "settings": "Настройки",
        "logout": "Выйти",
        "search": "Поиск",
        "add_item": "+ Новый товар",
        "language_select": "Выберите язык",
        "save": "Сохранить",
        "edit_drug": "Редактирование лекарства",
        "price": "Цена",
        "quantity": "Количество"
    }
}

def get_current_lang():
    """Читает сохраненный язык или возвращает 'pl' (Польский) по умолчанию."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                # Если в файле пусто или ошибка, вернется 'pl'
                return json.load(f).get("language", "pl")
        except:
            return "pl"
    return "pl" # <--- Здесь мы установили Польский основным

def save_lang(lang_code):
    """Сохраняет выбранный язык в файл."""
    # Создаем папку database, если её нет
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, 'w') as f:
        json.dump({"language": lang_code}, f)

def _(key):
    """Функция получения перевода."""
    lang = get_current_lang()
    # Если ключа нет в польском, попробует найти в русском, иначе вернет сам ключ
    return TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS["pl"].get(key, key))