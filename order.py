from db import Database
import tkinter as tk
from tkinter import ttk
from widgets import AutocompleteCombobox
from datetime import datetime


class Order:
    def __init__(self):
        self.id,
        self.orderId,
        self.userId,
        self.orderStatus,
        self.paymentStatus,
        self.orderDate,
        self.deliveryDate,
        self.sum


def __str__(self):
    return "ID: " + str(self.login) + "\n" + \
           "Utworzone przez: " + str(self.userId) + "\n" + \
           "Data zamówienia: " + str(self.orderDate) + "\n" + \
           "Status zamówienia: " + str(self.orderStatus) + "\n" + \
           "Status płatności: " + str(self.paymentStatus) + "\n" + \
           "Data dostarczenia: " + str(self.deliveryDate) + "\n" + \
           "Do zapłaty: " + str(self.sum)
