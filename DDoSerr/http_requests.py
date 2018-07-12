#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Модуль отправки HTTP-запросов для DDoSerr.
v.1.5.4.2b. от 12.07.2018.
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

#Настройка логгирования.
logging.basicConfig(filename='log.log',level=logging.INFO, \
format='%(asctime)s %(message)s', datefmt='%d.%m.%Y - %I:%M:%S |')


def http_connection(repeat, pause, url="http://127.0.0.1"):
    """
    Функция для создания одного запроса к сайту и получения ответа.
    """
    #Если не задаётся извне значение url, то берётся указанное.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #!Добавить в аргументы user_agent!
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    

    
    for _ in range(repeat):
        response = requests.get(url, stream=True)
        #Для post запросов, пригодится в будущем.
        #response = requests.post("http://httpbin.org/post")
        
        #Код возврата.
        status = str(response.status_code)
        #Размер ответа, большой ответ разбивается на куски по 8196 Байт.
        size = str(sum(len(chunk) for chunk in response.iter_content(8196)))
        
        #Этот вывод результата можно убрать для повышения производительности.
        print(status, size)
        
        answer = str("code " + status + "," + '\t' + "size " + size)
        
        #Логгируем запуск процесса с его PID.
        logging.info('Process ' + str(os.getpid()) + ' received the task.')
        #Логгируем результаты.
        logging.info('Answer: ' + answer)
        
        #Задержка перед повтором цикла.
        time.sleep(pause)
    
"""
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!Вместо url надо сделать список адресов с задерками.
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


if __name__ == "__main__":
    """
    То, что находится внутри if __name__ == "__main__" будет выполнено 
    только в том случае, когда модуль запущен отдельно, а не импортирован. 
    """
    #Запуск функции.
    http_connection(repeat, pause, url)

