# import mysql.connector
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="h5k11s00",
#     database="test"
# )
# mycursor=db.cursor()

import tkinter as tk
from tkinter import ttk
import mainProgram

bgColor = 'white'
menuColor = 'white'
fontColor = 'black'
global login, password
login="1"
password="2"

def combine(root, loginGet, passwordGet):
    if loginGet==login and passwordGet==password:
        root.destroy()
        mainProgram.MainProgram()

root = tk.Tk()
root.configure(background=bgColor)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.title("Tworzenie ogłoszeń")

style = ttk.Style()
style.configure('TLabel', background=bgColor, foreground=fontColor, font=('Verdana', 12))
style.configure('TCheckbutton', background=bgColor)

root.update()
frame = tk.Frame(root,bg=menuColor,width=root.winfo_width(),height=root.winfo_height())
frame.grid(row=0,column=0, sticky='nws')

loginEntry = ttk.Entry(frame)
loginEntry.grid(row=0,column=0,pady=5,sticky="nwes")
passwordEntry = ttk.Entry(frame, show="●")
passwordEntry.grid(row=1,column=0,pady=5,sticky="nwes")
menuButton = tk.Button(frame,text="Zaloguj",background=menuColor, fg=fontColor, command=lambda: combine(root, loginEntry.get(), passwordEntry.get()))
menuButton.grid(row=2,column=0,pady=5,sticky="nwes")


root.mainloop()