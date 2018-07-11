#!/usr/bin/python3
#Путь к интерпретатору пайтона.
# -*- coding: utf-8 -*-
#Выбор кодировки (без него не работает русский язык).

"""
Модуль парсинга HTTP страниц для DDoSerr.
v.1.2.4b. от 11.07.2018.
"""
#Подключаем модуль Beautiful Soup.
from bs4 import BeautifulSoup
#Подключаем модуль работы с csv файлами.
#import csv


def obj_search(url):
    """
    Функция для поиска URL-ов на странице.
    Записывает найденный URL-ы в файл "urls.txt".
    """   
    #Получаем объект BeautifulSoup с содержимым страницы html_doc.
    soup = BeautifulSoup(page, 'html.parser')

    #Ищем все ссылки и записываем список в переменную urls.
    for link in soup.find_all('a'):
        #Получаем список из строк по тэгу <a> и записываем в перем. link.
        
        #Из переменной link для каждого элемента списка 
        #достаём всё, что с тэгом <href>.
        #И записываем по 1 найденному элементу (не только url) 
        #в переменную urls - список.
        urls = link.get('href')
        
        #print("URLS type " + str(type(urls)))
        
    #urls = soup.find_all('a').get('href')
    
        #-----
        #Показываем ссылки. Для отладки.
        #print(str(urls))
        #-----
        
        #!Надо фильтровать по "http" и по имени сайта!

        
        #Надо избавиться от элементов списка типа 'NonType'.
        #Плохой способ, переводящий в строки всё подряд.
        #Переводим всё в строки, т.к. есть элементы 'NonType' и 
        #затем в список с разделителем (новая строка).
        urls = str(urls).split()
        
        
        
        #-----
        #print(type(urls))
        #print(urls)
        #-----
        
        
        #Объявляем пустую переменную, чтобы потом работать с ней.
        #(Иначе из условия if не выводился результат.)
        #(Всё, что объявлено под if, остаётся внутри и недоступно в ф-ции.)
        #urls_sort_str=""   #Пустая строка.
        urls_sort=[]    #Пустой список.
        
        #Сортировка строк.
        for line in urls:
            """
            #По наличию слова 'http'. Возможно, и не надо, 
            #т.к. далее используется имя сайта.
            if "http" in line:
                #-print("Работает")
                #-print(line)
                #print(line, end='\n')
                #Перезапись после первой правки.
                urls_sort = line
                #print(urls_sort)
            """
            #По наличию имени сайта в строке.
            if url in line:
                #!!Почему возвращает True, если строка line пустая, выполняя запись пустого элемента в список??
                #Оно работает вне зависимости от ответа (true или false)!
                
                #Сохраняем найденную строку в переменную.
                #!Записывается только ОДНА строка 
                #(каждый раз перезаписывая предыдущую).
                #urls_sort = line
                
                #Добавляем в список строки.
                #!Добавляются и пустые элементы списка на места, 
                #где были отброшенные строки.
                urls_sort.append(line)
                #print(line+'\n')
                #Удаление лишних пустых элементов.
                #[x for x in urls_sort if x]
                #' '.join(urls_sort).split()
                #urls_sort = list(filter(None, urls_sort))
                #urls_sort = [x for x in urls_sort if x != []]
                
                
                #Переводим в списки.
                #urls_sort = line.split('\n')

                
                #print(type(urls_sort))
                #print(urls_sort)
            else:
                print("False")
                
        print(urls_sort)
        #print(urls)
        
    ##print(type(urls_sort))
    ##print(len(urls_sort))
    
    ##print('\n'.join(urls_sort))
    
    #for line in urls_sort:
    #    print(line)    
        
        
    #Ищем все картинки для подгрузки, записывем список в переменную imgs.
    for link in soup.find_all('img'):
        imgs = link.get('src')
        #-----
        #print(str(imgs))
        #-----
        
        #!Надо фильтровать по имени сайта (если без сторонних картинок)
        #и, что не очень гибко, по расширениям (.gif, .png, .jpg)!
        
        
    #Ищем все CSS стили и записываем список в переменную css.
    for link in soup.find_all('link'):
        css = link.get('href')
        #-----
        #print(str(css))
        #-----
        
        #!Надо фильтровать по имени сайта и расширению .css!
        
        
    #Ищем все Java-скрипты и записываем список в переменную java.
    for link in soup.find_all('script'):
        java = link.get('src')
        #-----
        #print(str(java))
        #-----
        
        #!Надо фильтровать по расширению .js и, 
        #если не нужны сторонние скрипты, по имени сайта (нам нужны)!
        
        
        """
        #!!!!!Фильтровать внутри циклов поиска, до записи!!!!!
        #!Записывать в переменную (список) только то, 
        #что соответствует требованиям!
        """

        

    
    """
    #Проба поиска строк простым методом.
    #РАБОТАЕТ со списками и, вроде бы, со строками в тройных кавычках!
    word = "ku"
    string = "123353434 
    vmcklfdk 
    ku 
    ffewf"
    
    list = ['123353434', 'vmcklfdk', 'ku', 'ffewf']
    print(string)
    for line in list:
        if word in line:
            print("Работает")
            print(line)
    """
    
    """
    !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    !Надо использовать метод строки find для поиска подстрок в строке!
    !Из найденных результатов надо отбирать только те, которые начинаются
    на http и относятся к атакуемому сайту (содержат урл сайта)!
    
    !Не использовать файл для временного хранения урлов!
    
    !Переделать механизм поиска ссылок: надо искать не в тегах <a>,
    а в других, например, <img> для картинок. И искать надо
    не <href>, а <src>!
    !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """

#Для самостоятельного запуска модуля.
if __name__ == "__main__":
    #Добавляем модуль requests.
    import requests
    #Пока жёстко зададим url для отладки модуля и запросим страницу.
    url="https://edu.vsu.ru"
    #Получаем пока объект, а не файл html.
    page = requests.get(url)
    #Перевод в текст.
    page = page.text
    
    #Вызываем функцию парсера.
    obj_search(url)
    
