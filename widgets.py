import tkinter as tk
from tkinter import ttk
from main import Login
import pyglet
from user import User
from product import Product
from order import Order
from cart import Cart
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
            self.root.destroy()
            commandPassed()

        def close():
            self.root.destroy()
            popButton.config(state="normal")

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
    def __init__(self, db, name, id, user):
        root = tk.Tk()
        objectToDisplay = ""
        if name == "products":
            objectToDisplay = Product(db, id, user.dept_id)
            root.title(objectToDisplay.name)
        elif name == "users":
            objectToDisplay = User(db, id)
            root.title(objectToDisplay.login)
        elif name == "orders":
            objectToDisplay = Order(db, id)
            root.title("Zamówienie o id = " + str(objectToDisplay.id))
        elif name == "carts":
            objectToDisplay = Cart(db, id)

        bgColor = "white"


        root.configure(background=bgColor, borderwidth=1,
                       relief=tk.RIDGE)
        ttk.Label(root, text=objectToDisplay, background=bgColor, font=("Roboto Light", 12)).grid(row=0, column=0)

        root.resizable(False, False)

        if name == "products":
            today = datetime.today()
            months = []
            amounts = []
            for i in range(12):
                month = today + dateutil.relativedelta.relativedelta(months=-i)
                months.append(month)
                amount = db.chartData(id, user.dept_id, month.strftime("%m"), month.strftime("%Y"))
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
    def __init__(self, popButton):
        def close():
            root.destroy()
            popButton.config(state="normal")

        def command(amount):
            for i in range(int(amount)):
                ttk.Label(root, text="Produkt " + str(i) + ":", background=bgColor, font=("Roboto Light", 12)).grid(row=i+1, column=0)
                entries.append(ttk.Entry(root))
                entries[i].grid(row=i+1, column=1)

        entries=[]
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

        ttk.Label(root, text="Wybierz ilość rodzajów produktów:", background=bgColor, font=("Roboto Light", 12)).grid(
            row=0, column=0)
        entry = ttk.Entry(root)
        entry.grid(row=0, column=1)
        tk.Button(root, text="Zatwierdź", command=lambda: command(entry.get())).grid(row=0, column=2)



class AddBox:
    def __init__(self, popButton, db, table, names):
        def command():
            flag = True
            for entry in entries:
                if entry.get() == '':
                    entry.configure()
                    errorLabel.configure(text="Wypełnij wszystkie wymagane pola")
                    flag = False
            if flag:
                popButton.config(state="normal")
                db.insert(table, entries)
                root.destroy()

        def close():
            root.destroy()
            popButton.config(state="normal")

        bgColor = "white"
        buttonColor = "#0589CF"

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
        for key, value in names.items():
            if value[-1] != "X":
                entry = ttk.Entry(root)
                entry.grid(row=counter, column=1, sticky="w")
            else:
                entry = ttk.Combobox(root)
                entry.grid(row=counter, column=1, sticky="w")
                value = value[:-1]
                entry.configure(values=db.fetchAll("tax_rates", "tax_rate"))
            ttk.Label(root, text=key + ":", background=bgColor, font=("Roboto Light", 12)).grid(row=counter, column=0,
                                                                                                sticky="w")
            counter += 1
            entries.append(entry)

        errorLabel = ttk.Label(root, text="", foreground="red", background=bgColor, font=("Roboto Light", 8))
        errorLabel.grid(row=len(entries), column=0, sticky="w")

        tk.Button(root, text="Dodaj", width=10, background=buttonColor, fg="white",
                  command=lambda: command()).grid(row=len(entries) + 1, column=0, sticky="w")


