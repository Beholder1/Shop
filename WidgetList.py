import tkinter as tk
from tkinter import ttk
from main import Login
import pyglet
from order import Order
from product import Product
from cart import Cart
from user import User
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import dateutil.relativedelta


class WidgetList:
    def __init__(self, framePassed, db, table, columnNames, names, user, title, **kwargs):

        def objectOperation(objectId, operation, button):
            itemObject = ""
            if table == "products":
                itemObject = Product(db, objectId, user.id)
            elif table == "orders":
                itemObject = Order(db, objectId)
            elif table == "users":
                itemObject = User(db, objectId)
            elif table == "carts":
                itemObject = Cart(db, objectId)

            if operation == "add" and table == "orders":
                itemObject.add(button, user.id)
            elif operation == "add" and table == "carts":
                itemObject.add(button, user.id)
            elif operation == "add" and table == "users":
                user.add(button)
            elif operation == "add":
                itemObject.add(button)
            elif operation == "display":
                itemObject.display()
            elif operation == "delete":
                itemObject.delete(button)
            elif operation == "edit":
                itemObject.edit(button)

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
        else:
            for key, item in kwargs.items():
                if key == "add":
                    addition = item
            self.itemList = db.fetchAll(table, columnNames, add=addition)
        for i in range(len(self.itemList)):
            k = list(self.itemList[i])
            for x in range(len(k)):
                if k[x] is None:
                    k[x]="-"
            self.itemList[i] = tuple(k)

        self.itemList.sort()
        self.iterator = 25

        self.rangeEnd = self.iterator + self.startingIndex
        self.labels = []

        self.sortingMethod = 0
        self.reverse = False

        if len(self.itemList) % self.iterator != 0:
            for i in range(self.iterator - len(self.itemList) % self.iterator):
                self.itemList

        buttonsFrame = tk.Frame(frame, background=bgColor)
        buttonsFrame.grid(row=0, column=0, sticky="w")
        addButton = tk.Button(buttonsFrame, image=self.addIcon, relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                              activebackground=bgColor, command=lambda: objectOperation(1, "add", addButton))
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
                if table == "users":
                    self.itemList = db.fetchEmployeesAdmin(user.id, columnNames)
                    self.itemList.sort(key=lambda x: x[self.sortingMethod])
                else:
                    self.itemList = db.fetchAll(table, columnNames, add=addition)
                    self.itemList.sort(key=lambda x: x[self.sortingMethod])
                index -= self.iterator - 1
            counter = index
            for widget in self.labels:
                try:
                    for label in range(5):
                        widget[label].configure(text=self.itemList[counter][label])
                    widget[5].configure(
                        command=lambda idToPass=widget[0].cget("text"): objectOperation(idToPass, "display", widget[5]),
                        state="normal", image=self.displayIcon)
                    widget[6].configure(
                        command=lambda idToPass=widget[0].cget("text"), thisButton=widget[6]: objectOperation(idToPass,
                                                                                                              "edit",
                                                                                                              thisButton),
                        state="normal", image=self.editIcon)
                    widget[7].configure(
                        command=lambda idToPass=widget[0].cget("text"), thisButton=widget[7]: objectOperation(idToPass,
                                                                                                              "delete",
                                                                                                              thisButton),
                        state="normal", image=self.deleteIcon)
                    counter += 1
                except IndexError:
                    for label in range(5):
                        widget[label].configure(text=" ")
                    widget[5].configure(state="disabled", image="")
                    widget[6].configure(state="disabled", image="")
                    widget[7].configure(state="disabled", image="")
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
                                      command=lambda idToPass=self.itemList[self.startingIndex][0]: objectOperation(
                                          idToPass, "display", displayButton))
            displayButton.grid(row=row, column=5, sticky="nwse")
            columns.append(displayButton)
            editButton = tk.Button(frame, image=self.editIcon, relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                   activebackground=bgColor)
            idForButton = str(columns[0].cget("text"))

            editButton.configure(
                command=lambda idToPass=idForButton, thisButton=editButton: objectOperation(idToPass, "edit",
                                                                                            thisButton))

            editButton.grid(row=row, column=6, sticky="nwse")
            columns.append(editButton)
            deleteButton = tk.Button(frame, image=self.deleteIcon, relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                     activebackground=bgColor)
            deleteButton.configure(
                command=lambda idToPass=idForButton, thisButton=deleteButton: objectOperation(idToPass, "delete",
                                                                                              thisButton))
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
            page1Button = tk.Button(pageButtonsFrame3, text="-", font=("Roboto Light", 10), relief=tk.SUNKEN,
                                    borderwidth=0, background=bgColor,
                                    activebackground=bgColor)
            page1Button.grid(row=0, column=2, sticky="w")
            page2Button = tk.Button(pageButtonsFrame3, text="-", font=("Roboto Light", 10), relief=tk.SUNKEN,
                                    borderwidth=0, background=bgColor,
                                    activebackground=bgColor)
            page2Button.grid(row=0, column=3, sticky="w")
            page3Button = tk.Button(pageButtonsFrame3, text="-", font=("Roboto Light", 10), relief=tk.SUNKEN,
                                    borderwidth=0, background=bgColor,
                                    activebackground=bgColor)
            page3Button.grid(row=0, column=4, sticky="w")
            ttk.Label(pageButtonsFrame3, text="-", font=("Roboto Light", 10)).grid(row=0,
                                                                                   column=5,
                                                                                   sticky="w",
                                                                                   pady=(1, 0))
            page5Button = tk.Button(pageButtonsFrame3, text="-", font=("Roboto Light", 10), relief=tk.SUNKEN,
                                    borderwidth=0, background=bgColor,
                                    activebackground=bgColor)
            page5Button.grid(row=0, column=6, sticky="w")
            page6Button = tk.Button(pageButtonsFrame3, text="-", font=("Roboto Light", 10), relief=tk.SUNKEN,
                                    borderwidth=0, background=bgColor,
                                    activebackground=bgColor)
            page6Button.grid(row=0, column=7, sticky="w")
            page7Button = tk.Button(pageButtonsFrame3, text="-", font=("Roboto Light", 10), relief=tk.SUNKEN,
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
