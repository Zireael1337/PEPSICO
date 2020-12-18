import tkinter as tk
import time

class DictFrame(tk.Frame):
    def __init__(self, root, items={}, entry=True, validate="focusout", width=20, command=None):
        super().__init__(root)
        self.root = root
        self.width = width
        self.entry = entry
        self.validate = validate
        self.command = command
        self.items = {}
        self.rows = []
        self.insert(items)

    def update(self, items={}):
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
            lk = tk.Label(text=i, padx=5, pady=1, font='bold')
            lk.grid(row=n, column=0, padx=5, pady=1, sticky='W')
            if self.entry:
                self.items[i] = tk.StringVar()
                ev = tk.Entry(width=self.width,
                              textvariable=self.items[i],
                              validate=self.validate,
                              validatecommand=self.callback,
                              invalidcommand=self.callback)
                ev.insert(0, items[i] if items[i] else '')
                ev.grid(row=n, column=2, padx=5, pady=1, sticky='W')
                self.rows.append([lk, ev])
            else:
                lv = tk.Label(text=items[i], padx=5, pady=1, relief=tk.GROOVE)
                lv.grid(row=n, column=2, padx=5, pady=1, sticky='W')
                self.rows.append([lk, lv])

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
if __name__ == '__main__':
    class App(tk.Frame):
        def __init__(self, root=None):
            super().__init__(root)

            a = {'a': 123,
                 'b': 'abc',
                 'c': None}

            #list_frame = ListFrame(self, a, entry=False)
            list_frame = DictFrame(self, a, entry=True, command=self.f)
            list_frame.pack()

            a = {'m': 'ddd',
                 'n': '777'}
            self.after(2000, lambda: list_frame.insert(a))
            b = {'m': 'ppp',
                 'n': '888'}
            self.after(4000, lambda: list_frame.update(b))
            self.after(20000, lambda: list_frame.clear())

        def f(self, callback):
            print(callback)

    App(root=tk.Tk()).mainloop()

