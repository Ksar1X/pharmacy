import pandas as pd
from src.services.backend.drug_manager import load_drugs, save_drugs
from src.services.backend.logger import log_event
from src.services.logic.purchase import save_to_history

_cart_items = []


def add_to_cart(drug_id, name, price_raw, amount=1):
    """Rezerwuje podaną ilość towaru."""
    global _cart_items
    df = load_drugs()
    mask = df['id'].astype(str) == str(drug_id)

    if not mask.any(): return False

    current_stock = df.loc[mask, 'quantity'].values[0]
    if current_stock < amount:
        return False

    df.loc[mask, 'quantity'] -= amount
    save_drugs(df)

    for item in _cart_items:
        if str(item['id']) == str(drug_id):
            item['qty'] += amount
            return True

    try:
        price = float(str(price_raw).replace(' zł', '').replace(',', '.'))
    except:
        price = 0.0

    _cart_items.append({'id': drug_id, 'name': name, 'price': price, 'qty': amount})
    return True


def remove_from_cart(drug_id, amount=1):
    """Zwraca określoną ilość towaru do magazynu."""
    global _cart_items

    for item in _cart_items:
        if str(item['id']) == str(drug_id):
            actual_to_remove = min(amount, item['qty'])

            df = load_drugs()
            mask = df['id'].astype(str) == str(drug_id)
            if mask.any():
                df.loc[mask, 'quantity'] += actual_to_remove
                save_drugs(df)

            if item['qty'] > actual_to_remove:
                item['qty'] -= actual_to_remove
            else:
                _cart_items.remove(item)
            return True
    return False

def get_cart_content():
    """Wyświetla aktualną zawartość koszyka."""
    return _cart_items

def get_cart_total():
    """Oblicza łączną kwotę wszystkich produktów w koszyku."""
    return sum(item['price'] * item['qty'] for item in _cart_items)

def clear_cart():
    """Całkowicie usuwa zawartość koszyka (na przykład po dokonaniu płatności lub anulowaniu zamówienia)."""
    global _cart_items
    _cart_items = []


def checkout(current_user_id):
    """
    Teraz operacja checkout służy jedynie do zarejestrowania sprzedaży w historii i logach,
    ponieważ ilość została już zmieniona podczas dodawania produktu do koszyka.
    """
    global _cart_items
    if not _cart_items: return False, "Koszyk pusty"

    from src.services.logic.purchase import save_to_history
    from src.services.backend.logger import log_event

    total_sum = get_cart_total()
    save_to_history(current_user_id, _cart_items, total_sum)
    log_event(f"Finalizacja zakupu. Suma: {total_sum}", user=current_user_id)

    clear_cart()
    return True, "Zakup zakończony!"


def cancel_cart():
    """Przenosi wszystkie zarezerwowane produkty z koszyka z powrotem do bazy danych."""
    global _cart_items
    if not _cart_items:
        return

    try:
        df = load_drugs()
        for item in _cart_items:
            mask = df['id'].astype(str) == str(item['id'])
            if mask.any():
                df.loc[mask, 'quantity'] += item['qty']

        save_drugs(df)
        _cart_items = []
        print("Корзина аннулирована, товары возвращены на склад.")
    except Exception as e:
        print(f"Ошибка при отмене корзины: {e}")