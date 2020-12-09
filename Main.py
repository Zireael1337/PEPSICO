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

        """Меню"""
        self.create_menu()
        """Фреймы"""
        self.frame_toolbar = ttk.Frame(root)
        self.book = ttk.Notebook(root)

        self.frame_table = ttk.Frame(self.book)
        self.frame_graph = ttk.Frame(self.book)

        """Заполнение фреймов"""
        self.toolbar_widgets()
        self.table_widgets()
        self.graph_widgets()

        self.frame_table.grid(row=0, column=1, ipadx=5, ipady=5, padx=5, pady=5, sticky='NESW')
        self.frame_graph.grid(row=0, column=1, ipadx=5, ipady=5, padx=5, pady=5, sticky='NESW')

        """Добавление фреймов"""
        self.book.add(self.frame_table, text='page1')
        self.book.add(self.frame_graph, text='page2')



        """Сетка root"""
        self.frame_toolbar.grid(row=0, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky='NESW')
        self.book.grid(row=0, column=1, ipadx=5, ipady=5, padx=5, pady=5, sticky='NESW')


        """Настройка стилей"""
        self.settings()

    def create_menu(self):
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
        self.b_swith_frame = tk.Button(self.frame_toolbar, text="Кнопка", command = self.table_widgets()).grid(row=0, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky='NESW')
        self.listppl = tk.Listbox(self.frame_toolbar)
        self.listobr = tk.Listbox(self.frame_toolbar)


    def table_widgets(self):
        self.tree = ttk.Treeview(self.frame_table, show="headings", selectmode="browse")
        self.tree.grid(row=0, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky='NESW')


    def graph_widgets(self):
        tk.Label(self.frame_graph, text="Тут должен быть график").grid(row=0, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky='NESW')

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
        for i in [self.frame_table, self.frame_graph]:
            tk.Grid.rowconfigure(i, 0, weight=1)
            tk.Grid.columnconfigure(i, 0, weight=1)


def main():
    app = App(root=tk.Tk())
    app.mainloop()


if __name__ == '__main__':
    main()
