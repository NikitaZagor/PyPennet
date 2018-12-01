from tkinter.colorchooser import askcolor
from tkinter.filedialog import *
from PyPennet.utility import constants as const

# Сортирует строку символов в алфавитном порядке независимо от регистра
def sortStr(string):
    source = list(string)
    source.sort()
    if source[0].islower():
        return ''.join(source)
    else:
        result = []
        length = len(source)
        for i in range(length):
            char = ''
            if source[i] != const.orig_char:
                result.append(source[i])
                char = source[i].upper()
            else:
                continue
            for j in range(i + 1, length):
                if source[j] != const.orig_char:
                    temp = source[j].upper()
                    if temp == char:
                        result.append(source[j])
                        source[j] = const.orig_char
        return ''.join(result)

# Выбор цвета из стандартного диалога
def selectColor():
    color = askcolor()
    return color[1]

# Подсчитываем генотипы. Так как один генотип может несколько раз повторятся в данном наборе,
# то количество и процентное содержание данного генотипа мы сохраняем в словаре
# где ключом будет данный генотип, а данные - кортежиз количества и процентного содержания
def calcGenotype(string):
    ss = string.split(',') # Разбиваем строку на элементы
    num = len(ss) # Общее количество элементов
    dict_count = {} # Словарь для генотипов
    for elm in ss:
        count = ss.count(elm) # Количество данного генотипа
        proc = (count/num) * 100 # Процентное содержание данного геноттиипа
        dict_count[elm] = (count, proc) # Заносим эти данные в словарь
    result = ''
    for key in dict_count.keys():
        count, proc = dict_count[key]
        temp = '{} {} {:.2f}%, '.format(key, count, proc)
        result += temp
    result = result.rstrip(' ')
    result = result.rstrip(',')
    return result

def newList(source, data):
    result = []
    for item in source:
        if data in item:
            result.append(item)
    return result

def calcPhenResult(num_base, num_find):
    proc = (num_find/num_base) * 100
    result = '{} {:.2f}%'.format(num_find, proc)  # Формируем строку результата
    return result

#  Вычисляем данные по конкретному фенотипу
# Используем то свойство нашей сортировки строк, что символы идут в алфавитном порядке независимо от регистра
# В стандартоной сортировке сначала идут символы верхнего регистра, затем символы нижнего регистра
# Например стандартная: ACacgg, наша сортировка: AaCcgg
def calcPhenotype(string, phenotype):
    main_lst = string.split(',') # Разбиваем входную строку данных на элементы
    num = len(main_lst) # Общее количество элементов
    simbols = list(phenotype) # Преобразуем входную строку наименования фенотипа в список символов
    set_one = set() # Здесь будет символы, которые встречаются в фенотипе только один раз
    dic_more = {} # Здесь будут символы входящие в имя феноипа более одного раза
    for ch in simbols: # Заполняем множество и словарь
        number = simbols.count(ch)
        if number == 1:
            set_one.add(ch)
        else:
            dic_more[ch] = number
    notfind = False
    for ch in set_one:
        main_lst = newList(main_lst, ch)
        if len(main_lst) == 0:
            notfind = True
            break
    if notfind:
        return '0 0%'
    lst_keys = dic_more.keys()  # Получаем список двойных символов
    if len(lst_keys) == 0:  # Это значит двойных и более символов нет
        length = len(main_lst)
        result = calcPhenResult(num, length)
        return result
    notfind = False
    for key in lst_keys:
        number = dic_more[key]
        s = key * number  # Формируем строку из данного количества символов
        main_lst = newList(main_lst, s)
        if len(main_lst) == 0:
            notfind = True
            break
    if notfind:
        return '0 0%'
    else:
        length = len(main_lst)
        result = calcPhenResult(num, length)
        return result

# Здесь мы должны расчитать и сформировать результат
# Получаем список из трех строк: заглавной строки, заглавной колонки и строки данных матрицы
def calcResult(lst_string):
    genotype = calcGenotype(lst_string[2])
    result = 'Row:{}\nColumn:{}\nData:{}\nGenotype:{}\n'.format(lst_string[0], lst_string[1], lst_string[2],genotype)
    return result

# Сохранение результата в файле
def saveToFile(lst_string):
    result = calcResult(lst_string)
    save = asksaveasfilename()
    file = open(save, 'w')
    file.write(result)
    file.close()

# Получение предыдущего результата из файла
def getFromFile():
    op = askopenfilename()
    file = open(op, 'r')
    for line in file:
        if line.startswith('Data:'):
            s = line.split(':')
            return s[1].rstrip('\n')
    return None

# Формируем строку из списка Entries
def getStrFromEntries(entries):
    result =''
    for entr in entries:
        result += entr.get()
        result += ','
    result = result.rstrip(',')
    return result
