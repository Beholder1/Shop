from db import Database


class Product:
    def __init__(self, db, id):
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

    def __str__(self):
        return "Nazwa: " + str(self.name) + "\n" + \
               "Producent: " + str(self.brand) + "\n" + \
               "Cena zakupu: " + str(self.purchasePrice) + "zł\n" + \
               "Cena sprzedaży: " + str(self.price) + "zł\n" + \
               "Podatek: " + str(self.taxRate) + "\n" + \
               "Kategoria: " + str(self.category) + "\n" + \
               "Jednostka: " + str(self.unit)
