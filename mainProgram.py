import tkinter as tk
from tkinter import ttk
from user import User
from product import Product
from widgets import AutocompleteCombobox



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
        root.grid_columnconfigure(0, weight=1)
        root.title("Kamil Włodarczyk to kozak")

        style = ttk.Style()
        style.configure('TLabel', background="white", foreground=fontColor, font=('Verdana', 12))
        style.configure('TCheckbutton', background="white")
        min_w = 50
        max_w = 150
        self.cur_width = min_w
        self.expanded = False

        def raise_frame(frameToRaise):
            frameToRaise.tkraise()

        def expand():
            rep = root.after(2, expand)
            if not self.expanded:
                self.cur_width += 10
                frame.config(width=self.cur_width)
            if self.cur_width >= max_w:
                self.expanded = True
                root.after_cancel(rep)
                fill()

        def contract():
            self.cur_width -= 10
            rep = root.after(2, contract)
            frame.config(width=self.cur_width)
            if self.cur_width <= min_w:
                self.expanded = False
                root.after_cancel(rep)
                fill()

        def fill():
            if self.expanded:
                menuButton.config(image=closeIcon, command=contract)
                homeButton.config(image="", text="Strona główna", borderwidth=0)
                homeButton.grid_configure(pady=0)
                accountButton.config(image="", text="Konto", borderwidth=0)
                accountButton.grid_configure(pady=0)
                productButton.config(image="", text="Produkty", borderwidth=0)
                productButton.grid_configure(pady=0)
                locationButton.config(image="", text="Dostawy", borderwidth=0)
                locationButton.grid_configure(pady=0)
                if user.role != "pracownik":
                    employeesButton.config(image="", text="Pracownicy", borderwidth=0)
                    employeesButton.grid_configure(pady=0)
            else:
                menuButton.config(image=menuIcon, command=expand)
                homeButton.config(image=homeIcon, borderwidth=0)
                homeButton.grid_configure(pady=5)
                accountButton.config(image=accountIcon, borderwidth=0)
                accountButton.grid_configure(pady=5)
                productButton.config(image=productIcon, borderwidth=0)
                productButton.grid_configure(pady=5)
                locationButton.config(image=locationIcon, borderwidth=0)
                locationButton.grid_configure(pady=5)
                if user.role != "pracownik":
                    employeesButton.config(image=employeesIcon, borderwidth=0)
                    employeesButton.grid_configure(pady=5)

        menuIcon = tk.PhotoImage(file='icons/menu.png')
        closeIcon = tk.PhotoImage(file='icons/close.png')
        homeIcon = tk.PhotoImage(file='icons/home.png')
        accountIcon = tk.PhotoImage(file='icons/account.png')
        productIcon = tk.PhotoImage(file='icons/product.png')
        locationIcon = tk.PhotoImage(file='icons/delivery.png')
        employeesIcon = tk.PhotoImage(file='icons/employees.png')

        frame = tk.Frame(root, bg=menuColor, width=50, height=root.winfo_height())
        frame.grid(row=0, column=0, sticky='nws')

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
                                      command=lambda: self.db.insertProduct(entryProductPrice.get(),entryProductBrand.get(),entryProductCategory.get(),comboProductUnit.get(),entryProductName.get()))
        addProductButton.grid(row=5, column=1)

        # Dostawy
        frame4 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame4.grid(row=0, column=1, sticky="nwse")
        ttk.Label(frame4, text="Informacje o dostawach", foreground=menuColor).grid(row=0, column=0, sticky="w")

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

        menuButton = tk.Button(
            frame,
            image=menuIcon,
            background=menuColor,
            fg=fontColor,
            relief=tk.SUNKEN,
            borderwidth=0,
            activebackground=menuColor,
            command=lambda: expand()
        )
        menuButton.grid(row=1, column=0, pady=5, padx=(10, 10), sticky='nw')
        homeButton = tk.Button(frame, image=homeIcon, background=menuColor, fg=fontColor,
                               font=('MS Reference Sans Serif', 13), relief=tk.SUNKEN, borderwidth=0,
                               activebackground=menuColor, command=lambda: raise_frame(frame1))
        homeButton.grid(row=2, column=0, pady=5, sticky='nwe')
        accountButton = tk.Button(frame, image=accountIcon, background=menuColor, fg=fontColor,
                                  font=('MS Reference Sans Serif', 13), relief=tk.SUNKEN, borderwidth=0,
                                  activebackground=menuColor, command=lambda: raise_frame(frame2))
        accountButton.grid(row=3, column=0, pady=5, sticky='nwe')
        productButton = tk.Button(frame, image=productIcon, background=menuColor, fg=fontColor,
                                  font=('MS Reference Sans Serif', 13), relief=tk.SUNKEN, borderwidth=0,
                                  activebackground=menuColor, command=lambda: raise_frame(frame3))
        productButton.grid(row=4, column=0, pady=5, sticky='nwe')
        locationButton = tk.Button(frame, image=locationIcon, background=menuColor, fg=fontColor,
                                   font=('MS Reference Sans Serif', 13), relief=tk.SUNKEN, borderwidth=0,
                                   activebackground=menuColor, command=lambda: raise_frame(frame4))
        locationButton.grid(row=5, column=0, pady=5, sticky='nwe')
        if user.role != "pracownik":
            employeesButton = tk.Button(frame, image=employeesIcon, background=menuColor, fg=fontColor,
                                        font=('MS Reference Sans Serif', 13), relief=tk.SUNKEN, borderwidth=0,
                                        activebackground=menuColor, command=lambda: raise_frame(frame5))
            employeesButton.grid(row=6, column=0, pady=5, sticky='nwe')

        # frame.bind('<Enter>',lambda e: expand())
        # frame.bind('<Leave>',lambda e: contract())

        frame.grid_propagate(False)

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
