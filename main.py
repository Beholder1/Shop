import tkinter as tk
from tkinter import ttk
import mainProgram
from db import Database

db = Database()
bgColor = 'white'
menuColor = 'white'
fontColor = 'black'


def combine(rootToDestroy, loginGet, passwordGet):
    if db.fetch("users", "login", loginGet)[3] == passwordGet:
        rootToDestroy.destroy()
        mainProgram.MainProgram(db, loginGet)


root = tk.Tk()
root.geometry("1280x720")
root.configure(background=bgColor)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.title("Zaloguj się")

style = ttk.Style()
style.configure('TLabel', background=bgColor, foreground=fontColor, font=('Verdana', 12))
style.configure('TCheckbutton', background=bgColor)
root.update()

frame = tk.Frame(root, bg=menuColor)
frame.place(relheight=1, relwidth=0.67)

loginEntry = ttk.Entry(frame)
loginEntry.grid(row=0, column=0, pady=5, sticky="nwes")
passwordEntry = ttk.Entry(frame, show="●")
passwordEntry.grid(row=1, column=0, pady=5, sticky="nwes")
menuButton = tk.Button(frame, text="Zaloguj", background=menuColor, fg=fontColor,
                       command=lambda: combine(root, loginEntry.get(), passwordEntry.get()))
menuButton.grid(row=2, column=0, pady=5, sticky="nwes")

# frame1 = tk.Frame(root, bg=fontColor)
# frame1.place(relheight=1, relwidth=0.33)

root.mainloop()
