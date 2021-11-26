import tkinter as tk
from tkinter import ttk

class MainProgram:
    def __init__(self):
        bgColor = 'white'
        menuColor = 'white'
        fontColor = 'black'

        root = tk.Tk()
        root.configure(background=bgColor)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.title("Tworzenie ogłoszeń")

        style = ttk.Style()
        style.configure('TLabel', background=bgColor, foreground=fontColor, font=('Verdana', 12))
        style.configure('TCheckbutton', background=bgColor)

        min_w = 50
        max_w = 150
        self.cur_width = min_w
        self.expanded = False

        def raise_frame(frame):
            frame.tkraise()

        def expand():
            rep = root.after(5, expand)
            if self.expanded == False:
                self.cur_width += 5
                frame.config(width=self.cur_width)
            if self.cur_width >= max_w:
                self.expanded = True
                root.after_cancel(rep)
                fill()

        def contract():
            self.cur_width -= 5
            rep = root.after(5, contract)
            frame.config(width=self.cur_width)
            if self.cur_width <= min_w:
                self.expanded = False
                root.after_cancel(rep)
                fill()

        def fill():
            if self.expanded:
                menuButton.config(image=closeIcon, command=contract)
                homeButton.config(image="", text="Strona główna", borderwidth=1)
                homeButton.grid_configure(pady=0)
                accountButton.config(image="", text="Konta", borderwidth=1)
                accountButton.grid_configure(pady=0)
                productButton.config(image="", text="Produkty", borderwidth=1)
                productButton.grid_configure(pady=0)
                locationButton.config(image="", text="Lokalizacje", borderwidth=1)
                locationButton.grid_configure(pady=0)
            else:
                menuButton.config(image=menuIcon, command=expand)
                homeButton.config(image=homeIcon, borderwidth=0)
                homeButton.grid_configure(pady=5)
                accountButton.config(image=homeIcon, borderwidth=0)
                accountButton.grid_configure(pady=5)
                productButton.config(image=homeIcon, borderwidth=0)
                productButton.grid_configure(pady=5)
                locationButton.config(image=homeIcon, borderwidth=0)
                locationButton.grid_configure(pady=5)

        homeIcon = tk.PhotoImage(file='icons/home.png')
        menuIcon = tk.PhotoImage(file='icons/menu.png')
        closeIcon = tk.PhotoImage(file='icons/close.png')
        root.update()
        frame = tk.Frame(root, bg=menuColor, width=50, height=root.winfo_height(), borderwidth=1, relief=tk.RIDGE)
        frame.grid(row=0, column=0, sticky='nws')

        menuButton = tk.Button(frame, image=menuIcon, background=menuColor, fg=fontColor, relief=tk.SUNKEN, borderwidth=0, activebackground='white', command=lambda: expand())
        menuButton.grid(row=1, column=0, pady=5, padx=(10, 10), sticky='nw')
        homeButton = tk.Button(frame, image=homeIcon, background=menuColor, fg=fontColor, font=('MS Reference Sans Serif', 13), relief=tk.SUNKEN, borderwidth=0, activebackground='white', command=lambda: raise_frame(f1))
        homeButton.grid(row=2, column=0, pady=5, sticky='nwe')
        accountButton = tk.Button(frame, image=homeIcon, background=menuColor, fg=fontColor, font=('MS Reference Sans Serif', 13), relief=tk.SUNKEN, borderwidth=0, activebackground='white', command=lambda: raise_frame(f2))
        accountButton.grid(row=3, column=0, pady=5, sticky='nwe')
        productButton = tk.Button(frame, image=homeIcon, background=menuColor, fg=fontColor, font=('MS Reference Sans Serif', 13), relief=tk.SUNKEN, borderwidth=0, activebackground='white', command=lambda: raise_frame(f3))
        productButton.grid(row=4, column=0, pady=5, sticky='nwe')
        locationButton = tk.Button(frame, image=homeIcon, background=menuColor, fg=fontColor, font=('MS Reference Sans Serif', 13), relief=tk.SUNKEN, borderwidth=0, activebackground='white', command=lambda: raise_frame(f4))
        locationButton.grid(row=5, column=0, pady=5, sticky='nwe')

        # frame.bind('<Enter>',lambda e: expand())
        # frame.bind('<Leave>',lambda e: contract())

        frame.grid_propagate(False)

        f2 = tk.Frame(root, bg=bgColor)
        f2.grid(row=0, column=1, sticky="nwse")
        ttk.Label(f2, text="2: ").grid(row=0, column=0)

        f3 = tk.Frame(root, bg=bgColor)
        f3.grid(row=0, column=1, sticky="nwse")
        ttk.Label(f3, text="3: ").grid(row=0, column=0)

        f4 = tk.Frame(root, bg=bgColor)
        f4.grid(row=0, column=1, sticky="nwse")
        ttk.Label(f4, text="4: ").grid(row=0, column=0)

        f1 = tk.Frame(root, bg=bgColor)
        f1.grid(row=0, column=1, sticky="nwse")
        ttk.Label(f1, text="1: ").grid(row=0, column=0)



