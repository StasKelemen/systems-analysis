"""
Provide a way to access the elements of an aggregate objects equentially
without exposing its underlying representation.
"""

import collections.abc

import pymysql.cursors

class ConcreteAggregate(collections.abc.Iterable):
    """
    Implement the Iterator creation interface to return an instance of
    the proper ConcreteIterator.
    """

    def __init__(self, low, high):
        self.current = low
        self.high = high-1

    def __iter__(self):
        return ConcreteIterator(self)


class ConcreteIterator(collections.abc.Iterator):
    """
    Implement the Iterator interface.
    """

    def __init__(self, concrete_aggregate):
        self._concrete_aggregate = concrete_aggregate
        self.current = concrete_aggregate.current
        self.high = concrete_aggregate.high

    def __next__(self):
        if self.current > self.high:
            raise StopIteration
        else:
            self.current += 1
            return self.current - 1


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

    things = cursor.fetchall()
    concrete_aggregate = ConcreteAggregate(0, len(things))
    iteration = ConcreteIterator(concrete_aggregate)
    counter = 0
    for _ in iteration:
        counter += 1
    print(counter)

if __name__ == "__main__":
    main()