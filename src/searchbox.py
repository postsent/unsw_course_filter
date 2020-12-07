"""
https://stackoverflow.com/questions/50606250/how-do-i-return-a-word-using-the-tkinter-entry-search-bar
"""

from tkinter import*
from gui_table import Table
from class_scraper import Class_scrapter

class Searchbox:
    def __init__(self):
        self.entry = None
        self.resultox = None
        self.acronym_dictionary = {}
        self.var = None
        self.master=Tk()
        self.master.title("The Acronym Search Engine")
        self.master.geometry('300x100')

    def return_entry(self, en):
        
        content = self.entry.get()
        is_undergrad = bool("under" in self.var.get())
        try:
            self.resultox.delete(0,END)
            self.resultox.insert(0,"FOUND")
            c = Class_scrapter(content, is_undergrad)
        except:
            self.resultox.delete(0,END)
            self.resultox.insert(0,"404 NOT FOUND")
    
    def cb_drop_down_menu(self, *args):
        # https://stackoverflow.com/questions/56525395/save-tkinter-dropdown-menu-choice-in-a-variable-to-compare
        # res = self.var.get()
        # print(res)
        #print(bool("under" in self.var.get()))
        pass
    def create_dropdown(self):
        OPTIONS = [
            "undergrad",
            "postgard"
        ]
        #
        self.var = StringVar(self.master)
        self.var.set(OPTIONS[0]) # default value

        OptionMenu(self.master, self.var, *OPTIONS).grid(row=1, sticky=W)

        self.entry=Entry(self.master)
        self.entry.grid(row=1, column=1)
        self.var.trace('w', self.cb_drop_down_menu)

        #
    def create_search_box(self):

        self.create_dropdown()
        
        Label(self.master, text="Search box:").grid(row=0, sticky=W)
        self.entry=Entry(self.master)
        self.entry.grid(row=0, column=1)
        self.entry.bind('<Return>', self.return_entry)

        Label(self.master, text="Result:").grid(row=2,column=0)
        self.resultox=Entry(self.master)
        self.resultox.grid(row=2,column=1)
        mainloop()
t = Searchbox()
t.create_search_box()
