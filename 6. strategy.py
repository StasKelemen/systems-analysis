"""
Визначає сімейство алгоритмів, об'єднуючи їх всіх та роблячи взаємозамінними.
Шаблон стратегія робить алгоритм незалежним від клієнта, який його використовує.
"""

import abc

class Context:
    """
    Визначає інтерфейс, що відповідає за бажання клієнта.
    Підтримує зв'язок з об'єктом Strategy.
    """

    def __init__(self, strategy):
        self._strategy = strategy

    def context_interface(self):
        self._strategy.algorithm_interface()

class Strategy(metaclass=abc.ABCMeta):
    """
    Визначає інтерфейс, спільний для всіх алгоритмів.
    Контекст використовує його, шоб вибирати стратегію.
    """
    whishes = 0
    buys = 0

    @abc.abstractmethod
    def algorithm_interface(self):
        pass


class Search(Strategy):
    """Імплементує конкретну стратегію."""

    def algorithm_interface(self):
        print('Пошук товарів...')


class Recommends(Strategy):

    def algorithm_interface(self):
        print('Перегляд рекомендованих...')

class WishList(Strategy):

    def algorithm_interface(self):
        print('Перегляд списку бажань...')

def main():
    print('1 - Шукати товари\n2 - Переглянути рекомендовані\n3 - Переглянути список бажань\n0 - Вийти')
    print('\nЩо ви хочете робити?')
    while(exit != True):
        choice = int(input())
        if choice == 1:
            inst = Search()
        elif choice == 2:
            inst = Recommends()
        elif choice == 3:
            inst = WishList()
        elif choice == 0:
            break
        else:
            print("Введіть число з діапазону значень!")
            continue
        context = Context(inst)
        context.context_interface()


if __name__ == "__main__":
    main()