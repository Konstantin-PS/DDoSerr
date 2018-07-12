#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Модуль парсинга HTTP страниц для DDoSerr.
v.1.3.6b. от 12.07.2018.
"""
#Подключаем модуль Beautiful Soup.
from bs4 import BeautifulSoup


def obj_search(url):
    """
    Функция для поиска URL-ов объектов на странице.
    Находит ссылки на другие страницы, картинки (.gif, .png, .jpg), 
    CSS стили и на Java-скрипты.
    """   
    #Получаем объект BeautifulSoup с содержимым страницы html_doc.
    soup = BeautifulSoup(page, 'html.parser')
    
    
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
                
    print("Найдены следующие URL страниц: ")
    print(urls_sort)
    
    
        
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
    
    #Показываем список найденных картинок с атакуемого сайта.
    print("Найдены следующие URL картинок: ")
    print(imgs_sort)
    
    
    
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
    
    print("Найдены следующие URL стилей CSS: ")
    print(css_sort)
    
    
        
    """    
    Ищем все Java-скрипты и записываем список в переменную java.
    Выдаёт список URL Java-скриптов со страницы (для подгрузки).
    !Опять элементы 'NonType'!
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
        if url in line:
            java_sort.append(line)
            
    print("Найдены следующие URL Java-скриптов: ")
    print(java_sort)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #!content_urls должен запрашиваться в http_requests!
    #Объединяем все списки, кроме списка со ссылками на другие страницы.
    content_urls.extend(imgs_sort)
    content_urls.extend(css_sort)
    content_urls.extend(java_sort)
    
    print('\n')
    print(content_urls)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    


#Для самостоятельного запуска модуля.
if __name__ == "__main__":
    #Добавляем модуль requests.
    import requests
    #Пока жёстко зададим url для отладки модуля и запросим страницу.
    url="https://edu.vsu.ru"
    
    #Получаем пока объект, а не файл html.
    page = requests.get(url)
    #Перевод объекта в текст методом 'text'.
    page = page.text
    
    #Вызываем функцию парсера.
    obj_search(url)
    
