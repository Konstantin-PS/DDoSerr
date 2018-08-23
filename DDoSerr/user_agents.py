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
Модуль для DDoSerr, считывающий файл с user agent-ами и 
записывающий их в список.
v.1.2.3.3b от 21.08.2018.
"""

"""
Легенда обозначений:
"___" - переделать / удалить;
"---" - отладка;
"~~~" - сделать;
"!" - первоочередная задача.
"""

import random

class Agents:

    def __init__(self, user_agents_file='user_agents.txt'):
        self.agents_file = open(user_agents_file, 'r')
        self.agents_list = [row.strip() for row in self.agents_file]
    

    def random_agent(self):
        #Запуск генератора случайных чисел.
        #Проверить, не будут ли числа повторяться!
        #random.seed([X], version=2)
        random.seed()
        #random.randint(A, B) - случайное целое число N, A ≤ N ≤ B.
        #Список с 0.
        
        #Даёт выход за пределы списка.
        #self.rnd = random.randint(0, len(self.agents_list))
        
        #При попытке вызвать 24 элемент всё падает, т.к. это 25 строка
        #в самом файле и она пустая.
        #print(len(self.agents_list))
        #print(self.agents_list[24])
        #Поэтому вычитаем 1.
        
        
        #Псевдослучайный номер строки списка.
        self.rnd = random.randint(0, len(self.agents_list)-1)
        #Содержимое выбранной строки из списка.
        self.random_agent = self.agents_list[self.rnd]
        
        #Добавляем "User-Agent: " чтобы использовать как заголовок.
        ##self.random_agent = "User-Agent: " + self.random_agent
        
        #---------------------------------------------------------------
        #Для отладки.
        #print(self.rnd) #Номер строки.
        #print(self.random_agent)    #Содержимое.
        print("Случайно выбранный из списка user agent: " + \
        self.random_agent)    #Содержимое с пояснением.
        #Для повышения производительности можно убрать.
        
        #print(self.agents_list[0])
        #---------------------------------------------------------------
        
        #_______________________________________________________________
        #Возвращаем строку с рандомным агентом.
        #Возможно, надо переделать без return.
        return(self.random_agent)
        #_______________________________________________________________
        
        
    
    def agents_close(self):
        #Закрываем файл агентов.
        self.agents_file.close()



if __name__ == "__main__":
    Agents().random_agent()
    Agents().agents_close()