class EditBox:
    def __init__(self, db, popButton, name, id, user, **kwargs):
        def close():
            root.destroy()
            popButton.config(state="normal")

        root = tk.Tk()
        objectToDisplay = ""
        if name == "products":
            objectToDisplay = Product(db, id, user.dept_id)
            root.title(objectToDisplay.name)
        elif name == "users":
            objectToDisplay = User(db, id)
        elif name == "orders":
            objectToDisplay = Order(db, id)
        elif name == "carts":
            objectToDisplay = Cart(db, id)

        bgColor = "white"
        pyglet.font.add_file('Roboto-Light.ttf')
        popButton.config(state="disabled")
        root.configure(background=bgColor, borderwidth=1,
                       relief=tk.RIDGE)
        root.resizable(False, False)
        root.protocol("WM_DELETE_WINDOW", lambda: close())
        root.title("Edytuj")



        splittedToRows = str(objectToDisplay).split("\n")
        for key, item in kwargs.items():
            if key == "indexes":
                tmp=[]
                for i in item:
                    tmp.append(splittedToRows[i])
                splittedToRows=tmp
        counter = 0
        for row in splittedToRows:
            row1 = row.split(": ")
            ttk.Label(root, text=row1[0] + ":", background=bgColor, font=("Roboto Light", 12)).grid(row=counter, column=0,
                                                                                              sticky="nw")
            ttk.Label(root, text=row1[1], background=bgColor, font=("Roboto Light", 12)).grid(row=counter, column=1,
                                                                                              sticky="nw")
            entry = ttk.Entry(root)
            entry.grid(row=counter, column=2)
            button = tk.Button(root, text="Edytuj...")
            button.configure(command=lambda buttonToPass=button, rowToPass=row1, entryToPass=entry: MessageBox(
                'Czy na pewno chcesz zmienić wartość elementu ' + rowToPass[0] + ' z ' + rowToPass[
                    1] + ' na ' + str(entryToPass.get()) + '?', buttonToPass, print(1), "Edytuj"))
            button.grid(row=counter, column=3, sticky="w")
            counter += 1


