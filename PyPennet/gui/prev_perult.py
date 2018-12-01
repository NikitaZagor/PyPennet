from tkinter import Toplevel, Frame, Button, Listbox, Scrollbar
from tkinter import SINGLE, END, LEFT, RIGHT, RAISED, RIDGE, TOP, BOTH, X, Y, SUNKEN

class PrevResult(Toplevel):
    def __init__(self, grids, selected, parent=None):
        Toplevel.__init__(self, parent)
        self.parent = parent
        self.title('Параметры новой решетки')
        self.grid = grids
        self.select = selected
        self.initUI()

    def initUI(self):
        main_frame = Frame(self, bd=5, relief=RIDGE)
        main_frame.pack(side=TOP, expand=True, fill=BOTH)

        listbox = Listbox(main_frame,  width=35, height=4, selectmode=SINGLE, bd=5, relief=RIDGE)
        listbox.bind('<<ListboxSelect>>', self.selected)
        scrbary = Scrollbar(main_frame, orient='vertical')
        scrbarx = Scrollbar(main_frame, orient='horizontal')
        scrbary.config(command=listbox.yview, relief=SUNKEN)
        scrbarx.config(command=listbox.xview, relief=SUNKEN)
        listbox.config(yscrollcommand=scrbary.set, xscrollcommand=scrbarx.set)
        scrbary.pack(side=RIGHT, fill=Y)
        scrbarx.pack(side='bottom', fill=X)
        for key in self.grid.keys():
            listbox.insert(END, key)
        listbox.pack(side=TOP, expand=True, fill=BOTH)

        frame_buttons = Frame(self, bd=5, relief=RIDGE)
        frame_buttons.pack(side=TOP, expand=True, fill=X)
        btn_ok = Button(frame_buttons, text='Выбрать ', bd=5, relief=RAISED, command=self.on_ok)
        btn_ok.pack(side=LEFT, padx=5, pady=5)
        btn_cancel = Button(frame_buttons, text='Отменить', bd=5, relief=RAISED, command=self.on_cancel)
        btn_cancel.pack(side=RIGHT, padx=5, pady=5)

    def selected(self, event):
        widget = event.widget
        items = widget.curselection()
        self.select.set(widget.get(items[0]))

    def on_ok(self):
        self.destroy()

    def on_cancel(self):
        self.select.set(None)
        self.destroy()

if __name__ == '__main__':

    from tkinter import Tk, StringVar
    root = Tk()
    select = StringVar()
    grids = {'Test1': [2, 'Test1', 'R', 'r', 'Y','y','RY,Ry,rY,ry'], 'Test2': [2, 'Test1', 'R', 'r', 'Y','y','RY,Ry,rY,ry']}
    prev_res = PrevResult(grids, select, root)
    prev_res.pack_slaves()
    prev_res.focus_get()
    prev_res.grab_set()
    prev_res.wait_window()
    print(select.get())
    root.mainloop()