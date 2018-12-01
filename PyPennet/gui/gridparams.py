from tkinter import Toplevel, Frame, Button, Label, Entry, Menu, StringVar
from tkinter import END, LEFT, RIGHT, RAISED, RIDGE, TOP, BOTH, X
import PyPennet.utility.util as my_util
import PyPennet.gui.prev_perult as prev

# Вспомогательный класс контейнер для элементов основоного окна диалога
class FrameRow(Frame):
    def __init__(self, title, t_size, e_size, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.cur_font = 'Courier 10 bold'
        self.enter = None
        self.initUI(title, t_size, e_size)

    def initUI(self, title, t_size, e_size):
        frame = Frame(self.parent)
        frame.pack(side=TOP, expand=True, fill=X)
        sf = '{: <' + str(t_size) + '}'  # Шаблон для выравнивания метки контейнера к одному размеру
        s_title = sf.format(title)
        lbl = Label(frame, text=s_title, font=self.cur_font)
        lbl.pack(side=LEFT, padx=5, pady=5)
        self.enter = Entry(frame, width=e_size, bd=5, relief=RIDGE, font=self.cur_font)
        self.enter.pack(side=LEFT, padx=5, pady=5)

    def get_entry(self):
        return self.enter

# Класс диалога для определения параметов создаваемой решетки
# В качестве параметров получает: Пустой список для заполнения параметрами и ссылку на владельца окна
class GridParams(Toplevel):
    def __init__(self, lst_params, grids, parent=None):
        Toplevel.__init__(self, parent)
        self.resizable(False,False)
        self.parent = parent
        self.title('Параметры новой решетки')
        self.lst_params = lst_params
        self.grids = grids
        self.initUI()

    def initUI(self):
        grid_menubar = Menu(self, tearoff=0)
        self.config(menu=grid_menubar)
        file_menu = Menu(grid_menubar, tearoff=0)
        file_menu.add_command(label='Очистить заголовоки колонок', command=self.clearColumns)
        file_menu.add_command(label='Очистить заголовки строк', command=self.clearRows)
        file_menu.add_separator()
        file_menu.add_command(label='Заполнить колоноки из файла', command=self.fillColumns)
        file_menu.add_command(label='Заполнить заголовки из файла', command=self.fillRows)
        file_menu.add_separator()
        file_menu.add_command(label='Колонки из предыдущего результата', command=self.column_prev)
        file_menu.add_command(label='Строки из предыдущего результата', command=self.row_prev)
        file_menu.add_separator()
        file_menu.add_command(label='Закрыть', command=self.onCancel)
        grid_menubar.add_cascade(label='Файл', menu=file_menu)

        frame_params = Frame(self, bd=5, relief=RIDGE)
        frame_params.pack(side=TOP, expand=True, fill=BOTH)
        t_size = 18  # Длина всех меток
        # Контьейнер для ввода размера решетки
        frm_size = FrameRow('Размер решетки', t_size, 4, frame_params)
        self.entr_size = frm_size.get_entry()
        # Контейнер для ввода заголовка окна
        frm_title = FrameRow('Заголовок окна', t_size, 50, frame_params)
        self.entr_name = frm_title.get_entry()
        # Контейнер для ввода заголовок колонок
        frm_column_title = FrameRow('Заголовки колонок', t_size, 50, frame_params)
        self.entr_title_column = frm_column_title.get_entry()
        # Контейнер для ввода заголовок строк
        frm_row_title = FrameRow('Заголовки строк', t_size, 50, frame_params)
        self.entr_title_row = frm_row_title = frm_row_title.get_entry()

        frame_buttons = Frame(self, bd=5, relief=RIDGE)
        frame_buttons.pack(side=TOP, expand=True, fill=X)
        btnOk = Button(frame_buttons, text='Создать  ', bd=5, relief=RAISED, command=self.onOk)
        btnOk.pack(side=LEFT, padx=5, pady=5)
        btnCancel = Button(frame_buttons, text='Отменить', bd=5, relief=RAISED, command=self.onCancel)
        btnCancel.pack(side=RIGHT, padx=5, pady=5)

    def clearColumns(self):
        self.entr_title_column.delete('0', END)

    def clearRows(self):
        self.entr_title_row.delete('0', END)

    def fillColumns(self):
        string = my_util.getFromFile()
        if string is not None:
            self.entr_title_column.insert(END, string)

    def fillRows(self):
        string = my_util.getFromFile()
        if string is not None:
            self.entr_title_row.insert(END, string)

    def getEntryTitleColumns(self):
        return self.entr_title_column

    def getEntryTitleRows(self):
        return self.entr_title_row

    def column_prev(self):
        name = StringVar()
        prev_grid = prev.PrevResult(self.grids, name, self.parent)
        prev_grid.focus_set()
        prev_grid.grab_set()
        prev_grid.wait_window()
        if name is not None:
            lst = self.grids[name.get()]
            self.entr_title_column.insert(END, lst[4])

    def row_prev(self):
        name = StringVar()
        prev_grid = prev.PrevResult(self.grids, name, self.parent)
        prev_grid.focus_set()
        prev_grid.grab_set()
        prev_grid.wait_window()
        if name is not None:
            lst = self.grids[name.get()]
            self.entr_title_row.insert(END, lst[4])

    # Процедура считывания введенных параметров
    def onOk(self):
        # Должен быть введен либо размер решетки, либо заголовки колонок (и) или загололвки строк
        grid_size = self.entr_size.get().strip()
        lst_column = [s.strip() for s in self.entr_title_column.get().split(',')]
        len_column = len(lst_column)
        lst_row = [s.strip() for s in self.entr_title_row.get().split(',')]
        len_row = len(lst_row)
        if not grid_size.isdigit():
            if len_column > 1:
                grid_size = str(len_column)
            elif len_row > 1:
                grid_size = str(len_row)
            else:
                self.destroy()
                self.lst_params = []
                return
        self.lst_params.append(grid_size)
        title = self.entr_name.get().strip()
        if len(title) == 0:
            title = 'Решетка Пенета {} на {}'.format(grid_size, grid_size)  # Иначе устанавливаем стандартный заголовок
        self.lst_params.append(title)
        self.lst_params.append(self.entr_title_column.get().strip())
        self.lst_params.append(self.entr_title_row.get().strip())
        self.destroy()

    def onCancel(self):
        self.destroy()

if __name__ == '__main__':
    from tkinter import Tk

    def showDialog(lst):
        if len(lst) > 0:
            lst.clear()
        gridParams = GridParams(lst, root)
        gridParams.focus_set()
        gridParams.grab_set()
        gridParams.wait_window()
        print(lst)

    lst_params = []
    root = Tk()
    btn = Button(root, text='Show Dlg', command=lambda: showDialog(lst_params)).pack()
    root.mainloop()