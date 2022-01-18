import tkinter as tk
from tkinter import ttk
#from widgets import AutocompleteCombobox
from datetime import datetime


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

class User:
    def __init__(self, db, id):
        self.db = db
        self.id = id
        [self.login,
         self.dept_id,
         self.password,
         self.role,
         self.email,
         self.phoneNumber,
         self.name,
         self.last_name,
         self.salary,
         self.pesel,
         self.creationDate,
         self.lastLogin,
         self.isBlocked,
         self.employerId] = [self.db.fetch("users", "*", "user_id", id)[i] for i in (1, 13, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14)]

    def accountConfigureBox(self, column, popButton):
        def edit():
            if entry0.get() == entry1.get():
                self.db.set("users", column, entry0.get(), "user_id", self.id)
                close()

        def close():
            root.destroy()
            popButton.config(state="normal")

        popButton.config(state="disabled")

        if column == "phone_number":
            text = "numer telefonu"
        elif column == "password":
            text = "hasło"
        else:
            text = column

        bgColor = "white"
        root = tk.Tk()
        root.configure(background=bgColor, borderwidth=1,
                            relief=tk.RIDGE)
        root.protocol("WM_DELETE_WINDOW", lambda: close())
        root.title("Zmień " + text)

        frame = tk.Frame(root, background=bgColor)
        frame.grid(row=0, column=0, pady=5, padx=5)
        ttk.Label(frame, text="Podaj " + text, background=bgColor, font=("Roboto Light", 12)).grid(row=0, column=0)
        entry0 = ttk.Entry(frame)
        entry0.grid(row=0, column=1)
        ttk.Label(frame, text="Powtórz " + text, background=bgColor, font=("Roboto Light", 12)).grid(row=1, column=0)
        entry1 = ttk.Entry(frame)
        entry1.grid(row=1, column=1)
        tk.Button(frame, text="Zatwierdź", command=edit).grid(row=2, column=1)

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
                                                                         createLogin(entryEmployeeName.get(),
                                                                                     entryEmployeeLastName.get()),
                                                                         entryEmployeePesel.get(), "pracownik",
                                                                         entryEmployeeEmail.get(),
                                                                         entryEmployeeName.get(),
                                                                         entryEmployeeLastName.get(),
                                                                         entryEmployeeSalary.get(),
                                                                         entryEmployeePesel.get(), datetime.now(),
                                                                         self.id))
        addEmployeeButton.grid(row=5, column=1)

    def __str__(self):
        return "Login: " + str(self.login) + "\n" + \
               "Imię: " + str(self.name) + "\n" + \
               "Nazwisko: " + str(self.last_name) + "\n" + \
               "Stanowisko: " + str(self.role) + "\n" + \
               "Email: " + str(self.email) + "\n" + \
               "Telefon: " + str(self.phoneNumber) + "\n" + \
               "Pensja: " + str(self.salary) + "\n" + \
               "Konto utworzone: " + str(self.creationDate)
