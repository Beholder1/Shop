import tkinter as tk
from tkinter import ttk
from user import User
from product import Product
from widgets import AutocompleteCombobox, SidebarMenu, WidgetList
import pyglet


class MainProgram:
    def __init__(self, db, login):
        self.db = db
        self.login = login
        user = User(self.login, self.db)

        bgColor = '#FFFFFF'
        fontColor = 'black'
        pyglet.font.add_file('Roboto-Light.ttf')

        root = tk.Tk()
        root.configure(background=bgColor)
        root.grid_rowconfigure(0, weight=1)
        root.geometry("1280x720")

        root.title("Store manager")

        style = ttk.Style()
        style.configure('TLabel', background="white", foreground=fontColor, font=('Roboto Light', 12))
        style.configure('TCheckbutton', background="white")

        addIcon = tk.PhotoImage(file='icons/add.png')
        refreshIcon = tk.PhotoImage(file='icons/refresh.png')
        displayIcon = tk.PhotoImage(file='icons/display.png')
        deleteIcon = tk.PhotoImage(file='icons/delete.png')

        # Konto
        frame2 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame2.grid(row=0, column=1, sticky="nwse")
        ttk.Label(frame2, text=user.__str__()).grid(row=0, column=0, sticky="w")

        # Produkty
        frame3 = tk.Frame(root, height=root.winfo_height(), width=root.winfo_width(), bg=bgColor, borderwidth=1,
                          relief=tk.RIDGE)
        frame3.grid(row=0, column=1, sticky="nwse")
        frame3.grid_propagate(False)

        products = ("0.Id", "1.Nazwa", "4.Producent", "3.Cena zakupu", "2.Cena sprzedaży")
        WidgetList(frame3, db, "products", products)

        # Dostawy
        frame4 = tk.Frame(root, height=root.winfo_height(), width=root.winfo_width(), bg=bgColor, borderwidth=1,
                          relief=tk.RIDGE)
        frame4.grid(row=0, column=1, sticky="nwse")
        frame4.grid_propagate(False)

        # Pracownicy
        frame5 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame5.grid(row=0, column=1, sticky="nwse")

        users = ("0.Id", "6.Imię", "7.Nazwisko", "8.Pensja", "11.Ostatnio zalogowany")
        WidgetList(frame5, db, "users", users)

        frame1 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame1.grid(row=0, column=1, sticky="nwse")

        SidebarMenu(root, frame1, frame2, frame3, frame4, frame5, user, db)
        root.grid_columnconfigure(1, weight=1)
        root.mainloop()

    @staticmethod
    def show(frame, row, column, objectToShow):
        ttk.Label(frame, text=objectToShow.__str__()).grid(row=row, column=column, sticky="w")

    @staticmethod
    def createLogin(name, lastName):
        if len(name) > 3:
            login = name[:-(len(name) - 3)]
        else:
            login = name
        if len(lastName) > 3:
            login = login + lastName[:-(len(lastName) - 3)]
        else:
            login = login + lastName
        return login
