import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
#from tkinter import Menu
#from datetime import timedelta, datetime
#from tkcalendar import Calendar, DateEntry
import re
import matplotlib

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd

LARGE_FONT = ("Verdana", 12)

def normalization(row):
    if not pd.isna(row):
        row = re.sub(r'\s*/\s', '/', row)
        row = re.sub(r'\s*[*]\s*', '', row)
        row.strip()
        fw = re.match(r'^[а-я]', row)
        if fw:
            row = re.sub(r'^[а-я]', fw[0].upper(), row)
    return row

def openxlsx():
    file = fd.askopenfile(filetypes=[("Excel", "*.xlsx")])
    if not file:
        mb.showinfo("Открытие файла", "Файл не выбран!")
    else:
        MESPEPSI.text = pd.read_excel(file.name)


# Основной класс окна. Здесь происходит вызов и смена фреймов.
class MESPEPSI(tk.Tk):
    text = None
    ne_toro = None
    worktime = None
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("1000x600")
        file = fd.askopenfile(filetypes=[("Excel", "*.xlsx")])
        MESPEPSI.ne_toro = pd.read_excel('Заказы не TOPO.xlsx')
        MESPEPSI.ne_toro['Задачи HE TOPO'] = MESPEPSI.ne_toro['Задачи HE TOPO'].apply(normalization)
        MESPEPSI.worktime = pd.read_excel('Рабочее время 2020.xlsx')
        MESPEPSI.worktime = MESPEPSI.worktime[['Рабочее место', 'Часы месяц']]
        print(MESPEPSI.worktime.columns.values)
        print(MESPEPSI.worktime)
        if not file:
            mb.showinfo("Открытие файла", "Файл не выбран!")
        else:
            MESPEPSI.text = pd.read_excel(file.name)
        # Всплывающее меню
        mainmenu = tk.Menu(self)
        self.config(menu=mainmenu)
        filemenu = tk.Menu(mainmenu, tearoff=0)
        filemenu.add_command(label="Открыть...", command=lambda: openxlsx())
        filemenu.add_command(label="Выход", command=self.destroy)
        mainmenu.add_cascade(label="Файл", menu=filemenu)
        # Хранилище инициализированных фреймов.
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
        """так должно быть:"""
        self.StartPage = self.frames[StartPage]
        """self.frames[StartPage] <-- это обьект фрейма
        """
        self.frames[StartPage].grid(row=0, column=0, sticky='NESW')
        self.frames[PageOne].grid(row=0, column=1, sticky='NESW')
        self.frames[PageTwo].grid(row=0, column=1, sticky='NESW')


        self.show_frame(StartPage)
        self.workerlist(self.text)
        self.techplace(self.text)


    # Функция вывода на экран фрейма
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        print('eeeeeeeeeeeeeeeeee')
        print(self.frames[StartPage].listppl.size())
        print(self.StartPage.listppl.size())

    def workerlist(self, df1):
        df = self.text
        workerlist = df.groupby("Рабочее место").sum()
        workerlist = workerlist.index.values
        workerlist = ", ".join(workerlist)
        # with pd.option_context('display.max_rows', None, 'display.max_columns',
        #                      None):  # more options can be specified also
        #print(workerlist)
        StartPage.ppl = workerlist

    def techplace(self, df):
        df = self.text
        #print(df)
        techplace = df.groupby("Название").sum()
        techplace = techplace.index.values
        techplace = ", ".join(techplace)
        #print(techplace)
        StartPage.obr = techplace



# Класс Окна главного меню. Вызывается при старте программы
class StartPage(tk.Frame):
    ppl: str = ""
    obr: str = ""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.text = tk.Text(self, height=8)
        label = tk.Label(self, text="Главное меню", font=LARGE_FONT)
        label.pack(anchor='nw', side="top")
        # self.listppl = tk.Listbox(self)
        # self.listobr = tk.Listbox(self)
        button = tk.Button(self, text="График",
                           command=lambda: controller.show_frame(PageOne), width="35")

        button.pack(anchor='nw', side="top")

        button2 = tk.Button(self, text="Таблица",
                            command=lambda: controller.show_frame(PageTwo), width="35")
        button2.pack(anchor='nw', side="top")

        button3 = tk.Button(self, text="Список работников",
                            command=lambda: self.inserttext('ppl'), width="35")
        button3.pack(anchor='nw', side="top")

        button4 = tk.Button(self, text="Список оборудования",
                            command=lambda: self.inserttext('obr'), width="35")
        button4.pack(anchor='nw', side="top")
        self.listppl = tk.Listbox(self)
        self.listobr = tk.Listbox(self)
        # self.inserttext(listppl, StartPage.df)

        # self.inserttext(listobr, StartPage.df1)

    def inserttext(self, k):
        sw = {'ppl': {'list': self.listppl,
                      'df': StartPage.ppl},
              'obr': {'list': self.listobr,
                      'df': StartPage.obr}}
        sw[k]['list'].delete(0, tk.END)
        sw[k]['list']["width"] = "40"
        sw[k]['list']["height"] = "40"
        for i in sw[k]['df'].split(","):
            sw[k]['list'].insert(tk.END, i)
        sw[k]['list'].pack(anchor="nw", padx=10, pady=10)
        """
        if k == 'ppl':
            self.listppl.delete(0, tk.END)

        if k == 'obr':
            self.listobr.delete(0, tk.END)
            self.listobr["width"] = "40"
            self.listobr["height"] = "40"
        sw = {'ppl': {'list': self.listppl,
                      'df': StartPage.ppl},
              'obr': {'list': self.listobr,
                      'df': StartPage.obr}}

        for i in sw[k]['df'].split(","):
            sw[k]['list'].insert(tk.END, i)
        sw[k]['list'].pack(anchor="nw", padx=10, pady=10)
        # self.list2["selectmode"] = "extended"
        # self.list2["width"] = "50"
        # self.list2["height"] = "20"
        """

