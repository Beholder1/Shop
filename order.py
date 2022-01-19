from db import Database
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from widgets import MessageBox
from widgets import EditBox
from widgets import AddOrdersBox
from widgets import DisplayBox


class Order:
    def __init__(self, db, id):
        self.tableName = "orders"
        self.db = db
        self.id = id
        [self.orderStatus,
         self.orderDate,
         self.deliveryDate,
         self.user] = [self.db.fetchAll(self.tableName, ("order_status", "order_date", "delivery_date", "login"),
                                        add="INNER JOIN users USING (user_id) WHERE order_id = " + str(id))[0][i] for i
                       in range(4)]
        self.products = self.db.fetchAll("products", ("name", "amount"),
                                         add="INNER JOIN ordered_products USING(product_id) WHERE order_id = " + str(self.id))

    def add(self, button, userId):
        AddOrdersBox(self.db, button, self.tableName, userId)

    def delete(self, button):
        MessageBox("Czy na pewno chcesz usunąć element o id = " + str(self.id) + "?", button, lambda: self.db.delete(self.tableName, "order_id", self.id), "Usuń")

    def edit(self, button):
        EditBox(self.db, button, self.__str__(), indexes=3, combos=0)

    def display(self):
        DisplayBox(self.db, self.tableName, self.id, self.user, self.__str__())

    def __str__(self):
        string = "ID: " + str(self.id) + "\n" + \
                 "Utworzone przez: " + str(self.user) + "\n" + \
                 "Data zamówienia: " + str(self.orderDate) + "\n" + \
                 "Status zamówienia: " + str(self.orderStatus) + "\n" + \
                 "Data dostarczenia: " + str(self.deliveryDate) + "\n" + \
                 "\nZawartość zamówienia"
        counter = 1
        for p in self.products:
            string += "\nProdukt " + str(counter) + ": " + str(p[0]) + " x " + str(p[1])
            counter += 1
        return string
