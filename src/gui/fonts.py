import pyglet
import ctypes
from pathlib import Path



BASE_DIR = Path(__file__).parent.parent.parent  # доходим до корня PharmaCare/
FONTS_DIR = BASE_DIR / "assets" / "fonts"

pyglet.font.add_file(str(FONTS_DIR / "DMSerifDisplay-Regular.ttf"))
pyglet.font.add_file(str(FONTS_DIR / "DMSans-Regular.ttf"))
pyglet.font.add_file(str(FONTS_DIR / "DMSans-Medium.ttf"))
pyglet.font.add_file(str(FONTS_DIR / "DMSans-SemiBold.ttf"))

FONT_TITLE   = ("DM Serif Display", 28, "normal")
FONT_HEADING = ("DM Sans", 17, "bold")
FONT_BODY    = ("DM Sans", 13, "normal")
FONT_SMALL   = ("DM Sans", 9, "normal")
FONT_LOGO    = ("DM Serif Display", 22, "normal")

def load_fonts():
    if not FONTS_DIR.exists():
        print(f"⚠️ Папка шрифтов не найдена: {FONTS_DIR}")
        return

    FR_PRIVATE = 0x10
    gdi32 = ctypes.WinDLL("gdi32")

    for ttf in FONTS_DIR.glob("*.ttf"):
        result = gdi32.AddFontResourceExW(str(ttf), FR_PRIVATE, 0)
        status = "✅" if result else "❌"
        print(f"{status} Загружен шрифт: {ttf.name}")