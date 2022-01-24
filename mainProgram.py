import tkinter as tk
from tkinter import ttk, filedialog
from user import User
from widgets import AutocompleteCombobox, SidebarMenu, OnlyMessageBox
from WidgetList import WidgetList
import pyglet
from datetime import datetime
from tkcalendar import Calendar
import xlsxwriter


class MainProgram:
    def __init__(self, db, login):
        self.db = db
        self.login = login
        db.fetch("users", "*", "user_id", self.login)
        db.set("users", "last_login", str(datetime.now()), "user_id", str(login))
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

            # Konto
            frame1 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
            frame1.grid(row=0, column=1, sticky="nwse")
            accountInfo = user.__str__().split("\n")
            counter = 0
            for singleInfo in accountInfo:
                ttk.Label(frame1, text=singleInfo).grid(row=counter, column=0, sticky="w")
                counter += 1
            emailButton = tk.Button(frame1, text="Zmień...", width=10, background="#0589CF", foreground="white", command=lambda: user.accountConfigureBox("email", emailButton))
            emailButton.grid(row=5, column=1, sticky="w")
            phoneButton = tk.Button(frame1, text="Zmień...", width=10, background="#0589CF", foreground="white", command=lambda: user.accountConfigureBox("phone_number", phoneButton))
            phoneButton.grid(row=6, column=1, sticky="w")
            ttk.Label(frame1, text="Hasło: ").grid(row=9, column=0, sticky="w")
            passwordButton = tk.Button(frame1, text="Zmień...", width=10, background="#0589CF", foreground="white", command=lambda: user.accountConfigureBox("password", passwordButton))
            passwordButton.grid(row=9, column=1, sticky="w")

            # Produkty
            frame2 = tk.Frame(root, height=root.winfo_height(), width=root.winfo_width(), bg=bgColor, borderwidth=1,
                              relief=tk.RIDGE)
            frame2.grid(row=0, column=1, sticky="nwse")
            frame2.grid_propagate(False)

            products = ("Id", "Nazwa", "Producent", "Cena zakupu", "Cena sprzedaży")
            WidgetList(frame2, db, "products", ("product_id", "name", "marks.mark", "purchase_price", "price"),
                       products,
                       user, "Produkty", add="INNER JOIN marks USING (mark_id)",)

            # Dostawy
            frame3 = tk.Frame(root, height=root.winfo_height(), width=root.winfo_width(), bg=bgColor, borderwidth=1,
                              relief=tk.RIDGE)
            frame3.grid(row=0, column=1, sticky="nwse")
            frame3.grid_propagate(False)

            orders = ("Id", "Status", "Data złożenia", "Data dostarczenia", "Użytkownik")
            WidgetList(frame3, db, "orders", ("order_id", "order_status", "order_date", "delivery_date", "users.login"),
                       orders, user, "Dostawy", add="INNER JOIN users USING (user_id)")

            # Zamówienia
            frame4 = tk.Frame(root, height=root.winfo_height(), width=root.winfo_width(), bg=bgColor, borderwidth=1,
                              relief=tk.RIDGE)
            frame4.grid(row=0, column=1, sticky="nwse")
            frame4.grid_propagate(False)
            cart = ("Id", "Data złożenia", "Status", "Pracownik", "Klient")

            cartDictionary = {
                "Klient": "client_id",
            }

            WidgetList(frame4, db, "carts", ("cart_id", "purchase_date", "order_status", "login",
                                             "concat(clients.first_name, ' ', clients.last_name)"),
                       cart, user, "Zamówienia",
                       add="INNER JOIN users USING (user_id) INNER JOIN clients USING (client_id)")

            # Pracownicy
            frame5 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
            frame5.grid(row=0, column=1, sticky="nwse")

            users = ("Id", "Imię", "Nazwisko", "Pensja", "Ostatnio zalogowany")
            WidgetList(frame5, db, "users", ("user_id", "first_name", "last_name", "salary", "last_login"), users, user,
                       "Pracownicy")

            def generateExcel(date1, date2):
                data = db.getReport(user.dept_id, date1, date2)
                data1 = db.getReport1(user.dept_id, date1, date2)
                data2 = db.getReport2(user.dept_id, date1, date2)
                # file = filedialog.asksaveasfile(filetypes=(("Plik Excel", ".xlsx"),
                #                                            ("Plik Excel", ".xlsx")),
                #                                 initialfile="Raport " + date1.replace("/", ".") + " - " + date2.replace(
                #                                     "/", ".") + ".xlsx",
                #                                 title='Zapisz plik',
                #                                 initialdir="/")
                workbook = xlsxwriter.Workbook("Raport " + date1.replace("/", ".") + " - " + date2.replace("/", ".") + ".xlsx")
                worksheet = workbook.add_worksheet("Pracownicy")
                worksheet.write(0, 0, "Użytkownik")
                worksheet.write(0, 1, "Nazwa produktu")
                worksheet.write(0, 2, "Ilość")
                worksheet.write(0, 3, "Zysk")
                row = 1
                for d in data:
                    worksheet.write(row, 0, d[0])
                    worksheet.write(row, 1, d[1])
                    worksheet.write(row, 2, d[2])
                    worksheet.write(row, 3, d[3])
                    row += 1

                worksheet1 = workbook.add_worksheet("Zamówienia")
                worksheet1.write(0, 0, "Zamówienie")
                worksheet1.write(0, 1, "Nazwa produktu")
                worksheet1.write(0, 2, "Przychód")
                row = 1
                for d in data1:
                    worksheet1.write(row, 0, d[0])
                    worksheet1.write(row, 1, d[1])
                    worksheet1.write(row, 2, d[2])
                    row += 1

                worksheet2 = workbook.add_worksheet("Dostawy")
                worksheet2.write(0, 0, "Dostawa")
                worksheet2.write(0, 1, "Nazwa produktu")
                worksheet2.write(0, 2, "Koszt")
                row = 1
                for d in data2:
                    worksheet2.write(row, 0, d[0])
                    worksheet2.write(row, 1, d[1])
                    worksheet2.write(row, 2, d[2])
                    row += 1

                workbook.close()


            # Raporty
            frame6 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
            frame6.grid(row=0, column=1, sticky="nwse")
            ttk.Label(frame6, text="Raporty", font=("Roboto Light", 25, "bold"), foreground="#0589CF").grid(row=0,
                                                                                                             column=0)
            frame6Content = tk.Frame(frame6, bg=bgColor)
            frame6Content.grid(row=1, column=0)
            ttk.Label(frame6Content, text="Od:", background=bgColor).grid(row=0, column=0)
            ttk.Label(frame6Content, text="Do:", background=bgColor).grid(row=0, column=2)
            dateStart = Calendar(frame6Content, background="#0589CF", bordercolor="black",
               headersbackground="#d8edf8", normalbackground="white", foreground='white',
               normalforeground='black', headersforeground='black')
            dateStart.grid(row=1, column=0)
            dateEnd = Calendar(frame6Content, background="#0589CF", bordercolor="black",
               headersbackground="#d8edf8", normalbackground="white", foreground='white',
               normalforeground='black', headersforeground='black')
            dateEnd.grid(row=1, column=2)
            tk.Button(frame6Content, text="Pokaż raport", command=lambda: generateExcel(dateStart.get_date(), dateEnd.get_date())).grid(row=2, column=1)

            frame0 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
            frame0.grid(row=0, column=1, sticky="nwse")
            ttk.Label(frame0, text="Witaj, " + user.name, font=('Roboto Light', 40)).grid(row=0, column=0, padx=10)

            SidebarMenu(root, (frame0, frame1, frame2, frame3, frame4, frame5, frame6), user, db)
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
