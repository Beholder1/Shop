import tkinter as tk
from tkinter import ttk
from main import Login


class AutocompleteCombobox(ttk.Combobox):

    def set_completion_list(self, completion_list):
        """Use our completion list as our drop down selection menu, arrows move through menu."""
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
        else:  # set position to end so selection starts where textentry ended
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
        # now finally perform the auto completion
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


class SidebarMenu():
    def __init__(self, root, frame1, frame2, frame3, frame4, frame5, user, db):
        menuIcon = tk.PhotoImage(file='icons/menu.png')
        closeIcon = tk.PhotoImage(file='icons/close.png')
        homeIcon = tk.PhotoImage(file='icons/home.png')
        accountIcon = tk.PhotoImage(file='icons/account.png')
        productIcon = tk.PhotoImage(file='icons/product.png')
        locationIcon = tk.PhotoImage(file='icons/delivery.png')
        employeesIcon = tk.PhotoImage(file='icons/employees.png')
        logoutIcon = tk.PhotoImage(file='icons/logout.png')

        menuColor = '#0589CF'
        fontColor = 'black'
        min_w = 50
        max_w = 150
        self.cur_width = min_w
        self.expanded = False

        frame = tk.Frame(root, bg=menuColor, width=50, height=root.winfo_height())
        frame.grid(row=0, column=0, sticky='nws')

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
                locationButton.config(image=locationIcon, borderwidth=0)
                locationButton.grid_configure(pady=5)
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
        menuButton.grid(row=1, column=0, pady=5, padx=(10, 10), sticky='nw')
        homeButton = tk.Button(frame, image=homeIcon, background=menuColor, fg=fontColor,
                               font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                               activebackground=menuColor, command=lambda: frame1.tkraise())
        homeButton.grid(row=2, column=0, pady=5, sticky='nwe')
        accountButton = tk.Button(frame, image=accountIcon, background=menuColor, fg=fontColor,
                                  font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                                  activebackground=menuColor, command=lambda: frame2.tkraise())
        accountButton.grid(row=3, column=0, pady=5, sticky='nwe')
        productButton = tk.Button(frame, image=productIcon, background=menuColor, fg=fontColor,
                                  font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                                  activebackground=menuColor, command=lambda: frame3.tkraise())
        productButton.grid(row=4, column=0, pady=5, sticky='nwe')
        locationButton = tk.Button(frame, image=locationIcon, background=menuColor, fg=fontColor,
                                   font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                                   activebackground=menuColor, command=lambda: frame4.tkraise())
        locationButton.grid(row=5, column=0, pady=5, sticky='nwe')

        def logout():
            root.destroy()
            db.disconnect()
            Login()

        logoutButton = tk.Button(frame, image=logoutIcon, background=menuColor, fg=fontColor,
                                 font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                                 activebackground=menuColor, command=lambda: logout())

        if user.role != "pracownik":
            employeesButton = tk.Button(frame, image=employeesIcon, background=menuColor, fg=fontColor,
                                        font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                                        activebackground=menuColor, command=lambda: frame5.tkraise())
            employeesButton.grid(row=6, column=0, pady=5, sticky='nwe')
            logoutButton.grid(row=7, column=0, pady=5, sticky='nwe')
        else:
            logoutButton.grid(row=6, column=0, pady=5, sticky='nwe')

        frame.grid_propagate(False)


