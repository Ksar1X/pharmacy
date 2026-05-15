import tkinter as tk
from gui.fonts import *
from gui.theme import *


def build_sidebar(parent, items, on_nav):
    sidebar = tk.Frame(parent, width=200)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    sidebar.configure(
        bg=COLORS["bg_sidebar"],
        highlightbackground=COLORS["border"],
        highlightthickness=1
    )

    # Разделитель
    sep = tk.Frame(sidebar, height=1)
    sep.pack(fill="x", padx=8, pady=(8, 0))
    sep.configure(bg=COLORS["border"])

    for item in items:
        if item["type"] == "section":
            lbl = tk.Label(sidebar, text=item["label"], font=FONT_SMALL)
            lbl.pack(anchor="w", padx=12, pady=(14, 4))
            lbl.configure(bg=COLORS["bg_sidebar"], fg=COLORS["muted"])

        elif item["type"] == "btn":
            active = item.get("active", False)
            bg_btn = COLORS["accent"] if active else COLORS["bg_sidebar"]
            fg_btn = "#000000"        if active else COLORS["text"]

            btn_frame = tk.Frame(sidebar, cursor="hand2")
            btn_frame.pack(fill="x", padx=8, pady=2)
            btn_frame.configure(bg=bg_btn)

            lbl = tk.Label(btn_frame, text=item["label"], font=FONT_SMALL, anchor="w")
            lbl.pack(fill="x", padx=10, pady=6)
            lbl.configure(bg=bg_btn, fg=fg_btn)

            lbl.bind("<Button-1>", lambda e, name=item["label"]: on_nav(name))
            btn_frame.bind("<Button-1>", lambda e, name=item["label"]: on_nav(name))

    return sidebar