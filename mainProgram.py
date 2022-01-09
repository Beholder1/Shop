import tkinter as tk
from tkinter import ttk
from user import User
from product import Product
from widgets import AutocompleteCombobox, SidebarMenu, WidgetList, OnlyMessageBox
import pyglet


class MainProgram:
    def __init__(self, db, login):
        self.db = db
        self.login = login
        db.fetch("users", "login", self.login)
        user = User(self.login, self.db)

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
            ttk.Label(frame2, text=user.__str__()).grid(row=0, column=0, sticky="w")

            # Produkty
            frame3 = tk.Frame(root, height=root.winfo_height(), width=root.winfo_width(), bg=bgColor, borderwidth=1,
                              relief=tk.RIDGE)
            frame3.grid(row=0, column=1, sticky="nwse")
            frame3.grid_propagate(False)

            products = ("Id", "Nazwa", "Producent", "Cena zakupu", "Cena sprzedaży")
            WidgetList(frame3, db, "products", ("product_id", "name", "marks.mark", "purchase_price", "price"), products,
                       user, add="INNER JOIN marks USING (mark_id)")

            # Dostawy
            frame4 = tk.Frame(root, height=root.winfo_height(), width=root.winfo_width(), bg=bgColor, borderwidth=1,
                              relief=tk.RIDGE)
            frame4.grid(row=0, column=1, sticky="nwse")
            frame4.grid_propagate(False)

            orders = ("Id", "Status", "Data złożenia", "Data dostarczenia", "Użytkownik")
            WidgetList(frame4, db, "orders", ("order_id", "order_status", "order_date", "delivery_date", "users.login"), orders,
                       user, add="INNER JOIN users USING (user_id)")

            # Pracownicy
            frame5 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
            frame5.grid(row=0, column=1, sticky="nwse")

            users = ("Id", "Imię", "Nazwisko", "Pensja", "Ostatnio zalogowany")
            WidgetList(frame5, db, "users", ("user_id", "first_name", "last_name", "salary", "last_login"), users, user)

            frame1 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
            frame1.grid(row=0, column=1, sticky="nwse")
            ttk.Label(frame1, text="Witaj, " + user.name, font=('Roboto Light', 40)).grid(row=0, column=0, padx=10)

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
