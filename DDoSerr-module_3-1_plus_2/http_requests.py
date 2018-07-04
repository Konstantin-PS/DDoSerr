#!/usr/bin/python3
#Путь к интерпретатору пайтона.
# -*- coding: utf-8 -*-
#Выбор кодировки (без него не работает русский язык).

"""
Модуль отправки HTTP-запросов для DDoSerr.
v.1.2.1 от 04.07.2018.
"""

#Используем библиотеку requests.
import requests


def http_connection(url='https://yandex.ru'):
	#https://httpbin.org/get
	#Если не задаётся извне значение url, то берётся указанное.
	#!Позже добавить в аргументы user agent!
	request = requests.get(url)
	#Для post запросов пригодится.
	#request = requests.post("http://httpbin.org/post")
	
	status = request.status_code
	print(status)
	head = request.headers['content-type']
	print(head)
	return(status, head)

#Вызов функции особым способом.
#То, что находится внутри if __name__ == "__main__" будет выполнено 
#только в том случае, когда модуль запущен отдельно, а не импортирован. 
if __name__ == "__http_connection__":
	http_connection()	
