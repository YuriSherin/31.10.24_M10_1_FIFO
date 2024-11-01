import threading
from time import sleep
from random import randint
from queue import Queue

"""Потоки гостей в кафе"""
class Table:
    """Класс Table стол, хранит информацию о находящемся за ним гостем,
     обладает следующими атрибутами объекта:
    number - номер стола, guest - гость, который сидит за этим столом"""
    def __init__(self, number:int, guest=None):
        """Конструктор класса"""
        self.number = number        # номер стола
        self.guest = guest          # гость


class Guest(threading.Thread):
    """Дочерний класс Guest - гость, поток, при запуске которого происходит задержка
    от 3 до 10 секунд. Хранит атрибут name с именем гостя"""
    def __init__(self, name:str):
        """Конструктор класса"""
        super().__init__()
        self.name = name

    def run(self):
        """Метод является точкой входа для потока. Когда мы запускаем
        поток на исполнение методом start(), мы по сути дела
        обращаемся к методу run"""
        sleep(randint(3, 10))       # спим


class Cafe:
    """Класс Cafe - кафе, в котором есть определённое кол-во столов
    и происходит обслуживание гостей"""
    def __init__(self, *tables):
        """Конструктор класса"""
        self.tables = list(tables)  # список столов, имеющихся в кафе
        self.queue = Queue()        # синхронизированная очередь FIFO

    def find_empty_table(self):
        """Метод ищет первый свободный стол в кафе.
        Возвращает -1, если все столы заняты или номер найденного свободного стола"""
        res = -1
        for i in range(len(self.tables)):
            if self.tables[i].guest is None:
                res = i
                break
        return res

    def check_free_tables(self):
        """Метод возвращает True, если все столы в кафе свободны"""
        res = True
        for table in self.tables:
            if not table.guest is None:
                res = False
                break
        return res

    def guest_arrival(self, *guests):
        """Метод прибытия гостей, где *guests - список гостей"""
        for guest in guests:    # рассматриваем каждого прибывшего гостя
            num_empty_table =  self.find_empty_table()      # ищем пустой стол
            if num_empty_table >= 0:     # если есть пустой стол
                self.tables[num_empty_table].guest = guest      # садим гостя за стол
                print(f'{guest.name} сел(-а) за стол номер {self.tables[num_empty_table].number}')
                self.tables[num_empty_table].guest.start()      # запускаем поток на выполнение
            else:
                self.queue.put(guest)   # если свободного стола нет, помещаем гостя в очередь
                print(f'{guest.name} в очереди')


    def discuss_guests(self):
        """Метод обслуживания гостей"""
        # пока очередь не станет пуста и пока все столы не будут свободные
        while not self.queue.empty() and not self.check_free_tables():
            for table in self.tables:
                if not table.guest.is_alive():  # проверяем, жив ли поток
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None
                if table.guest is None:                 # если стол свободен
                    if not self.queue.empty():          # если очередь не пустая
                        table.guest = self.queue.get()  # берем гостя из очереди и садим за стол
                        print(f'{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                        table.guest.start()


def main():
    tables = [Table(number) for number in range(1, 6)]      # Создание столов
    guests_names = [        # Имена гостей
        'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
        'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
    ]

    guests = [Guest(name) for name in guests_names]     # Создание гостей
    cafe = Cafe(*tables)            # Заполнение кафе столами
    cafe.guest_arrival(*guests)     # Приём гостей
    cafe.discuss_guests()           # Обслуживание гостей

if __name__ == '__main__':
    main()