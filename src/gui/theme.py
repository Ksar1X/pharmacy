import ttkbootstrap as tb
from src.gui.fonts import *

COLORS = {
    "bg_main":    "#111720",
    "bg_sidebar": "#0B0F14",
    "bg_topbar":  "#0B0F14",
    "bg_card":    "#1e2d40",
    "bg_btn":     "#1e3048",
    "accent":     "#00D4A1",
    "accent2":    "#0099FF",
    "warn":       "#FFB347",
    "danger":     "#FF4D6D",
    "text":       "#e2e8f0",
    "muted":      "#5a7090",
    "border":     "#2d3748",
}


def setup_custom_style():
    style = tb.Style()
    style.configure('my.TButton', font=FONT_SMALL, background=COLORS["accent"], foreground=COLORS["bg_main"], borderwidth=0, relief="flat", focusthickness=0, focuscolor=style.colors.primary)
    style.map('my.TButton', relief=[('pressed', 'flat'), ('active', 'flat')])

    style.configure("high.TLabel", font=FONT_HEADING, foreground=COLORS["text"], background=COLORS["bg_main"])
    style.configure("low.TLabel", font=FONT_SMALL, foreground=COLORS["text"], background=COLORS["bg_main"])

    style.configure("tip.TLable", font=FONT_HEADING, foreground=COLORS["text"])



