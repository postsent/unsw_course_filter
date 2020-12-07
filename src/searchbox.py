"""
https://stackoverflow.com/questions/50606250/how-do-i-return-a-word-using-the-tkinter-entry-search-bar
"""

from tkinter import*
from gui_table import Table
from class_scraper import Class_scrapter
from enum import Enum

class Opt(int, Enum):
    UGRD_or_PGRD = 0
    PERC_or_NUM = 1


class Searchbox:
    def __init__(self):
        self.entry = None
        self.resultox = None
        self.acronym_dictionary = {}
        self.vars = {Opt.UGRD_or_PGRD:None, Opt.PERC_or_NUM:None}
        self.master=Tk()
        self.master.title("The Acronym Search Engine")
        self.master.geometry('300x100')

    def return_entry(self, tmp):
        
        content = self.entry.get()
        under_or_post = bool("under" in self.vars[Opt.UGRD_or_PGRD].get())

        try:
            self.resultox.delete(0,END)
            self.resultox.insert(0,"FOUND")
            c = Class_scrapter(content, under_or_post)

        except:
            self.resultox.delete(0,END)
            self.resultox.insert(0,"404 NOT FOUND")
    
    def cb_drop_down_menu(self, *args):
        # https://stackoverflow.com/questions/56525395/save-tkinter-dropdown-menu-choice-in-a-variable-to-compare
        # res = self.var.get()
        # print(res)
        #print(bool("under" in self.var.get()))
        pass
    def create_dropdown(self, which=0):
        grad_options = [
            "undergrad",
            "postgard"
        ]
        perc_options = [
            "percentage",
            "total_number"
        ]
        options_dict = {
            Opt.UGRD_or_PGRD:grad_options,
            Opt.PERC_or_NUM:perc_options
        }
        OPTIONS = options_dict[which]
        #
        var = StringVar(self.master)
        var.set(OPTIONS[0]) # default value

        OptionMenu(self.master, var, *OPTIONS).grid(row=1, sticky=W)

        self.entry=Entry(self.master)
        self.entry.grid(row=1, column=1)
        var.trace('w', self.cb_drop_down_menu)
        self.vars[which] = var
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
