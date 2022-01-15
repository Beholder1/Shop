import tkinter as tk
from tkinter import ttk
from main import Login
import pyglet
from user import User
from product import Product
from order import Order
from cart import Cart
from tkinter import Canvas


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
    def __init__(self, root, frame1, frame2, frame3, frame4, frame5, frame6, user, db):
        menuIcon = tk.PhotoImage(file='icons/menu.png')
        closeIcon = tk.PhotoImage(file='icons/close.png')
        homeIcon = tk.PhotoImage(file='icons/home.png')
        accountIcon = tk.PhotoImage(file='icons/account.png')
        productIcon = tk.PhotoImage(file='icons/product.png')
        deliveryIcon = tk.PhotoImage(file='icons/delivery.png')
        orderIcon = tk.PhotoImage(file='icons/order.png')
        employeesIcon = tk.PhotoImage(file='icons/employees.png')
        logoutIcon = tk.PhotoImage(file='icons/logout.png')

        self.currentFrame = frame1

        menuColor = '#0589CF'
        fontColor = 'black'
        min_w = 50
        max_w = 130
        self.cur_width = min_w
        self.expanded = False

        frame = tk.Frame(root, bg=menuColor, width=50, height=root.winfo_height())
        frame.grid(row=0, column=0, sticky='nws')

        def expand():
            rep = root.after(2, expand)
            if not self.expanded:
                self.cur_width += 80
                frame.config(width=self.cur_width)
            if self.cur_width >= max_w:
                self.expanded = True
                root.after_cancel(rep)
                fill()

        def contract():
            self.cur_width -= 80
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
                deliveryButton.config(image="", text="Dostawy", borderwidth=0)
                deliveryButton.grid_configure(pady=0)
                orderButton.config(image="", text="Zamówienia", borderwidth=0)
                orderButton.grid_configure(pady=0)
                logoutButton.config(image="", text="Wyloguj", borderwidth=0)
                logoutButton.grid_configure(pady=0)
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
                deliveryButton.config(image=deliveryIcon, borderwidth=0)
                deliveryButton.grid_configure(pady=5)
                orderButton.config(image=orderIcon, borderwidth=0)
                orderButton.grid_configure(pady=5)
                logoutButton.config(image=logoutIcon, borderwidth=0)
                logoutButton.grid_configure(pady=5)
                if user.role != "pracownik":
                    employeesButton.config(image=employeesIcon, borderwidth=0)
                    employeesButton.grid_configure(pady=5)

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
                               activebackground=menuColor, command=lambda: changeFrame(frame1))
        homeButton.grid(row=2, column=0, pady=5, sticky='nwe')
        accountButton = tk.Button(frame, image=accountIcon, background=menuColor, fg=fontColor,
                                  font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                                  activebackground=menuColor, command=lambda: changeFrame(frame2))
        accountButton.grid(row=3, column=0, pady=5, sticky='nwe')
        productButton = tk.Button(frame, image=productIcon, background=menuColor, fg=fontColor,
                                  font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                                  activebackground=menuColor, command=lambda: changeFrame(frame3))
        productButton.grid(row=4, column=0, pady=5, sticky='nwe')
        deliveryButton = tk.Button(frame, image=deliveryIcon, background=menuColor, fg=fontColor,
                                   font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                                   activebackground=menuColor, command=lambda: changeFrame(frame4))
        deliveryButton.grid(row=5, column=0, pady=5, sticky='nwe')
        orderButton = tk.Button(frame, image=orderIcon, background=menuColor, fg=fontColor,
                                font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                                activebackground=menuColor, command=lambda: changeFrame(frame5))
        orderButton.grid(row=6, column=0, pady=5, sticky='nwe')

        def logout():
            root.destroy()
            db.disconnect()
            Login()

        logoutButton = tk.Button(frame, image=logoutIcon, background=menuColor, fg=fontColor,
                                 font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                                 activebackground=menuColor,
                                 command=lambda: MessageBox("Czy na pewno chcesz się wylogować?", logoutButton,
                                                            logout))

        if user.role != "pracownik":
            employeesButton = tk.Button(frame, image=employeesIcon, background=menuColor, fg=fontColor,
                                        font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                                        activebackground=menuColor, command=lambda: changeFrame(frame6))
            employeesButton.grid(row=7, column=0, pady=5, sticky='nwe')
            logoutButton.grid(row=8, column=0, pady=5, sticky='nwe')
        else:
            logoutButton.grid(row=7, column=0, pady=5, sticky='nwe')

        frame.grid_propagate(False)


