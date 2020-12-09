"""
given the order of course listed is in ascending order
"""

"""
Notes:
below approach by using search button on source page e.g. if cu10 not found, then ignore
cu00 - less than half
cu50 - over half
cu80 - over 80
cufull - full

new found:
cuwarn: (/stop)
<td>CRS</td><td>CR02</td><td> 2453</td><td></td><td class="cuwarn">Stop</td><td>173/173</td> <td class="cufull">100%&nbsp;&nbsp;</td>
<td>(Course Enrolment, UGRD)</td> </tr>
"""

"""
status of "cancel" and "closed" not included 
"""
from bs4 import BeautifulSoup
import requests
import re
from enum import Enum
from tkinter import Tk

from gui_table import Table
from scrollbar import Scrollbar

class C(str, Enum):
    COURSE_NAME = "name"
    COURSE_CODE = "code"
    ENROL_PRECENT = "prec"
    ENROL_NUM = "num"

def main():
    Class_scrapter()

class Class_scrapter:

    def __init__(self, url_search=None, is_undergrad=True, is_perc=False, is_table=True, courses_done=None):

        response = requests.get(url_search, timeout=5)
        self.content = BeautifulSoup(response.content, "html.parser")
        self.output_list = []
        self.perc_condition = ["class=\"cufull\">", "class=\"cu80\">", "class=\"cu50\">", "class=\"cu00\">"] # see explain above
        self.level = "(Course Enrolment, UGRD)" if is_undergrad else "(Course Enrolment, PGRD)"
        self.term = url_search[-7:-5] # term from url e.g.http://classutil.unsw.edu.au/COMP_T2.html
        self.courses_done = courses_done.split(",")
        self.tweet = self.content.findAll(["a", "tr"])
        self.is_table = is_table
        self.collect_data()
        self.sort_based_percent(C.ENROL_PRECENT) if is_perc else self.sort_based_percent(C.ENROL_NUM)
        #self.print_output()
        self.output_to_gui()

    def collect_data(self):

        is_first = True
        is_one_record = True # get only the first percent record which is about enrolment, others are class %
        info_bag = self.get_empty_bag()
        check_online = False
        
        for i, t in enumerate(self.tweet):
            
            t = str(t)
            if not is_first:
                t = t[26:] #  get rid of duplicate of previous #TODO: be improved
            if check_online:
                #print(t)
                self.get_online_course(t, info_bag)
                check_online = False
                info_bag = self.get_empty_bag()
                continue

            if (("href=\"#COMP" not in t and "name=\"COMP" in t) or any(i in t for i in self.perc_condition)) :
                
                try:
                    #print(t)
                    info_bag[C.COURSE_CODE] = self.get_str_between(t, C.COURSE_CODE)[:-2]
                    info_bag[C.COURSE_NAME] = self.get_str_between(t, C.COURSE_NAME)
                    is_first = False
                    is_one_record = True
                except Exception as e:
                    pass
                    #print(e)
                if any(i in t for i in self.perc_condition) and is_one_record and self.level in t:
                    
                    info_bag[C.ENROL_PRECENT] = self.get_str_between(t, C.ENROL_PRECENT)
                    info_bag[C.ENROL_NUM] = self.get_str_between(t, C.ENROL_NUM)
                    is_one_record = False
                    if "CR02" in t:
                        check_online = True

                    self.output_list.append(info_bag)
                    info_bag = self.get_empty_bag()

    def get_online_course(self, t:str, info_bag:list)->None:
        """
        a few courses in 2021 term2 has offering both online nad offline
        """
        info_bag[C.ENROL_PRECENT] = self.get_str_between(t, C.ENROL_PRECENT)
        info_bag[C.ENROL_NUM] = self.get_str_between(t, C.ENROL_NUM)
        #print(info_bag[C.ENROL_PRECENT], info_bag[C.ENROL_NUM])
        info_bag[C.COURSE_CODE] = self.output_list[-1][C.COURSE_CODE]
        info_bag[C.COURSE_NAME] = self.output_list[-1][C.COURSE_NAME]
        self.output_list[-1][C.COURSE_NAME] += " -ONLINE"
        self.output_list.append(info_bag)

    def sort_based_percent(self, which=C.ENROL_PRECENT):
        """
        sort in ascending order
        """
        res = []
        is_end = True
        while len(self.output_list) != 0:
            maxv = -1
            p = None
            for i in self.output_list:
                perc = int(i[C.ENROL_PRECENT].replace("%", ""))
                if which == C.ENROL_NUM:
                    try:
                        perc = int(i[C.ENROL_NUM][:i[C.ENROL_NUM].index("/")]) #TODO
                    except Exception as e:
                        print(i)
                        print(e)
                        print(i[C.ENROL_NUM])
                        print(i[C.ENROL_NUM][:i[C.ENROL_NUM].index("/")])

                if perc > maxv:
                    maxv = perc
                    p = i
            res.append(p)
            self.output_list.remove(p)
        self.output_list = res


    def print_output(self):
        
        print("\nBelow is the list in descending order of popularity in courses enrolled:\n")
        for i in self.output_list:
            print(i[C.COURSE_CODE], i[C.ENROL_PRECENT], i[C.ENROL_NUM], i[C.COURSE_NAME])
    
    def output_to_gui(self):
        res = []
        res.append(("count", f"course code ({self.term})", "enrol_precentage", "enrol_number", "course_name"))
        total_enrol = 0
        total_enrol_size = 0
        total_courses = 0
        for n, i in enumerate(self.output_list):
            enrolled_num = int(i[C.ENROL_NUM][:i[C.ENROL_NUM].index("/")])
            total_enrol_size += int(i[C.ENROL_NUM][i[C.ENROL_NUM].index("/") + 1:])
            total_enrol += enrolled_num
            total_courses += 1

            if any(c in i[C.COURSE_CODE] for c in self.courses_done) and self.courses_done != [""]: # ignore course done
                res.append((n + 1, "", "", "", ""))
            else:
                res.append((n + 1, i[C.COURSE_CODE], i[C.ENROL_PRECENT], i[C.ENROL_NUM], i[C.COURSE_NAME]))
        res.append(("total", "", "", f"{total_enrol} / {total_enrol_size}", ""))
        
        root = Tk() 
        if self.is_table:
            t = Table(root, res) 
        else:
            example = Scrollbar(root, res)
            example.pack(side="top", fill="both", expand=True)
        root.mainloop() 

    def get_empty_bag(self):
        return {
            C.COURSE_CODE: None,
            C.COURSE_NAME: None,
            C.ENROL_PRECENT: None,
            C.ENROL_NUM: None
        }
    def get_str_between(self, s, which):
        
        course_dict = {
            C.COURSE_CODE:["name=\"", "\"></a>"],
            C.COURSE_NAME:["<td class=\"cucourse\" colspan=\"6\" valign=\"center\">", "</td>"],
            C.ENROL_PRECENT:[self.perc_condition, "</td>"],
            C.ENROL_NUM:[["Open\*</td><td>", "Stop</td><td>", "Full</td><td>", "Open</td><td>"], "</td> <td class="] 
        }
        sub1 = course_dict[which][0]
        sub2 = course_dict[which][1]
        
        if which == C.ENROL_PRECENT or which == C.ENROL_NUM:
            
            for i in sub1:
                try:
                    result = re.search(f"{i}(.*){sub2}", s)
                    result = result.group(1)
                    return result
                except:
                    pass
        
        
        result = re.search(f"{sub1}(.*){sub2}", s)
        result = result.group(1)
        if "&amp" in result:
            result = result.replace("&amp;", "&") # normalise
        return result

if __name__=="__main__":
    main()
