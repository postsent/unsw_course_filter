from tkinter import*
from gui_table import Table

acronym_dictionary={"AKA":"Also known as", "OT":"Overtime"}

def return_entry(en):
    content=entry.get()
    result = acronym_dictionary.get(content,"Not Found")
    print(result)
    resultBox.delete(0,END)
    resultBox.insert(0,result)
    root = Tk() 
    t = Table(root) 
    root.mainloop() 

    

master=Tk()
master.title("The Acronym Search Engine")
master.geometry('300x100')

Label(master, text="Search box:").grid(row=0, sticky=W)
entry=Entry(master)
entry.grid(row=0, column=1)
entry.bind('<Return>', return_entry)
Label(master, text="Result:").grid(row=1,column=0)
resultBox=Entry(master)
resultBox.grid(row=1,column=1)
mainloop()