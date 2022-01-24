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

    def fetch(self, table, column0, column1, criterion, **kwargs):
        command = "SELECT " + column0 + " FROM " + table + " WHERE " + column1 + " = '" + str(criterion) + "'"
        for key, item in kwargs.items():
            if key == "add":
                command += " " + item
        self.cur.execute(command)
        data = self.cur.fetchone()
        return data

    def fetchAll(self, table, columns, **kwargs):
        command = "SELECT "
        if type(columns) == str:
            command += columns
        else:
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
                command += str(column) + ", '"
            else:
                command += str(column)
                command += "', '"
        command = command[:-3]
        command += ")"
        self.cur.execute(command)
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

    def set(self, table, column, value, criterionColumn, criterionValue, **kwargs):
        command = "UPDATE " + str(table) + " SET " + str(column) + " = '" + str(value) + "' WHERE " + str(
                criterionColumn) + " = '" + str(criterionValue) + "'"
        for key, item in kwargs.items():
            if key == "add":
                command += " " + item
        self.cur.execute(command)
        self.conn.commit()

    def delete(self, table, column, value):
        self.cur.execute(
            "DELETE FROM " + table + " WHERE " + column + " = '" + str(value) + "'")
        self.conn.commit()

    def insertProducts(self, list, userId):
        self.cur.execute("select add_order(ARRAY" + str(list) + ", " + str(userId) + ")")
        self.conn.commit()

    def insertCart(self, list, userId, payment, name, lastName, country, province, city, code, street, number):
        command = "select add_cart(ARRAY" + str(list) + ", " + str(userId) + ", '" + str(payment) + "', '" + str(
            name) + "', '" + str(lastName) + "', '" + str(country) + "', '" + str(province) + "', '" + str(
            city) + "', '" + str(code) + "', '" + str(street) + "', '" + str(number) + "')"
        print(command)
        self.cur.execute(command)

        self.conn.commit()

    def getLastId(self):
        self.cur.execute("select max(user_id) from users")
        return self.cur.fetchall()

    def chartData(self, productId, deptId, month, year):
        self.cur.execute(
            "SELECT SUM(amount) FROM carts INNER JOIN products_in_carts USING(cart_id) INNER JOIN users USING(user_id) WHERE product_id = " + str(
                productId) + " AND dept_id = " + str(deptId) + " AND EXTRACT(MONTH FROM purchase_date) = " + str(
                month) + " AND EXTRACT(YEAR FROM purchase_date) = " + str(year))
        return self.cur.fetchone()

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

    def addAmount(self, productId, deptId, amount):
        self.cur.execute("select add_amount(" + str(productId) + ", " + str(deptId) + ", " + str(amount) + ")")
        self.conn.commit()

    def createLogin(self):
        self.cur.execute("UPDATE users SET login = concat(login, (SELECT currval('users_user_id_seq'))) WHERE user_id = (SELECT currval('users_user_id_seq'))")
        self.conn.commit()

    def getReport(self, dept_id, dateStart, dateEnd):
        self.cur.execute(
            "SELECT login, name, SUM(amount), ROUND(SUM(amount*(price * (1-tax_rate) - purchase_price))::numeric, 2) FROM carts INNER JOIN users USING(user_id) INNER JOIN products_in_carts USING(cart_id) INNER JOIN products USING (product_id) INNER JOIN departments USING (dept_id) INNER JOIN locations USING (location_id) INNER JOIN tax_rates USING(tax_rate_id) WHERE purchase_date BETWEEN TO_DATE('" + str(
                dateStart) + "','MM/DD/YY') AND TO_DATE('" + str(dateEnd) + "','MM/DD/YY') AND dept_id = " + str(
                dept_id) + " AND order_status <> 'nieopłacono' GROUP BY ROLLUP(login, name) ORDER BY login, name")
        data = self.cur.fetchall()
        return data

    def getReport1(self, dept_id, dateStart, dateEnd):
        self.cur.execute(
            "SELECT order_id, name, ROUND(sum(amount*purchase_price)::numeric, 2) cena_zakupu FROM products INNER JOIN ordered_products USING(product_id) INNER JOIN orders USING(order_id) INNER JOIN users USING(user_id) WHERE order_date BETWEEN TO_DATE('" + str(dateStart) + "','MM/DD/YY') AND TO_DATE('" + str(dateEnd) + "','MM/DD/YY') AND dept_id = " + str(
                dept_id) + " AND order_status <> 'nieopłacono' GROUP BY order_id, ROLLUP(name) ORDER BY order_id, name")
        data = self.cur.fetchall()
        return data

    def getReport2(self, dept_id, dateStart, dateEnd):
        self.cur.execute(
            "SELECT cart_id, name, ROUND(sum(amount*purchase_price)::numeric, 2) cena_zakupu FROM products INNER JOIN products_in_carts USING(product_id) INNER JOIN carts USING(cart_id) INNER JOIN users USING(user_id) WHERE purchase_date BETWEEN TO_DATE('" + str(dateStart) + "','MM/DD/YY') AND TO_DATE('" + str(dateEnd) + "','MM/DD/YY') AND dept_id = " + str(
                dept_id) + " AND order_status <> 'nieopłacono' GROUP BY cart_id, ROLLUP(name) ORDER BY cart_id, name;")
        data = self.cur.fetchall()
        return data

    def tmp1(self):
        self.cur.execute("SELECT user_id, salary from users")
        salary = self.cur.fetchall()
        for s in salary:
            n = round(s[1], 2)
            self.cur.execute("UPDATE users SET salary = " + str(n) + " WHERE user_id = " + str(s[0]))
            self.conn.commit()

    def tmp2(self):
        self.cur.execute("SELECT order_id from orders WHERE order_id BETWEEN 1 and 1000")
        dupa = self.cur.fetchall()
        for dup in dupa:
            self.cur.execute("SELECT product_id from products")
            pro1 = self.cur.fetchall()
            k = random.randint(1, 5)
            for i in range(k):
                amount = random.randint(10, 100)
                product1 = random.choice(pro1)
                product = product1[0]
                pro1.remove(product1)
                self.cur.execute(
                    "INSERT INTO ordered_products values(" + str(dup[0]) + ", " + str(product) + ", " + str(
                        amount) + ")")
                self.conn.commit()

    def tmp3(self):
        self.cur.execute("SELECT cart_id from carts WHERE cart_id BETWEEN 1 and 1000")
        dupa = self.cur.fetchall()
        for dup in dupa:
            self.cur.execute("SELECT product_id from products")
            pro1 = self.cur.fetchall()
            k = random.randint(1, 5)
            for i in range(k):
                amount = random.randint(1, 15)
                product1 = random.choice(pro1)
                product = product1[0]
                pro1.remove(product1)
                self.cur.execute(
                    "INSERT INTO products_in_carts values(" + str(dup[0]) + ", " + str(product) + ", " + str(
                        amount) + ")")
                self.conn.commit()

    def disconnect(self):
        self.conn.close()
