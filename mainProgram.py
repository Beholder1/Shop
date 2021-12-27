import tkinter as tk
from tkinter import ttk
from user import User
from product import Product
from widgets import AutocompleteCombobox, SidebarMenu
import pyglet


class MainProgram:
    def __init__(self, db, login):
        self.db = db
        self.login = login
        user = User(self.login, self.db)

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

        addIcon = tk.PhotoImage(file='icons/add.png')
        refreshIcon = tk.PhotoImage(file='icons/refresh.png')
        displayIcon = tk.PhotoImage(file='icons/display.png')
        deleteIcon = tk.PhotoImage(file='icons/delete.png')

        # Konto
        frame2 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame2.grid(row=0, column=1, sticky="nwse")
        ttk.Label(frame2, text=user.__str__()).grid(row=0, column=0, sticky="w")

        # Produkty
        frame3 = tk.Frame(root, height=root.winfo_height(), width=root.winfo_width(), bg=bgColor, borderwidth=1,
                          relief=tk.RIDGE)
        frame3.grid(row=0, column=1, sticky="nwse")
        frame3.grid_propagate(False)

        def listOfProducts(startingIndex):
            buttonsFrame3 = tk.Frame(frame3)
            buttonsFrame3.grid(row=0, column=0, sticky="w")
            addButton3 = tk.Button(buttonsFrame3, image=addIcon, relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                   activebackground=bgColor)
            addButton3.grid(row=0, column=0, sticky="w")
            refreshButton3 = tk.Button(buttonsFrame3, image=refreshIcon, relief=tk.SUNKEN, borderwidth=0,
                                       background=bgColor,
                                       activebackground=bgColor, command=lambda: listOfProducts())
            refreshButton3.grid(row=0, column=1, sticky="w")
            frame3.grid_columnconfigure(0, weight=1)
            frame3.grid_columnconfigure(1, weight=1)
            frame3.grid_columnconfigure(2, weight=1)
            frame3.grid_columnconfigure(3, weight=1)
            frame3.grid_columnconfigure(4, weight=1)
            ttk.Label(frame3, text="Id").grid(row=1, column=0, sticky="nwse")
            ttk.Label(frame3, text="Nazwa").grid(row=1, column=1, sticky="nwse")
            ttk.Label(frame3, text="Producent").grid(row=1, column=2, sticky="nwse")
            ttk.Label(frame3, text="Cena zakupu").grid(row=1, column=3, sticky="nwse")
            ttk.Label(frame3, text="Cena sprzedaży").grid(row=1, column=4, sticky="nwse")
            productList = db.fetchAll("products")
            productList.sort()
            iterator = 25
            rangeEnd = iterator + startingIndex
            for startingIndex in range(rangeEnd):
                ttk.Label(frame3, text=productList[startingIndex][0]).grid(row=startingIndex % iterator + 2, column=0,
                                                                           sticky="nwse")
                ttk.Label(frame3, text=productList[startingIndex][1]).grid(row=startingIndex % iterator + 2, column=1,
                                                                           sticky="nwse")
                ttk.Label(frame3, text=productList[startingIndex][2]).grid(row=startingIndex % iterator + 2, column=2,
                                                                           sticky="nwse")
                ttk.Label(frame3, text=productList[startingIndex][3]).grid(row=startingIndex % iterator + 2, column=3,
                                                                           sticky="nwse")
                ttk.Label(frame3, text=productList[startingIndex][4]).grid(row=startingIndex % iterator + 2, column=4,
                                                                           sticky="nwse")
                displayButton = tk.Button(frame3, image=displayIcon, relief=tk.SUNKEN, borderwidth=0,
                                          background=bgColor,
                                          activebackground=bgColor)
                displayButton.grid(row=startingIndex % iterator + 2, column=5, sticky="w")
                deleteButton = tk.Button(frame3, image=deleteIcon, relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                         activebackground=bgColor)
                deleteButton.grid(row=startingIndex % iterator + 2, column=6, sticky="w")

            pageButtonsFrame3 = tk.Frame(frame3)
            pageButtonsFrame3.grid(row=startingIndex % iterator + 3, column=0, sticky="w")
            previousPageButton = tk.Button(pageButtonsFrame3, text="|<", relief=tk.SUNKEN, borderwidth=0,
                                           background=bgColor,
                                           activebackground=bgColor,
                                           command=lambda: listOfProducts(0))
            previousPageButton.grid(row=0, column=0, sticky="w")
            previousPageButton = tk.Button(pageButtonsFrame3, text="<", relief=tk.SUNKEN, borderwidth=0,
                                           background=bgColor,
                                           activebackground=bgColor,
                                           command=lambda: listOfProducts(rangeEnd - 2 * iterator))
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
                                    activebackground=bgColor, command=lambda: listOfProducts(rangeEnd))
            page4Button.grid(row=0, column=8, sticky="w")
            page4Button = tk.Button(pageButtonsFrame3, text=">|", relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                    activebackground=bgColor, command=lambda: listOfProducts(rangeEnd))
            page4Button.grid(row=0, column=8, sticky="w")

        listOfProducts(0)

        # Dostawy
        frame4 = tk.Frame(root, height=root.winfo_height(), width=root.winfo_width(), bg=bgColor, borderwidth=1,
                          relief=tk.RIDGE)
        frame4.grid(row=0, column=1, sticky="nwse")
        frame4.grid_propagate(False)
        buttonsFrame4 = tk.Frame(frame4)
        buttonsFrame4.grid(row=0, column=0, sticky="w")
        addButton = tk.Button(buttonsFrame4, image=addIcon, relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                              activebackground=bgColor)
        addButton.grid(row=0, column=0, sticky="w")
        refreshButton = tk.Button(buttonsFrame4, image=refreshIcon, relief=tk.SUNKEN, borderwidth=0, background=bgColor,
                                  activebackground=bgColor)
        refreshButton.grid(row=0, column=1, sticky="w")
        frame4.grid_columnconfigure(0, weight=1)
        frame4.grid_columnconfigure(1, weight=1)
        frame4.grid_columnconfigure(2, weight=1)
        frame4.grid_columnconfigure(3, weight=1)
        frame4.grid_columnconfigure(4, weight=1)
        ttk.Label(frame4, text="Id").grid(row=1, column=0, sticky="nwse")
        ttk.Label(frame4, text="Data zamówienia").grid(row=1, column=1, sticky="nwse")
        ttk.Label(frame4, text="Status").grid(row=1, column=2, sticky="nwse")
        ttk.Label(frame4, text="Złożone przez").grid(row=1, column=3, sticky="nwse")
        ttk.Label(frame4, text="Suma").grid(row=1, column=4, sticky="nwse")
        # orderList=db.fetchAll("orders")
        # for i in range(10):
        #     ttk.Label(frame4, text=orderList[i][0]).grid(row=i+1,column=0, sticky="nwse")
        #     ttk.Label(frame4, text=orderList[i][4]).grid(row=i+1,column=1, sticky="nwse")
        #     ttk.Label(frame4, text=orderList[i][2]).grid(row=i+1,column=2, sticky="nwse")
        #     ttk.Label(frame4, text=orderList[i][1]).grid(row=i+1,column=3, sticky="nwse")
        #     ttk.Label(frame4, text=orderList[i][6]).grid(row=i+1,column=4, sticky="nwse")
        #     displayButton=tk.Button(frame4, image=displayIcon, relief=tk.SUNKEN, borderwidth=0, background=bgColor, activebackground=bgColor)
        #     displayButton.grid(row=i+1, column=5, sticky="w")
        #     deleteButton = tk.Button(frame4, image=deleteIcon, relief=tk.SUNKEN, borderwidth=0, background=bgColor, activebackground=bgColor)
        #     deleteButton.grid(row=i+1, column=6, sticky="w")

        # Pracownicy
        frame5 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame5.grid(row=0, column=1, sticky="nwse")
        frame5a = tk.Frame(frame5, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame5a.grid(row=0, column=0, sticky="nwse")
        user.showUser(frame5a, self.show)

        frame5b = tk.Frame(frame5, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame5b.grid(row=0, column=1, sticky="nwse")
        user.addUser(frame5b)

        frame1 = tk.Frame(root, bg=bgColor, borderwidth=1, relief=tk.RIDGE)
        frame1.grid(row=0, column=1, sticky="nwse")

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
