import pymysql.cursors

class Singleton:

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Singleton.__instance == None:
            Singleton()
        return Singleton.__instance

    def __init__(self, all):
        """ Virtually private constructor. """
        if Singleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Singleton.__instance = self
            Singleton.name = all['name']
            Singleton.price = all['price']
            Singleton.number = all['number']

connection = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='test', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
with connection.cursor() as cursor:
    # SQL
    sql = "SELECT name, price, number FROM thing"

    cursor.execute(sql)

tng1 = cursor.fetchall()
s = Singleton(tng1[0])

print(f"({s.name}, {s.price}, {s.number})")

s = Singleton.getInstance()
print(f"({s.name}, {s.price}, {s.number})")

s = Singleton(tng1[0])
