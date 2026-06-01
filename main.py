import ttkbootstrap as tb
from src.gui.screens.login_screen import show_login
from src.gui.screens.main_layout import show_dashboard
from src.gui.theme import setup_custom_style


def main():
    root = tb.Window(themename="cyborg")
    root.title("PharmaCare")
    root.geometry("1400x850")
    setup_custom_style()

    def on_success(role, user_id):
        for widget in root.winfo_children():
            widget.destroy()
        show_dashboard(root, role, user_id)

    show_login(root, on_success=on_success)
    root.mainloop()

if __name__ == "__main__":
    main()