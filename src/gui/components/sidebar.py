import tkinter as tk
from src.gui.theme import *


def build_sidebar(parent, items, on_nav):
    sidebar = tk.Frame(parent, width=200)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    sidebar.configure(
        bg=COLORS["bg_sidebar"],
        highlightbackground=COLORS["border"],
        highlightthickness=1
    )

    sep = tk.Frame(sidebar, height=1)
    sep.pack(fill="x", padx=8, pady=(8, 0))
    sep.configure(bg=COLORS["border"])

    btn_widgets = []

    def set_active(active_key):
        for btn_frame, lbl, key in btn_widgets:
            if key == active_key:
                btn_frame.configure(bg=COLORS["accent"])
                lbl.configure(bg=COLORS["accent"], fg="#000000")
            else:
                btn_frame.configure(bg=COLORS["bg_sidebar"])
                lbl.configure(bg=COLORS["bg_sidebar"], fg=COLORS["text"])

    for item in items:
        if item["type"] == "section":
            lbl = tk.Label(sidebar, text=item["label"], font=FONT_SMALL)
            lbl.pack(anchor="w", padx=12, pady=(14, 4))
            lbl.configure(bg=COLORS["bg_sidebar"], fg=COLORS["muted"])

        elif item["type"] == "btn":
            active  = item.get("active", False)
            bg_btn  = COLORS["accent"]   if active else COLORS["bg_sidebar"]
            fg_btn  = "#000000"          if active else COLORS["text"]
            key     = item.get("key", item["label"])

            btn_frame = tk.Frame(sidebar, cursor="hand2")
            btn_frame.pack(fill="x", padx=8, pady=2)
            btn_frame.configure(bg=bg_btn)

            lbl = tk.Label(btn_frame, text=item["label"], font=FONT_SMALL, anchor="w")
            lbl.pack(fill="x", padx=10, pady=6)
            lbl.configure(bg=bg_btn, fg=fg_btn)

            btn_widgets.append((btn_frame, lbl, key))

            def on_click(e, k=key):
                set_active(k)
                on_nav(k)

            lbl.bind("<Button-1>", on_click)
            btn_frame.bind("<Button-1>", on_click)

    return sidebar