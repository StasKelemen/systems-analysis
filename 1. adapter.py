"""
Convert the interface of a class into another interface clients expect.
Adapter lets classes work together that couldn't otherwise because of
incompatible interfaces.
"""

import pymysql.cursors
import abc

class Thing:

    def __init__(self, all):
        self.name = all['name']
        self.price = all['price']
        self.number = all['number']

class Target(metaclass=abc.ABCMeta):
    """
    Define the domain-specific interface that Client uses.
    """

    def __init__(self, convert, rate, ctype):
        self._adaptee = Adaptee(convert, rate, ctype)

    @abc.abstractmethod
    def request(self):
        pass


class Adapter(Target):
    """
    Adapt the interface of Adaptee to the Target interface.
    """

    def request(self):
        return self._adaptee.specific_request()


class Adaptee:
    """
    Define an existing interface that needs adapting.
    """
    def __init__(self, convert, rate, ctype):
        self.convert = convert[0]
        self.rate = rate
        self.ctype = ctype

    def specific_request(self):
        return [self.convert / self.rate, self.ctype]


def main():
    connection = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='test', charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        # SQL
        sql = "SELECT name, price, number FROM thing"

        cursor.execute(sql)

    tng1 = cursor.fetchall()
    tng = Thing(tng1[6])
    gryvna = [tng.price, '0']
    adapter = Adapter(gryvna, 27, 'dollar')
    print(adapter.request())


if __name__ == "__main__":
    main()