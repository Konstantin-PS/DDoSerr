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
Модуль парсинга HTTP страниц для DDoSerr.
v.1.4.1.3b. от 02.08.2018.
"""

"""
Легенда обозначений:
"___" - переделать / удалить;
"---" - отладка;
"~~~" - сделать;
"!" - первоочередная задача.
"""

#Подключаем модуль Beautiful Soup.
from bs4 import BeautifulSoup
#Добавляем модуль requests.
import requests


def obj_search(url):
    """
    Функция для поиска URL-ов объектов на странице.
    Находит ссылки на другие страницы, картинки (.gif, .png, .jpg), 
    CSS стили и на Java-скрипты.
    Возвращает список всех найденных ссылок (content_urls).
    """   
    #Получаем пока объект, а не файл html.
    main_page = requests.get(url)
    #Переводим объект в текст методом 'text'.
    main_page_txt = main_page.text
    
    #Получаем объект BeautifulSoup с содержимым страницы.
    soup = BeautifulSoup(main_page_txt, 'html.parser')
    
    
    #Объявляем пустую переменную, чтобы потом работать с ней.
    #(Иначе из условия if не выводился результат.
    #Всё, что объявлено под if, остаётся внутри и недоступно в ф-ции.)
    #Пустые списки.
    urls_list=[]
    urls_sort=[]
    imgs_list=[]
    imgs_sort=[]
    css_list=[]
    css_sort=[]
    java_list=[]
    java_sort=[]
    content_urls=[]
    
    
    """
    Ищем все ссылки и записываем список в переменную urls.
    """
    
    for link in soup.find_all('a'):
        #Методм поиска древа 'find_all' получаем список из строк 
        #по тэгу <a> и записываем в переменную link.
        #Из переменной link для каждого элемента списка 
        #достаём всё, что с тэгом <href>.
        #И записываем по 1 найденному элементу (не только url) 
        #в переменную urls (строка).
        urls = link.get('href')
        
        #Записываем строки в список (по одной).
        urls_list.append(urls)
        
        #Отфильтровываем элементы списка типа 'None' ('NoneType').
        urls_presort = list(filter(None, urls_list))
        
        #!Надо сортировать по имени сайта (по "http" тогда не требуется)!
        
    #Сортировка элементов списка по наличию имени сайта в строке (поле).
    for line in urls_presort:  #Убрать этот цикл.
        if url in line:
                #Делаем список из найденных строк.
                urls_sort.append(line)
    
    
    
    """    
    Ищем все картинки для подгрузки, записывем список в переменную imgs.
    Выдаёт список URL картинок (.gif, .png, .jpg) с атакуемого сайта.
    """    
    for link in soup.find_all('img'):
        imgs = link.get('src')  #Строки!
        
        #Засовываем строки в список.
        imgs_list.append(imgs)
        
        #Отфильтровываем элементы типа 'None' ('NoneType').
        imgs_presort = list(filter(None, imgs_list))
        
    #!Надо фильтровать по имени сайта (если без сторонних картинок)
    #и, что не очень гибко, по расширениям (.gif, .png, .jpg)!
        
    for line in imgs_presort:
        if url in line:
            #Выполняется, если по множественному условию в строке (line) 
            #есть любой ('any') элемент (строка) из списка условий.
            #Если нужно соблюдение всех условий, то 'all'.
            if any([('.gif' in line), ('.png' in line), ('.jpg' in line)]):
                #Делаем список из найденных строк.
                imgs_sort.append(line)
    
    
    
    """    
    Ищем все CSS стили и записываем список в переменную css.
    Выдаёт список URL стилей CSS со страницы (для подгрузки).
    """
    for link in soup.find_all('link'):
        css = link.get('href')

        #Засовываем строки в список.
        css_list.append(css)
        
        #Отфильтровываем элементы типа 'None' ('NoneType').
        css_presort = list(filter(None, css_list))
        
    #!Надо фильтровать по имени сайта и расширению .css!
        
    for line in css_presort:
        if '.css' in line:
            css_sort.append(line)
    
    
    
    """    
    Ищем все Java-скрипты и записываем список в переменную java.
    Выдаёт список URL Java-скриптов со страницы (для подгрузки).
    """
    for link in soup.find_all('script'):
        java = link.get('src')

        #Засовываем строки в список.
        java_list.append(java)
        
        #Отфильтровываем элементы типа 'None' ('NoneType').
        java_presort = list(filter(None, java_list))
        
     #!Надо фильтровать по расширению .js и, 
     #если не нужны сторонние скрипты, по имени сайта (нам нужны)!
        
    for line in java_presort:
        if '.js' in line:
            java_sort.append(line)
    
    
    

    """
    Объединяем все ссылки на подгружаемый контент в один список.
    """
    #!Список content_urls должен запрашиваться в http_requests!
    #Объединяем все списки, кроме списка со ссылками на другие страницы.
    #content_urls.append(url)    #Добавляем url начальной страницы.
    content_urls.extend(imgs_sort)
    content_urls.extend(css_sort)
    content_urls.extend(java_sort)
    
    #Возвращаем список со ссылками на весь контент.
    return(content_urls)

    


#Для самостоятельного запуска модуля.
if __name__ == "__main__":
    #Пока жёстко зададим url для отладки.
    url="https://edu.vsu.ru"
    
    #Вызываем функцию парсера.
    content_urls = obj_search(url)
    
    #Почему-то нет типа у объекта. А если возвращать значение, то работает.
    print(content_urls)
    #print(len(content_urls))
    
    
    """
    #Нет типа.
    print("Найдены следующие URL страниц: ")
    print(obj_search(url).urls_sort)
    
    print("Найдены следующие URL картинок: ")
    print(obj_search(url).imgs_sort)
    
    print("Найдены следующие URL стилей CSS: ")
    print(obj_search(url).css_sort)
    
    print("Найдены следующие URL Java-скриптов: ")
    print(obj_search(url).java_sort)

    print('\n' + "Объединённый список ссылок на контент: ")
    print(obj_search(url).content_urls)
    """
