from tkinter import Frame, Button, Menu, StringVar
from tkinter import BOTH, END, LEFT, RIGHT, RAISED, SUNKEN, TOP, X
from PyPennet.gui.baseEntry import BaseEntry
import PyPennet.utility.util as my_util

class BaseFrame:
    def __init__(self, num, onClose, onExecution, parent=None):
        self.parent = parent
        self.onClose = onClose
        self.onExecution = onExecution
        if(parent is not None):
            parent.resizable(False, False)   # Запрещаем изменение размеров окна
        self.countColumn = num
        self.entries = []   # В этом списке num X num будут храниться ссылки на entry результатов
        for i in range(num):
            self.entries.append([])
        self.columnTitles = []   # В этом списке будут храниться ссылки на entry заглавной строки
        self.rowTitles = []  # В этом списке будут храниться ссылки на entry заглавной колонки
        self.curResult = StringVar()
        self.initUI()

    def initUI(self):
        # Создаем контейнер для размещения матрицы полей ввода данных и вывода результатов
        self.entryFrame = Frame(self.parent, bd = 5, relief = SUNKEN)
        # Создаем меню
        self.makeMenu()
        # Размещаем поля ввода данных для верхней строки и запоминаем ссылки на них в списке: firstRow
        for i in range(self.countColumn + 1):
            entr = BaseEntry(self.countColumn, self.entryFrame)
            if i != 0:
                self.columnTitles.append(entr)
                entr.grid(row = 0, column = i, padx = 10, pady = 10)

        # Размещаем поля ввода для первой колонки и для строк вывода результатов
        for i in range(self.countColumn):
            for j in range(self.countColumn + 1):
                entr = BaseEntry(self.countColumn, self.entryFrame)
                if j == 0:  # Это первое поле колонки
                    self.rowTitles.append(entr)
                else:  # Это поле матрицы результата
                    self.entries[i].append(entr)
                    entr.setReadOnly()
                entr.grid(row=i+1, column=j, padx = 10, pady = 10)
        self.entryFrame.pack(side = TOP,  expand = True, fill = BOTH)

        # Размещаем командные кнопки
        self.frameBtn = Frame(self.parent, bd=5, relief=SUNKEN)
        self.btnExec = Button(self.frameBtn, text='Построить', command=self.onExec,  bd=5, relief=RAISED)
        self.btnExec.pack(side = LEFT, padx = 10, pady = 10)
        self.btnExit = Button(self.frameBtn, text='Закрыть', command=self.onExit,  bd=5, relief=RAISED)
        self.btnExit.pack(side = RIGHT, padx = 10, pady = 10)
        self.frameBtn.pack(side = TOP, expand = True, fill = X)

    def makeMenu(self):
        menubar = Menu(self.parent, tearoff=0)
        self.parent.config(menu=menubar)
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label='Сохранить результат', command = self.saveResult)
        clear_menu = Menu(file_menu, tearoff=0)
        clear_menu.add_command(label='Очистить заголовоки колонок', command = self.clearRow)
        clear_menu.add_command(label='Очистить заголовки строк', command = self.clearColumn)
        clear_menu.add_command(label='Очистить результат', command = self.clearGrid)
        file_menu.add_cascade(label='Очистить данные', menu = clear_menu, underline = 0)
        use_menu = Menu(file_menu, tearoff=0)
        use_menu.add_command(label='Заполнить заголовоки колонок', command = lambda: self.fill_column_titles(''))
        use_menu.add_command(label='Заполнить заголовки строк', command = lambda: self.fill_row_titles(''))
        file_menu.add_cascade(label='Использовать результат',menu = use_menu, underline = 0)
        file_menu.add_separator()
        file_menu.add_command(label='Закрыть', command = self.onExit)
        menubar.add_cascade(label='Файл', menu=file_menu)

    def onExit(self):
        title = self.parent.title()
        result = self.curResult.get()
        if len(result.strip()) == 0:
            self.onClose(title)
        self.parent.destroy()

    def onExec(self):  # Заполняем ячейки сетки и формируем строку содержимого ячеек
        self.curResult.set('')  # Обнуляем текущие данные
        tmp = ''
        for i in range(self.countColumn):  # Прхолим по строкам таблицы
            for j in range(self.countColumn):  # Проходим по колонкам таблицы
                valRow = self.rowTitles[i].get()
                valColumn = self.columnTitles[j].get()
                if len(valRow) != 0 and len(valColumn) != 0:
                    result = valRow + valColumn  # Результат соединение строки из ячейки первой колонки
                    result = my_util.sortStr(result)     # и строки из ячейки первой строки
                    entr = self.entries[i][j]
                    entr['width'] = len(result) + 1
                    entr.setText(result)         # Заносим текст в ячейку результата
                    tmp += result     # Накапливаем результат вы строке результата
                    tmp += ','        # Разделяем данные запятой
        tmp = tmp.rstrip(',')
        self.curResult.set(tmp)
        title = self.parent.title()
        self.onExecution(title, self.curResult.get())

    def saveResult(self):
        if len(self.curResult.get()) > 0:
            result = []
            row = my_util.getStrFromEntries(self.columnTitles)
            result.append(row)
            column = my_util.getStrFromEntries(self.rowTitles)
            result.append(column)
            result.append(self.curResult.get())
            my_util.saveToFile(result)

    def fillEntries(self, entryLst, string):
        lst = [s.strip() for s in string.split(',')]
        length = len(lst)
        # Очистим ячейки
        for i in range(self.countColumn):
            entryLst[i].delete(0, END)
        # Заносим новые значения
        if length > self.countColumn:
            for i in range(self.countColumn):
                entryLst[i].insert(0, lst[i])
        else:
            for i in range(length):
                entryLst[i].insert(0, lst[i])

    def fill_column_titles(self, string):
        if len(string) == 0:
            prevResult = my_util.getFromFile()
            if prevResult != None:
                self.fillEntries(self.columnTitles, prevResult)
        else:
            self.fillEntries(self.columnTitles, string)

    def fill_row_titles(self, string):
        if len(string) == 0:
            prevResult = my_util.getFromFile()
            if prevResult != None:
                self.fillEntries(self.rowTitles, prevResult)
        else:
            self.fillEntries(self.rowTitles, string)

    def clearRow(self):
        for entr in self.columnTitles:
            entr.setText('')

    def clearColumn(self):
        for entr in self.rowTitles:
            entr.setText('')

    def clearGrid(self):
        for i in range(self.countColumn):
            for j in range(self.countColumn):
                self.entries[i][j].setText('')

if __name__ == '__main__':
    from tkinter import Toplevel, Tk, Label, Entry
    def showTopLevel(parent, entr):
        window = Toplevel(parent)
        size = entr.get()
        dim = int(size)
        baseFrame = BaseFrame(dim, window)

    root = Tk()
    btn = Button(root, text = 'Show', command = lambda: showTopLevel(root, entr))
    btn.grid(row = 0, column = 0, padx = 10, pady = 10)
    lbl = Label(text = 'Размер')
    lbl.grid(row = 0, column = 1, padx = 10, pady = 10)
    entr = Entry(root, width = 4)
    entr.grid(row = 0, column = 2,padx =  10, pady = 10)

    root.mainloop()
