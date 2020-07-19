"""
Визначає зв'язок один до багатьох між об'єктами таким чином, що коли
один об'єкт змінює стан, всі залежні сповіщуються і оновлються автоматично.
"""

import pymysql.cursors
import abc

class Thing:

    def __init__(self, all):
        self.name = all['name']
        self.price = all['price']
        self.number = all['number']

    def inc_price(self):
        self.price += 2

    def dec_price(self):
        self.price -= 2

    def inc_num(self):
        self.number += 10

    def dec_num(self):
        self.number -= 10

class Subject:
    """
     Знає всіх своїх спостерігачів. Будь-яка кількість спостерігачів може спостерігати
    Надсилає сповіщення до спостерігачів, коли його стан змінюється.
    """

    def __init__(self):
        self._observers = set()
        self._subject_state = None

    def attach(self, observer):
        observer._subject = self
        self._observers.add(observer)

    def detach(self, observer):
        observer._subject = None
        self._observers.discard(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._subject_state)

    @property
    def subject_state(self):
        return self._subject_state

    @subject_state.setter
    def subject_state(self, arg):
        self._subject_state = arg
        self._notify()


class Observer(metaclass=abc.ABCMeta):
    """
    Define an updating interface for objects that should be notified of
    changes in a subject.
    """

    def __init__(self):
        self._subject = None
        self._observer_state = None

    @abc.abstractmethod
    def update(self, arg):
        pass


class User(Observer):
    """
    Implement the Observer updating interface to keep its state
    consistent with the subject's.
    Store state that should stay consistent with the subject's.
    """

    def update(self, arg):
        self._observer_state = arg

def main():
     connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='1234',
                                 db='test',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
     with connection.cursor() as cursor:

        # SQL
        sql = "SELECT name, price, number FROM thing"

        cursor.execute(sql)


     print('\n1 - Додати користувача\n2 - Видалити користувача\n3 - Підвищити ціну\n4 - Знизити ціну\n5 - Збільшити кількість\n6 - Зменшити кількість\n7 - Переглянути стани користувачів\n0 - Вийти')
     concrete_observer = []
     users = 0
     tng1 = cursor.fetchall()
     tng = Thing(tng1[0])
     subject = Subject()
     while (exit != True):
         choice = int(input())
         if choice == 1:
             concrete_observer.append(User())
             subject.attach(concrete_observer[users])
             print("Кількість користувачів: " + str(len(subject._observers)))
             users += 1
         elif choice == 2:
             subject.detach(concrete_observer[users-1])
             del concrete_observer[users-1]
             print("Кількість користувачів: " + str(len(subject._observers)))
             users -= 1
         elif choice == 3:
             tng.inc_price()
             print("Ціна виросла до " + str(tng.price))
         elif choice == 4:
             tng.dec_price()
             print("Ціна знизилась до " + str(tng.price))
         elif choice == 5:
             tng.inc_num()
             print("Кількість виросла до " + str(tng.number))
         elif choice == 6:
             tng.dec_num()
             print("Кількість знизилась до " + str(tng.number))
         elif choice == 7:
             for indx, i in enumerate(concrete_observer):
                 print(f"Користувач №{indx+1}: ({i._observer_state.name}, {i._observer_state.price}, {i._observer_state.number})")
         elif choice == 0:
             break
         subject.subject_state = tng
         subject._notify()

     connection.close()


if __name__ == "__main__":
    main()