import psycopg2

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
        self.cur.execute("SELECT * FROM " + table + " WHERE " + column + " = '" + criterion + "'")
        data = self.cur.fetchone()
        return data

    def fetchColumnAll(self, table, column):
        self.cur.execute("SELECT " + column + " FROM " + table)
        data = self.cur.fetchall()
        counter=0
        for i in data:
            data[counter] = i[0]
            counter+=1
        return data

    def insertUser(self, deptId, login, password, role, email, name, lastName, salary, pesel, createdOn, managerId):
        self.cur.execute("INSERT INTO users VALUES (default, " + str(deptId) + ", '" + login + "', '" + password + "', '" + role + "', '" + email + "', '" + name + "', '" + lastName + "', " + salary + ", '" + pesel + "', '" + str(createdOn) + "', NULL, " + str(managerId) + ")")
        self.conn.commit()
        # (user_id, dept_id, login, password, role, email, name, last_name, salary, pesel, created_on, last_login, manager_id)

    def insertProduct(self, deptId, login, password, role, email, name, lastName, salary, pesel, createdOn, managerId):
        self.cur.execute("INSERT INTO users VALUES (default, " + str(deptId) + ", '" + login + "', '" + password + "', '" + role + "', '" + email + "', '" + name + "', '" + lastName + "', " + salary + ", '" + pesel + "', '" + str(createdOn) + "', NULL, " + str(managerId) + ")")
        self.conn.commit()