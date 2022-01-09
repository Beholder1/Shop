import tkinter as tk
from tkinter import ttk
from main import Login
import pyglet
from user import User


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
                                 activebackground=menuColor,
                                 command=lambda: MessageBox("Czy na pewno chcesz się wylogować?", logoutButton,
                                                            logout))

        if user.role != "pracownik":
            employeesButton = tk.Button(frame, image=employeesIcon, background=menuColor, fg=fontColor,
                                        font=('Roboto Light', 13), relief=tk.SUNKEN, borderwidth=0,
                                        activebackground=menuColor, command=lambda: frame5.tkraise())
            employeesButton.grid(row=6, column=0, pady=5, sticky='nwe')
            logoutButton.grid(row=7, column=0, pady=5, sticky='nwe')
        else:
            logoutButton.grid(row=6, column=0, pady=5, sticky='nwe')

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
    def __init__(self, object):
        bgColor = "white"

        self.root = tk.Tk()
        self.root.configure(background=bgColor, borderwidth=1,
                            relief=tk.RIDGE)
        self.root.geometry("400x400")
        ttk.Label(self.root, text=object, background=bgColor, font=("Roboto Light", 12)).grid(row=0, column=0)

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
    def __init__(self, frame, db, table, columns, names, user, **kwargs):
        self.addIcon = tk.PhotoImage(file='icons/add.png')
        self.refreshIcon = tk.PhotoImage(file='icons/refresh.png')
        self.displayIcon = tk.PhotoImage(file='icons/display.png')
        self.editIcon = tk.PhotoImage(file='icons/edit.png')
        self.deleteIcon = tk.PhotoImage(file='icons/delete.png')

        bgColor = '#FFFFFF'

        addition = ""
        self.startingIndex = 0
        if table == "users":
            self.itemList = db.fetchEmployeesAdmin(user.id, columns)
        else:
            for key, item in kwargs.items():
                if key == "add":
                    addition = item
            self.itemList = db.fetchAll(table, columns, add=addition)
        self.itemList.sort()
        self.iterator = 25
        if len(self.itemList) < self.iterator:
            self.rangeEnd = len(self.itemList)
        else:
            self.rangeEnd = self.iterator + self.startingIndex
        self.labels = []
        self.choices = ("start", "backwards", "forwards", "end", "refresh")

        self.sortingMethod = 0
        self.reverse = False

        buttonsFrame = tk.Frame(frame)
        buttonsFrame.grid(row=0, column=0, sticky="w")
        addButton = tk.Button(buttonsFrame, image=self.addIcon, relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                              activebackground=bgColor, command=lambda: AddBox(addButton, db))
        addButton.grid(row=0, column=0, sticky="w")
        refreshButton = tk.Button(buttonsFrame, image=self.refreshIcon, relief=tk.SUNKEN, borderwidth=0,
                                  background=bgColor,
                                  activebackground=bgColor,
                                  command=lambda: configureWidgets(self.startingIndex, self.choices[4]))
        refreshButton.grid(row=0, column=1, sticky="w")
        for i in range(5):
            frame.grid_columnconfigure(i, weight=1)

        sortButtons = []
        button0 = tk.Button(frame, text=names[0], font=("Roboto Light", 12), relief=tk.SUNKEN, borderwidth=0,
                            background=bgColor,
                            activebackground=bgColor, command=lambda: sort(names[0]))
        button0.grid(row=1, column=0, sticky="w")
        sortButtons.append(button0)
        button1 = tk.Button(frame, text=names[1], font=("Roboto Light", 12), relief=tk.SUNKEN, borderwidth=0,
                            background=bgColor,
                            activebackground=bgColor, command=lambda: sort(names[1]))
        button1.grid(row=1, column=1, sticky="w")
        sortButtons.append(button1)
        button2 = tk.Button(frame, text=names[2], font=("Roboto Light", 12), relief=tk.SUNKEN, borderwidth=0,
                            background=bgColor,
                            activebackground=bgColor, command=lambda: sort(names[2]))
        button2.grid(row=1, column=2, sticky="w")
        sortButtons.append(button2)
        button3 = tk.Button(frame, text=names[3], font=("Roboto Light", 12), relief=tk.SUNKEN, borderwidth=0,
                            background=bgColor,
                            activebackground=bgColor, command=lambda: sort(names[3]))
        button3.grid(row=1, column=3, sticky="w")
        sortButtons.append(button3)
        button4 = tk.Button(frame, text=names[4], font=("Roboto Light", 12), relief=tk.SUNKEN, borderwidth=0,
                            background=bgColor,
                            activebackground=bgColor, command=lambda: sort(names[4]))
        button4.grid(row=1, column=4, sticky="w")
        sortButtons.append(button4)

        def sort(name):
            index = names.index(name)
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
            configureWidgets(self.startingIndex - self.iterator + 1, "")

        def configureWidgets(index, choice):
            if (index >= len(self.itemList)) and choice == self.choices[2]:
                index = 0
                self.rangeEnd = self.iterator
                self.startingIndex = 0
            if choice == self.choices[4]:
                self.itemList = db.fetchAll(table, columns)
                self.itemList.sort(key=lambda x: x[self.sortingMethod])
                index -= self.iterator - 1
            counter = index
            for widget in self.labels:
                for label in range(5):
                    widget[label].configure(text=self.itemList[counter][label])
                widget[5].configure()
                widget[6].configure()
                widget[7].configure()
                counter += 1
            if choice == self.choices[0]:
                self.rangeEnd = self.iterator
                self.startingIndex = 0
            elif choice == self.choices[1]:
                self.rangeEnd -= self.iterator
                self.startingIndex -= self.iterator
                if self.startingIndex < 0:
                    self.rangeEnd = len(self.itemList)
                    self.startingIndex = len(self.itemList) - self.iterator + len(self.itemList) % self.iterator
            elif choice == self.choices[2]:
                self.rangeEnd += self.iterator
                self.startingIndex += self.iterator
            elif choice == self.choices[3]:
                self.rangeEnd = len(self.itemList)
                self.startingIndex = index

        for self.startingIndex in range(self.rangeEnd):
            columns = []
            label0 = ttk.Label(frame, text=self.itemList[self.startingIndex][0])
            label0.grid(row=self.startingIndex % self.iterator + 2, column=0, sticky="nwse")
            columns.append(label0)
            label1 = ttk.Label(frame, text=self.itemList[self.startingIndex][1])
            label1.grid(row=self.startingIndex % self.iterator + 2, column=1, sticky="nwse")
            columns.append(label1)
            label2 = ttk.Label(frame, text=self.itemList[self.startingIndex][2])
            label2.grid(row=self.startingIndex % self.iterator + 2, column=2, sticky="nwse")
            columns.append(label2)
            label3 = ttk.Label(frame, text=self.itemList[self.startingIndex][3])
            label3.grid(row=self.startingIndex % self.iterator + 2, column=3, sticky="nwse")
            columns.append(label3)
            label4 = ttk.Label(frame, text=self.itemList[self.startingIndex][4])
            label4.grid(row=self.startingIndex % self.iterator + 2, column=4, sticky="nwse")
            columns.append(label4)
            if table == "users":
                isBlocked = db.fetch(table, "user_id", self.itemList[self.startingIndex][0])[12]
                if isBlocked:
                    for label in columns:
                        label.configure(foreground="red")
            displayButton = tk.Button(frame, image=self.displayIcon, relief=tk.SUNKEN, borderwidth=0,
                                      background=bgColor,
                                      activebackground=bgColor,
                                      command=lambda: DisplayBox(User(self.itemList[self.startingIndex][0], db)))
            displayButton.grid(row=self.startingIndex % self.iterator + 2, column=5, sticky="w")
            columns.append(displayButton)
            editButton = tk.Button(frame, image=self.editIcon, relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                   activebackground=bgColor)
            editButton.grid(row=self.startingIndex % self.iterator + 2, column=6, sticky="w")
            columns.append(editButton)
            deleteButton = tk.Button(frame, image=self.deleteIcon, relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                     activebackground=bgColor)
            deleteButton.grid(row=self.startingIndex % self.iterator + 2, column=7, sticky="w")
            columns.append(deleteButton)
            self.labels.append(columns)

        if len(self.itemList) > self.iterator:
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
                                        len(self.itemList) - self.iterator + len(self.itemList) % self.iterator,
                                        self.choices[3]))
            page4Button.grid(row=0, column=9, sticky="w")
