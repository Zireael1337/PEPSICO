import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import pandas as pd
import numpy as np

# гавно гавно гавно
#123
# гавно гавно

class App(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root

        """Создание Меню"""
        self.window_menu()
        """Фреймы в главном окне"""
        self.toolbar = ttk.Frame(root)
        self.book = ttk.Notebook(root)
        self.book.bind('<<NotebookTabChanged>>', self.tab_change)
        """Создание виджетов"""
        self.toolbar_widgets()
        #self.frames_widgets()
        self.tree = ttk.Treeview(root, show="headings", selectmode="browse")

        """Создание фреймов(вкладок)"""
        self.frames = {'lt_to_cr': {'devices': 'Оборудование, рабочее время',
                                    'personal': 'Загрузка персонала',
                                    'percent': 'Процент выполнения диаграмма'},
                        'cr_to_obj': {}}

        for i in self.frames['lt_to_cr'].keys():
            exec(f"self.{i} = ttk.Frame(self.book)")
            frm = eval(f"self.{i}")
            self.frames['cr_to_obj'][self.frames['lt_to_cr'][i]] = frm
            frm.grid(row=0, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky='NESW')
            self.book.add(frm, text= self.frames['lt_to_cr'][i])
            tk.Grid.rowconfigure(frm, 0, weight=1)


        #self.graph_widgets()

        #self.frame_table.grid(row=0, column=1, ipadx=5, ipady=5, padx=5, pady=5, sticky='NESW')
        #self.frame_graph.grid(row=0, column=1, ipadx=5, ipady=5, padx=5, pady=5, sticky='NESW')

        """Добавление фреймов"""
        #self.book.add(self.frame_table, text='page1')
        #self.book.add(self.frame_graph, text='page2')



        """Сетка root"""
        self.toolbar.grid(row=0, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky='NESW')
        self.book.grid(row=0, column=1, ipadx=5, ipady=5, padx=5, pady=5, sticky='NESW')

        """Настройка стилей"""
        self.settings()

    def window_menu(self):
        main = tk.Menu(self.root)
        self.root.config(menu=main)
        settings = tk.Menu(main, tearoff=0)
        settings.add_command(label="Open", command=self.openfile)
        main.add_cascade(label="File", menu=settings)

    def openfile(self):
        """Диалог файла"""
        path = fd.askopenfile(parent=self.root,
                              filetypes=[("Excel", "*.xlsx")]).name
        """Датафрейм"""
        self.df = pd.read_excel(io=path, verbose=True)
        self.df = self.df.replace(np.nan,'', regex=True)
        """Хуня с Tree"""
        for item in self.tree.get_children(): self.tree.delete(item)
        self.tree.config(columns = list(self.df.columns))
        for col in self.df.columns:
            self.tree.heading(col, text=str(col))
        for row in self.df.itertuples():
            self.tree.insert('', 'end', values = tuple(row[1:]))

    def workerlist(self):
        df = self.df
        workerlist = df.groupby("Рабочее место").sum()
        workerlist = workerlist.index.values
        workerlist = ", ".join(workerlist)
        self.ppl = workerlist

    def techplace(self):
        df = self.df
        #print(df)
        techplace = df.groupby("Название").sum()
        techplace = techplace.index.values
        techplace = ", ".join(techplace)
        self.obr = techplace

    def inserttext(self, k):
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


    def toolbar_widgets(self):
        self.df = None
        self.b_swith_frame = tk.Button(self.toolbar, text="Кнопка").grid(row=0, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky='NESW')
        self.listppl = tk.Listbox(self.toolbar)
        self.listobr = tk.Listbox(self.toolbar)


    def frames_widgets(self):
        self.tree = ttk.Treeview(self, show="headings", selectmode="browse")
        #.grid(row=0, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky='NESW')

    def tab_change(self, event):
        tab = event.widget.tab('current')['text']
        frm = self.frames['cr_to_obj'][tab]
        self.tree.grid(in_=frm, row=0, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky='NESW')



   # def graph_widgets(self):
    #    tk.Label(self.frame_graph, text="Тут должен быть график").grid(row=0, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky='NESW')

    def settings(self):
        """Настройка стиля"""
        self.root.title("ТЕСТ")
        self.root.minsize(640, 360)
        self.root.geometry('848x480')
        self.root.maxsize(1280, 720)
        style = ttk.Style(self.root)
        style.configure('Treeview', rowheight=30)
        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 0, weight=0)
        tk.Grid.columnconfigure(self.root, 1, weight=1)
        #for i in [self.frame_table, self.frame_graph]:
         #   tk.Grid.rowconfigure(i, 0, weight=1)
          #  tk.Grid.columnconfigure(i, 0, weight=1)


def main():
    app = App(root=tk.Tk())
    app.mainloop()


if __name__ == '__main__':
    main()
