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
v.1.6.7.5b. от 10.09.2018.

Считывает и, при необходимости, переопределяет настройки,
запускает модуль HTTP-запросов и логгирует ответы.
Для имитации работы браузера и человека используется подгрузка контента
со страницы (картинки, java-скрипты и CSS стили) и, при выборе 
соответствующего режима работы ('p'), план тестирования (атаки), 
позволяющий осуществлять автоматические переходы по заданным в 
текстовом файле ("attack_plan.txt") адресам с задаваемой там же паузой
для имитации чтения страницы.
Режим плана тестирования не работает со ссылками на загрузку файлов!
Есть возможность конфигурации через ключи командной строки - запустите
DDoSerr без аргументов или с ключом '-h' ('--help') для справки.
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
#Подключаем модуль многопроцессовости, а точнее, его класс Pool.
from multiprocessing import Pool
#Подключаем готовый модуль логгирования.
import logging
#Подключаем модуль парсинга аргументов (ключей) командной строки.
import argparse


#Настройка логгирования.
logging.basicConfig(filename='log.log',level=logging.INFO, \
format='%(asctime)s %(message)s', datefmt='%d.%m.%Y - %H:%M:%S |')

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
        self.delay = float(config.get("Settings", "Delay"))
        self.repeat = int(config.get("Settings", "Repeat"))
          
          
    
    def interact_input(self):
        """
        Ввод одноразовых настроек из консоли 
        с переопределением переменных.
        Вызывается ключом '-i' или '--interactive'.
        """
        #Переменная для выбора режима работы: по url или по плану тестирования.
        mode = str(input("Выберите режим работы: u - по URL, " + 
        "p - по плану тестирования: "))
        if mode == 'u':
            self.mode = 'u'
            #Ввод URL атакуемого ресурса. В интерактивном режиме.
            self.url = str(input("Введите полный адрес цели " + 
            "(с http(s)://): "))
            #url = "https://www.edu.vsu.ru"
        elif mode == 'p':
            self.mode = 'p'
            #Костыль для работы режима по плану.
            self.url = None
        else:
            print("Вы ввели неверное имя режима.")
            
        
        #Запрос на переопределение настроек и ввод с клавиатуры.
        switch = input("Хотите ли Вы однократно переопределить" + 
        "заданные в конфиг-файле настройки программы?"+\
            '\n'+"Да - 'y', Нет - 'n'."+'\n'+"Ваш выбор: ")
        if switch == "y":
            print("Введите свои параметры.")
            #Переопределение настроек.
            self.proc_num = int(input("Введите количество " + 
            "создаваемых подпроцессов: "))
            self.delay = float(input("Введите длительность задержки" + 
            "между заданиями для одного процесса (секунд): "))
            self.repeat = int(input("Введите количество" + 
            "повторов запросов: "))  
            
        elif switch == "n":
            print("Используются настройки из файла конфигурации.")
            
    
    
    def parse_params(self):
    #def parse_params(self, args):
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Функция для переопределения настроек
        параметрами командной строки.
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        #Вызов парсера.
        argprs = argparse.ArgumentParser(prog='DDoSerr',\
        description='DDoSerr - программа для моделирования (D)DoS атаки.',\
        prefix_chars='-/')
    
        #Для включения интерактивного режима (только один этот ключ):
        #Создаём группу для отображение в подсказке.
        interactive = argprs.add_argument_group('Interactive mode',\
        'Полностью интерактивный режим. Требуется только один ключ.')
        #Добавляем в группу аргумент.
        interactive.add_argument('-i', '--interactive',\
        action='store_true', dest='interact',\
        help='Запуск DDoSerr в интерактивном режиме настройки.' + 
        'Требуется только этот ключ.')
        
        
        #Далее для мануального режима.
        #Группа для определения настроек ключами командной строки.
        cmd_args = argprs.add_argument_group('Command line arguments',\
        'Определение настроек ключами (аргументами) командной строки.')
        #Для выбора режима работы (по URL или по плану тестирования):
        cmd_args.add_argument('-m', '--mode', default='u', type=str,\
        choices=['u', 'p'], dest='mode',\
        help='Выбор режима работы DDoSerr: "u" - по URL, ' + 
        '"p" - по плану тестирования.' +
        '\t' + 'Для режима по URL задание ключа -u или' + 
        '--url обязательно!')
        
        #Для URL:
        cmd_args.add_argument('-u', '--url', type=str, dest='url',\
        help='Задание URL только для соответствующего режима работы.' + 
        'Вводить полностью, с "http(s)://".')
        
        
        #Для переопределения настроек конфиг-файла.
        #Группа для переопределение настроек конфига.
        cfg_redef = argprs.add_argument_group('Config redefinition',\
        'Переопределение настроек из конфигурационного файла.' + 
        'Без указания ключа (ключей) используется значение из конфига.')
        #Количество подпроцессов:
        cfg_redef.add_argument('--proc_num', type=int, dest='proc_num',\
        help='Переопределение количества создаваемых подпроцессов.')
        
        
        #Для задержки между заданиями:
        cfg_redef.add_argument('--delay', type=float, dest='delay',\
        help='Переопределение задержки между заданиями.')
        
        #Для количества повторов запросов.
        cfg_redef.add_argument('--repeat', type=int, dest='repeat',\
        help='Переопределение количества повторов запросов.')
        
        
        #Если при запуске программы не заданы ключи командной строки,
        #то показывается справка.
        if len(sys.argv)==1:
            argprs.print_help(sys.stderr)
            sys.exit(1)
        
        #Запуск парсера аргументов с заданием ему имени
        #для дальнейшего обращения к результату.
        self.arguments = argprs.parse_args()
        
        #Возвращаем значения аргументов из функции.
        return self.arguments




