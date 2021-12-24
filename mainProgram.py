import tkinter as tk
from tkinter import ttk
from user import User
from product import Product
from widgets import AutocompleteCombobox
from widgets import SidebarMenu


class MainProgram:
    def __init__(self, db, login):
        self.db = db
        self.login = login
        user = User(self.login)

        bgColor = '#FCFCFF'
        activeColor = "#FDA50F"
        menuColor = '#FD6A02'
        fontColor = 'black'

        root = tk.Tk()
        root.configure(background=bgColor)
        root.grid_rowconfigure(0, weight=1)

        root.title("Kamil Włodarczyk to kozak")

        style = ttk.Style()
        style.configure('TLabel', background="white", foreground=fontColor, font=('Verdana', 12))
        style.configure('TCheckbutton', background="white")

        # Konto
        frame2 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame2.grid(row=0, column=1, sticky="nwse")
        ttk.Label(frame2, text=user.__str__()).grid(row=0, column=0, sticky="w")

        # Produkty
        frame3 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame3.grid(row=0, column=1, sticky="nwse")
        frame3a = tk.Frame(frame3, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame3a.grid(row=0, column=0, sticky="nwse")
        ttk.Label(frame3a, text="Produkt: ").grid(row=0, column=0, sticky="w")
        comboProductName = AutocompleteCombobox(frame3a)
        comboProductName.set_completion_list(self.db.fetchColumnAll("products", "name"))
        comboProductName.grid(row=0, column=1, sticky="w")
        comboProductName.focus_set()
        ttk.Label(frame3a, text="Producent: ").grid(row=1, column=0, sticky="w")
        comboProductBrand = AutocompleteCombobox(frame3a)
        comboProductBrand.set_completion_list(self.db.fetchColumnAll("products", "mark"))
        comboProductBrand.grid(row=1, column=1, sticky="w")
        comboProductBrand.focus_set()
        showProductButton = tk.Button(frame3a, text="Pokaż",
                                      command=lambda: self.show(frame3a, 2, 0, Product(comboProductName.get(),
                                                                                       comboProductBrand.get())))
        showProductButton.grid(row=0, column=2)

        frame3b = tk.Frame(frame3, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame3b.grid(row=0, column=1, sticky="nwse")

        ttk.Label(frame3b, text="Nazwa: ").grid(row=0, column=0, sticky="w")
        entryProductName = ttk.Entry(frame3b)
        entryProductName.grid(row=0, column=1, sticky="w")

        ttk.Label(frame3b, text="Producent: ").grid(row=1, column=0, sticky="w")
        entryProductBrand = ttk.Entry(frame3b)
        entryProductBrand.grid(row=1, column=1, sticky="w")

        ttk.Label(frame3b, text="Cena: ").grid(row=2, column=0, sticky="w")
        entryProductPrice = ttk.Entry(frame3b)
        entryProductPrice.grid(row=2, column=1, sticky="w")

        ttk.Label(frame3b, text="Kategoria ").grid(row=3, column=0, sticky="w")
        entryProductCategory = ttk.Entry(frame3b)
        entryProductCategory.grid(row=3, column=1, sticky="w")

        ttk.Label(frame3b, text="Jednostka: ").grid(row=4, column=0, sticky="w")
        comboProductUnit = AutocompleteCombobox(frame3b)
        comboProductUnit.set_completion_list(db.getEnum("amount_type"))
        comboProductUnit.grid(row=4, column=1, sticky="w")
        comboProductUnit.focus_set()

        addProductButton = tk.Button(frame3b, text="Dodaj",
                                     command=lambda: self.db.insertProduct(entryProductPrice.get(),
                                                                           entryProductBrand.get(),
                                                                           entryProductCategory.get(),
                                                                           comboProductUnit.get(),
                                                                           entryProductName.get()))
        addProductButton.grid(row=5, column=1)

        # Dostawy
        frame4 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame4.grid(row=0, column=1, sticky="nwse")
        ttk.Label(frame4, text="Informacje o dostawach", foreground=fontColor).grid(row=0, column=0, sticky="w")

        # Pracownicy
        frame5 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame5.grid(row=0, column=1, sticky="nwse")
        frame5a = tk.Frame(frame5, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame5a.grid(row=0, column=0, sticky="nwse")
        user.showUser(frame5a, self.show)

        frame5b = tk.Frame(frame5, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame5b.grid(row=0, column=1, sticky="nwse")
        user.addUser(frame5b)

        frame1 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame1.grid(row=0, column=1, sticky="nwse")

        SidebarMenu(root, frame1, frame2, frame3, frame4, frame5, user)
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
