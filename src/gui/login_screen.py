import ttkbootstrap as tb
from ttkbootstrap.constants import *

from gui.fonts import *

def show_login(root, on_success):
    login_frame = tb.Frame(root, padding=30)
    login_frame.pack(fill=BOTH, expand=True)

    tb.Label(login_frame, text="PharmaCare", font=FONT_LOGO).pack(pady=20)

    #Поля ввода
    tb.Label(login_frame, text="Login").pack(anchor="w")
    user_ent = tb.Entry(login_frame)
    user_ent.pack(fill="x", pady=5)
    user_ent.insert(0, "") #для теста

    tb.Label(login_frame, text="Password").pack(anchor="w", pady=(10, 0))
    pass_ent = tb.Entry(login_frame, show="*")
    pass_ent.pack(fill="x", pady=5)

    def handle_login():
        if user_ent.get() == "admin" and pass_ent.get() == "1111":
            login_frame.destroy() #закрывает окно
            on_success("admin")
        else:
            from tkinter.messagebox import showerror
            showerror("Error", "User not found!")

    tb.Button(login_frame, text="SingUp", bootstyle=SUCCESS, command=handle_login).pack(fill=X, pady=30)
    login_frame.mainloop()