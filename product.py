from db import Database


class Product:
    def __init__(self, name, brand):
        db = Database()
        self.name = name
        self.brand = brand
        [self.id,
         self.price,
         self.category,
         self.unit] = [db.fetch("products", "name", name)[i] for i in (0, 1, 3, 4)]

    def __str__(self):
        return "Nazwa: " + str(self.name) + "\n" + \
               "Producent: " + str(self.brand) + "\n" + \
               "Cena: " + str(self.price) + "zł\n" + \
               "Kategoria: " + str(self.category) + "\n" + \
               "Jednostka: " + str(self.unit)
