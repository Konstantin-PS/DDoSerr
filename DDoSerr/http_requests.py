#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This file is part of DDoSerr.
DDoSerr is a research program for emulating (D)DoS traffic and
its analysis (in development).
Use this program on your own pril and risk, as with improper use 
there is a risk of disruption of the network infrastucture.
DDoSerr Copyright © 2018 Konstantin Pankov 
(e-mail: konstantin.p.96@gmail.com), Mikhail Riapolov.

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
Модуль отправки HTTP-запросов для DDoSerr.
v.1.6.4.2b. от 20.09.2018.
"""

"""
Легенда обозначений:
"___" - переделать / удалить;
"---" - отладка;
"~~~" - сделать;
"!" - первоочередная задача.
"""

#Используем библиотеку requests.
import requests
#from requests import Request, Session
#Подключаем модуль времени.
import time
#Подключаем модуль взаимодействия с системой.
import os
#Подключаем готовый модуль логгирования.
import logging
#Подключаем модуль парсера страницы.
import html_parser
#Подключаем класс для получения случайного user agent-a.
from user_agents import Agents
#Подключаем модуль работы с файлами csv.
import csv

#Настройка логгирования.
logging.basicConfig(filename='log.log',level=logging.INFO, \
format='%(asctime)s %(message)s', datefmt='%d.%m.%Y - %H:%M:%S |')


def http_connection(repeat, delay, url):
    """
    Функция для создания 1 процесса, запросов к сайту и получения ответа.
    Подгружает страницу и контент со страницы 
    (картинки, java-скрипты, CSS стили).
    """
    
    #Вызов парсера странцы и получение списка ссылок 
    #на подгружаемый контент.
    content_urls = html_parser.obj_search(url)
    

    #Цикл выполняет задание 'repeat' раз в каждом процессе.
    for _ in range(repeat):
        #Создаём сессию.
        session = requests.Session()
        
        #Вызываем модуль агентов и получаем рандомного агента из списка.
        random_agent = Agents().random_agent()
        
        """
        #Для post запросов, пригодится в будущем.
        #main_page = requests.post("http://httpbin.org/post")
        """
        
        #Запрос к url (атакуемой странице) с юзер агентом в сессии.
        main_page = session.get(url, stream=True, headers=\
        {'User-Agent': random_agent})
        
        
        #Получение информации по запросу к странице по url.
        
        #Код возврата.
        status_url = str(main_page.status_code)
        #Размер ответа. Большой ответ разбивается на куски по 8196 Байт.
        size_url = str(sum(len(chunk) for chunk in\
        main_page.iter_content(8196)))
    
        #Этот вывод результата (для наглядности работы и отладки)
        #можно убрать для небольшого повышения производительности.
        print(status_url, size_url)
        
        answer_url = str("code " + status_url + "," + '\t' + "size " +
        size_url + " bytes")
        
        #Логгируем запуск процесса с его PID.
        logging.info('Process ' + str(os.getpid()) +
        ' received the task.')
        #Логгируем результаты.
        logging.info('URL: ' + url)
        logging.info('Answer: ' + answer_url)
        
        
        #Запрос контента со страницы по найденным ссылкам.

        for _ in range(len(content_urls)):
            #Система прохода по списку ссылок на контент 
            #для его подгрузки.
            #И всё это должно подгружаться сразу, для каждой сессии,
            #поэтому нужен отдельный цикл внутри задания.
            
            #_ или item.
            current_url = content_urls[_]
            
            #Содаём подготовленный запрос с юзер агентом.
            
            req = requests.Request('GET', current_url, \
            headers={'User-Agent': random_agent})
            
            prepped = session.prepare_request(req)
            
            content_on_page = session.send(prepped)

            
            #Получение информации по контенту.
            
            #Код возврата.
            status = str(content_on_page.status_code)
            #Размер ответа. Большой ответ разбивается на куски 
            #по 8196 Байт.
            size = str(sum(len(chunk) for chunk in\
            content_on_page.iter_content(8196)))
        
            #Этот вывод результата (для наглядности работы и отладки)
            #можно убрать для небольшого повышения производительности.
            print(status, size)
        
            answer = str("code " + status + "," + '\t' + "size " +
            size + " bytes")
        
            #Логгируем запуск процесса с его PID.
            logging.info('Process ' + str(os.getpid()) +
            ' received the task.')
            #Логгируем результаты.
            logging.info('URL: ' + current_url)
            logging.info('Answer: ' + answer)
        
        
        #Задержка перед повтором цикла.
        time.sleep(delay)
        
    #Закрываем файл юзер агентов.
    Agents().agents_close()
        

def http_connection_plan(repeat, delay):
    
    """
    Модификация функции для создания 1 процесса, 
    запросов к сайту и получения ответа.
    Использует план тестирования (атаки).
    Подгружает страницу и контент со страницы 
    (картинки, java-скрипты, CSS стили).
    """
    #Выбираем файл плана.
    plan_file = "attack_plan.csv"
    #Открываем файл плана тестирования (атаки).
    plan = open(plan_file, "r", newline="")
    #Считываем содержимое.
    reader = csv.reader(plan)

    #Цикл выполняет задание 'repeat' раз в каждом процессе.
    for _ in range(repeat):
        #!Добавить сюда рандомную паузу перед началом работы
        #от 0 до 2 минут (120 сек.), отключаемую.
        
        #Создаём сессию.
        session = requests.Session()
        
        #Вызываем модуль агентов и получаем рандомного агента из списка.
        random_agent = Agents().random_agent()
        

        #Работа с планом тестирования.
        for row in reader:
            url = row[0]
            pause = int(row[1])
            #!Добавить к паузе рандомное значение от 0 до 120 сек.
            #отключаемое (для 100 процессов).
            
            #Вызов парсера странцы и получение списка ссылок 
            #на подгружаемый контент.
            content_urls = html_parser.obj_search(url)
        
            #Запрос к url (атакуемой странице) с юзер агентом в сессии.
            main_page = session.get(url, stream=True, headers=\
            {'User-Agent': random_agent})
            
            
            #Получение информации по запросу к странице по url.
            
            #Код возврата.
            status_url = str(main_page.status_code)
            #Размер ответа. Большой ответ разбивается на куски
            #по 8196 Байт.
            size_url = str(sum(len(chunk) for chunk in\
            main_page.iter_content(8196)))
        
            #Этот вывод результата (для наглядности работы и отладки)
            #можно убрать для небольшого повышения производительности.
            print(status_url, size_url)
            
            answer_url = str("code " + status_url + "," + '\t' +
            "size " + size_url + " bytes")
            
            #Логгируем запуск процесса с его PID.
            logging.info('Process ' + str(os.getpid()) +
            ' received the task.')
            #Логгируем результаты.
            logging.info('URL: ' + url)
            logging.info('Answer: ' + answer_url)
            
            
            #Запрос контента со страницы по найденным ссылкам.
        
            for _ in range(len(content_urls)):
                #Система прохода по списку ссылок на контент 
                #для его подгрузки.
                #И всё это должно подгружаться сразу, для каждой сессии,
                #поэтому нужен отдельный цикл внутри задания.
                
                current_url = content_urls[_]
                
                #Содаём подготовленный запрос с юзер агентом.
                
                req = requests.Request('GET', current_url, \
                headers={'User-Agent': random_agent})
                
                prepped = session.prepare_request(req)
                
                content_on_page = session.send(prepped)

                
                #Получение информации по контенту.
                
                #Код возврата.
                status = str(content_on_page.status_code)
                #Размер ответа. Большой ответ разбивается на куски
                #по 8196 Байт.
                size = str(sum(len(chunk) for chunk in\
                content_on_page.iter_content(8196)))
            
                #Этот вывод результата (для наглядности работы и отладки)
                #можно убрать для небольшого повышения производительности.
                print(status, size)
            
                answer = str("code " + status + "," + '\t' + "size " +
                size + " bytes")
            
                #Логгируем запуск процесса с его PID.
                logging.info('Process ' + str(os.getpid()) +
                ' received the task.')
                #Логгируем результаты.
                logging.info('URL: ' + current_url)
                logging.info('Answer: ' + answer)
                
            #Пауза перед переходом по следующей ссылке из плана.
            time.sleep(pause)
        
        #Задержка перед повтором цикла.
        time.sleep(delay)
        
    #Закрываем файл юзер агентов.
    agents_close = Agents().agents_close()
    
    #Закрываем файл плана тестирования.
    plan.close()
        


if __name__ == "__main__":
    #Временные параметры для самостоятельного запуска.
    repeat = 1
    delay = 0.5
    
    ##mode = 'u'
    ##url = "https://edu.vsu.ru"
    ##content_urls = html_parser.obj_search(url)
    ##Запуск функции.
    ##http_connection(repeat, delay, url)
    
    #mode = "p"
    http_connection_plan(repeat, delay)

