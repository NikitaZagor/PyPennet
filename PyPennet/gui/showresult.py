from tkinter import Frame, Label, Text, Scrollbar, Entry, Button
from tkinter import END, TOP, WORD, RIDGE, BOTH, RIGHT, LEFT, X, Y, SUNKEN, RAISED
from PyPennet.utility import util as my_util, constants as const

# Здесь будем отображать результат подсчета генотипов и фенотипа
class ShowResult(Frame):
    def __init__(self, parent = None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.text_width = 65
        self.initUI()

    def initUI(self):
        frameSource = Frame(self, bd = 5, relief = SUNKEN)
        frameSource.pack(side = TOP, expand = True, fill = BOTH)
        lblSource = Label(frameSource, text = 'Исходные данные', font = 'Courier 10 bold')
        lblSource.pack(side = TOP)
        self.source = Text(frameSource, height = 4, width = self.text_width, bd = 5, relief = RIDGE, font = 'Courier 10 bold', wrap = WORD)
        scrlSource = Scrollbar(frameSource, relief = SUNKEN)
        scrlSource['command'] = self.source.yview
        self.source['yscrollcommand'] = scrlSource.set
        scrlSource.pack(side = RIGHT, expand = True, fill = Y)
        self.source.pack(side=TOP, expand=True, fill = X)

        frameGenotype = Frame(self, bd = 5, relief = SUNKEN)
        frameGenotype.pack(side = TOP, expand = True, fill = BOTH)
        # Создаем метку заголовка текстового поля результата вычисления генотипов
        lblGenotype = Label(frameGenotype, text = 'Результат вычисления генотипов', font = 'Courier 10 bold')
        lblGenotype.pack(side = TOP)
        # Сщздаем текстовое поле для представления результат вычисления генотипов
        self.genotype = Text(frameGenotype, height = 4, width = self.text_width, bd = 5, relief = RIDGE, font = 'Courier 10 bold', wrap = WORD)
        # Создаем скролбар для скроллинга текста по горизонтали
        scrolbar = Scrollbar(frameGenotype, relief = SUNKEN)
        scrolbar['command'] = self.genotype.yview
        self.genotype['yscrollcommand'] = scrolbar.set
        scrolbar.pack(side = RIGHT, expand = True, fill = Y)
        self.genotype.pack(side=TOP, padx=5, pady=5, expand=True, fill = X)

        # Создаем контейнер для элементов вычисления фенотипа
        frame = Frame(self, bd = 5, relief = SUNKEN)
        frame.pack(side = TOP, padx = 5, pady = 5, expand = True, fill = BOTH)
        # Создаем метку заголовка раздела вычисления фенотипа
        lblPhenotype = Label(frame, font = 'Courier 10 bold', text = 'Вычисление фенотипов')
        lblPhenotype.pack(side = TOP)
        lblData = Label(frame, font = 'Courier 10 bold', text = 'Искомый фенотип')
        lblData.pack(side = LEFT, padx = 5, pady = 5)
        self.entrData = Entry(frame, bd = 5, relief = RIDGE, width = 10, font = 'Courier 10 bold')
        self.entrData.pack(side = LEFT, padx = 5, pady = 5)
        lblResult = Label(frame, text = 'Результат:', font = 'Courier 10 bold')
        lblResult.pack(side = LEFT, padx = 5, pady = 5)
        self.entrResult = Entry(frame, bd = 5, relief = RIDGE, width = 10, font = 'Courier 10 bold')
        self.entrResult.pack(side = LEFT, padx = 5, pady = 5)
        self.entrData.bind('<KeyPress>', self.clearResult)
        btnExec = Button(frame, text = 'Вычислить', bd = 5, relief = RAISED, command = self.execPhenotype)
        btnExec.pack(side = RIGHT, padx = 5, pady = 5)

    def clearResult(self, event):
        self.entrResult.delete('0', END)

    def execPhenotype(self):
        string = self.source.get('3.0', END).rstrip('\n')
        ss = string.split(':')
        data = ss[1].strip()
        phenotype = self.entrData.get()
        result = my_util.calcPhenotype(data,phenotype)
        self.entrResult.insert(0, result)

    def clearData(self):
        self.source.delete('1.0', END)
        self.genotype.delete('1.0', END)
        self.entrData.delete('0', END)
        self.entrResult.delete('0', END)

    def insertData(self, my_grid):
        temp = 'Заголовки колонок: ' + my_grid[const.pos_columns] + '\n'
        self.source.insert('1.0', temp)
        temp = 'Загловки строк: ' + my_grid[const.pos_rows] + '\n'
        self.source.insert('2.0', temp)
        temp = 'Данные решетки: ' + my_grid[const.pos_data] + '\n'
        self.source.insert('3.0', temp)
        if len(my_grid[const.pos_data]) > 1: #
            temp = my_util.calcGenotype(my_grid[const.pos_data])
            self.genotype.insert('1.0', temp)


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()
    #root.geometry('600x400')
    showResult = ShowResult(root)
    showResult.pack()
    root.mainloop()
