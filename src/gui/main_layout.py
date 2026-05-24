# gui/main_layout.py
import tkinter as tk
from src.gui.fonts import *
from src.gui.theme import *
from src.gui.router import route
from src.gui.components import (
    build_topbar,
    build_sidebar,
)


def show_dashboard(root, role):

    # ── Основной фрейм ────────────────────────────────
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)
    frame.configure(bg=COLORS["bg_main"])

    # ── ТОПБАР ────────────────────────────────────────
    def on_nav(section):
        route(section, content,role)
    build_topbar(frame, role, on_nav=on_nav)

    # ── BODY ──────────────────────────────────────────
    body = tk.Frame(frame)
    body.pack(side="top", fill="both", expand=True)
    body.configure(bg=COLORS["bg_main"])

    # ── САЙДБАР ───────────────────────────────────────
    # Пункты меню зависят от роли
    if role == "admin":
        items = [
            {"label": "ZASOBY", "type": "section"},
            {"label": "💊 Leki", "type": "btn", "key": "Leki"},
            {"label": "🧾 Recepty", "type": "btn", "key": "Recepty"},
            {"label": "KLIENCI", "type": "section"},
            {"label": "👥 Klienci", "type": "btn", "key": "Klienci"},
            {"label": "📊 Statystyki", "type": "btn", "key": "Statystyki"},
            {"label": "SYSTEM", "type": "section"},
            {"label": "📋 Logi", "type": "btn", "key": "Logi"},
            {"label": "⚙️ Ustawienia", "type": "btn", "key": "Ustawienia"},
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
        route("Dashboard", content, role)
    elif role == "cashier":
        route("Dashboard", content, role)
    elif role == "customer":
        route("Dashboard", content, role)