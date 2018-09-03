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
Модуль плана атаки (тестирования) для DDoSerr.
v.1.0.3.2b от 03.09.2018.

Синтаксис текстового файла со списком ссылок и пауз (attack_plan.txt):
Первая строка - URL полностью, с 'http(s)://';
Вторая строка - всремя паузы после выполнения запроса и 
подгрузки контента, в секундах, только цифрами.
Модуль (и программа) не работает с прямыми ссылками на скачивание файлов.
Размер списка, теоретически, не ограничен.
Нельзя использовать пустые строки, т.к. они обработаны как паузы.
"""

class Plan:
    def __init__(self, p_file = "attack_plan.txt"):
        self.plan_file = open(p_file, 'r')
        
    #Заводим пустые списки. 
    #Так как они вне функций, то к ним можно обратится при импорте класса!
    plan_url = []
    plan_pause = []
        
    def plan(self):
    
        #Сортировка.
        for line in self.plan_file:
            #Выбираем строки со ссылками и с задержками, сортируем на 2 списка.
            if 'http' in line:
                #Удаляем последний двойной символ новой строки (2 символа).
                line = line[:-1]
                self.plan_url.append(line)
            else:
                #Паузы. Всё, что не содержит 'http'.
                line = line[:-1]
                self.plan_pause.append(line)
        #Как вариант, не надо делать сортировку на два списка, 
        #а только один совмещённый список и потом его обрабатывать по
        #чётным и нечётным элементам.

    
    def plan_one(self, num):
        """
        Ф-я для передачи только одной пары значений, num-той.
        Список начинается с 0!
        Идея: сначала вызвать ф-ю plan(),потом передать num и вызвать эту ф-ю.
        """
        self.plan_url = Plan().plan_url
        self.plan_pause = Plan().plan_pause
        return self.plan_url[num], int(self.plan_pause[num])
    
    
    def plan_close(self):
        #Закрываем файл плана.
        self.plan_file.close()


if __name__ == "__main__":
    
    Plan().plan()
    
    plan_url = Plan().plan_url
    plan_pause = Plan().plan_pause
    
    print(plan_url)
    print('\n')
    print(plan_pause)
    
    
    plan_length = len(plan_url)
    for item in range(plan_length):
        url = plan_url[item]
        pause = plan_pause[item]
        print (url, pause)
    
    print(len(plan_url), len(plan_pause))
    
    Plan().plan_close()
    #plan = plan()
    
    #plan_url = plan().plan_url
    #plan_pause = plan().plan_pause
    #print(plan_url)
    #print('\n')
    #print(plan_pause)
