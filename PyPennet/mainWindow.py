from tkinter import Tk, Frame, Button, Menu, Toplevel
from tkinter import BOTH, RIGHT, LEFT, RAISED, RIDGE, TOP, X
from tkinter import messagebox
from tkinter import filedialog
from tkinter import messagebox as mb
import pickle
import webbrowser
from PyPennet.gui.listwindow import ListWindow
from PyPennet.gui.gridparams import GridParams
from PyPennet.gui.baseFrame import BaseFrame
from PyPennet.gui.showresult import ShowResult
from PyPennet.gui.about_dlg import AboutDlg
from PyPennet.utility import constants as const

# Глобальные переменные
root = None  # Главное окно программы
listbox = None  # Listbox со списком открытых окон (Идентификатор и заголовок окна)
show_result = None  # Контейнер резултатов обработки решетки
dic_grids = {}  # Словарь с параметрами созданных решеток. Ключ - заголовок окна

def makeMenu(root):
    main_menu = Menu(root)
    root.config(menu=main_menu)
    file_menu = Menu(main_menu, tearoff=0)
    file_menu.add_command(label='Сохранить в файл', command=save_to_file)
    file_menu.add_command(label='Загрузить из файла', command=from_file)
    file_menu.add_separator()
    file_menu.add_command(label='Закрыть', command=root.quit)
    main_menu.add_cascade(label='Файл', menu=file_menu)
    help_menu = Menu(main_menu, tearoff=0)
    help_menu.add_command(label='Справка', command=help_app)
    help_menu.add_command(label='О Программе', command=about_app)
    main_menu.add_cascade(label='Справка', menu=help_menu)

def save_to_file():
    global dic_grids
    fout = filedialog.asksaveasfilename()
    with open(fout, 'wb') as f:
        pickle.dump(dic_grids, f, 3)

def from_file():
    global dic_grids
    dic_grids.clear()
    fin = filedialog.askopenfilename()
    with open(fin, 'rb') as f:
        dic_grids = pickle.load(f, encoding='UTF-8')
    global listbox
    listbox.clear()

    for key in dic_grids.keys():
        listbox.insertData(key)

def help_app():
    webbrowser.open_new_tab("index.html")

def about_app():
    global root
    dlg = AboutDlg(root)

# При выборе записи в окне списка проверим сформирована ли уже решетка
# Если сформирована - выводим в окна результата
# Если нет - выводим сообщение о том, что надо сформировать решетку
def showSelected(selected):
    global dic_grids
    lst = dic_grids[selected]
    if len(lst[const.pos_data]) == 0:
        messagebox.showerror('Ошибка', 'Решетка ' + selected + ' еще не сформирована')
        return
    global show_result
    show_result.clearData()
    show_result.insertData(lst)

# При закрытии окна удаляем все его следы
def closeGrid(string):
    global dic_grids
    del (dic_grids[string])  # Удаляем соответствующую запись из словаря
    global listbox
    listbox.removeData(string)  # Удаляем запись из Listbox
    global root
    for item in root.winfo_children():  # Проходим по списку дочерних элементов главного окна
        cls = item.winfo_class()  # Определяем класс текущего элемента
        if cls == 'Toplevel':  # Если это окно верхнего уровня
            title = item.title()  # Читаем его заголовок
            if title == string:  # Если он равен искомому удаляем окно
                item.destroy()
                break
    global show_result
    show_result.clearData()

# При построении решетки, результат построения заносим в соответствующий элемент словаря
def execGrid(title, data):
    global dic_grids
    dic_grids[title][4] = data

