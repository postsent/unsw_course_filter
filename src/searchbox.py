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

    def return_entry(self, en):
        content = self.entry.get()
        # url = self.acronym_dictionary.get(content,"Not Found")
        c = Class_scrapter(content)
        #print(url)
        self.resultox.delete(0,END)
        self.resultox.insert(0,"hi")


    def create_search_box(self):
        master=Tk()
        master.title("The Acronym Search Engine")
        master.geometry('300x100')

        Label(master, text="Search box:").grid(row=0, sticky=W)
        self.entry=Entry(master)
        self.entry.grid(row=0, column=1)
        self.entry.bind('<Return>', self.return_entry)
        Label(master, text="Result:").grid(row=1,column=0)
        self.resultox=Entry(master)
        self.resultox.grid(row=1,column=1)
        mainloop()
t = Searchbox()
t.create_search_box()