# График
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="График", font=LARGE_FONT)
        label.pack(anchor='nw', side="top")

        button1 = tk.Button(self, text="Главное меню",
                            command=lambda: controller.show_frame(StartPage), width="35")
        button1.pack(anchor='nw', side="top")

        button2 = tk.Button(self, text="Таблица",
                            command=lambda: controller.show_frame(PageTwo), width="35")
        button2.pack(anchor='nw', side="top")

        # button3 = tk.Button(self, text="Показать таблицу",
        #                    command=None)
        # button3.pack(anchor='nw', side="left")

        # self.table = ttk.Treeview()
        # self.table.pack()


# Таблица
class PageTwo(tk.Frame):
    zb = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Таблица", font=LARGE_FONT)
        label.pack(anchor='nw', side="top")

        button1 = tk.Button(self, text="Главное меню",
                            command=lambda: controller.show_frame(StartPage), width="35")
        button1.pack(anchor='nw', side="top")

        button2 = tk.Button(self, text="График",
                            command=lambda: controller.show_frame(PageOne), width="35")
        button2.pack(anchor='nw', side="top")

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        # PageTwo.createtable(table, MESPEPSI.text)
        # button3 = tk.Button(self, text="Показать график",
        #                  command=PageTwo.createtable(table, MESPEPSI.text))
        # button3.pack(anchor='nw', side="top")

        button3 = tk.Button(self, text="Вывести таблицу",
                            command=lambda: self.createtable(table, MESPEPSI.text), width="35")
        button3.pack(anchor='nw', side="top")

        button4 = tk.Button(self, text="Вывести рабочее время",
                            command=lambda: self.createtable(table, MESPEPSI.worktime), width="35")
        button4.pack(anchor='nw', side="top")

        button5 = tk.Button(self, text="Вывести список НЕ ТОРО",
                            command=lambda: self.createtable(table, MESPEPSI.ne_toro), width="35")
        button5.pack(anchor='nw', side="top")

        PageTwo.createtable(table, MESPEPSI.text)

    @staticmethod
    def createtable(table, df):
        x = table.get_children()
        table.delete(*table.get_children())
        # df=MESPEPSI.text
        # table.text = df.columns.values
        columns = df.columns.values
        print(df)
        table["columns"] = tuple(columns)

        #print(table["columns"])
        # for i in columns:
        #    table.heading(i, text=columns[i])
        if len(x) == 0:
            scrollx = tk.Scrollbar(table, orient="horizontal", command=table.xview)
            scrollx.pack(side="bottom", fill="x")
        if len(x) == 0:
            scrolly = tk.Scrollbar(table, orient="vertical", command=table.yview)
            scrolly.pack(side="right", fill="y")
        # table.configure(yscrollcommand=scrolly.set)
        for i, j in enumerate(df):
            table.heading(f"#{i+1}", text=j)
            #print(table.heading(f"#{i}", text=j))
        # self.parent = parent
        # self.tree = ttk.Treeview(self, columns=self.text[1:])
        # vsb = tk.Scrollbar(orient="vertical", command=table.yview)
        # table.configure(yscrollcommand=vsb.set)
        for i in df.values:
            table.insert("", tk.END, values=tuple(i))

        table.pack(side="left", expand=True, fill="both")

        # vsb.pack(side="right", fill="y")


#        for i in range(len(df[table.text[0]])):
#            table.insert('', 'end', text=df,
#                         values=list(map(lambda x: df[x][i], table.text[1:])))
# self.tree.pack(side="top", expand=True, fill="both")


app = MESPEPSI()
app.mainloop()
