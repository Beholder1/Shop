from db import Database
import tkinter as tk
from tkinter import ttk
from datetime import datetime


class Order:
    def __init__(self, db, id):
        self.db = db
        self.id = id
        [self.orderStatus,
         self.orderDate,
         self.deliveryDate,
         self.user] = [self.db.fetchAll("orders", ("order_status", "order_date", "delivery_date", "login"),
                                        add="INNER JOIN users USING (user_id) WHERE order_id = " + str(id))[0][i] for i
                       in range(4)]

    def __str__(self):
        return "ID: " + str(self.id) + "\n" + \
               "Utworzone przez: " + str(self.user) + "\n" + \
               "Data zamówienia: " + str(self.orderDate) + "\n" + \
               "Status zamówienia: " + str(self.orderStatus) + "\n" + \
               "Data dostarczenia: " + str(self.deliveryDate)
