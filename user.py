import tkinter as tk
from tkinter import ttk
from widgets import MessageBox
from widgets import EditBox
from widgets import AddBox
from widgets import DisplayBox


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
        self.tableName = "users"
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
         self.employerId] = [self.db.fetch(self.tableName, "*", "user_id", id)[i] for i in (1, 13, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14)]

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

    def add(self, button):
        addDictionary = {
            "Imię": "first_name",
            "Nazwisko": "last_name",
            "Pesel": "pesel",
            "Pensja": "salary",
            "Email": "email",
            "Telefon": "phone_number",
        }
        AddBox(button, self.db, self.tableName, addDictionary)

    def delete(self, button):
        MessageBox("Czy na pewno chcesz usunąć element o id = " + str(self.id) + "?", button,
                   lambda: self.db.delete(self.tableName, "product_id", self.id), "Usuń")

    def edit(self, button):
        EditBox(self.db, button, self.__str__(), indexes=(1, 2, 3, 5, 6, 7))

    def display(self):
        DisplayBox(self.db, self.tableName, self.id, self.dept_id, self.__str__())


    def __str__(self):
        return "Id: " + str(self.id) + "\n" + \
               "Login: " + str(self.login) + "\n" + \
               "Imię: " + str(self.name) + "\n" + \
               "Nazwisko: " + str(self.last_name) + "\n" + \
               "Stanowisko: " + str(self.role) + "\n" + \
               "Email: " + str(self.email) + "\n" + \
               "Telefon: " + str(self.phoneNumber) + "\n" + \
               "Pensja: " + str(self.salary) + "\n" + \
               "Konto utworzone: " + str(self.creationDate)
