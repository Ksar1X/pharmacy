import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from gui.fonts import *
from gui.theme import *

def show_dashboard(root, role):
    card_bg = root.style.colors.dark
    topbar = tk.Frame(root, bg=COLORS["bg_topbar"], height=60)
    topbar.pack(fill="x")

    body = tk.Frame(root, bg=COLORS["bg_main"])
    body.pack(fill="both", expand=True)

    sidebar = tk.Frame(body, bg=COLORS["bg_dark"], width=220)
    sidebar.pack(side="left", fill="y")

    main = tk.Frame(body, bg=COLORS["bg_main"])
    main.pack(side="left", fill="both", expand=True)


    if role == "admin":
        tb.Label(sidebar, text="SYSTEM", font=FONT_SMALL,
                 bootstyle=SUCCESS, background=card_bg).pack(pady=30)
        tb.Button(sidebar, text="⚙️ Настройки", bootstyle=SECONDARY).pack(fill="x", padx=15, pady=5)

    tb.Label(main, text="Dzień dobry, Admin 👋", font=FONT_BODY, background=card_bg).pack(pady=(70,0))

    # Карточки статистики с константами цветов
    def draw_card(parent, title, value, text, color_const):
        card = tb.Frame(parent, bootstyle=DARK, padding=20)
        card.pack(side="left", fill="both", expand=True, padx=5, pady=(100,0))

        # Полоска сверху
        tb.Frame(card, bootstyle=color_const, height=3).pack(fill="x", pady=(0, 24))

        tb.Label(card, text=title, font=FONT_BODY, background=card_bg).pack(anchor="w")
        tb.Label(card, text=value, font=FONT_HEADING, bootstyle=color_const, background=card_bg).pack(anchor="w")
        tb.Label(card, text=text, font=FONT_SMALL, bootstyle=color_const, background=card_bg).pack(anchor="w")

    stats_container = tb.Frame(main)
    stats_container.pack(fill="x", pady=10)

    # Вызываем с константами: SUCCESS, WARNING, DANGER
    draw_card(stats_container, "Dostępne leki", "148", "12 nowych w tym tygodniu",SUCCESS)
    draw_card(stats_container, "Klienci", "312", "8 nowych dziś", INFO)
    draw_card(stats_container, "Zakupy dziś", "47", "śr. wartość: 89 zł", WARNING)
    draw_card(stats_container, "Niski stan", "12", "leków wymaga uzupełnienia", DANGER)


    root.mainloop()