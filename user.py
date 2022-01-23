from widgets import MessageBox
from widgets import EditBox
from widgets import AddBox
from widgets import DisplayBox
from tkinter import ttk
import pyglet
import tkinter as tk
from datetime import datetime


def createLogin(name, lastName, id):
    if len(name) > 3:
        login = name[:-(len(name) - 3)]
    else:
        login = name
    if len(lastName) > 3:
        login = login + lastName[:-(len(lastName) - 3)]
    else:
        login = login + lastName + str(id)
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
                button.config(state="normal")
                if self.role == "admin":
                    self.db.insert(self.tableName, [createLogin(t[0], t[1], self.db.getLastId()[0][0]+1), t[2], t[3], t[5], t[6], t[0], t[1], t[4], t[2], datetime.now(), datetime.now(), "false", self.dept_id, self.id])
                else:
                    self.db.insert(self.tableName,
                                   [createLogin(t[0], t[1], self.db.getLastId()[0][0] + 1), t[2], "pracownik", t[5], t[6],
                                    t[0], t[1], t[4], t[2], datetime.now(), datetime.now(), "false", self.dept_id,
                                    self.id])
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
        ttk.Label(root, text="Imię:", background=bgColor, font=("Roboto Light", 12)).grid(row=0,
                                                                                           column=0,
                                                                                           sticky="w")
        entries.append(entry0)

        entry1 = ttk.Entry(root)
        entry1.grid(row=1, column=1, sticky="w")
        ttk.Label(root, text="Nazwisko:", background=bgColor, font=("Roboto Light", 12)).grid(row=1,
                                                                                               column=0,
                                                                                               sticky="w")
        entries.append(entry1)

        entry2 = ttk.Entry(root)
        entry2.grid(row=2, column=1, sticky="w")
        ttk.Label(root, text="Pesel:", background=bgColor, font=("Roboto Light", 12)).grid(row=2,
                                                                                               column=0,
                                                                                               sticky="w")
        entries.append(entry2)
        add = 0
        if self.role == "admin":
            l4 = []
            for i in self.db.getEnum("rank")[1:]:
                l4.append(i)
            entry3 = ttk.Combobox(root, values=l4)
            entry3.grid(row=3, column=1, sticky="w")
            ttk.Label(root, text="Stanowisko:", background=bgColor, font=("Roboto Light", 12)).grid(row=3,
                                                                                                     column=0,
                                                                                                     sticky="w")
            entries.append(entry3)
            add=1
        else:
            entry3 = ""
            entries.append(entry3)

        entry4 = ttk.Entry(root)
        entry4.grid(row=4+add, column=1, sticky="w")
        ttk.Label(root, text="Pensja:", background=bgColor, font=("Roboto Light", 12)).grid(row=4+add,
                                                                                                    column=0,
                                                                                                    sticky="w")
        entries.append(entry4)

        entry5 = ttk.Entry(root)
        entry5.grid(row=5+add, column=1, sticky="w")
        ttk.Label(root, text="Email:", background=bgColor, font=("Roboto Light", 12)).grid(row=5+add,
                                                                                               column=0,
                                                                                               sticky="w")
        entries.append(entry5)


        entry6 = ttk.Entry(root)
        entry6.grid(row=6+add, column=1, sticky="w")
        ttk.Label(root, text="Telefon:", background=bgColor, font=("Roboto Light", 12)).grid(row=6+add,
                                                                                             column=0,
                                                                                             sticky="w")
        entries.append(entry6)

        errorLabel = ttk.Label(root, text="", foreground="red", background=bgColor, font=("Roboto Light", 8))
        errorLabel.grid(row=7+add, column=0, sticky="w")

        tk.Button(root, text="Dodaj", width=10, background=buttonColor, fg="white",
                  command=lambda: command()).grid(row=8+add, column=0, sticky="w")

    def delete(self, button):
        MessageBox("Czy na pewno chcesz usunąć element o id = " + str(self.id) + "?", button,
                   lambda: self.db.delete(self.tableName, "user_id", self.id), "Usuń")

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

        ttk.Label(root, text="Imię:").grid(row=0, column=0)
        entry0 = ttk.Entry(root)
        entry0.grid(row=0, column=1)
        tk.Button(root, text="Edytuj").grid(row=0, column=2)

        ttk.Label(root, text="Nazwisko:").grid(row=1, column=0)
        entry1 = ttk.Entry(root)
        entry1.grid(row=1, column=1)
        tk.Button(root, text="Edytuj").grid(row=1, column=2)

        ttk.Label(root, text="Pensja:").grid(row=2, column=0)
        entry2 = ttk.Entry(root)
        entry2.grid(row=2, column=1)
        tk.Button(root, text="Edytuj").grid(row=2, column=2)

        ttk.Label(root, text="Odblokuj/Zablokuj:").grid(row=3, column=0)
        entry3 = ttk.Entry(root)
        entry3.grid(row=3, column=1)
        tk.Button(root, text="Edytuj").grid(row=3, column=2)



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