class MessageBox:
    def __init__(self, text, popButton, commandPassed):
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
        self.root.configure(background=bgColor, borderwidth=1,
                            relief=tk.RIDGE)
        self.root.geometry("400x125")
        self.root.resizable(False, False)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.protocol("WM_DELETE_WINDOW", lambda: close())
        ttk.Label(self.root, text=text, background=bgColor, font=("Roboto Light", 12)).grid(row=0, column=0)
        buttonsFrame = tk.Frame(self.root, background=bgColor)
        buttonsFrame.grid(row=1, column=0)
        tk.Button(buttonsFrame, text="Tak", width=10, background=buttonColor, fg="white",
                  command=lambda: command()).grid(row=0, column=0,
                                                  padx=15)
        tk.Button(buttonsFrame, text="Nie", width=10, background=buttonColor, fg="white",
                  command=lambda: close()).grid(row=0, column=1,
                                                padx=15)


class Boxes:
    def __init__(self, db):
        self.db = db

    def accountConfigureBox(self, id, column, popButton):
        def edit():
            if entry0.get() == entry1.get():
                self.db.set("users", column, entry0.get(), "user_id", id)
                close()

        def close():
            root.destroy()
            popButton.config(state="normal")

        popButton.config(state="disabled")

        bgColor = "white"
        root = tk.Tk()
        root.configure(background=bgColor, borderwidth=1,
                            relief=tk.RIDGE)
        root.geometry("400x400")
        root.protocol("WM_DELETE_WINDOW", lambda: close())

        ttk.Label(root, text="Podaj " + column, background=bgColor, font=("Roboto Light", 12)).grid(row=0, column=0)
        entry0 = ttk.Entry(root)
        entry0.grid(row=0, column=1)
        ttk.Label(root, text="Powtórz " + column, background=bgColor, font=("Roboto Light", 12)).grid(row=1, column=0)
        entry1 = ttk.Entry(root)
        entry1.grid(row=1, column=1)
        tk.Button(root, text="Zatwierdź", command=edit).grid(row=2, column=1)


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
    def __init__(self, db, name, id):
        objectToDisplay = ""
        if name == "products":
            objectToDisplay = Product(db, id)
        elif name == "users":
            objectToDisplay = User(db, id)
        elif name == "orders":
            objectToDisplay = Order(db, id)
        elif name == "carts":
            objectToDisplay = Cart(db, id)

        bgColor = "white"

        self.root = tk.Tk()
        self.root.configure(background=bgColor, borderwidth=1,
                            relief=tk.RIDGE)
        self.root.geometry("400x400")
        ttk.Label(self.root, text=objectToDisplay, background=bgColor, font=("Roboto Light", 12)).grid(row=0, column=0)

        self.root.resizable(False, False)


