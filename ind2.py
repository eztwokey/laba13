#!/usr/bin/env python3
# -*- config: utf-8 -*-

# Использовать словарь, содержащий следующие ключи: фамилия, имя; номер телефона;
# дата рождения. Написать программу, выполняющую следующие
# действия: ввод с клавиатуры данных в список, состоящий из словарей заданной структуры;
# записи должны быть упорядочены по трем первым цифрам номера телефона; вывод на
# экран информации о человеке, чья фамилия введена с клавиатуры; если такого нет, выдать
# на дисплей соответствующее сообщение.

# Выполнить индивидуальное задание 2 лабораторной работы 9, использовав классы данных, а
# также загрузку и сохранение данных в формат XML.

from dataclasses import dataclass, field
import sys
from typing import List
import xml.etree.ElementTree as ET


@dataclass(frozen=True)
class people:
    surname: str
    name: str
    number: int
    year: int


@dataclass
class Staff:
    peoples: List[people] = field(default_factory=lambda: [])

    def add(self, surname, name, number, year):
        self.peoples.append(
            people(
                surname=surname,
                name=name,
                number=number,
                year=year
            )
        )

        self.peoples.sort(key=lambda people: people.number)

    def __str__(self):
        table = []
        line = '+-{}-+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 20,
            '-' * 20,
            '-' * 20,
            '-' * 15
        )
        table.append(line)
        table.append(
            '| {:^4} | {:^20} | {:^20} | {:^20} | {:^15} |'.format(
                "№",
                "Фамилия ",
                "Имя",
                "Номер телефона",
                "Дата рождения"
            )
        )
        table.append(line)

        for idx, people in enumerate(self.peoples, 1):
            table.append(
                '| {:>4} | {:<20} | {:<20} | {:<20} | {:>15} |'.format(
                    idx,
                    people.surname,
                    people.name,
                    people.number,
                    people.year
                )
            )
        table.append(line)

        return '\n'.join(table)

    def select(self):
        parts = command.split(' ', maxsplit=2)
        sur = (parts[1])

        count = 0

        for people in self.peoples:
            if people.get('surname') == sur:
                count += 1
                print('Фамилия:', people.surname)
                print('Имя:', people.name)
                print('Номер телефона:', people.number)
                print('Дата рождения:', people.year)

        if count == 0:
            print("Таких фамилий нет !")

        def load(self, filename):
            with open(filename, 'r', encoding='utf8') as fin:
                xml = fin.read()
            parser = ET.XMLParser(encoding="utf8")
            tree = ET.fromstring(xml, parser=parser)
            self.peoples = []

            for people_element in tree:
                surname, name, number, year = None, None, None, None

                for element in people_element:
                    if element.tag == 'surname':
                        surname = element.text
                    elif element.tag == 'name':
                        name = element.text
                    elif element.tag == 'number':
                        number = element.text
                    elif element.tag == 'year':
                        year = element.text

                    if surname is not None and name is not None \
                            and number is not None and year is not None:
                        self.peoples.append(
                            people(
                                suname=surname,
                                name=name,
                                number=number,
                                year=year
                            )
                        )

        def save(self, filename):
            root = ET.Element('peoples')
            for people in self.peoples:
                people_element = ET.Element('people')

                surname_element = ET.SubElement(people_element, 'surname')
                surname_element.text = people.surname

                name_element = ET.SubElement(people_element, 'name')
                name_element.text = people.name

                number_element = ET.SubElement(people_element, 'number')
                number_element.text = str(people.number)

                year_element = ET.SubElement(people_element, 'year')
                year_element.text = str(people.year)

                root.append(people_element)

            tree = ET.ElementTree(root)
            with open(filename, 'wb') as fout:
                tree.write(fout, encoding='utf8', xml_declaration=True)

    if __name__ == '__main__':
        peoples = []
        staff = Staff
        while True:
            command = input(">>> ").lower()
            if command == 'exit':
                break

            elif command == 'add':
                surname = input("Фамилия ")
                name = input("Имя ")
                number = int(input("Номер телефона "))
                year = input("Дата рождения в формате: дд.мм.гггг ")

                staff.add(surname, name, number, year)


            elif command == 'list':
                print(staff)

            elif command.startswith('select '):
                parts = command.split(' ', maxsplit=2)
                sur = (parts[1])

                count = 0

                for people in peoples:
                    if people.get('surname') == sur:
                        count += 1
                        print('Фамилия:', people.surname)
                        print('Имя:', people.name)
                        print('Номер телефона:', people.number)
                        print('Дата рождения:', people.year)

                if count == 0:
                    print("Таких фамилий нет !")

            elif command.startswith('load '):
                parts = command.split(' ', maxsplit=1)
                staff.load(parts[1])

            elif command.startswith('save '):
                parts = command.split(' ', maxsplit=1)
                staff.save(parts[1])

            elif command == 'help':
                print("Список команд:\n")
                print("add - добавить человека;")
                print("list - вывести список людей;")
                print("select <фамилия> - запросить информацию по фамилии;")
                print("load <имя файла> - загрузить данные из файла;")
                print("save <имя файла> - сохранить данные в файл;")
                print("help - отобразить справку;")
                print("exit - завершить работу с программой.")
            else:
                print(f
                "Неизвестная команда {command}", file = sys.stderr)