# Заголовок окна заносим в список окон и его параметры в словарь lst_grids созданных решеток
def addNewGrid(root, listbox):
    listParams = []  # Список содержит строки: размер решетки; заголовок окна; заголовки колонок; заголовки строк
    global dic_grids
    gridParams = GridParams(listParams, dic_grids, root)  # Вызываем диалоговое окно для получения параметров новой решетки
    gridParams.focus_set()  # Устанавливаем фокус на окно
    gridParams.grab_set()  # Удерживаем фокус на этом окне
    gridParams.wait_window()  # Ждем завершения работы этого окна
    # Если после его отработки listParams не пустой создаем окно с решеткой и введенными праметорами
    if len(listParams) > 1:
        listParams.append('')  # Добавляем пустую строку для результата
        result = listbox.insertData(listParams[const.pos_name]) # Вставим строку с заголовком окна в Listbox
        if not result:
            return
        window = Toplevel(root) # Создаем окно верхнего уровня для размещения в нем создаваемой решетки
        size = listParams[const.pos_size]
        # Создаем решетку и размещаем ее на окне верхнего уровня
        window.title(listParams[const.pos_name])  # устанавливаем заголовок окна
        baseFrame = BaseFrame(int(size), closeGrid, execGrid, window)
        if len(listParams[const.pos_columns]) > 0:
            # Если задали заголовки колонок, устанавливаем их в решетке
            baseFrame.fill_column_titles(listParams[const.pos_columns])
        if len(listParams[const.pos_rows]) > 0:
            baseFrame.fill_row_titles(listParams[const.pos_rows])  # Аналогично с заголовками строк
        dic_grids[listParams[const.pos_name]] = listParams  # Заносим созданный класс с парамертами решетки в список

# Удаляем выбранную в Listbox решетку
def deleteGrid(root, listbox):
    global show_result
    show_result.clearData()
    string = listbox.getSelectedItem()  # Получаем строку выбранную в Listbox, это заголовок окна
    if string is not None:
        listbox.removeData(string)  # Удаляем эту строку из Listbox
        global dic_grids
        del(dic_grids[string])  # Удаляем соответствующую запись из словаря
        for item in root.winfo_children():  # Проходим по списку дочерних элементов главного окна
            cls = item.winfo_class()  # Определяем класс текущего элемента
            if cls == 'Toplevel':  # Если это окно верхнего уровня
                title = item.title()  # Читаем его заголовок
                if title == string:  # Усли он равен искомому удаляем окно
                    item.destroy()
                    break


def main():
    global root
    root = Tk()
    #root.geometry("600x400")
    root.title('Решетки Пеннета для законов Менделя')
    makeMenu(root)
    # Создаем Frame контейнер для Listbox
    frame_listbox = Frame(root, bd=5, relief=RIDGE)
    frame_listbox.pack(side=TOP, expand=True, fill=BOTH)
    global listbox
    listbox = ListWindow(showSelected, frame_listbox)  # Создаем экземпляр класса ListWindow
    listbox.pack(side=TOP)  # И размещаем его в контейнере
    # Создаем контейнер для кнопок "Добавить" и "Удалить"
    frame_btn = Frame(root, bd=5, relief=RIDGE)
    frame_btn.pack(side=TOP, expand=True, fill=X)
    btnAdd = Button(frame_btn, text='Добавить', bd=5, relief=RAISED, command=lambda: addNewGrid(root, listbox))
    btnAdd.pack(side=LEFT, padx=5, pady=5)
    btnDelete = Button(frame_btn, text='Удалить', bd=5, relief=RAISED, command=lambda: deleteGrid(root, listbox))
    btnDelete.pack(side=RIGHT)
    # Создаем экземпляр класса ShowResult и размещаем его в нашем окне
    global show_result
    show_result = ShowResult(root)
    show_result.pack(side=TOP)
    status_bar = Frame(root, bd=5, relief=RIDGE)
    status_bar.pack(side=TOP, expand=True, fill=X)
    btn_quit = Button(status_bar, text='Закрыть', command=root.quit, bd=5, relief=RAISED)
    btn_quit.pack(side=RIGHT, padx=5, pady=5)
    try:
        root.iconbitmap('app.ico')
    except:
        mb.showerror("Ошибка", "Отсутствует файл app.ico")
    root.mainloop()

if __name__ == '__main__':
    main()

