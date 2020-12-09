"""
https://stackoverflow.com/questions/50606250/how-do-i-return-a-word-using-the-tkinter-entry-search-bar
"""

from tkinter import*
from gui_table import Table
from class_scraper import Class_scrapter
from enum import IntEnum

class Opt(IntEnum):
    SEARCH = 0
    RESULT = 1
    UGRD_or_PGRD = 2
    PERC_or_NUM = 3
    COURSE_DONE = 4
    


class Searchbox:
    def __init__(self):
        self.entry = None
        self.resultox = None
        self.courses_done = None
        self.vars = {int(Opt.UGRD_or_PGRD):None, int(Opt.PERC_or_NUM):None}
        self.master=Tk()
        self.master.title("The Course Search Engine")
        self.master.geometry('500x200')

        self.body = None
        self.entry_content = None
        self.courses_done = None
        self.bb = None
        
    def return_entry(self, event):
        
        content = self.entry.get()
        under_or_post = bool("under" in self.vars[int(Opt.UGRD_or_PGRD)].get())
        perc_or_num = bool("percentage" in self.vars[int(Opt.PERC_or_NUM)].get())
        
        try:
            self.resultox.delete(0,END)
            self.resultox.insert(0,"FOUND")
            c = Class_scrapter(content, under_or_post, perc_or_num)

        except ArithmeticError as e:
            print(e)
            self.resultox.delete(0,END)
            self.resultox.insert(0,"404 NOT FOUND")
    
    def cb_drop_down_menu(self, *args):
        # https://stackoverflow.com/questions/56525395/save-tkinter-dropdown-menu-choice-in-a-variable-to-compare
        # res = self.var.get()
        # print(res)
        #print(bool("under" in self.var.get()))
        pass

    def create_dropdown(self, which=Opt.UGRD_or_PGRD):
        """sorting and create dropdown based on which

        Args:
            which (IntEnum): filter based on ugrd/pgrd or enrolled percentage/number. Defaults to Opt.UGRD_or_PGRD.
        """
        which = int(which)
        grad_options = [
            "postgard",
            "undergrad"
            
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
        var.set(OPTIONS[1]) # default value
        
        OptionMenu(self.master, var, *OPTIONS).grid(row=which, sticky=W)

        # self.entry=Entry(self.master)
        # self.entry.grid(row=which, column=1)
        var.trace('w', self.cb_drop_down_menu)
        self.vars[which] = var

    def cb_courses_done(self, event):
        print(self.courses_done.get())
        
    def create_label(self, _text:str, r:int, cb, _var):
        Label(self.master, text=_text).grid(row=r, sticky=W)
        self.courses_done=Entry(self.master)
        self.courses_done.grid(row=r, column=1)    
        self.courses_done.bind('<Return>', cb)
        self.courses_done.config(width=40) # expand the width of search box

    def create_search_box(self):

        self.create_dropdown()
        self.create_dropdown(Opt.PERC_or_NUM)
        s = int(Opt.SEARCH)
        r = int(Opt.RESULT)
        cd = int(Opt.COURSE_DONE) 
        #

        Label(self.master, text="cds:").grid(row=cd, sticky=W)
        self.courses_done=Entry(self.master)
        self.courses_done.grid(row=cd, column=1)    
        self.courses_done.bind('<Return>', self.cb_courses_done)
        self.courses_done.config(width=40) # expand the width of search box
        #

        l_s = Label(self.master, text="Search box:")#.grid(row=s, sticky=W)
        l_s.grid(row=s, sticky=W)
        
        self.entry=Entry(self.master)
        self.entry.grid(row=s, column=1)    
        self.entry.bind('<Return>', self.return_entry)
        self.entry.config(width=40) # expand the width of search box

        Label(self.master, text="Result:").grid(row=r,column=0)
        self.resultox=Entry(self.master)
        self.resultox.grid(row=r,column=1)
        
        mainloop()

if __name__ == "__main__":
    
    t = Searchbox()
    t.create_search_box()
