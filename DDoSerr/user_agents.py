#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Модуль для DDoSerr, считывающий файл с user agent-ами и 
записывающий их в список.
"""

import random

class Agents:

    def __init__(self, user_agents_file='user_agents.txt'):
        self.agents_list = [row.strip() for row in (open(user_agents_file))]
    

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
        
        
        self.rnd = random.randint(0, len(self.agents_list)-1)
        self.random_agent = self.agents_list[self.rnd]
        
        
        print(self.rnd)
        print(self.random_agent)
        #print(self.agents_list[0])
        
        
    
    def agents_close(self):
        #Закрываем файл агентов.
        self.user_agents.close()



if __name__ == "__main__":
    Agents().random_agent()
    #print(Agents().agents_to_list().agents_list)
    #Agents().agents_close()


"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!Добавить рандомайзер.
Сделать: при каждом вызове функции 'agents_to_list', которую надо 
переименовать в 'random_agent' и, возможно, убрать перевод в список,
надо брать из списка (или сразу из файла?) случайное поле (строку)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
