from tkinter import Toplevel, Button, Label
from PIL import Image, ImageTk

class AboutDlg():

    def __init__(self, parent=None):
        self.dlg = Toplevel(parent)
        self.dlg.pack_slaves()
        self.dlg.geometry('610x375')
        self.dlg.title = 'О Программе'
        self.dlg.resizable(False,False)
        self.initUI()

    def initUI(self):
        try:
            im = Image.open("about.jpg")
        except FileNotFoundError:
            lbl = Label(self.dlg, text='Генетический калькулятор', font=("Arial", 24, "bold"))
            lbl.place(x=80, y=20)
            lbl_name = Label(self.dlg, text='Автор: Никита Загородников', font=("Arial", 18, "bold"))
            lbl_name.place(x=120, y=100)
            lbl_mail = Label(self.dlg, text='e-mail: nikitazggor01@gmail.com', font=("Arial", 18, "bold"))
            lbl_mail.place(x=100, y=130)
        else:
            photo = ImageTk.PhotoImage(im)
            lbl = Label(self.dlg, image=photo)
            lbl.place(x=0, y=0, relheight=1, relwidth=1)
            lbl.image = photo
        finally:
            btn = Button(self.dlg, text='Закрыть', command=self.dlg.destroy)
            btn.place(x=280, y=330)

if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()
    dlg = AboutDlg(root)
    root.mainloop()