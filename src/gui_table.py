# Python program to create a table 

from tkinter import *

class Table: 
    
    def __init__(self,root, lst): 

        # find total number of rows and 
        # columns in list 
        total_rows = len(lst) 
        total_columns = len(lst[0]) 
        # code for creating table 
        for i in range(total_rows): 
            for j in range(total_columns): 
                
                self.e = Entry(root, width=40, fg='black', 
                            font=('Arial',7,'normal')) 
                
                self.e.grid(row=i, column=j) 
                self.e.insert(END, lst[i][j]) 

if __name__ == "__main__":
    # create root window 
    lst = [(1,'Raj','Mumbai',19), 
            (2,'Aaryan','Pune',18), 
            (3,'Vaishnavi','Mumbai',20), 
            (4,'Rachna','Mumbai',21), 
            (5,'Shubham','Delhi',21)] 
    root = Tk() 
    t = Table(root, lst) 
    root.mainloop() 