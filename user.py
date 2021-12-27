import tkinter as tk
from tkinter import ttk
from widgets import AutocompleteCombobox
from datetime import datetime


class User:
    def __init__(self, login, db):
        self.db = db
        self.login = login
        [self.id,
         self.dept_id,
         self.password,
         self.role,
         self.email,
         self.name,
         self.last_name,
         self.salary,
         self.pesel,
         self.creationDate,
         self.lastLogin,
         self.employerId] = [self.db.fetch("users", "login", login)[i] for i in (0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)]

    def showUser(self, frame, show):
        ttk.Label(frame, text="Pracownik: ").grid(row=0, column=0, sticky="w")
        comboEmployees = AutocompleteCombobox(frame)
        comboEmployees.set_completion_list(self.db.fetchColumnAll("users", "name"))
        comboEmployees.grid(row=0, column=1, sticky="w")
        comboEmployees.focus_set()
        showEmployeeButton = tk.Button(frame, text="Pokaż",
                                       command=lambda: show(frame, 1, 0, User(
                                           self.db.fetch("users", "name", comboEmployees.get())[2])))
        showEmployeeButton.grid(row=0, column=2)

    def addUser(self, frame):
        ttk.Label(frame, text="Imię: ").grid(row=0, column=0, sticky="w")
        entryEmployeeName = ttk.Entry(frame)
        entryEmployeeName.grid(row=0, column=1, sticky="w")

        ttk.Label(frame, text="Nazwisko: ").grid(row=1, column=0, sticky="w")
        entryEmployeeLastName = ttk.Entry(frame)
        entryEmployeeLastName.grid(row=1, column=1, sticky="w")

        ttk.Label(frame, text="PESEL: ").grid(row=2, column=0, sticky="w")
        entryEmployeePesel = ttk.Entry(frame)
        entryEmployeePesel.grid(row=2, column=1, sticky="w")

        ttk.Label(frame, text="Email: ").grid(row=3, column=0, sticky="w")
        entryEmployeeEmail = ttk.Entry(frame)
        entryEmployeeEmail.grid(row=3, column=1, sticky="w")

        ttk.Label(frame, text="Pensja: ").grid(row=4, column=0, sticky="w")
        entryEmployeeSalary = ttk.Entry(frame)
        entryEmployeeSalary.grid(row=4, column=1, sticky="w")

        addEmployeeButton = tk.Button(frame, text="Dodaj",
                                      command=lambda: self.db.insertUser(self.dept_id,
                                                                         self.createLogin(entryEmployeeName.get(),
                                                                                          entryEmployeeLastName.get()),
                                                                         entryEmployeePesel.get(), "pracownik",
                                                                         entryEmployeeEmail.get(),
                                                                         entryEmployeeName.get(),
                                                                         entryEmployeeLastName.get(),
                                                                         entryEmployeeSalary.get(),
                                                                         entryEmployeePesel.get(), datetime.now(),
                                                                         self.id))
        addEmployeeButton.grid(row=5, column=1)

    def createLogin(self, name, lastName):
        if len(name) > 3:
            login = name[:-(len(name) - 3)]
        else:
            login = name
        if len(lastName) > 3:
            login = login + lastName[:-(len(lastName) - 3)]
        else:
            login = login + lastName
        return login

    def __str__(self):
        return "Login: " + str(self.login) + "\n" + \
               "Imię: " + str(self.name) + "\n" + \
               "Nazwisko: " + str(self.last_name) + "\n" + \
               "Email: " + str(self.email) + "\n" + \
               "Pensja: " + str(self.salary) + "\n" + \
               "Konto utworzone: " + str(self.creationDate)
