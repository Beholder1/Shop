import tkinter as tk
from tkinter import ttk
from main import Login
import pyglet

from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import dateutil.relativedelta


class AutocompleteCombobox(ttk.Combobox):

    def set_completion_list(self, completion_list):
        """Use our completion list as our dropdown selection menu, arrows move through menu."""
        self._completion_list = sorted(completion_list, key=str.lower)  # Work with a sorted list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list  # Setup our popup menu

    def autocomplete(self, delta=0):
        """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
        if delta:  # need to delete selection otherwise we would fix the current position
            self.delete(self.position, tk.END)
        else:  # set position to end so selection starts where text-entry ended
            self.position = len(self.get())
        # collect hits
        _hits = []
        for element in self._completion_list:
            if element.lower().startswith(self.get().lower()):  # Match case insensitively
                _hits.append(element)
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        # now finally perform the autocompletion
        if self._hits:
            self.delete(0, tk.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tk.END)

    def handle_keyrelease(self, event):
        """event handler for the keyrelease event on this widget"""
        if event.keysym == "BackSpace":
            self.delete(self.index(tk.INSERT), tk.END)
            self.position = self.index(tk.END)
        if event.keysym == "Left":
            if self.position < self.index(tk.END):  # delete the selection
                self.delete(self.position, tk.END)
            else:
                self.position = self.position - 1  # delete one character
                self.delete(self.position, tk.END)
        if event.keysym == "Right":
            self.position = self.index(tk.END)  # go to end (no selection)
        if len(event.keysym) == 1:
            self.autocomplete()


class SidebarMenu:
    def __init__(self, root, frames, user, db):
        menuIcon = tk.PhotoImage(file='icons/menu.png')
        closeIcon = tk.PhotoImage(file='icons/close.png')
        homeIcon = tk.PhotoImage(file='icons/home.png')
        accountIcon = tk.PhotoImage(file='icons/account.png')
        productIcon = tk.PhotoImage(file='icons/product.png')
        deliveryIcon = tk.PhotoImage(file='icons/delivery.png')
        orderIcon = tk.PhotoImage(file='icons/order.png')
        employeesIcon = tk.PhotoImage(file='icons/employees.png')
        logoutIcon = tk.PhotoImage(file='icons/logout.png')
        reportIcon = tk.PhotoImage(file="icons/report.png")

        self.currentFrame = frames[0]

        menuColor = '#0589CF'
        fontColor = 'black'
        min_w = 50
        max_w = 120
        self.cur_width = min_w
        self.expanded = False

        frame = tk.Frame(root, bg=menuColor, width=50, height=root.winfo_height())
        frame.grid(row=0, column=0, sticky='nws')

        def expand():
            rep = root.after(2, expand)
            if not self.expanded:
                self.cur_width += 70
                frame.config(width=self.cur_width)
            if self.cur_width >= max_w:
                self.expanded = True
                root.after_cancel(rep)
                fill()

        def contract():
            self.cur_width -= 70
            rep = root.after(2, contract)
            frame.config(width=self.cur_width)
            if self.cur_width <= min_w:
                self.expanded = False
                root.after_cancel(rep)
                fill()

        def fill():
            if self.expanded:
                menuButton.config(image=closeIcon, command=contract)
                homeButton.config(image="", text="Strona główna")
                homeButton.grid_configure(pady=0)
                accountButton.config(image="", text="Konto")
                accountButton.grid_configure(pady=0)
                productButton.config(image="", text="Produkty")
                productButton.grid_configure(pady=0)
                deliveryButton.config(image="", text="Dostawy")
                deliveryButton.grid_configure(pady=0)
                orderButton.config(image="", text="Zamówienia")
                orderButton.grid_configure(pady=0)
                logoutButton.config(image="", text="Wyloguj")
                logoutButton.grid_configure(pady=0)
                if user.role != "pracownik":
                    employeesButton.config(image="", text="Pracownicy")
                    employeesButton.grid_configure(pady=0)
                    reportButton.config(image="", text="Raporty")
                    reportButton.grid_configure(pady=0)
            else:
                menuButton.config(image=menuIcon, command=expand)
                homeButton.config(image=homeIcon)
                homeButton.grid_configure(pady=5)
                accountButton.config(image=accountIcon)
                accountButton.grid_configure(pady=5)
                productButton.config(image=productIcon)
                productButton.grid_configure(pady=5)
                deliveryButton.config(image=deliveryIcon)
                deliveryButton.grid_configure(pady=5)
                orderButton.config(image=orderIcon)
                orderButton.grid_configure(pady=5)
                logoutButton.config(image=logoutIcon)
                logoutButton.grid_configure(pady=5)
                if user.role != "pracownik":
                    employeesButton.config(image=employeesIcon)
                    employeesButton.grid_configure(pady=5)
                    reportButton.config(image=reportIcon)
                    reportButton.grid_configure(pady=5)

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

        def changeFrame(frameNew):
            # self.currentFrame.grid_forget()
            # frameNew.grid_configure(row=0, column=1, sticky="nwse")
            # self.currentFrame = frameNew
            frameNew.tkraise()

        menuButton.grid(row=1, column=0, pady=5, padx=(10, 10), sticky='nw')
        homeButton = tk.Button(frame, image=homeIcon, background=menuColor, fg=fontColor,
                               font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                               activebackground=menuColor, command=lambda: changeFrame(frames[0]))
        homeButton.grid(row=2, column=0, pady=5, sticky='nwe')
        accountButton = tk.Button(frame, image=accountIcon, background=menuColor, fg=fontColor,
                                  font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                                  activebackground=menuColor, command=lambda: changeFrame(frames[1]))
        accountButton.grid(row=3, column=0, pady=5, sticky='nwe')
        productButton = tk.Button(frame, image=productIcon, background=menuColor, fg=fontColor,
                                  font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                                  activebackground=menuColor, command=lambda: changeFrame(frames[2]))
        productButton.grid(row=4, column=0, pady=5, sticky='nwe')
        deliveryButton = tk.Button(frame, image=deliveryIcon, background=menuColor, fg=fontColor,
                                   font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                                   activebackground=menuColor, command=lambda: changeFrame(frames[3]))
        deliveryButton.grid(row=5, column=0, pady=5, sticky='nwe')
        orderButton = tk.Button(frame, image=orderIcon, background=menuColor, fg=fontColor,
                                font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                                activebackground=menuColor, command=lambda: changeFrame(frames[4]))
        orderButton.grid(row=6, column=0, pady=5, sticky='nwe')

        def logout():
            root.destroy()
            db.disconnect()
            Login()

        logoutButton = tk.Button(frame, image=logoutIcon, background=menuColor, fg=fontColor,
                                 font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                                 activebackground=menuColor,
                                 command=lambda: MessageBox("Czy na pewno chcesz się wylogować?", logoutButton,
                                                            logout, "Wyloguj się"))

        if user.role != "pracownik":
            employeesButton = tk.Button(frame, image=employeesIcon, background=menuColor, fg=fontColor,
                                        font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                                        activebackground=menuColor, command=lambda: changeFrame(frames[5]))
            employeesButton.grid(row=7, column=0, pady=5, sticky='nwe')
            reportButton = tk.Button(frame, image=reportIcon, background=menuColor, fg=fontColor,
                                     font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                                     activebackground=menuColor, command=lambda: changeFrame(frames[6]))
            reportButton.grid(row=8, column=0, pady=5, sticky='nwe')
            logoutButton.grid(row=9, column=0, pady=5, sticky='nwe')
        else:
            logoutButton.grid(row=7, column=0, pady=5, sticky='nwe')

        frame.grid_propagate(False)


class MessageBox:
    def __init__(self, text, popButton, commandPassed, title):
        def command():
            popButton.config(state="normal")
            self.root.destroy()
            commandPassed()

        def close():
            popButton.config(state="normal")
            self.root.destroy()

        bgColor = "white"
        buttonColor = "#0589CF"

        pyglet.font.add_file('Roboto-Light.ttf')
        popButton.config(state="disabled")
        self.root = tk.Tk()
        self.root.title(title)
        self.root.configure(background=bgColor, borderwidth=1,
                            relief=tk.RIDGE)
        self.root.geometry("400x125")
        self.root.resizable(False, False)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.protocol("WM_DELETE_WINDOW", lambda: close())
        label = ttk.Label(self.root, text=text, background=bgColor, font=("Roboto Light", 12), wraplength=390)
        label.grid(row=0, column=0)
        buttonsFrame = tk.Frame(self.root, background=bgColor)
        buttonsFrame.grid(row=1, column=0)
        tk.Button(buttonsFrame, text="Tak", width=10, background=buttonColor, fg="white",
                  command=lambda: command()).grid(row=0, column=0,
                                                  padx=15)
        tk.Button(buttonsFrame, text="Nie", width=10, background=buttonColor, fg="white",
                  command=lambda: close()).grid(row=0, column=1,
                                                padx=15)


class OnlyMessageBox:
    def __init__(self, text):
        bgColor = "white"
        self.root = tk.Tk()
        self.root.configure(background=bgColor, borderwidth=1,
                            relief=tk.RIDGE)
        self.root.geometry("400x400")
        ttk.Label(self.root, text=text, background=bgColor, font=("Roboto Light", 12)).grid(row=0, column=0)

        self.root.resizable(False, False)


class DisplayBox:
    def __init__(self, db, name, id, deptId, strCommand):
        root = tk.Tk()

        bgColor = "white"

        root.configure(background=bgColor, borderwidth=1,
                       relief=tk.RIDGE)
        ttk.Label(root, text=strCommand, background=bgColor, font=("Roboto Light", 12)).grid(row=0, column=0)

        root.resizable(False, False)

        if name == "products":
            today = datetime.today()
            months = []
            amounts = []
            for i in range(12):
                month = today + dateutil.relativedelta.relativedelta(months=-i)
                months.append(month)
                amount = db.chartData(id, deptId, month.strftime("%m"), month.strftime("%Y"))
                if not amount:
                    amount = 0
                    amounts.append(amount)
                else:
                    amounts.append(amount[0])

            data = {
                "Miesiąc": months,
                "Ilość sprzedanych sztuk": amounts
            }
            df = DataFrame(data, columns=["Miesiąc", "Ilość sprzedanych sztuk"])
            figure = plt.Figure(figsize=(6, 5), dpi=50)
            ax = figure.add_subplot(111)
            chart_type = FigureCanvasTkAgg(figure, root)
            chart_type.get_tk_widget().grid(row=0, column=1)
            df = df[['Miesiąc', 'Ilość sprzedanych sztuk']].groupby('Miesiąc').sum()
            df.plot(kind='line', legend=True, ax=ax)
            ax.set_title('Ilość sprzedanych sztuk w ciągu ostatniego roku')


class AddOrdersBox:
    def __init__(self, db, popButton, name, userId):
        def close():
            root.destroy()
            popButton.config(state="normal")

        def insertToDb():
            list = []
            counter=0
            for i in entries:
                list.append([int(entries[counter].get()), int(entries1[counter].get())])
                counter+=1
            if name == "carts":
                db.insertCart(list, userId, combo.get(), entry0.get(), entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get(), entry6.get(), entry7.get())
            else:
                db.insertProducts(list, userId)

        def command(amount):
            for i in range(int(amount)):
                ttk.Label(root, text="Produkt " + str(i + 1) + ":", background=bgColor, font=("Roboto Light", 12)).grid(
                    row=i + 1 + add, column=0)
                entries.append(ttk.Entry(root))
                entries[i].grid(row=i + 1 + add, column=1)
                ttk.Label(root, text="Ilość: ", background=bgColor, font=("Roboto Light", 12)).grid(
                    row=i + 1 + add, column=2)
                entries1.append(ttk.Entry(root))
                entries1[i].grid(row=i + 1 + add, column=3)
            tk.Button(root, text="Dodaj", command=lambda: insertToDb()).grid(row=i + 2 + add, column=1)

        entries = []
        entries1 = []
        bgColor = "white"
        buttonColor = "#0589CF"

        pyglet.font.add_file('Roboto-Light.ttf')
        popButton.config(state="disabled")
        root = tk.Tk()
        root.configure(background=bgColor, borderwidth=1,
                       relief=tk.RIDGE)
        root.resizable(False, False)
        root.protocol("WM_DELETE_WINDOW", lambda: close())
        root.title("Dodaj")
        add = 0
        if name == "carts":
            ttk.Label(root, text="Imię:", background=bgColor,
                      font=("Roboto Light", 12)).grid(
                row=0, column=0)
            entry0 = ttk.Entry(root)
            entry0.grid(row=0, column=1)

            ttk.Label(root, text="Nazwisko:", background=bgColor,
                      font=("Roboto Light", 12)).grid(
                row=1, column=0)
            entry1 = ttk.Entry(root)
            entry1.grid(row=1, column=1)

            ttk.Label(root, text="Państwo:", background=bgColor,
                      font=("Roboto Light", 12)).grid(
                row=2, column=0)
            entry2 = ttk.Entry(root)
            entry2.grid(row=2, column=1)

            ttk.Label(root, text="Województwo:", background=bgColor,
                      font=("Roboto Light", 12)).grid(
                row=3, column=0)
            entry3 = ttk.Entry(root)
            entry3.grid(row=3, column=1)

            ttk.Label(root, text="Miasto:", background=bgColor,
                      font=("Roboto Light", 12)).grid(
                row=4, column=0)
            entry4 = ttk.Entry(root)
            entry4.grid(row=4, column=1)

            ttk.Label(root, text="Kod pocztowy:", background=bgColor,
                      font=("Roboto Light", 12)).grid(
                row=5, column=0)
            entry5 = ttk.Entry(root)
            entry5.grid(row=5, column=1)

            ttk.Label(root, text="Ulica:", background=bgColor,
                      font=("Roboto Light", 12)).grid(
                row=6, column=0)
            entry6 = ttk.Entry(root)
            entry6.grid(row=6, column=1)

            ttk.Label(root, text="Numer ulicy:", background=bgColor,
                      font=("Roboto Light", 12)).grid(
                row=7, column=0)
            entry7 = ttk.Entry(root)
            entry7.grid(row=7, column=1)

            ttk.Label(root, text="Metoda płatności:", background=bgColor,
                      font=("Roboto Light", 12)).grid(
                row=8, column=0)
            li = []
            for i in db.getEnum("payment_method"):
                li.append(i)
            combo = ttk.Combobox(root, values=li)
            combo.grid(row=8, column=1)
            add = 9
        ttk.Label(root, text="Wybierz ilość rodzajów produktów:", background=bgColor, font=("Roboto Light", 12)).grid(
            row=0 + add, column=0)
        entry = ttk.Entry(root)
        entry.grid(row=0 + add, column=1)
        tk.Button(root, text="Zatwierdź", command=lambda: command(entry.get())).grid(row=0 + add, column=2)


class AddBox:
    def __init__(self, popButton, db, table, names, **kwargs):
        def command():
            flag1 = True
            for entry in entries:
                if entry.get() == '':
                    entry.configure()
                    errorLabel.configure(text="Wypełnij wszystkie wymagane pola")
                    flag1 = False
            if flag1:
                t = []
                v = 0
                for e in entries:
                    if entries.index(e) == k[v][0]:
                        t.append(db.fetchAll(str(fetch[v][1]), str(fetch[v][3]), add="WHERE "+str(fetch[v][2])+" = '"+str(e.get())+"'")[0][0])
                    else:
                        t.append(e.get())
                popButton.config(state="normal")
                db.insert(table, t)
                root.destroy()

        def close():
            root.destroy()
            popButton.config(state="normal")

        bgColor = "white"
        buttonColor = "#0589CF"

        fetch = []
        for key, item in kwargs.items():
            if key == "fetch":
                fetch = item

        pyglet.font.add_file('Roboto-Light.ttf')
        popButton.config(state="disabled")
        root = tk.Tk()
        root.configure(background=bgColor, borderwidth=1,
                       relief=tk.RIDGE)
        root.resizable(False, False)
        root.title("Dodaj")

        root.protocol("WM_DELETE_WINDOW", lambda: close())

        entries = []
        counter = 0
        k=[]
        c = 0
        for key, value in names.items():
            flag = False
            if value[-1] != "X":
                entry = ttk.Entry(root)
                entry.grid(row=counter, column=1, sticky="w")
            else:
                entry = ttk.Combobox(root)
                entry.grid(row=counter, column=1, sticky="w")
                value = value[:-1]
                if fetch[c][0] == "d":
                    l1 = []
                    for i in db.fetchAll(fetch[c][1], fetch[c][2]):
                        l1.append(i[0])
                    entry.configure(values=l1)
                    flag = True
                else:
                    l1 = []
                    for i in db.getEnum(fetch[c][1]):
                        l1.append(i)
                    entry.configure(values=l1)
                c+=1
            ttk.Label(root, text=key + ":", background=bgColor, font=("Roboto Light", 12)).grid(row=counter, column=0,
                                                                                                sticky="w")
            counter += 1
            entries.append(entry)
            if flag:
                k.append((entries.index(entry), c))

        errorLabel = ttk.Label(root, text="", foreground="red", background=bgColor, font=("Roboto Light", 8))
        errorLabel.grid(row=len(entries), column=0, sticky="w")

        tk.Button(root, text="Dodaj", width=10, background=buttonColor, fg="white",
                  command=lambda: command()).grid(row=len(entries) + 1, column=0, sticky="w")


class EditBox:
    def __init__(self, db, popButton, strCommand, **kwargs):
        def close():
            root.destroy()
            popButton.config(state="normal")

        root = tk.Tk()

        bgColor = "white"
        pyglet.font.add_file('Roboto-Light.ttf')
        popButton.config(state="disabled")
        root.configure(background=bgColor, borderwidth=1,
                       relief=tk.RIDGE)
        root.resizable(False, False)
        root.protocol("WM_DELETE_WINDOW", lambda: close())
        root.title("Edytuj")

        combosIndexes = []

        splittedToRows = strCommand.split("\n")
        for key, item in kwargs.items():
            if key == "indexes":
                tmp = []
                if type(item) == int:
                    tmp.append(splittedToRows[item])
                    splittedToRows = tmp
                else:
                    for i in item:
                        tmp.append(splittedToRows[i])
                    splittedToRows = tmp

            if key == "combos":
                if type(item) == int:
                    combosIndexes.append(item)
                else:
                    for i in item:
                        combosIndexes.append(i)
        counter = 0
        for row in splittedToRows:
            if counter in combosIndexes:
                entry = ttk.Combobox(root, values=db.getEnum("order_status"))
                entry.grid(row=counter, column=2)
            else:
                entry = ttk.Entry(root)
                entry.grid(row=counter, column=2)
            row1 = row.split(": ")
            ttk.Label(root, text=row1[0] + ":", background=bgColor, font=("Roboto Light", 12)).grid(row=counter,
                                                                                                    column=0,
                                                                                                    sticky="nw")
            ttk.Label(root, text=row1[1], background=bgColor, font=("Roboto Light", 12)).grid(row=counter, column=1,
                                                                                              sticky="nw")

            button = tk.Button(root, text="Edytuj...")
            button.configure(command=lambda buttonToPass=button, rowToPass=row1, entryToPass=entry: MessageBox(
                'Czy na pewno chcesz zmienić wartość elementu ' + rowToPass[0] + ' z ' + rowToPass[
                    1] + ' na ' + str(entryToPass.get()) + '?', buttonToPass, db.s, "Edytuj"))
            button.grid(row=counter, column=3, sticky="w")
            counter += 1



