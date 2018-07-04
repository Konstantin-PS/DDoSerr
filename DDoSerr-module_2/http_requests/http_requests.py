#!/usr/bin/python3
#Путь к интерпретатору пайтона (может работать и без этого, если в системе прописан).
# -*- coding: utf-8 -*-
#Выбор кодировки (без него не работает русский язык).

"""
Модуль отправки HTTP-запросов для DDoSerr.
v.1.1.2 от 03.07.2018.
"""

#import httplib					#Подключаем модуль для работы с HTTP (низкоуровневый).

#connection = httplib.HTTPConnection("https://httpbin.org/get")	#Будем соединяться с сайтом Microsoft.
#connection.request("HEAD", "/index.html")					#Запрашиваем начальную страницу.
#result = connection.getresponse()							#Записываем ответ.
#print result.status, result.reason							#Выводим результат.


#Способ лучше.
import requests

def http_connection():
	request = requests.get('https://google.com')
	#request = requests.get('https://httpbin.org/get')
	#request = requests.post("http://httpbin.org/post")
	status = request.status_code
	print(status)
	head = request.headers['content-type']
	print(head)

http_connection()	#Вызов функции.
