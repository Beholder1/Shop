from widgets import MessageBox
from widgets import EditBox
from widgets import AddBox
from widgets import DisplayBox
from tkinter import ttk
import pyglet
import tkinter as tk


class Product:
    def __init__(self, db, id, deptId):
        self.tableName = "products"
        self.deptId = deptId
        self.db = db
        self.id = id
        [self.name,
         self.price,
         self.purchasePrice,
         self.unit,
         self.taxRate,
         self.category,
         self.brand] = [
            self.db.fetchAll(self.tableName, ("name", "price", "purchase_price", "amount_type", "tax_rate", "category", "mark"),
                        add="INNER JOIN tax_rates USING (tax_rate_id) INNER JOIN categories USING (category_id) INNER JOIN marks USING (mark_id) WHERE product_id = " + str(
                            id))[0][
                i] for i in range(7)]
        self.amount = self.db.fetch("products_in_departments", "SUM (amount)", "dept_id", deptId, add="AND product_id = " + str(self.id))[0]
        if not self.amount:
            self.amount = 0
        self.margin = round((((self.price * (1-self.taxRate) - self.purchasePrice) / self.purchasePrice) * 100), 2)
        self.SoldInTotal = self.db.fetchAll("carts", ["SUM (amount)"], add="INNER JOIN products_in_carts USING(cart_id) INNER JOIN users USING(user_id) WHERE dept_id = " + str(deptId) + " AND product_id = " + str(self.id) + " AND order_status <> 'nieopłacono'")[0][0]
        if not self.SoldInTotal:
            self.SoldInTotal = 0
        self.totalIncome = round((self.price * (1-self.taxRate) - self.purchasePrice) * self.SoldInTotal, 2)

    def add(self, button):

        def command():
            flag1 = True
            for entry in entries:
                if entry.get() == '':
                    entry.configure()
                    errorLabel.configure(text="Wypełnij wszystkie wymagane pola")
                    flag1 = False
            if flag1:
                t = []
                for e in entries:
                    t.append(e.get())
                t[1] = self.db.fetchAll("marks", "mark_id", add="WHERE mark = '"+str(t[1])+"'")[0][0]
                t[2] = self.db.fetchAll("categories", "category_id", add="WHERE category = '"+str(t[2])+"'")[0][0]
                t[6] = self.db.fetchAll("tax_rates", "tax_rate_id", add="WHERE tax_rate = '"+str(t[6])+"'")[0][0]
                button.config(state="normal")
                self.db.insert(self.tableName, [t[0], t[4], t[3], t[5], t[6], t[2], t[1]])
                root.destroy()

        def close():
            root.destroy()
            button.config(state="normal")

        bgColor = "white"
        buttonColor = "#0589CF"


        pyglet.font.add_file('Roboto-Light.ttf')
        button.config(state="disabled")
        root = tk.Tk()
        root.configure(background=bgColor, borderwidth=1,
                       relief=tk.RIDGE)
        root.resizable(False, False)
        root.title("Dodaj")

        root.protocol("WM_DELETE_WINDOW", lambda: close())

        entries = []
        entry0 = ttk.Entry(root)
        entry0.grid(row=0, column=1, sticky="w")
        ttk.Label(root, text="Nazwa:", background=bgColor, font=("Roboto Light", 12)).grid(row=0,
                                                                                            column=0,
                                                                                            sticky="w")
        entries.append(entry0)

        l1 = []
        for i in self.db.fetchAll("marks", "mark"):
            l1.append(i[0])
        entry1 = ttk.Combobox(root, values=l1)
        entry1.grid(row=1, column=1, sticky="w")
        ttk.Label(root, text="Producent:", background=bgColor, font=("Roboto Light", 12)).grid(row=1,
                                                                                            column=0,
                                                                                            sticky="w")
        entries.append(entry1)

        l2 = []
        for i in self.db.fetchAll("categories", "category"):
            l2.append(i[0])
        entry2 = ttk.Combobox(root, values=l2)
        entry2.grid(row=2, column=1, sticky="w")
        ttk.Label(root, text="Kategoria:", background=bgColor, font=("Roboto Light", 12)).grid(row=2,
                                                                                            column=0,
                                                                                            sticky="w")
        entries.append(entry2)
        entry3 = ttk.Entry(root)
        entry3.grid(row=3, column=1, sticky="w")
        ttk.Label(root, text="Cena zakupu:", background=bgColor, font=("Roboto Light", 12)).grid(row=3,
                                                                                            column=0,
                                                                                            sticky="w")
        entries.append(entry3)

        entry4 = ttk.Entry(root)
        entry4.grid(row=4, column=1, sticky="w")
        ttk.Label(root, text="Cena sprzedaży:", background=bgColor, font=("Roboto Light", 12)).grid(row=4,
                                                                                            column=0,
                                                                                            sticky="w")
        entries.append(entry4)

        l4 = []
        for i in self.db.getEnum("amount_type"):
            l4.append(i)
        entry5 = ttk.Combobox(root, values=l4)
        entry5.grid(row=5, column=1, sticky="w")
        ttk.Label(root, text="Jednostka:", background=bgColor, font=("Roboto Light", 12)).grid(row=5,
                                                                                            column=0,
                                                                                            sticky="w")
        entries.append(entry5)

        l3 = []
        for i in self.db.fetchAll("tax_rates", "tax_rate"):
            l3.append(i[0])
        entry6 = ttk.Combobox(root, values=l3)
        entry6.grid(row=6, column=1, sticky="w")
        ttk.Label(root, text="Podatek:", background=bgColor, font=("Roboto Light", 12)).grid(row=6,
                                                                                            column=0,
                                                                                            sticky="w")
        entries.append(entry6)

        errorLabel = ttk.Label(root, text="", foreground="red", background=bgColor, font=("Roboto Light", 8))
        errorLabel.grid(row=7, column=0, sticky="w")

        tk.Button(root, text="Dodaj", width=10, background=buttonColor, fg="white",
                  command=lambda: command()).grid(row=8, column=0, sticky="w")

    def delete(self, button):
        MessageBox("Czy na pewno chcesz usunąć element o id = " + str(self.id) + "?", button,
                   lambda: self.db.delete(self.tableName, "product_id", self.id), "Usuń")

    def edit(self, button):
        def close():
            root.destroy()
            button.config(state="normal")

        root = tk.Tk()

        bgColor = "white"
        pyglet.font.add_file('Roboto-Light.ttf')
        button.config(state="disabled")
        root.configure(background=bgColor, borderwidth=1,
                       relief=tk.RIDGE)
        root.resizable(False, False)
        root.protocol("WM_DELETE_WINDOW", lambda: close())
        root.title("Edytuj")

        ttk.Label(root, text="Nazwa:", background=bgColor, font=("Roboto Light", 12)).grid(row=0, column=0)
        ttk.Label(root, text=self.name, background=bgColor, font=("Roboto Light", 12)).grid(row=0, column=1)
        entry0 = ttk.Entry(root)
        entry0.grid(row=0, column=2)
        button0 = tk.Button(root, width=10, background="#0589CF", fg="white", text="Edytuj")
        button0.grid(row=0, column=3)
        button0.configure(command=lambda: self.db.set(self.tableName, "name", entry0.get(), "product_id", self.id))

        l1 = []
        for i in self.db.fetchAll("marks", "mark"):
            l1.append(i[0])
        ttk.Label(root, text="Producent:", background=bgColor, font=("Roboto Light", 12)).grid(row=1, column=0)
        ttk.Label(root, text=self.brand, background=bgColor, font=("Roboto Light", 12)).grid(row=1, column=1)
        entry1 = ttk.Combobox(root, values=l1)
        entry1.grid(row=1, column=2)
        button1 = tk.Button(root, width=10, background="#0589CF", fg="white", text="Edytuj")
        button1.grid(row=1, column=3)
        button1.configure(command=lambda: self.db.set(self.tableName, "name", entry1.get(), "product_id", self.id))

        ttk.Label(root, text="Cena zakupu:", background=bgColor, font=("Roboto Light", 12)).grid(row=2, column=0)
        ttk.Label(root, text=self.purchasePrice, background=bgColor, font=("Roboto Light", 12)).grid(row=2, column=1)
        entry2 = ttk.Entry(root)
        entry2.grid(row=2, column=2)
        button2 = tk.Button(root, width=10, background="#0589CF", fg="white", text="Edytuj")
        button2.grid(row=2, column=3)
        button2.configure(command=lambda: self.db.set(self.tableName, "purchase_price", entry2.get(), "product_id", self.id))

        ttk.Label(root, text="Cena sprzedaży:", background=bgColor, font=("Roboto Light", 12)).grid(row=3, column=0)
        ttk.Label(root, text=self.price, background=bgColor, font=("Roboto Light", 12)).grid(row=3, column=1)
        entry3 = ttk.Entry(root)
        entry3.grid(row=3, column=2)
        button3 = tk.Button(root, width=10, background="#0589CF", fg="white", text="Edytuj")
        button3.grid(row=3, column=3)
        button3.configure(command=lambda: self.db.set(self.tableName, "price", entry3.get(), "product_id", self.id))

        l3 = []
        for i in self.db.fetchAll("tax_rates", "tax_rate"):
            l3.append(i[0])
        ttk.Label(root, text="Podatek:", background=bgColor, font=("Roboto Light", 12)).grid(row=4, column=0)
        ttk.Label(root, text=self.taxRate, background=bgColor, font=("Roboto Light", 12)).grid(row=4, column=1)
        entry4 = ttk.Combobox(root, values=l3)
        entry4.grid(row=4, column=2)
        button4 = tk.Button(root, width=10, background="#0589CF", fg="white", text="Edytuj")
        button4.grid(row=4, column=3)
        button4.configure(command=lambda: self.db.set(self.tableName, "name", entry4.get(), "product_id", self.id))

        l2 = []
        for i in self.db.fetchAll("categories", "category"):
            l2.append(i[0])
        ttk.Label(root, text="Kategoria:", background=bgColor, font=("Roboto Light", 12)).grid(row=5, column=0)
        ttk.Label(root, text=self.category, background=bgColor, font=("Roboto Light", 12)).grid(row=5, column=1)
        entry5 = ttk.Combobox(root, values=l2)
        entry5.grid(row=5, column=2)
        button5 = tk.Button(root, width=10, background="#0589CF", fg="white", text="Edytuj")
        button5.grid(row=5, column=3)
        button5.configure(command=lambda: self.db.set(self.tableName, "name", entry5.get(), "product_id", self.id))

        l4 = []
        for i in self.db.getEnum("amount_type"):
            l4.append(i)
        ttk.Label(root, text="Jednostka:", background=bgColor, font=("Roboto Light", 12)).grid(row=6, column=0)
        ttk.Label(root, text=self.unit, background=bgColor, font=("Roboto Light", 12)).grid(row=6, column=1)
        entry6 = ttk.Combobox(root, values=l4)
        entry6.grid(row=6, column=2)
        button6 = tk.Button(root, width=10, background="#0589CF", fg="white", text="Edytuj")
        button6.grid(row=6, column=3)
        button6.configure(command=lambda: self.db.set(self.tableName, "name", entry6.get(), "product_id", self.id))

        ttk.Label(root, text="Ilość:", background=bgColor, font=("Roboto Light", 12)).grid(row=7, column=0)
        ttk.Label(root, text=self.amount, background=bgColor, font=("Roboto Light", 12)).grid(row=7, column=1)
        entry7 = ttk.Entry(root)
        entry7.grid(row=7, column=2)
        button7 = tk.Button(root, width=10, background="#0589CF", fg="white", text="Edytuj")
        button7.grid(row=7, column=3)
        button7.configure(command=lambda: self.db.set(self.tableName, "name", entry7.get(), "product_id", self.id))

    def display(self):
        DisplayBox(self.db, self.tableName, self.id, self.deptId, self.__str__())

    def __str__(self):
        return "Id: " + str(self.id) + "\n" + \
               "Nazwa: " + str(self.name) + "\n" + \
               "Producent: " + str(self.brand) + "\n" + \
               "Cena zakupu: " + str(self.purchasePrice) + "zł\n" + \
               "Cena sprzedaży: " + str(self.price) + "zł\n" + \
               "Podatek: " + str(self.taxRate*100) + "%\n" + \
               "Kategoria: " + str(self.category) + "\n" + \
               "Ilość: " + str(self.amount) + " " + str(self.unit) + "\n" + \
               "Marża: " + str(self.margin) + "%\n" + \
               "Sprzedano łącznie: " + str(self.SoldInTotal) + " " + str(self.unit) + "\n" + \
               "Całkowity zysk: " + str(self.totalIncome) + "zł"

