import tkinter as tk
from tkinter import ttk
from user import User
from product import Product
from widgets import AutocompleteCombobox, SidebarMenu, WidgetList, OnlyMessageBox
import pyglet
from datetime import datetime
from widgets import Boxes


class MainProgram:
    def __init__(self, db, login):
        self.db = db
        self.login = login
        db.fetch("users", "login", self.login)
        db.set("users", "last_login", str(datetime.now()), "user_id", str(db.fetch("users", "login", self.login)[0]))
        user = User(self.db, self.login)

        if user.isBlocked:
            OnlyMessageBox("Twoje konto zostało zablokowane. Skontaktuj się z przełożonym, w celu jego odblokowania.")
        else:
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

            # Konto
            frame2 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
            frame2.grid(row=0, column=1, sticky="nwse")
            accountInfo = user.__str__().split("\n")
            counter = 0
            for singleInfo in accountInfo:
                ttk.Label(frame2, text=singleInfo).grid(row=counter, column=0, sticky="w")
                counter += 1
            box = Boxes(db)
            emailButton = tk.Button(frame2, text="Zmień...", command=lambda: box.accountConfigureBox(user.id, "email", emailButton))
            emailButton.grid(row=3, column=1, sticky="w")
            phoneButton = tk.Button(frame2, text="Zmień...", command=lambda: box.accountConfigureBox(user.id, "phone_number", phoneButton))
            phoneButton.grid(row=4, column=1, sticky="w")
            ttk.Label(frame2, text="Hasło: ").grid(row=7, column=0, sticky="w")
            passwordButton = tk.Button(frame2, text="Zmień...", command=lambda: box.accountConfigureBox(user.id, "password", passwordButton))
            passwordButton.grid(row=7, column=1, sticky="w")

            # Produkty
            frame3 = tk.Frame(root, height=root.winfo_height(), width=root.winfo_width(), bg=bgColor, borderwidth=1,
                              relief=tk.RIDGE)
            frame3.grid(row=0, column=1, sticky="nwse")
            frame3.grid_propagate(False)

            products = ("Id", "Nazwa", "Producent", "Cena zakupu", "Cena sprzedaży")
            WidgetList(frame3, db, "products", ("product_id", "name", "marks.mark", "purchase_price", "price"),
                       products,
                       user, "Produkty", add="INNER JOIN marks USING (mark_id)")

            # Dostawy
            frame4 = tk.Frame(root, height=root.winfo_height(), width=root.winfo_width(), bg=bgColor, borderwidth=1,
                              relief=tk.RIDGE)
            frame4.grid(row=0, column=1, sticky="nwse")
            frame4.grid_propagate(False)

            orders = ("Id", "Status", "Data złożenia", "Data dostarczenia", "Użytkownik")
            WidgetList(frame4, db, "orders", ("order_id", "order_status", "order_date", "delivery_date", "users.login"),
                       orders, user, "Dostawy", add="INNER JOIN users USING (user_id)")

            # Zamówienia
            frame5 = tk.Frame(root, height=root.winfo_height(), width=root.winfo_width(), bg=bgColor, borderwidth=1,
                              relief=tk.RIDGE)
            frame5.grid(row=0, column=1, sticky="nwse")
            frame5.grid_propagate(False)
            cart = ("Id", "Data złożenia", "Status", "Pracownik", "Klient")
            WidgetList(frame5, db, "carts", ("cart_id", "purchase_date", "order_status", "login",
                                             "concat(clients.first_name, ' ', clients.last_name)"),
                       cart, user, "Zamówienia",
                       add="INNER JOIN users USING (user_id) INNER JOIN clients USING (client_id)")

            # Pracownicy
            frame6 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
            frame6.grid(row=0, column=1, sticky="nwse")

            users = ("Id", "Imię", "Nazwisko", "Pensja", "Ostatnio zalogowany")
            WidgetList(frame6, db, "users", ("user_id", "first_name", "last_name", "salary", "last_login"), users, user,
                       "Pracownicy")

            frame1 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
            frame1.grid(row=0, column=1, sticky="nwse")
            ttk.Label(frame1, text="Witaj, " + user.name, font=('Roboto Light', 40)).grid(row=0, column=0, padx=10)

            SidebarMenu(root, frame1, frame2, frame3, frame4, frame5, frame6, user, db)
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
