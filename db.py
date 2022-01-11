import psycopg2
import random


class Database:
    def __init__(self):
        hostname = 'b28hao8o7ssiga5bdpcr-postgresql.services.clever-cloud.com'
        database = 'b28hao8o7ssiga5bdpcr'
        username = 'u57vrkize7lzaxiysrwo'
        pwd = 'Y9HUpF30wvSg7MaNWWY8'
        port_id = 5432
        self.conn = None
        self.cur = None

        self.conn = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id)
        self.cur = self.conn.cursor()

    def fetch(self, table, column, criterion):
        self.cur.execute("SELECT * FROM " + table + " WHERE " + column + " = '" + str(criterion) + "'")
        data = self.cur.fetchone()
        return data

    def fetchAll(self, table, columns, **kwargs):
        command = "SELECT "
        for column in columns:
            command += column
            command += ", "
        command = command[:-2]
        command += " FROM "
        command += table
        for key, item in kwargs.items():
            if key == "add":
                command += " " + item
        self.cur.execute(command)
        data = self.cur.fetchall()
        return data

    def fetchColumnAll(self, table, column):
        self.cur.execute("SELECT DISTINCT " + column + " FROM " + table)
        data = self.cur.fetchall()
        counter = 0
        for i in data:
            data[counter] = i[0]
            counter += 1
        return data

    def insert(self, table, data):
        command = "INSERT INTO " + table + " VALUES (default, '"
        for column in data:
            if column == "NULL":
                command = command[:-1]
                command += column + ", '"
            else:
                command += column
                command += "', '"
        command = command[:-3]
        command += ")"
        self.conn.commit()

    def insertUser(self, deptId, login, password, role, email, name, lastName, salary, pesel, createdOn, managerId):
        self.cur.execute("INSERT INTO users VALUES (default, " + str(
            deptId) + ", '" + login + "', '" + password + "', '" + role + "', '" + email + "', '" + name + "', '" + lastName + "', " + salary + ", '" + pesel + "', '" + str(
            createdOn) + "', NULL, " + str(managerId) + ")")
        self.conn.commit()

    def insertProduct(self, name, selling_price, purchase_price, brand, category, unit, tax_rate):
        self.cur.execute("INSERT INTO products VALUES (default, '" +
                         name + "', '" + selling_price + "', '" + purchase_price + "', '" + brand + "', '" + category + "', '" + unit + "', '" + tax_rate + "')")
        self.conn.commit()

    def getEnum(self, name):
        self.cur.execute("SELECT unnest(enum_range(NULL::" + name + "))")
        data = self.cur.fetchall()
        counter = 0
        for i in data:
            data[counter] = i[0]
            counter += 1
        return data

    def fetchEmployeesAdmin(self, id, columns):
        command = "SELECT "
        for column in columns:
            command += column
            command += ", "
        command = command[:-2]
        command += " FROM users where manager_id = " + str(
            id) + "or user_id in (select user_id from users where manager_id in (select user_id from users where manager_id = " + str(
            id) + "))"
        self.cur.execute(command)
        data = self.cur.fetchall()
        return data

    def set(self, table, column, value, criterionColumn, criterionValue):
        self.cur.execute(
            "UPDATE " + table + " SET " + column + " = '" + value + "' WHERE " + criterionColumn + " = '" + criterionValue + "'")
        self.conn.commit()

    def delete(self, table, column, value):
        self.cur.execute(
            "DELETE FROM " + table + " WHERE " + column + " = '" + value + "'")
        self.conn.commit()

    def tmp(self):
        self.cur.execute("SELECT user_id, dept_id from users where rank='menedżer'")
        menedzerowie = self.cur.fetchall()
        self.cur.execute("SELECT user_id, dept_id from users where rank='pracownik'")
        pracownicy = self.cur.fetchall()
        gowno = []
        for i in range(101):
            gowno.append([])
        for m in menedzerowie:
            gowno[m[1]].append(m[0])
        for i in range(101):
            if not gowno[i]:
                gowno[i] = [i]
        for p in pracownicy:
            menedzer = random.choice(gowno[p[1]])
            self.cur.execute("UPDATE users SET manager_id = " + str(menedzer) + " WHERE user_id = " + str(p[0]))
            self.conn.commit()

    def tmp1(self):
        self.cur.execute("SELECT user_id, salary from users")
        salary = self.cur.fetchall()
        for s in salary:
            n = round(s[1], 2)
            self.cur.execute("UPDATE users SET salary = " + str(n) + " WHERE user_id = " + str(s[0]))
            self.conn.commit()

    def disconnect(self):
        self.conn.close()
