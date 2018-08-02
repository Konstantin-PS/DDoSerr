#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
Модуль отправки HTTP-запросов для DDoSerr.
v.1.6.1.2b. от 02.08.2018.
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
#Подключаем модуль времени.
import time
#Подключаем модуль взаимодействия с системой.
import os
#Подключаем готовый модуль логгирования.
import logging
#Подключаем модуль парсера страницы.
import html_parser
#Подключаем модуль работы с user agent-ами.
import user_agents

#Настройка логгирования.
logging.basicConfig(filename='log.log',level=logging.INFO, \
format='%(asctime)s %(message)s', datefmt='%d.%m.%Y - %I:%M:%S |')


def http_connection(repeat, pause, content_urls):
    #(repeat, pause, url="http://127.0.0.1")
    """
    Функция для создания 1 процесса, запросов к сайту и получения ответа.
    Подгружает контент.
    """
    #Если не задаётся извне значение url, то берётся указанное.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #!Добавить в аргументы user_agent!
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    random_agent = user_agents.Agents().random_agent().random_agent
    content_urls = html_parser.obj_search(url).content_urls

    #Цикл выполняет задание 'repeat' раз в каждом процессе.
    for _ in range(repeat):
        #Создаём сессию.
        session = requests.Session()
        
        
        #Отправляем один запрос к заглавной странице.
        #main_page = session.get(url, stream=True)
        
        #Для post запросов, пригодится в будущем.
        #main_page = requests.post("http://httpbin.org/post")
        
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        !Сделать цикл(ы) для запросов!
        !Добавить выбор рандомного юзер агента. Переделать headers!
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        #!!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #!Запрос контента со страницы по найденным ссылкам.
        #!Возможно, цикл не правильный.
        for i in content_urls:
            current_url = str(content_urls[i])
            headers = {random_agent}
            content_main_page = session.get(content_urls[i], headers=headers)
            
        
        #Для main_page.
        #Код возврата.
        #status = str(main_page.status_code)
        #Размер ответа, большой ответ разбивается на куски по 8196 Байт.
        #size = str(sum(len(chunk) for chunk in main_page.iter_content(8196)))
        
        #Код возврата.
        status = str(content_main_page.status_code)
        #Размер ответа, большой ответ разбивается на куски по 8196 Байт.
        size = str(sum(len(chunk) for chunk in content_main_page.iter_content(8196)))
        
        #Этот вывод результата можно убрать для повышения производительности.
        print(status, size)
        
        answer = str("code " + status + "," + '\t' + "size " + size)
        
        #Логгируем запуск процесса с его PID.
        logging.info('Process ' + str(os.getpid()) + ' received the task.')
        #Логгируем результаты.
        logging.info('URL: ' + current_url)
        logging.info('Answer: ' + answer)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #Задержка перед повтором цикла.
        time.sleep(pause)
        


"""
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!Вместо url надо сделать список адресов с задерками.
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


if __name__ == "__main__":
    #Запуск функции.
    http_connection(repeat, pause, url)

