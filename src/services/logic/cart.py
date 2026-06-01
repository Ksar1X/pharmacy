import pandas as pd
from src.services.backend.drug_manager import load_drugs, save_drugs
from src.services.backend.logger import log_event
from src.services.logic.purchase import save_to_history

_cart_items = []


def add_to_cart(drug_id, name, price_raw, amount=1):
    """Бронирует указанное количество товара."""
    global _cart_items
    df = load_drugs()
    mask = df['id'].astype(str) == str(drug_id)

    if not mask.any(): return False

    current_stock = df.loc[mask, 'quantity'].values[0]
    if current_stock < amount:
        return False  # Недостаточно товара

    # Списываем сразу amount
    df.loc[mask, 'quantity'] -= amount
    save_drugs(df)

    # Добавляем в список корзины
    for item in _cart_items:
        if str(item['id']) == str(drug_id):
            item['qty'] += amount
            return True

    # Если товара еще нет в корзине
    try:
        price = float(str(price_raw).replace(' zł', '').replace(',', '.'))
    except:
        price = 0.0

    _cart_items.append({'id': drug_id, 'name': name, 'price': price, 'qty': amount})
    return True


def remove_from_cart(drug_id, amount=1):
    """Возвращает указанное количество товара на склад."""
    global _cart_items

    for item in _cart_items:
        if str(item['id']) == str(drug_id):
            # Определяем, сколько реально можем удалить (не больше, чем есть в корзине)
            actual_to_remove = min(amount, item['qty'])

            # Возвращаем в базу
            df = load_drugs()
            mask = df['id'].astype(str) == str(drug_id)
            if mask.any():
                df.loc[mask, 'quantity'] += actual_to_remove
                save_drugs(df)

            # Убираем из корзины
            if item['qty'] > actual_to_remove:
                item['qty'] -= actual_to_remove
            else:
                _cart_items.remove(item)
            return True
    return False

def get_cart_content():
    """Возвращает текущие товары в корзине."""
    return _cart_items

def get_cart_total():
    """Считает итоговую сумму всех товаров в корзине."""
    return sum(item['price'] * item['qty'] for item in _cart_items)

def clear_cart():
    """Полностью очищает корзину (например, после оплаты или отмены)."""
    global _cart_items
    _cart_items = []


def checkout(current_user_id):
    """
    Теперь checkout только фиксирует продажу в историю и логи,
    так как количество уже изменено при добавлении в корзину.
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