if __name__ == "__main__":
    """
    Запуск функции main() только при запуске этого модуля, 
    но не при импорте.
    Если функция main не задана в явном виде (def main()),
    то весь код (после конструкции if __name__ == "__main__") 
    считается ею.
    """
    
    #Загрузка настроек из фала конфигурации с сохранением в переменную.
    #Если есть параметры командной строки, то они переопределяют
    #настройки из конфига.
    cfg = Config(sys.argv)
    
    

    #Вызов функции парсера командной строки.
    args = cfg.parse_params()
    
    
    #Режим работы.
    if args.mode != None:
        #Если задан ключ командной строки.
        mode = args.mode
    else:
        #Если не задан ключ, т.е. там None.
        mode = cfg.mode
    
    #Следующие 3 настройки будут подгружаться из конфига, если не заданы
    #в качестве параметров командной строки.
    
    #Количество процессов.
    if args.proc_num != None:
        proc = args.proc_num
    else:
        proc = cfg.proc_num
        
    #Количество повторов задания.
    if args.repeat != None:
        repeat = args.repeat
    else:
        repeat = cfg.repeat
        
    #Задержка повтора задания.
    if args.delay != None:
        delay = args.delay
    else:
        delay = cfg.delay
    
    
    
    #Проверка ключа интерактивного режима для выбора
    #между обычным (с ключами) и интерактивным режимом.
    interact = args.interact
    if interact==False:
        #Обычный режим.
        if args.mode == 'u':
            mode = 'u'
            if args.url != None:
                url = args.url
            else:
                url = cfg.url
            #mode = 'u'
            url = args.url
        elif args.mode == 'p':
            mode = 'p'
        
    elif interact==True:
        #Интерактивный режим.
        cfg.interact_input()
        
        #Переопределяемые, если нужно, параметры конфига.
        proc = cfg.proc_num
        delay = cfg.delay
        repeat = cfg.repeat
        
        #Используем url только если выбран соответствующий режим работы.
        if cfg.mode == 'u':
            mode = 'u'
            url = cfg.url
        if cfg.mode == 'p':
            mode = 'p'
    
    
    
    """
    Реализация "многопоточности" с помощью подпроцессов 
    для обхода "Глобальной блокировки интерпретатора" 
    ("Global Interpreter Lock"), позволяющей только одному потоку 
    исполнять код.
    Получается n процессов: один родительский и n-1 дочерних.
    """
    
    #Вывод информационных сообщений (для разных режимов).
    if mode == 'u':
        print('\n' + "DDoSerr запущен в режиме URL." + '\n' +
        "Атакуемый ресурс: " + url + 
        '\n' + "Запущено процессов: " + str(proc) + "." + '\n' +
        "Дано заданий: " + str(repeat) + "." + '\n' +
        "Задержка повторения: " + str(delay) + " секунд(ы)." + '\n' +
        "Атака выполняется." + '\n' + 
        "Пожалуйста, подождите и насладитесь своим величием. :)")
        #Запись информационных сообщений в лог.
        logging.info('\n' + '----------------------------------------'+ 
        '\n')
        logging.info("DDoSerr запущен в режиме URL." + '\n' + 
        "Атакуемый ресурс: " + url + '\n' +
        "Запущено процессов: " + str(proc) + "." + '\n' + 
        "Дано заданий: " + str(repeat) + "." + '\n' + 
        "Задержка повторения: " + str(delay) + " секунд(ы)." + '\n' +
        "Атака выполняется." + '\n' + 
        "Пожалуйста, подождите и насладитесь своим величием. :)")
    elif mode == 'p':
        print('\n' + "DDoSerr запущен в режиме плана тестирования." + 
        '\n' + '\n' + "Запущено процессов: " + str(proc) + "." + '\n' +
        "Дано заданий: " + str(repeat) + "." + '\n' +
        "Задержка повторения: " + str(delay) + " секунд(ы)." + '\n' +
        "Атака выполняется." + '\n' + 
        "Пожалуйста, подождите и насладитесь своим величием. :)")
        #Запись информационных сообщений в лог.
        logging.info('\n' + '----------------------------------------' +
        '\n')
        logging.info("DDoSerr запущен в режиме плана тестирования." + 
        '\n' + "Запущено процессов: " + str(proc) + "." + '\n' + 
        "Дано заданий: " + str(repeat) + "." + '\n' + 
        "Задержка повторения: " + str(delay) + " секунд(ы)." + '\n' +
        "Атака выполняется." + '\n' + 
        "Пожалуйста, подождите и насладитесь своим величием. :)")
    

    #Создаём пул из 'proc' штук работников (процессов).
    with Pool(processes=proc) as pool:

    #Даём им задание ПО ОДНОМУ через apply_async в цикле
    #и получаем результат.
    
    #Создаётся 'proc' штук процессов с заданием ('пачка').
        for _ in range(proc):
            if mode == 'u':
                worker = pool.apply_async(http_requests.\
                http_connection, (repeat, delay, url,))
            if mode == 'p':
                worker = pool.apply_async(http_requests.\
                http_connection_plan, (repeat, delay,))
            
            #Логгируем запуск процесса с его PID.
            logging.info('Process ' + str(os.getpid()) + 
            ' was started.')
            
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
