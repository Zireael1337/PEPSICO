import tkinter as tk

class ListFrame(tk.Frame):
    def __init__(self, root, items={}, entry=False, command=None):
        super().__init__(root)
        self.root = root
        self.entry = entry
        self.items = {}
        self.rows = []
        self.command = command
        self.insert(items)

    def update(self, items={}):
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
        #print(self, self.items, self.rows)
        for n, i in enumerate(items):
            lk = tk.Label(text=i+': ')
            lk.grid(row=n, column=0, sticky='NESW')
            if self.entry:
                self.items[i] = tk.StringVar()
                ev = tk.Entry(textvariable=self.items[i],
                              validate="focusout",
                              validatecommand=self.callback,
                              invalidcommand=self.callback)
                ev.insert(0, items[i] if items[i] else '')
                ev.grid(row=n, column=2, sticky='NESW')
                self.rows.append([lk, ev])
            else:
                lv = tk.Label(text=items[i])
                lv.grid(row=n, column=2, sticky='NESW')
                self.rows.append([lk, lv])

    def callback(self):
        items = {}
        for i in self.items:
            item = self.items[i].get()
            if item == '':
                item = None
            items[i] = item
        self.command(items)
        return True


###############################################################################
if __name__ == '__main__':
    class App(tk.Frame):
        def __init__(self, root=None):
            super().__init__(root)
            a = {'a': 123,
                 'b': 'abc',
                 'c': None}
            #list_frame = ListFrame(self, a, entry=False)
            list_frame = ListFrame(self, a, entry=True, command=self.f)
            list_frame.pack()
            a = {'m': 'ddd',
                 'n': '777'}
            self.after(2000, lambda: list_frame.insert(a))
            b = {'m': 'ppp',
                 'n': '888'}
            self.after(4000, lambda: list_frame.update(b))
            self.after(15000, lambda: list_frame.clear())

        def f(self, callback):
            print(callback)


    App(root=tk.Tk()).mainloop()
