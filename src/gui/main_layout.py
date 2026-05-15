# gui/main_layout.py
import tkinter as tk
from gui.fonts import *
from gui.theme import *
from gui.router import route
from gui.components import (
    build_topbar,
    build_sidebar,
)


def show_dashboard(root, role):

    # ── Основной фрейм ────────────────────────────────
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)
    frame.configure(bg=COLORS["bg_main"])

    # ── ТОПБАР ────────────────────────────────────────
    build_topbar(frame, role)

    # ── BODY ──────────────────────────────────────────
    body = tk.Frame(frame)
    body.pack(side="top", fill="both", expand=True)
    body.configure(bg=COLORS["bg_main"])

    # ── САЙДБАР ───────────────────────────────────────
    # Пункты меню зависят от роли
    if role == "admin":
        items = [
            {"label": "ZASOBY",        "type": "section"},
            {"label": "Leki",          "type": "btn"},
            {"label": "Stan Magazynu", "type": "btn"},
            {"label": "Recepty",       "type": "btn"},
            {"label": "KLIENCI",       "type": "section"},
            {"label": "Klienci",       "type": "btn"},
            {"label": "Statystyki",    "type": "btn"},
            {"label": "SYSTEM",        "type": "section"},
            {"label": "Logi",          "type": "btn"},
            {"label": "Ustawienia",    "type": "btn"},
        ]
    elif role == "cashier":
        items = [
            {"label": "MENU",          "type": "section"},
            {"label": "Dashboard",     "type": "btn", "active": True},
            {"label": "Zakupy",        "type": "btn"},
            {"label": "Szukaj",        "type": "btn"},
        ]
    elif role == "customer":
        items = [
            {"label": "MENU",          "type": "section"},
            {"label": "Dashboard",     "type": "btn", "active": True},
            {"label": "Katalog",       "type": "btn"},
            {"label": "Koszyk",        "type": "btn"},
            {"label": "Historia",      "type": "btn"},
        ]
    else:
        items = []

    # ── CONTENT — сюда роутер рисует экраны ───────────
    content = tk.Frame(body)
    content.pack(side="right", fill="both", expand=True)
    content.configure(bg=COLORS["bg_main"])

    # ── НАВИГАЦИЯ ─────────────────────────────────────
    def on_nav(section):
        route(section, content, role)

    # Сайдбар после content — чтобы on_nav видел content
    build_sidebar(body, items, on_nav)

    # ── СТАРТОВЫЙ ЭКРАН ───────────────────────────────
    # Показываем dashboard при входе
    if role == "admin":
        route("Leki", content, role)
    elif role == "cashier":
        route("Dashboard", content, role)
    elif role == "customer":
        route("Dashboard", content, role)