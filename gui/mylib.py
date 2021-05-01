# -*- coding: utf-8 -*-
# V. 1.0

import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
from datetime import datetime


###############################################################################
class DictFrame(ttk.Frame):
    def __init__(self, root, items={}, entry=True, width=20, command=None):
        super().__init__(root)
        self.root = root
        self.width = width
        self.entry = entry
        self.command = command
        self.items = {}
        self.rows = []
        if items:
            self.insert(items)


    def update(self, items):
        if any(self.items) is False:
            self.insert(items)
        else:
            if self.entry is False:
                self.items = items
            else:
                for i in items:
                    self.items[i].set(items[i] if items[i] else '')


    def clear(self):
        for i in self.rows:
            for j in i:
                j.destroy()
        self.items = {}
        self.rows = []

    def insert(self, items={}):
        self.clear()
        for n, i in enumerate(items):
            lk = ttk.Label(self, text=i)
            lk.grid(row=n, column=0, padx=5, pady=1, sticky='W')
            if self.entry:
                self.items[i] = tk.StringVar()
                ev = ttk.Entry(self, width=self.width,
                               textvariable=self.items[i])
                ev.insert(0, items[i] if items[i] else '')
                ev.grid(row=n, column=2, padx=5, pady=1, sticky='W')
                self.rows.append([lk, ev])
            else:
                lv = ttk.Label(self, text=items[i], width=self.width,
                               relief=tk.GROOVE)
                lv.grid(row=n, column=2, padx=5, pady=1, sticky='W')
                self.rows.append([lk, lv])

    # плохо работает как callback, заменить на валидацию
    def callback(self):
        if not self.command:
            return True
        items = {}
        for i in self.items:
            item = self.items[i].get()
            if item == '':
                item = None
            items[i] = item
        self.command(items)
        return True

###############################################################################
class TableFrame(ttk.Frame):
    def __init__(self, root, df, command=None):
        super().__init__(root)
        self.root = root
        self.init = False
        self.command = command
        self.height = 20
        self.width = 100
        self.minwidth = 50
        self.tree = ttk.Treeview(self, show="headings", height=self.height, selectmode="browse")
        self.tree.bind("<ButtonRelease>", self.callback)
        self.ysb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.xsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.xsb.set, yscrollcommand=self.ysb.set)

        self.tree.grid(row=0, column=0, sticky='NESW')
        self.ysb.grid(row=0, column=1, sticky='NS')
        self.xsb.grid(row=1, column=0, sticky='WE')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        if df:
            self.insert(self, df)

    def insert(self, df):
        columns = list(df.columns)
        self.tree["columns"] = columns
        for i in self.tree["columns"]:
            self.tree.heading(i, text=i)
            self.tree.column(i, minwidth=self.minwidth, width=self.width, stretch=True)
        self.init = True
        self.root.after(1, lambda: self.update(df))


    def update(self, df):
        if self.init is False:
            self.insert(df)

        if self.tree.get_children():
            [self.tree.delete(i) for i in self.tree.get_children()]

        # генератор
        #gen = (self.tree.insert(parent='', index='end', iid=i[0], values=i[1:])\
        #        for i in df.itertuples(index=True, name=None))
        for i in df.itertuples(index=True, name=None):
            self.tree.insert(parent='', index='end', iid=i[0], values=i[1:])

        # планирование запуска генератора
        #self.tree.grid_forget()
        #self.root.after(1000, lambda: self.insert(gen))

    # рекурсивное выполнение генератора в цикле TK
    def aaa(self, gen):
        try:
            next(gen)
        except StopIteration:
            self.tree.grid(row=0, column=0, sticky='NESW')
            print(str(datetime.now()))
            return
        self.root.after(0, lambda: self.insert(gen))

    def callback(self, event):
        if not self.command:
            return True
        iid = self.tree.selection()
        if iid:
            self.command(self.tree.set(iid))
        return True


###############################################################################

if __name__ == '__main__':
    class App(ttk.Frame):
        def __init__(self, root=None):
            super().__init__(root)
            self.root = root
            #self.root.minsize(640, 360)
            self.root.geometry('1000x600')
            #self.root.maxsize(1000, 600)


            df = pd.read_csv(filepath_or_buffer=r'D:\work\terminal\bailiffs\in\Banking201201.csv',
                                       encoding='cp1251', sep=';', decimal='.',
                                       usecols = [i for i in range(0,5)],
                                       skipinitialspace=True,
                                       verbose=True, low_memory=False)


            self.d_frame = DictFrame(root, items=None, entry=False)
            self.t_frame = TableFrame(root, df=df, command=self.ff)

            self.d_frame.grid(row=0, column=0)
            self.t_frame.grid(row=1, column=0)
            self.root.grid_columnconfigure(0, weight=1)
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_rowconfigure(1, weight=1)



        def ff(self, callback):
            self.d_frame.update(callback)

    App(root=tk.Tk()).mainloop()
