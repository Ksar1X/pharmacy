import tkinter as tk
from src.gui.theme import *
from src.gui.router import route
from src.gui.components import (
    build_topbar,
    build_sidebar,
)


def show_dashboard(root, role, user_id):

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)
    frame.configure(bg=COLORS["bg_main"])

    def on_nav(section):
        route(section, content,role)
    build_topbar(frame, role, on_nav=on_nav)

    body = tk.Frame(frame)
    body.pack(side="top", fill="both", expand=True)
    body.configure(bg=COLORS["bg_main"])

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
            {"label": "📊Dashboard",     "type": "btn", "active": True},
            {"label": "🧾Historia", "type": "btn", "key": "Recepty"},
        ]
    else:
        items = []

    content = tk.Frame(body)
    content.pack(side="right", fill="both", expand=True)
    content.configure(bg=COLORS["bg_main"])

    def on_nav(section):
        route(section, content, role)

    build_sidebar(body, items, on_nav)

    if role == "admin":
        route("Dashboard", content, role)
    elif role == "cashier":
        route("Dashboard", content, role)
    elif role == "customer":
        route("Dashboard", content, role)