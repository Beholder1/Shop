from db import Database

class User:
    def __init__(self, login):
        db = Database()
        self.login = login
        self.id,\
        self.dept_id,\
        self.password,\
        self.role,\
        self.email,\
        self.name,\
        self.last_name,\
        self.salary,\
        self.pesel,\
        self.creationDate,\
        self.lastLogin,\
        self.employerId = [db.fetch(login)[i] for i in (0,1,3,4,5,6,7,8,9,10,11,12)]

    def __str__(self):
        return "Login: " + str(self.login) + "\n" +\
               "Imię: " + str(self.name) + "\n" +\
               "Nazwisko: " + str(self.last_name) + "\n" +\
               "Email: " + str(self.email) + "\n" +\
               "Pensja: " + str(self.salary) + "\n" +\
               "Konto utworzone: " + str(self.creationDate)