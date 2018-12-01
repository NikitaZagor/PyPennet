from tkinter import Frame, Listbox, Label, Scrollbar
from tkinter import RIGHT, RIDGE, SUNKEN, TOP, BOTH, X, Y, SINGLE, END
from tkinter import messagebox

class ListWindow(Frame):
    def __init__(self, showSelected, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.showSelected = showSelected
        self.listBox = None
        self.initUI()

    def initUI(self):
        frame_lbl = Frame(self.parent, bd=5, relief=RIDGE)
        frame_lbl.pack(side=TOP, expand=True, fill=X)
        lbl_name = Label(frame_lbl, text='Созданные решетки')
        lbl_name.pack()

        frame_listbox = Frame(self.parent)
        frame_listbox.pack(side=TOP, expand=True, fill=BOTH)
        self.listBox = Listbox(frame_listbox, width=65, height=4, selectmode=SINGLE, bd=5, relief=RIDGE)
        self.listBox.bind('<<ListboxSelect>>', self.showSelect)
        scrbary = Scrollbar(frame_listbox, orient='vertical')
        scrbarx = Scrollbar(frame_listbox, orient='horizontal')
        scrbary.config(command=self.listBox.yview, relief=SUNKEN)
        scrbarx.config(command=self.listBox.xview, relief=SUNKEN)
        self.listBox.config(yscrollcommand=scrbary.set, xscrollcommand=scrbarx.set)
        scrbary.pack(side=RIGHT, fill=Y)
        scrbarx.pack(side='bottom', fill=X)
        self.listBox.pack(side=TOP, expand=True, fill=BOTH)

    def showSelect(self, event):
        item = self.getSelectedItem()
        self.showSelected(item)

    def getSelectedItem(self):
        items = self.listBox.curselection()
        item = self.listBox.get(items[0])
        return item

    def insertData(self, item):
        count = self.listBox.size()
        for i in range(count):
            s = self.listBox.get(i)
            if s == item:
                messagebox.showerror('Ошибка', 'Окно с таким заголовком уже есть в списке')
                return False
        self.listBox.insert(END, item)
        return True

    def removeData(self, title):
        count = self.listBox.size()
        for i in range(count):
            string = self.listBox.get(i)
            if string == title:
                self.listBox.delete(i)
                break

    def clear(self):
        count = self.listBox.size()
        self.listBox.delete(0, count - 1)

if __name__ == '__main__':
    from tkinter import Tk

    def showSelected(selected):
        print(selected)

    root = Tk()
    root.title('Тест Listbox')
    frame = Frame(root)
    frame.pack(expand = True, fill = BOTH)
    listWindow = ListWindow(showSelected, frame)
    for i in range(20):
        string = 'Это окно №{:0>10}'.format(i)
        listWindow.insertData(string)
    string = 'Это окно №{:0>10}'.format(10)
    listWindow.removeData(string)
    root.mainloop()