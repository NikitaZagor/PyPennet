from tkinter import *
import PyPennet.utility.util as my_util
import PyPennet.utility.constants as const

class BaseEntry(Entry):
    def __init__(self, w, parent=None):
        Entry.__init__(self, parent)
        self.menu = None
        self.initUI(w)

    def initUI(self, w):
        # Расчитываем размер символов полей ввода
        fsize = 22 - w
        if fsize < 10:
            fsize = 10
        strFont = 'Helvetica {} bold'.format(str(fsize))
        # Определяем ширину поля ввода, фонт и положение текста в нем
        self.config(width=w + 2, font=strFont, justify=CENTER, bd=5, relief=RIDGE)
        # Привязываем процедуру сортировки строки к событию ввода символов в поле ввода
        # Если мы введем аА, то получим Аа
        self.bind('<KeyRelease>', self.sortStr)
        # Создаем всплывающее меню
        self.menu = Menu(self, tearoff=0)
        self.menu.add_command(label='Цвет фона', command=lambda: self.setBackGround(None))
        self.menu.add_command(label='Цвет текста', command=lambda: self.setForeGround(None))
        self.bind('<Button-3>', self.showMenu)

    def showMenu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def getText(self): # Получаем строку из поля ввода
        return self.get()

    def setText(self, string):  # Заносим строку в поле ввода
        # Так как поля ввода для резултата имеют статус только для чтения, то их надо венуть в нормальное
        # состояние,записать текст, а затем опять вернуть в предыдущее состояние
        state = self['state']  # Определяем статус поля ввода
        if state == DISABLED:
            self['state'] = NORMAL
        if len(self.get()) > 0:  # Усли в поле ввода есть текст - удаляем его
            self.delete(0, END)
        if len(string) > 0:
            self.insert(0, string)  # Записываем текст в поле ввода
        if state == DISABLED:  # Устанавливаем статус в предыдущее состояние
            self['state'] = DISABLED

    def setBackGround(self,color):  # Устанавливаем цвет фона поля ввода
        if color is None:
            color = my_util.selectColor()
        state = self['state']
        if state == DISABLED:
            self['state'] = NORMAL
        self.config(bg=color)
        self['state'] = state

    def setForeGround(self, color):  # Устанавливаем цвет текста поля ввода
        if color is None:
            color = my_util.selectColor()
        state = self['state']
        if state == DISABLED:
            self['state'] = NORMAL
        self.config(fg=color)
        self['state'] = state

    def sortStr(self, event):  # Прцедура сортировки текста в поле ввода
        s = self.get()
        if len(s) > 0:
            if const.orig_char in s:  # Так как символ $ используется в подпрограмме сортировки, то запретим его ввод
                i = s.index('$')
                self.setText(s[:i])
            else:
                ss = my_util.sortStr(s)
                self.setText(ss)

    def setReadOnly(self):  # Установка поля ввода в состояние ТОЛЬКО ДЛЯ ЧТЕНИЯ
        state = self['state']
        if state == NORMAL:
            self['state'] = DISABLED

if __name__ == '__main__':
    root = Tk()
    frame = Frame(root)
    frame.pack(side=TOP)
    be = BaseEntry(8, frame)
    be.setText('Test')
    be.setBackGround('blue')
    be.setForeGround('yellow')
    be.pack()
    print(be.getText())
    root.mainloop()
