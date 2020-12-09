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
    TABLE_or_SCROLL = 4
    COURSE_DONE = 5

class Searchbox:
    def __init__(self):
        self.entry = None
        self.resultox = None
        self.courses_done = None
        self.vars = {int(Opt.UGRD_or_PGRD):None, int(Opt.PERC_or_NUM):None, int(Opt.TABLE_or_SCROLL):None}
        self.master=Tk()
        self.master.title("The Course Search Engine")
        self.master.geometry('500x200')

        self.body = None
        self.entry_content = None
        self.bb = None
        
    def return_entry(self, event):
        pass
    
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
        table_options = [
            "scroll",
            "table"
        ]
        options_dict = {
            Opt.UGRD_or_PGRD:grad_options,
            Opt.PERC_or_NUM:perc_options,
            Opt.TABLE_or_SCROLL:table_options
        }
        OPTIONS = options_dict[which]
        #
        var = StringVar(self.master)
        var.set(OPTIONS[1]) # default value
        
        OptionMenu(self.master, var, *OPTIONS).grid(row=which, column=0, sticky=W)

        # self.entry=Entry(self.master)
        # self.entry.grid(row=which, column=1)
        var.trace('w', self.cb_drop_down_menu)
        self.vars[which] = var

    def cb_courses_done(self, event):
        pass
        #print(self.courses_done.get())
        
    def create_label(self, _text:str, r:int, cb):
        Label(self.master, text=_text).grid(row=r, sticky=W)
        _var=Entry(self.master)
        _var.grid(row=r, column=1)    
        _var.bind('<Return>', cb)
        _var.config(width=40) # expand the width of search box
        return _var
        
    def cb__run_button(self):
        content = self.entry.get()
        under_or_post = bool("under" in self.vars[int(Opt.UGRD_or_PGRD)].get())
        perc_or_num = bool("percentage" in self.vars[int(Opt.PERC_or_NUM)].get())
        table_or_scroll = bool("table" in self.vars[int(Opt.TABLE_or_SCROLL)].get())
        try:
            self.resultox.delete(0,END)
            self.resultox.insert(0,"FOUND")
            # _tmp = 1 if self.courses_done.get() else self.courses_done.insert(END, '1521,1531,2511')
            c = Class_scrapter(content, under_or_post, perc_or_num, table_or_scroll, self.courses_done.get())

        except ArithmeticError as e: # (ValueError, IndexError)
            print(e)
            self.resultox.delete(0,END)
            self.resultox.insert(0,"404 NOT FOUND")

    def create_search_box(self):
        """
        main function 
        """
        self.create_dropdown()
        self.create_dropdown(Opt.PERC_or_NUM)
        self.create_dropdown(Opt.TABLE_or_SCROLL)
        s = int(Opt.SEARCH)
        r = int(Opt.RESULT)
        cd = int(Opt.COURSE_DONE) 
        
        self.courses_done = self.create_label("courses done:", cd, self.cb_courses_done)
        self.courses_done.insert(END, '1521,1521,1531,2511,2521,3431') # default
        self.entry = self.create_label("Search box:", s, self.return_entry)
        self.entry.insert(END, 'http://classutil.unsw.edu.au/COMP_T2.html') # default

        Label(self.master, text="Result:").grid(row=r,column=0)
        self.resultox=Entry(self.master)
        self.resultox.grid(row=r,column=1)
        
        #
        Button(self.master, text="run", command=self.cb__run_button).grid(row=7, column=1)    
        mainloop()

if __name__ == "__main__":
    
    t = Searchbox()
    t.create_search_box() # main function