class AddBox:
    def __init__(self, popButton, db):
        def command():
            flag = True
            for entry in self.entries:
                if entry.get() == '':
                    entry.configure()
                    self.errorLabel.configure(text="Wypełnij wszystkie wymagane pola")
                    flag = False
            if flag:
                popButton.config(state="normal")
                db.insert("products", (self.entries[0].get(), self.entries[3].get(), self.entries[2].get(),
                                       self.entries[1].get(), self.entries[4].get(), self.entries[5].get(),
                                       self.entries[6].get()))
                self.root.destroy()

        def close():
            self.root.destroy()
            popButton.config(state="normal")

        bgColor = "white"
        buttonColor = "#0589CF"

        pyglet.font.add_file('Roboto-Light.ttf')
        popButton.config(state="disabled")
        self.root = tk.Tk()
        self.root.configure(background=bgColor, borderwidth=1,
                            relief=tk.RIDGE)
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        self.root.protocol("WM_DELETE_WINDOW", lambda: close())

        ttk.Label(self.root, text="Nazwa:", background=bgColor, font=("Roboto Light", 12)).grid(row=0, column=0,
                                                                                                sticky="w")
        entry0 = ttk.Entry(self.root)
        entry0.grid(row=0, column=1, sticky="w")

        ttk.Label(self.root, text="Producent:", background=bgColor, font=("Roboto Light", 12)).grid(row=1, column=0,
                                                                                                    sticky="w")
        entry1 = ttk.Entry(self.root)
        entry1.grid(row=1, column=1, sticky="w")

        ttk.Label(self.root, text="Cena zakupu:", background=bgColor, font=("Roboto Light", 12)).grid(row=2, column=0,
                                                                                                      sticky="w")
        entry2 = ttk.Entry(self.root)
        entry2.grid(row=2, column=1, sticky="w")

        ttk.Label(self.root, text="Cena sprzedaży:", background=bgColor, font=("Roboto Light", 12)).grid(row=3,
                                                                                                         column=0,
                                                                                                         sticky="w")
        entry3 = ttk.Entry(self.root)
        entry3.grid(row=3, column=1, sticky="w")

        ttk.Label(self.root, text="Kategoria:", background=bgColor, font=("Roboto Light", 12)).grid(row=4, column=0,
                                                                                                    sticky="w")
        entry4 = ttk.Entry(self.root)
        entry4.grid(row=4, column=1, sticky="w")

        ttk.Label(self.root, text="Jednostka:", background=bgColor, font=("Roboto Light", 12)).grid(row=5, column=0,
                                                                                                    sticky="w")
        entry5 = ttk.Combobox(self.root, values=db.getEnum("amount_type"))
        entry5.grid(row=5, column=1, sticky="w")

        ttk.Label(self.root, text="Podatek:", background=bgColor, font=("Roboto Light", 12)).grid(row=6, column=0,
                                                                                                  sticky="w")
        entry6 = ttk.Entry(self.root)
        entry6.grid(row=6, column=1, sticky="w")
        ttk.Label(self.root, text="%", background=bgColor, font=("Roboto Light", 12)).grid(row=6, column=2,
                                                                                           sticky="w")

        self.entries = (entry0, entry1, entry2, entry3, entry4, entry5, entry6)

        self.errorLabel = ttk.Label(self.root, text="", foreground="red", background=bgColor, font=("Roboto Light", 8))
        self.errorLabel.grid(row=7, column=0, sticky="w")

        tk.Button(self.root, text="Dodaj", width=10, background=buttonColor, fg="white",
                  command=lambda: command()).grid(row=7, column=0, sticky="w")


class WidgetList:
    def __init__(self, framePassed, db, table, columnNames, names, user, title, **kwargs):
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
        ttk.Label(framePassed, text=title, font=("Roboto Light", 25, "bold"), foreground="#0589CF").grid(row=0,
                                                                                                         column=0)
        frame = tk.Frame(framePassed, background=bgColor)
        frame.grid(row=1, column=0, sticky="nwse")

        addition = ""
        self.startingIndex = 0
        if table == "users":
            self.itemList = db.fetchEmployeesAdmin(user.id, columnNames)
        else:
            for key, item in kwargs.items():
                if key == "add":
                    addition = item
            self.itemList = db.fetchAll(table, columnNames, add=addition)
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
                              activebackground=bgColor, command=lambda: AddBox(addButton, db))
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
                               background=bgColor,
                               activebackground=bgColor)
            button.grid(row=1, column=names.index(name), sticky="w")
            sortButtons.append(button)
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
                widget[5].configure(command=lambda idToPass=widget[0].cget("text"): DisplayBox(db, table, idToPass))
                widget[6].configure()
                widget[7].configure()
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
                isBlocked = db.fetch(table, "user_id", self.itemList[self.startingIndex][0])[12]
                if isBlocked:
                    for label in columns:
                        label.configure(foreground="red")
            displayButton = tk.Button(frame, image=self.displayIcon, relief=tk.SUNKEN, borderwidth=0,
                                      background=bgColor,
                                      activebackground=bgColor,
                                      command=lambda idToPass=self.itemList[self.startingIndex][0]: DisplayBox(db, table, idToPass))
            displayButton.grid(row=row, column=5, sticky="nwse")
            columns.append(displayButton)
            editButton = tk.Button(frame, image=self.editIcon, relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                   activebackground=bgColor)
            editButton.grid(row=row, column=6, sticky="nwse")
            columns.append(editButton)
            idForButton = str(columns[0].cget("text"))
            deleteButton = tk.Button(frame, image=self.deleteIcon, relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                     activebackground=bgColor)
            deleteButton.configure(command=lambda idToPass=idForButton, thisButton=deleteButton: MessageBox(
                "Czy na pewno chcesz usunąć element o id = " + idToPass + "?", thisButton,
                lambda: db.delete(table, columnNames[0], idToPass)))
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