class WidgetList():
    def __init__(self, frame, db):
        self.addIcon = tk.PhotoImage(file='icons/add.png')
        self.refreshIcon = tk.PhotoImage(file='icons/refresh.png')
        self.displayIcon = tk.PhotoImage(file='icons/display.png')
        self.deleteIcon = tk.PhotoImage(file='icons/delete.png')

        bgColor = '#FFFFFF'

        self.startingIndex = 0
        self.productList = db.fetchAll("products")
        self.productList.sort()
        self.iterator = 25
        self.rangeEnd = self.iterator + self.startingIndex
        self.labels = []
        self.choices = ("start", "backwards", "forwards", "end", "refresh")

        buttonsFrame3 = tk.Frame(frame)
        buttonsFrame3.grid(row=0, column=0, sticky="w")
        addButton3 = tk.Button(buttonsFrame3, image=self.addIcon, relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                               activebackground=bgColor)
        addButton3.grid(row=0, column=0, sticky="w")
        refreshButton3 = tk.Button(buttonsFrame3, image=self.refreshIcon, relief=tk.SUNKEN, borderwidth=0,
                                   background=bgColor,
                                   activebackground=bgColor,
                                   command=lambda: configureWidgets(self.startingIndex, self.choices[4]))
        refreshButton3.grid(row=0, column=1, sticky="w")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)
        frame.grid_columnconfigure(3, weight=1)
        frame.grid_columnconfigure(4, weight=1)
        ttk.Label(frame, text="Id").grid(row=1, column=0, sticky="nwse")
        ttk.Label(frame, text="Nazwa").grid(row=1, column=1, sticky="nwse")
        ttk.Label(frame, text="Producent").grid(row=1, column=2, sticky="nwse")
        ttk.Label(frame, text="Cena zakupu").grid(row=1, column=3, sticky="nwse")
        ttk.Label(frame, text="Cena sprzedaży").grid(row=1, column=4, sticky="nwse")

        def configureWidgets(index, choice):
            if (index >= len(self.productList)) and choice == self.choices[2]:
                index = 0
                self.rangeEnd = self.iterator
                self.startingIndex = 0
            if (choice == self.choices[4]):
                self.productList = db.fetchAll("products")
                self.productList.sort()
                index -= self.iterator - 1
            counter = index
            for i in self.labels:
                i[0].configure(text=self.productList[counter][0])
                i[1].configure(text=self.productList[counter][1])
                i[2].configure(text=self.productList[counter][2])
                i[3].configure(text=self.productList[counter][3])
                i[4].configure(text=self.productList[counter][4])
                i[5].configure()
                i[6].configure()
                counter += 1
            if choice == self.choices[0]:
                self.rangeEnd = self.iterator
                self.startingIndex = 0
            elif choice == self.choices[1]:
                self.rangeEnd -= self.iterator
                self.startingIndex -= self.iterator
                if self.startingIndex < 0:
                    self.rangeEnd = len(self.productList)
                    self.startingIndex = len(self.productList) - self.iterator + len(self.productList) % self.iterator
            elif choice == self.choices[2]:
                self.rangeEnd += self.iterator
                self.startingIndex += self.iterator
            elif choice == self.choices[3]:
                self.rangeEnd = len(self.productList)
                self.startingIndex = index

        for self.startingIndex in range(self.rangeEnd):
            columns = []
            label1 = ttk.Label(frame, text=self.productList[self.startingIndex][0])
            label1.grid(row=self.startingIndex % self.iterator + 2, column=0, sticky="nwse")
            columns.append(label1)
            label2 = ttk.Label(frame, text=self.productList[self.startingIndex][1])
            label2.grid(row=self.startingIndex % self.iterator + 2, column=1, sticky="nwse")
            columns.append(label2)
            label3 = ttk.Label(frame, text=self.productList[self.startingIndex][2])
            label3.grid(row=self.startingIndex % self.iterator + 2, column=2, sticky="nwse")
            columns.append(label3)
            label4 = ttk.Label(frame, text=self.productList[self.startingIndex][3])
            label4.grid(row=self.startingIndex % self.iterator + 2, column=3, sticky="nwse")
            columns.append(label4)
            label5 = ttk.Label(frame, text=self.productList[self.startingIndex][4])
            label5.grid(row=self.startingIndex % self.iterator + 2, column=4, sticky="nwse")
            columns.append(label5)
            displayButton = tk.Button(frame, image=self.displayIcon, relief=tk.SUNKEN, borderwidth=0,
                                      background=bgColor,
                                      activebackground=bgColor)
            displayButton.grid(row=self.startingIndex % self.iterator + 2, column=5, sticky="w")
            columns.append(displayButton)
            deleteButton = tk.Button(frame, image=self.deleteIcon, relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                     activebackground=bgColor)
            deleteButton.grid(row=self.startingIndex % self.iterator + 2, column=6, sticky="w")
            columns.append(deleteButton)
            self.labels.append(columns)

        pageButtonsFrame3 = tk.Frame(frame)
        pageButtonsFrame3.grid(row=self.startingIndex % self.iterator + 3, column=0, sticky="w")
        previousPageButton = tk.Button(pageButtonsFrame3, text="|<", relief=tk.SUNKEN, borderwidth=0,
                                       background=bgColor,
                                       activebackground=bgColor,
                                       command=lambda: configureWidgets(0, self.choices[0]))
        previousPageButton.grid(row=0, column=0, sticky="w")
        previousPageButton = tk.Button(pageButtonsFrame3, text="<", relief=tk.SUNKEN, borderwidth=0,
                                       background=bgColor,
                                       activebackground=bgColor,
                                       command=lambda: configureWidgets(self.rangeEnd - 2 * self.iterator,
                                                                        self.choices[1]))
        previousPageButton.grid(row=0, column=1, sticky="w")
        page1Button = tk.Button(pageButtonsFrame3, text="1", relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                activebackground=bgColor)
        page1Button.grid(row=0, column=2, sticky="w")
        page2Button = tk.Button(pageButtonsFrame3, text="2", relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                activebackground=bgColor)
        page2Button.grid(row=0, column=3, sticky="w")
        page3Button = tk.Button(pageButtonsFrame3, text="3", relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                activebackground=bgColor)
        page3Button.grid(row=0, column=4, sticky="w")
        page4Button = tk.Button(pageButtonsFrame3, text="5", relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                activebackground=bgColor)
        page4Button.grid(row=0, column=5, sticky="w")
        page4Button = tk.Button(pageButtonsFrame3, text="6", relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                activebackground=bgColor)
        page4Button.grid(row=0, column=6, sticky="w")
        page4Button = tk.Button(pageButtonsFrame3, text="7", relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                activebackground=bgColor)
        page4Button.grid(row=0, column=7, sticky="w")
        page4Button = tk.Button(pageButtonsFrame3, text=">", relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                activebackground=bgColor,
                                command=lambda: configureWidgets(self.rangeEnd, self.choices[2]))
        page4Button.grid(row=0, column=8, sticky="w")
        page4Button = tk.Button(pageButtonsFrame3, text=">|", relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                activebackground=bgColor,
                                command=lambda: configureWidgets(
                                    len(self.productList) - self.iterator + len(self.productList) % self.iterator,
                                    self.choices[3]))
        page4Button.grid(row=0, column=9, sticky="w")
