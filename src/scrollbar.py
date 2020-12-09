"""
https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter
"""
import tkinter as tk

class Scrollbar(tk.Frame):
    def __init__(self, parent, res:list):

        self.result = res
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff", width=800, height=600)
        self.frame = tk.Frame(self.canvas, background="#ffffff", width=100, height=100)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.populate()

    def populate(self):

        '''Put in some fake data'''
        for row, i in enumerate(self.result):
            
            a,b,c,d,e,f = i
            tk.Label(self.frame, text=a, width=10).grid(row=row+1, column=0)
            for n, t in enumerate(i[1:]):
                tk.Label(self.frame, text=t).grid(row=row+1, column=n+1)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root=tk.Tk()
    example = Scrollbar(root)
    example.pack(side="top", fill="both", expand=True)
    root.mainloop()