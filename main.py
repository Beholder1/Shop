import tkinter as tk
from tkinter import ttk
import mainProgram
from db import Database
import pyglet


class Login:
    def __init__(self):
        db = Database()
        bgColor = "#39A5DC"
        menuColor = 'white'
        fontColor = 'black'
        widgetWidth = 40
        pyglet.font.add_file('Roboto-Light.ttf')
        self.bigC = 0

        def combine(rootToDestroy, loginGet, passwordGet):
            if loginGet == '' or (loginGet == '' and passwordGet == ''):
                errorLabel.configure(text="Nie podano nazwy użytkownika")
            elif passwordGet == '':
                errorLabel.configure(text="Nie podano hasła")
            else:
                user = db.fetch("users", "*", "login", loginGet)
                if user:
                    if user[2] == passwordGet:
                        rootToDestroy.destroy()
                        mainProgram.MainProgram(db, user[0])
                    else:
                        errorLabel.configure(text="Niepoprawne hasło")
                        self.bigC += 1
                        if self.bigC == 3:
                            db.set("users", "is_blocked", True, "login", loginGet)
                            self.bigC = 0
                else:
                    errorLabel.configure(text="Nie ma takiego użytkownika")

        root = tk.Tk()
        root.geometry("1280x720")
        root.configure(background=bgColor)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.title("Zaloguj się")

        style = ttk.Style()
        style.configure('TLabel', background=bgColor, foreground=fontColor, font=('Roboto Light', 12))
        root.update()

        frame = tk.Frame(root, bg=menuColor, width=400, height=200)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        frame.grid_propagate(False)

        frameInterior = tk.Frame(frame, bg=menuColor)
        frameInterior.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ttk.Label(frameInterior, text="Nazwa użytkownika", background=menuColor).grid(row=0, column=0, sticky="nwes")
        loginEntry = ttk.Entry(frameInterior)
        loginEntry.grid(row=1, column=0, pady=5, sticky="nwes")
        ttk.Label(frameInterior, text="Hasło", background=menuColor).grid(row=2, column=0, pady=(10, 0), sticky="nwes")
        passwordEntry = ttk.Entry(frameInterior, show="●")
        passwordEntry.grid(row=3, column=0, pady=5, sticky="nwes")
        errorLabel = ttk.Label(frameInterior, text="", font=('Roboto Light', 8), foreground="red", background=menuColor)
        errorLabel.grid(row=4, column=0, sticky="nwes")
        menuButton = tk.Button(frameInterior, text="Zaloguj", font=("Roboto Light", 12), width=widgetWidth,
                               background="#0589CF", fg="white",
                               command=lambda: combine(root, loginEntry.get(), passwordEntry.get()))
        menuButton.grid(row=5, column=0, pady=(10, 5), sticky="nwes")

        root.mainloop()


if __name__ == "__main__":
    # db = Database()
    # print(db.fetchAll("orders", "*", add="WHERE order_id = 1001")[0][3])
    Login()
