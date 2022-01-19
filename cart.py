from widgets import MessageBox
from widgets import EditBox
from widgets import AddOrdersBox
from widgets import DisplayBox


class Cart:
    def __init__(self, db, id):
        self.tableName = "carts"
        self.db = db
        self.id = id
        [self.date,
         self.paymentMethod,
         self.status,
         self.user,
         self.client] = [self.db.fetchAll(self.tableName, ("purchase_date", "payment_method", "order_status", "login", "concat(clients.first_name, ' ', clients.last_name)"),
                                        add="INNER JOIN users USING (user_id) INNER JOIN clients USING(client_id) WHERE cart_id = " + str(id))[0][i] for i
                       in range(5)]
        self.products = self.db.fetchAll("products", ("name", "amount"),
                                         add="INNER JOIN products_in_carts USING(product_id) WHERE cart_id = " + str(
                                             self.id))

    def add(self, button):
        AddOrdersBox(button, self.tableName)

    def delete(self, button):
        MessageBox("Czy na pewno chcesz usunąć element o id = " + str(self.id) + "?", button, lambda: self.db.delete(self.tableName, "cart_id", self.id), "Usuń")

    def edit(self, button):
        EditBox(self.db, button, self.__str__(), indexes=4, combos=0)

    def display(self):
        DisplayBox(self.db, self.tableName, self.id, self.user, self.__str__())

    def __str__(self):
        string = "ID: " + str(self.id) + "\n" + \
                 "Utworzone przez: " + str(self.user) + "\n" + \
                 "Klient: " + str(self.client) + "\n" + \
                 "Data zamówienia: " + str(self.date) + "\n" + \
                 "Status zamówienia: " + str(self.status) + "\n" + \
                 "Metoda płatności: " + str(self.paymentMethod) + "\n" + \
                 "\nZawartość zamówienia"

        counter = 1
        for p in self.products:
            string += "\nProdukt " + str(counter) + ": " + str(p[0]) + " x " + str(p[1])
            counter += 1
        return string
