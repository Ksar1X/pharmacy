
# PharmacyCare 💊

System zarządzania apteką zbudowany w języku Python z wykorzystaniem interfejsu graficznego Tkinter. 
Aplikacja umożliwia zarządzanie magazynem leków, bazą klientów oraz przeglądanie statystyk operacyjnych.

## ✨ Główne Funkcje

- **Autoryzacja:** Kontrola dostępu oparta na rolach dla Administratora, Farmaceuty i Klienta.
- **Zarządzanie Magazynem:** Przeglądanie, wyszukiwanie, dodawanie i edycja leków (integracja z Excel/CSV).
- **Baza Klientów:** Zarządzanie profilami klientów, w tym historią zakupów i danymi adresowymi.
- **Dashboard:** Wizualizacja kluczowych wskaźników (liczba produktów, alerty o niskim stanie magazynowym).

## 📂 Struktura Projektu

* `main.py` — Punkt wejścia do aplikacji.
* `src/gui/` — Interfejs graficzny (ekrany, komponenty, style).
* `src/services/` — Logika biznesowa i zarządzanie danymi.
* `database/` — Przechowywanie danych w formatach `.xlsx` i `.csv`.
* `assets/` — Czcionki i ikony.

## 🛠 Stos Technologiczny

- **Język:** Python 3.10+
- **GUI:** Tkinter + [ttkbootstrap](https://ttkbootstrap.readthedocs.io/)
- **Przetwarzanie danych:** Pandas, Openpyxl
- **Stylizacja:** Niestandardowe czcionki (DM Sans) i motywy kolorystyczne.

## 📝 Programiści
- **Maksim Pyshynski / Ksar1X** - Lead Developer: Projektowanie GUI, logika biznesowa, architektura aplikacji oraz logika backendowa.
- **Ervin Senkevich / Ervin581** - Data Engineer: Struktura bazy danych (Excel/CSV), zarządzanie danymi oraz logika backendowa.

## 🚀 Jak zacząć

### Wymagania wstępne
Upewnij się, że masz zainstalowany Python 3.10 lub nowszy.

### Instalacja
Sklonuj repozytorium i zainstaluj wymagane biblioteki:
```bash
git clone [https://github.com/ksar1x/pharmacy.git](https://github.com/ksar1x/pharmacy.git)
cd pharmacy
pip install -r requirements.txt