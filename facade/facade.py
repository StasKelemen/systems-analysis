"""
Provide a unified interface to a set of interfaces in a subsystem.
Facade defines a higher-level interface that makes the subsystem easier
to use.
"""
import pymysql.cursors

class Thing:

    def __init__(self, all):
        self.name = all['name']
        self.brand = all['brand']
        self.price = all['price']
        self.number = all['number']
        self.delivery = all['delivery']

class Facade:
    """
    Know which subsystem classes are responsible for a request.
    Delegate client requests to appropriate subsystem objects.
    """

    def __init__(self, thing, change_price, change_number, change_delivery):
        self.thing = thing
        self.change_price = change_price
        self.change_number = change_number
        self.change_delivery = change_delivery
        self._subsystem_1 = Subsystem1(self.thing)
        self._subsystem_2 = Subsystem2(self.thing)

    def operation(self):
        self._subsystem_1.changeprice(self.change_price)
        self._subsystem_2.changenum(self.change_number)
        self._subsystem_2.changedelivery(self.change_delivery)
        print(f"({self._subsystem_1.fullname()}, {self.thing.price}, {self.thing.number}, {self.thing.delivery})")


class Subsystem1:
    """
    Implement subsystem functionality.
    Handle work assigned by the Facade object.
    Have no knowledge of the facade; that is, they keep no references to
    it.
    """
    def __init__(self, thing):
        self.thing = thing

    def fullname(self):
        return self.thing.name + " " + self.thing.brand

    def changeprice(self, price):
        self.thing.price = price


class Subsystem2:
    """
    Implement subsystem functionality.
    Handle work assigned by the Facade object.
    Have no knowledge of the facade; that is, they keep no references to
    it.
    """
    def __init__(self, thing):
        self.thing = thing

    def changenum(self, num):
        self.thing.number = num

    def changedelivery(self, delivery):
        self.thing.delivery = delivery


def main():
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='1234',
                                 db='test',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        # SQL
        sql = "SELECT name, brand, price, number, delivery FROM thing"

        cursor.execute(sql)

    tng1 = cursor.fetchall()
    tng = Thing(tng1[0])
    facade = Facade(tng, 50000, 3, 'Вантажівка')
    facade.operation()


if __name__ == "__main__":
    main()