class WidgetList:
    def __init__(self, framePassed, db, table, columnNames, names, user, title, addDictionary, **kwargs):
        self.addIcon = tk.PhotoImage(file='icons/add.png')
        self.refreshIcon = tk.PhotoImage(file='icons/refresh.png')
        self.displayIcon = tk.PhotoImage(file='icons/display.png')
        self.editIcon = tk.PhotoImage(file='icons/edit.png')
        self.deleteIcon = tk.PhotoImage(file='icons/delete.png')
        self.startIcon = tk.PhotoImage(file="icons/start.png")
        self.finishIcon = tk.PhotoImage(file="icons/finish.png")
        self.forwardsIcon = tk.PhotoImage(file="icons/forwards.png")
        self.backwardsIcon = tk.PhotoImage(file="icons/backwards.png")

        framePassed.grid_columnconfigure(0, weight=1)
        bgColor = '#FFFFFF'
        headerColor = "#0589CF"
        ttk.Label(framePassed, text=title, font=("Roboto Light", 25, "bold"), foreground="#0589CF").grid(row=0,
                                                                                                         column=0)
        frame = tk.Frame(framePassed, background=bgColor)
        frame.grid(row=1, column=0, sticky="nwse")

        addition = ""
        self.startingIndex = 0
        if table == "users":
            self.itemList = db.fetchEmployeesAdmin(user.id, columnNames)
            indexes = (1,2,3,4,5,6)
        else:
            for key, item in kwargs.items():
                if key == "add":
                    addition = item
            self.itemList = db.fetchAll(table, columnNames, add=addition)
            indexes = (1, 2, 3, 4, 5, 6, 7)
        self.itemList.sort()
        self.iterator = 25
        if len(self.itemList) < self.iterator:
            self.rangeEnd = len(self.itemList)
        else:
            self.rangeEnd = self.iterator + self.startingIndex
        self.labels = []

        self.sortingMethod = 0
        self.reverse = False

        buttonsFrame = tk.Frame(frame, background=bgColor)
        buttonsFrame.grid(row=0, column=0, sticky="w")
        addButton = tk.Button(buttonsFrame, image=self.addIcon, relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                              activebackground=bgColor, command=lambda: AddBox(addButton, db, table, addDictionary))
        if table == "orders":
            addButton.configure(command=lambda: AddOrdersBox(addButton))
        addButton.grid(row=0, column=0, sticky="w", padx=(10, 0))
        refreshButton = tk.Button(buttonsFrame, image=self.refreshIcon, relief=tk.SUNKEN, borderwidth=0,
                                  background=bgColor,
                                  activebackground=bgColor,
                                  command=lambda: configureWidgets(self.startingIndex, "refresh"))
        refreshButton.grid(row=0, column=1, sticky="w")
        for i in range(5):
            frame.grid_columnconfigure(i, weight=1)

        sortButtons = []
        for name in names:
            button = tk.Button(frame, text=name, font=("Roboto Light", 12), relief=tk.SUNKEN, borderwidth=0,
                               background=headerColor, foreground="white",
                               activebackground=headerColor)
            button.grid(row=1, column=names.index(name), sticky="we")
            sortButtons.append(button)
        ttk.Label(frame, background=headerColor).grid(row=1, column=len(sortButtons), sticky="nswe")
        ttk.Label(frame, background=headerColor).grid(row=1, column=len(sortButtons) + 1, sticky="nswe")
        ttk.Label(frame, background=headerColor).grid(row=1, column=len(sortButtons) + 2, sticky="nswe")
        sortButtons[0].grid_configure(padx=(7, 0))
        sortButtons[0].configure(command=lambda: sort(names[0]))
        sortButtons[1].configure(command=lambda: sort(names[1]))
        sortButtons[2].configure(command=lambda: sort(names[2]))
        sortButtons[3].configure(command=lambda: sort(names[3]))
        sortButtons[4].configure(command=lambda: sort(names[4]))

        def sort(buttonName):
            index = names.index(buttonName)
            if index == self.sortingMethod:
                if self.reverse:
                    sortButtons[index].configure(text=names[index] + "🠉")
                else:
                    sortButtons[index].configure(text=names[index] + "🠋")
                self.reverse = not self.reverse
                self.itemList.sort(key=lambda x: x[index], reverse=self.reverse)
            else:
                sortButtons[index].configure(text=names[index] + "🠉")
                sortButtons[self.sortingMethod].configure(text=names[self.sortingMethod])
                self.sortingMethod = index
                if self.reverse:
                    self.reverse = not self.reverse
                self.itemList.sort(key=lambda x: x[index])
            configureWidgets(self.startingIndex - self.iterator + 1, "sort")

        def configureWidgets(index, choice):
            if index < 0 and choice == "sort":
                index = 0
            if (index >= len(self.itemList)) and choice == "forwards":
                index = 0
                self.rangeEnd = self.iterator
                self.startingIndex = 0
            if choice == "refresh":
                self.itemList = db.fetchAll(table, columnNames, add=addition)
                self.itemList.sort(key=lambda x: x[self.sortingMethod])
                index -= self.iterator - 1
            counter = index
            for widget in self.labels:
                for label in range(5):
                    widget[label].configure(text=self.itemList[counter][label])
                widget[5].configure(
                    command=lambda idToPass=widget[0].cget("text"): DisplayBox(db, table, idToPass, user))
                widget[6].configure()
                widget[7].configure(command=lambda idToPass=widget[0].cget("text"), thisButton=deleteButton: MessageBox(
                    "Czy na pewno chcesz usunąć element o id = " + str(idToPass) + "?", thisButton,
                    lambda: db.delete(table, columnNames[0], idToPass), "Usuń"))
                counter += 1
            if choice == "start":
                self.rangeEnd = self.iterator
                self.startingIndex = 0
            elif choice == "backwards":
                self.rangeEnd -= self.iterator
                self.startingIndex -= self.iterator
                if self.startingIndex < 0:
                    self.rangeEnd = len(self.itemList)
                    self.startingIndex = len(self.itemList) - self.iterator + len(self.itemList) % self.iterator
            elif choice == "forwards":
                self.rangeEnd += self.iterator
                self.startingIndex += self.iterator
            elif choice == "end":
                self.rangeEnd = len(self.itemList)
                self.startingIndex = index

        for self.startingIndex in range(self.rangeEnd):
            row = self.startingIndex % self.iterator + 2
            columns = []
            label0 = ttk.Label(frame, text=self.itemList[self.startingIndex][0])
            label0.grid(row=row, column=0, sticky="we", padx=(10, 0))
            columns.append(label0)
            label1 = ttk.Label(frame, text=self.itemList[self.startingIndex][1])
            label1.grid(row=row, column=1, sticky="we")
            columns.append(label1)
            label2 = ttk.Label(frame, text=self.itemList[self.startingIndex][2])
            label2.grid(row=row, column=2, sticky="we")
            columns.append(label2)
            label3 = ttk.Label(frame, text=self.itemList[self.startingIndex][3])
            label3.grid(row=row, column=3, sticky="we")
            columns.append(label3)
            label4 = ttk.Label(frame, text=self.itemList[self.startingIndex][4])
            label4.grid(row=row, column=4, sticky="we")
            columns.append(label4)
            if table == "users":
                isBlocked = db.fetch(table, "*", "user_id", self.itemList[self.startingIndex][0])[12]
                if isBlocked:
                    for label in columns:
                        label.configure(foreground="red")
            displayButton = tk.Button(frame, image=self.displayIcon, relief=tk.SUNKEN, borderwidth=0,
                                      background=bgColor,
                                      activebackground=bgColor,
                                      command=lambda idToPass=self.itemList[self.startingIndex][0]: DisplayBox(db,
                                                                                                               table,
                                                                                                               idToPass,
                                                                                                               user))
            displayButton.grid(row=row, column=5, sticky="nwse")
            columns.append(displayButton)
            editButton = tk.Button(frame, image=self.editIcon, relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                   activebackground=bgColor)
            idForButton = str(columns[0].cget("text"))
            editButton.configure(command=lambda idToPass=idForButton: EditBox(db, editButton, table, idToPass, user, indexes=indexes))
            editButton.grid(row=row, column=6, sticky="nwse")
            columns.append(editButton)
            deleteButton = tk.Button(frame, image=self.deleteIcon, relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                     activebackground=bgColor)
            deleteButton.configure(command=lambda idToPass=idForButton, thisButton=deleteButton: MessageBox(
                "Czy na pewno chcesz usunąć element o id = " + idToPass + "?", thisButton,
                lambda: db.delete(table, columnNames[0], idToPass), "Usuń"))
            deleteButton.grid(row=row, column=7, sticky="nwse", padx=(0, 10))
            columns.append(deleteButton)
            if row % 2 != 0:
                for column in columns:
                    column.configure(background="#d8edf8")
            self.labels.append(columns)

        if len(self.itemList) > self.iterator:
            pageButtonsFrame3 = tk.Frame(frame, background=bgColor)
            pageButtonsFrame3.grid(row=row + 1, column=0, sticky="w", padx=(8, 0))
            firstPageButton = tk.Button(pageButtonsFrame3, image=self.startIcon, relief=tk.SUNKEN, borderwidth=0,
                                        background=bgColor,
                                        activebackground=bgColor,
                                        command=lambda: configureWidgets(0, "start"))
            firstPageButton.grid(row=0, column=0, sticky="w")
            previousPageButton = tk.Button(pageButtonsFrame3, image=self.backwardsIcon, relief=tk.SUNKEN, borderwidth=0,
                                           background=bgColor,
                                           activebackground=bgColor,
                                           command=lambda: configureWidgets(self.rangeEnd - 2 * self.iterator,
                                                                            "backwards"))
            previousPageButton.grid(row=0, column=1, sticky="w")
            page1Button = tk.Button(pageButtonsFrame3, text="1", font=("Roboto Light", 10), relief=tk.SUNKEN,
                                    borderwidth=0, background=bgColor,
                                    activebackground=bgColor)
            page1Button.grid(row=0, column=2, sticky="w")
            page2Button = tk.Button(pageButtonsFrame3, text="2", font=("Roboto Light", 10), relief=tk.SUNKEN,
                                    borderwidth=0, background=bgColor,
                                    activebackground=bgColor)
            page2Button.grid(row=0, column=3, sticky="w")
            page3Button = tk.Button(pageButtonsFrame3, text="3", font=("Roboto Light", 10), relief=tk.SUNKEN,
                                    borderwidth=0, background=bgColor,
                                    activebackground=bgColor)
            page3Button.grid(row=0, column=4, sticky="w")
            ttk.Label(pageButtonsFrame3, text="4", font=("Roboto Light", 10, "bold", "underline")).grid(row=0,
                                                                                                        column=5,
                                                                                                        sticky="w",
                                                                                                        pady=(1, 0))
            page5Button = tk.Button(pageButtonsFrame3, text="5", font=("Roboto Light", 10), relief=tk.SUNKEN,
                                    borderwidth=0, background=bgColor,
                                    activebackground=bgColor)
            page5Button.grid(row=0, column=6, sticky="w")
            page6Button = tk.Button(pageButtonsFrame3, text="6", font=("Roboto Light", 10), relief=tk.SUNKEN,
                                    borderwidth=0, background=bgColor,
                                    activebackground=bgColor)
            page6Button.grid(row=0, column=7, sticky="w")
            page7Button = tk.Button(pageButtonsFrame3, text="7", font=("Roboto Light", 10), relief=tk.SUNKEN,
                                    borderwidth=0, background=bgColor,
                                    activebackground=bgColor)
            page7Button.grid(row=0, column=8, sticky="w")
            nextPageButton = tk.Button(pageButtonsFrame3, image=self.forwardsIcon, relief=tk.SUNKEN, borderwidth=0,
                                       background=bgColor,
                                       activebackground=bgColor,
                                       command=lambda: configureWidgets(self.rangeEnd, "forwards"))
            nextPageButton.grid(row=0, column=9, sticky="w")
            lastPageButton = tk.Button(pageButtonsFrame3, image=self.finishIcon, relief=tk.SUNKEN, borderwidth=0,
                                       background=bgColor,
                                       activebackground=bgColor,
                                       command=lambda: configureWidgets(
                                           len(self.itemList) - self.iterator + len(self.itemList) % self.iterator,
                                           "end"))
            lastPageButton.grid(row=0, column=10, sticky="w")
