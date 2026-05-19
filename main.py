"""
Точка входа в приложение PharmaCare.
Здесь происходит инициализация всех модулей и запуск главного окна (gui.py).
Запускать проект нужно именно через этот файл.
"""
import ttkbootstrap as tb
from src.gui.login_screen import show_login
from src.gui.main_layout import show_dashboard


def main():
    root = tb.Window(themename="cyborg")
    root.title("PharmaCare")
    root.geometry("1400x850")

    def on_success(role):
        # очищаем экран логина
        for widget in root.winfo_children():
            widget.destroy()
        # рисуем dashboard в том же root
        show_dashboard(root, role)

    show_login(root, on_success=on_success)
    root.mainloop()

if __name__ == "__main__":
    main()