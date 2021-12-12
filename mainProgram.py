import tkinter as tk
from tkinter import ttk
from user import User
from widgets import AutocompleteCombobox

class MainProgram:
    def __init__(self, db, login):
        user = User(login)

        bgColor = '#FCFCFF'
        acriveColor = "#FDA50F"
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

        def raise_frame(frame):
            frame.tkraise()

        def expand():
            rep = root.after(2, expand)
            if self.expanded == False:
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
                if (user.role != "pracownik"):
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
                if (user.role != "pracownik"):
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
        if(user.role != "pracownik"):
            employeesButton = tk.Button(frame, image=employeesIcon, background=menuColor, fg=fontColor,
                                       font=('MS Reference Sans Serif', 13), relief=tk.SUNKEN, borderwidth=0,
                                       activebackground=menuColor, command=lambda: raise_frame(frame4))
            employeesButton.grid(row=6, column=0, pady=5, sticky='nwe')

        # frame.bind('<Enter>',lambda e: expand())
        # frame.bind('<Leave>',lambda e: contract())

        frame.grid_propagate(0)

        # Konto
        frame2 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame2.grid(row=0, column=1, sticky="nwse")
        ttk.Label(frame2, text=user).grid(row=0, column=0, sticky="w")

        # Produkty
        frame3 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame3.grid(row=0, column=1, sticky="nwse")
        ttk.Label(frame3, text="Wybierz produkt: ").grid(row=0, column=0, sticky="w")
        test_list=["kupa", "dupa", "trupa", "chałupa"]
        combo1 = AutocompleteCombobox(frame3)
        combo1.set_completion_list(db.fetchColumnAll("products", "name"))
        combo1.grid(row=0, column=1, sticky="w")
        combo1.focus_set()

        # Dostawy
        frame4 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame4.grid(row=0, column=1, sticky="nwse")
        ttk.Label(frame4, text="Informacje o dostawach", foreground=menuColor).grid(row=0, column=0, sticky="w")

        frame1 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame1.grid(row=0, column=1, sticky="nwse")
        ttk.Label(frame1, text="Tu będą staty").grid(row=0, column=0)

        root.grid_columnconfigure(1, weight=1)
        root.mainloop()



