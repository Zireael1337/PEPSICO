import tkinter as tk
from tkinter import ttk

class gui(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root

        toolbar_frame = tk.Frame(root)
        nb = ttk.Notebook(root)
        table_frame = tk.Frame(nb)
        graph_frame = tk.Frame(nb)

        for i in [toolbar_frame, table_frame, graph_frame]:
            gui.toolbar_widgets(i)

        nb.add(table_frame, text="table tab")
        nb.add(graph_frame, text="graph tab")

        toolbar_frame.grid  (row=0, column=0, pady=100, padx=100)
        nb.grid             (row=0, column=1, pady=100, padx=100)


    @staticmethod
    def toolbar_widgets(frame):
        l = tk.Label(frame, width=50, height=20, bg='yellow', text=frame)
        l.pack()

def main():
    gui(root=tk.Tk()).mainloop()

if __name__ == '__main__':
    main()
