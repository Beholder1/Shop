from db import Database


class Product:
    def __init__(self, db, id, deptId):
        self.id = id
        [self.name,
         self.price,
         self.purchasePrice,
         self.unit,
         self.taxRate,
         self.category,
         self.brand] = [
            db.fetchAll("products", ("name", "price", "purchase_price", "amount_type", "tax_rate", "category", "mark"),
                        add="INNER JOIN tax_rates USING (tax_rate_id) INNER JOIN categories USING (category_id) INNER JOIN marks USING (mark_id) WHERE product_id = " + str(
                            id))[0][
                i] for i in range(7)]
        self.amount = db.fetch("products_in_departments", "SUM (amount)", "dept_id", deptId, add="AND product_id = " + str(self.id))[0]
        if not self.amount:
            self.amount = 0
        self.margin = round((((self.price * (1-self.taxRate) - self.purchasePrice) / self.purchasePrice) * 100), 2)
        self.SoldInTotal = db.fetchAll("carts", ["SUM (amount)"], add="INNER JOIN products_in_carts USING(cart_id) INNER JOIN users USING(user_id) WHERE dept_id = " + str(deptId) + " AND product_id = " + str(self.id) + " AND order_status <> 'nieopłacono'")[0][0]
        if not self.SoldInTotal:
            self.SoldInTotal = 0
        self.totalIncome = round((self.price * (1-self.taxRate) - self.purchasePrice) * self.SoldInTotal, 2)

    def __str__(self):
        return "Id: " + str(self.id) + "\n" + \
               "Nazwa: " + str(self.name) + "\n" + \
               "Producent: " + str(self.brand) + "\n" + \
               "Cena zakupu: " + str(self.purchasePrice) + "zł\n" + \
               "Cena sprzedaży: " + str(self.price) + "zł\n" + \
               "Podatek: " + str(self.taxRate*100) + "%\n" + \
               "Kategoria: " + str(self.category) + "\n" + \
               "Ilość: " + str(self.amount) + " " + str(self.unit) + "\n" + \
               "Marża: " + str(self.margin) + "%\n" + \
               "Sprzedano łącznie: " + str(self.SoldInTotal) + " " + str(self.unit) + "\n" + \
               "Całkowity zysk: " + str(self.totalIncome) + "zł"

