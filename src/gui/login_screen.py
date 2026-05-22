# gui/login_screen.py
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from customer_manager import *

from gui.fonts import *
from gui.theme import *


def show_login(root, on_success):

    # ── Основной фрейм ────────────────────────────────
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)
    frame.configure(bg=COLORS["bg_main"])

    # ── Центральный контейнер ─────────────────────────
    center = tk.Frame(frame)
    center.place(relx=0.5, rely=0.5, anchor="center")
    center.configure(bg=COLORS["bg_main"])

    # ── ЛОГОТИП ───────────────────────────────────────
    logo_frame = tk.Frame(center)
    logo_frame.pack(pady=(0, 48))
    logo_frame.configure(bg=COLORS["bg_main"])

    logo_inner = tk.Frame(logo_frame)  # ← убрали bg=COLORS["accent"]
    logo_inner.pack()
    logo_inner.configure(bg=COLORS["bg_main"])

    pharma = tk.Label(logo_inner, text="Pharma", font=FONT_LOGO)
    pharma.pack(side="left")
    pharma.configure(bg=COLORS["bg_main"], fg=COLORS["accent"])

    care = tk.Label(logo_inner, text="Care", font=FONT_LOGO)
    care.pack(side="left")
    care.configure(bg=COLORS["bg_main"], fg=COLORS["text"])

    # ── ФОРМА ─────────────────────────────────────────
    form = tk.Frame(center)
    form.pack()
    form.configure(bg=COLORS["bg_main"])

    # LOGIN
    login_lbl = tk.Label(form, text="LOGIN", font=FONT_SMALL)
    login_lbl.pack(anchor="w", pady=(0, 6))
    login_lbl.configure(bg=COLORS["bg_main"], fg=COLORS["text"])

    login_var = tk.StringVar()
    login_entry = tk.Entry(
        form,
        textvariable=login_var,
        font=FONT_BODY,
        width=34,
        relief="flat",
        bd=0,
        bg="#d9d9d9",
        fg="#000000",
        insertbackground="#000000"
    )
    login_entry.pack(pady=(0, 20), ipady=10)

    # PASSWORD
    pass_lbl = tk.Label(form, text="PASSWORD", font=FONT_SMALL)
    pass_lbl.pack(anchor="w", pady=(0, 6))
    pass_lbl.configure(bg=COLORS["bg_main"], fg=COLORS["text"])

    password_var = tk.StringVar()
    password_entry = tk.Entry(
        form,
        textvariable=password_var,
        font=FONT_BODY,
        width=34,
        relief="flat",
        bd=0,
        bg="#d9d9d9",
        fg="#000000",
        insertbackground="#000000",
        show="•"
    )
    password_entry.pack(pady=(0, 32), ipady=10)

    # ── КНОПКА ────────────────────────────────────────
    def handle_login():
        login    = login_var.get().strip()
        password = password_var.get().strip()

        if not login or not password:
            error_lbl.configure(text="Введите логин и пароль")
            return

        # потом заменишь на: role = login_customer(login, password)
        role = login_customer(login, password)  # заглушка

        if role:
            frame.destroy()
            on_success(role)
        else:
            error_lbl.configure(text="Неверный логин или пароль")

    login_btn = tk.Button(
        form,
        text="Zaloguj się",
        font=FONT_BODY,
        width=20,
        relief="flat",
        bd=0,
        cursor="hand2",
        command=handle_login
    )
    login_btn.pack(ipady=10)
    login_btn.configure(bg=COLORS["accent"], fg="#000000")

    # ── ОШИБКА ────────────────────────────────────────
    error_lbl = tk.Label(form, text="", font=FONT_SMALL)
    error_lbl.pack(pady=(12, 0))
    error_lbl.configure(bg=COLORS["bg_main"], fg=COLORS["danger"])

    # Enter → логин
    root.bind("<Return>", lambda e: handle_login())
    login_entry.focus()