﻿#!/usr/bin/python
# -*- coding: utf-8 -*- 

import time				#Подключаем модуль времени.

#Для повтора чего-либо n раз можно использовать 'range(n)'.
for _ in range(60):		#Цикл на 60 повторов.
	print('КуЪ!')		#Функция(и), которую(ые) надо выполнять не раньше, чем через секунду 60 раз. Выполняются до sleep.
	time.sleep(1)		#Ждём секунду перед завершением итерации цикла. Повторяем выполнение функции.


