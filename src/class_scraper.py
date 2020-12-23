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
not included 
status of "cancel" and "closed" , "cuwarn"
(Course Enrolment, RSCH)
"""
from bs4 import BeautifulSoup
import requests
import re
from enum import Enum

#from tkinter import Tk

# from gui_table import Table
# from scrollbar import Scrollbar

class C(str, Enum):
    COURSE_NAME = "name"
    COURSE_CODE = "code"
    ENROL_PRECENT = "perc"
    ENROL_NUM = "num"
    LEC_NUM = "lec"
    ON_CAMPUS = "campus"

def main():
    Class_scrapter()

class Class_scrapter:

    def __init__(self, degree="COMP", term="T1", is_frontend=True, is_undergrad=True, sort_algo=C.ENROL_NUM, is_table=True, courses_done="", url_rank="", year="2021"):
        
        try: # handle invalid url
            self.degree = degree.upper()
            response = requests.get(self.generate_class_url(self.degree, term, year), timeout=5)
            if url_rank:
                response = requests.get(url_rank, timeout=5) # rank not implement 
        except Exception as e:
            print(e)
            self.output_list = []
            return
        self.current_year = "2021"
        self.year = year
        self.content = BeautifulSoup(response.content, "html.parser")
        self.output_list = []
        self.perc_condition = ["class=\""+ i + "\">" for i in ["cufull", "cu80", "cu50", "cu00"]]# see explain above
        self.level = "(Course Enrolment, UGRD)" if is_undergrad else "(Course Enrolment, PGRD)"
        self.opposite_level = "UGRD" if not is_undergrad else "PGRD"
        self.term = term
        self.postpone = ["Canc", "Stop", "Tent"]
        self.tweet = self.content.findAll(["a" ,"tr"])
        self.is_table = is_table
        self.course_on_campus = []
        self.courses_done = []
        if courses_done:
            self.courses_done = courses_done.split(",")
            self.courses_done = [i.strip() for i in self.courses_done]

        self.collect_data()
        #self.output_list = self.sort_based_percent(sort_algo, self.output_list)
        #self.convert_format()
        #self.print_output()
        if not is_frontend:
            self.output_to_gui()

    def collect_data(self):

        is_first = True
        is_one_record = True # get only the first percent record which is about enrolment, others are class %
        info_bag = self.get_empty_bag()
        check_online = False
        
        stop_count = False # stop count on campus course when meet opposite level, e.g. CRS	CR01	1092		Open	16/88	18%  	(Course Enrolment, PGRD)
        lec_record = "0/0"

        for i, t in enumerate(self.tweet):
            
            t = str(t)
            
            if not is_first:
                t = t[26:] #  get rid of duplicate of previous #TODO: be improved

            if check_online and self.year == self.current_year:
                #print(t)
                self.generate_online_course(t, info_bag)
                check_online = False
                info_bag = self.get_empty_bag()
                continue
            lec_record = self.generate_lec_record(t, lec_record) if self.generate_lec_record(t, lec_record) else lec_record
            
            if f"href=\"#{self.degree}" not in t and f"name=\"{self.degree}" in t:

                if "center" in t:
                    info_bag[C.LEC_NUM] = lec_record 
                    lec_record = "0/0" # reset when meet new course code

                try:
                    #print(t)
                    if info_bag[C.ENROL_NUM] and info_bag[C.ENROL_PRECENT]: # before shift to new course code, append bag
                        
                        self.output_list.append(info_bag)
                        stop_count = False # since the bag is updated before the new course introduced so stop count for the old one with on_campus course  here
                        info_bag = self.get_empty_bag()

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
                
                if "CR02" in t: # if two courses available, then first ususally is online version
                    check_online = True

            if not self.opposite_level in t and f"href=\"#{self.degree}" not in t and not f"name=\"{self.degree}" in t and not "CRS" in t:  # refresh when meets new course code regardless within the right leve
                self.generate_on_campus_course(t, info_bag[C.COURSE_CODE])
            
        print("courses on campus are: ", self.course_on_campus)
        
    def generate_lec_record(self, t, lec_record):
        """
        assume below list is disjoint condition, sum up all lec number regradless under or post grad
        OTH and Lec is disjoint, but OTH not consider yet #TODO
        """
        if any(i in t for i in ["LEC", "WEB", "THE", "PRJ"]) and all(i not in t for i in self.postpone):
                
            try:
                prev_enrol = int(lec_record[:lec_record.index("/")]) 
                prev_total = int(lec_record[lec_record.index("/") + 1:]) 

                cur = self.get_str_between(t, C.LEC_NUM)
                cur_enrol = int(cur[:cur.index("/")]) 
                cur_total = int(cur[cur.index("/") + 1:]) 
                return str(prev_enrol + cur_enrol) + "/" + str(cur_total + prev_total)
            except:
                return 

    def generate_class_url(self, course_code:str, term:str, year:str):
        
        if year != "2021":
            
            return "https://nss.cse.unsw.edu.au/sitar/classes" + f"{year}" + f"/{course_code}_{term}.html"
        return "http://classutil.unsw.edu.au/" + course_code + "_" + term + ".html"

    def get_list(self):
        return self.output_list

    def generate_on_campus_course(self, t, c): # add prj and the - project and thesis
        """check if contains on campus tut / lec, if so, it is a on-campus course
        
        found 
            TUT from ARTS degree
            TLB from COMP 
        Args:
            t (str): source page with tag
        """
        if any(l in t for l in ["TLB", "LAB", "LEC", "SEM", "TUT"]) and not "Online" in t \
        and any(d in t for d in ["Mon", "Tue", "Wed", "Thu", "Fri"]): 

            if not c in self.course_on_campus and c:
                self.course_on_campus.append(c) 
                    

    def generate_online_course(self, t:str, info_bag:list)->None:
        """
        a few courses in 2021 term2 has offering both online nad offline
        """
        info_bag[C.ENROL_PRECENT] = self.get_str_between(t, C.ENROL_PRECENT)
        info_bag[C.ENROL_NUM] = self.get_str_between(t, C.ENROL_NUM)
        #print(info_bag[C.ENROL_PRECENT], info_bag[C.ENROL_NUM])
        info_bag[C.COURSE_CODE] = self.output_list[-1][C.COURSE_CODE]
        info_bag[C.COURSE_NAME] = self.output_list[-1][C.COURSE_NAME]
        self.output_list[-1][C.COURSE_NAME] += " - ONLINE"
        self.output_list.append(info_bag)

    def sort_based_percent(self, which=C.ENROL_PRECENT, output_list=[], course_on_campus=[]):
        """
        sort in ascending order based on percent / num / lec num
        """
        
        if which == C.ON_CAMPUS:
            return self.sort_based_on_campus(output_list, course_on_campus)
            

        res = []
        is_end = True
        while len(output_list) != 0:
            maxv = -1
            p = None
            
            for i in output_list:
                perc = None   
                
                if "&gt;" in i[C.ENROL_PRECENT]: # e.g. > 100% , TODO add for others tag
                    i[C.ENROL_PRECENT] = i[C.ENROL_PRECENT].replace("&gt;", "")[1:]
            
                if which == C.ENROL_PRECENT:
                    perc = int(i[C.ENROL_PRECENT].replace("%", ""))

                elif which == C.ENROL_NUM:
                    perc = int(i[C.ENROL_NUM][:i[C.ENROL_NUM].index("/")]) #TODO
                
                elif which == C.LEC_NUM:
                    try:
                        perc = int(i[C.LEC_NUM][:i[C.LEC_NUM].index("/")]) 
                    except:
                        perc = 0 # fix None 
            
                if perc != None and perc > maxv:
                    maxv = perc
                    p = i
                
            if not p:
                break
            res.append(p)
            output_list.remove(p) # remove the max until nothing left
            
        return res

    def sort_based_on_campus(self, output_list, course_on_campus):
        res = []
        for c in output_list:
            if any(i in c[C.COURSE_CODE] for i in course_on_campus):
                res.append(c)
        tmp = [i for i in output_list if i not in res]
        res += tmp
        return res
        
    def print_output(self):
        
        print("\nBelow is the list in descending order of popularity in courses enrolled:\n")
        for i in self.output_list:
            print(i[C.COURSE_CODE], i[C.ENROL_PRECENT], i[C.ENROL_NUM], i[C.COURSE_NAME])

    def convert_format(self, output_list, course_on_campus, courses_done):
        """
        return  table like format in tuple
        """
        res = []
        total_enrol = 0
        total_enrol_size = 0
        total_lec = 0
        totla_lec_size = 0
        
        for n, i in enumerate(output_list):
            # try:
            total_enrol_size += int(i[C.ENROL_NUM][i[C.ENROL_NUM].index("/") + 1:])
            total_enrol += int(i[C.ENROL_NUM][:i[C.ENROL_NUM].index("/")])
            totla_lec_size += int(i[C.LEC_NUM][i[C.LEC_NUM].index("/") + 1:])
            total_lec += int(i[C.LEC_NUM][:i[C.LEC_NUM].index("/")])
            is_on_campus = "True" if i[C.COURSE_CODE] in course_on_campus else ""
            try:
                if any(c in i[C.COURSE_CODE] for c in courses_done) and courses_done != [""]: # ignore course done
                    res.append((str(n + 1), "", "", "", "", "", "")) # TODO clean up
                else:
                    res.append((str(n + 1), i[C.COURSE_CODE], i[C.ENROL_PRECENT], i[C.ENROL_NUM], i[C.LEC_NUM], i[C.COURSE_NAME], is_on_campus))
            except:
                print(111)
            # except Exception as e:
            #     print(e)
            #     print(i)
            #     print("line 282")
            #     break
                
        return res, total_enrol, total_enrol_size, total_lec, totla_lec_size, len(course_on_campus)

    def output_to_gui(self):
        
        # root = Tk() 
        # if self.is_table:
        #     t = Table(root, self.output_list) 
        # else:
        #     example = Scrollbar(root, self.output_list)
        #     example.pack(side="top", fill="both", expand=True)
        # root.mainloop() 
        pass

    def get_empty_bag(self):
        return {
            C.COURSE_CODE: None,
            C.COURSE_NAME: None,
            C.ENROL_PRECENT: None,
            C.ENROL_NUM: None,
            C.LEC_NUM:None
        }
        
    def get_str_between(self, s, which):
        
        prefix = [i + "</td><td>" for i in ["Open", "Open\*", "Stop", "Full"]]
        course_dict = {
            C.COURSE_CODE:["name=\"", "\"></a>"],
            C.COURSE_NAME:["<td class=\"cucourse\" colspan=\"6\" valign=\"center\">", "</td>"],
            C.ENROL_PRECENT:[self.perc_condition, "</td>"],
            C.ENROL_NUM:[prefix, "</td> <td class="] , # since it find the largest suitable range so need to be more specify
            C.LEC_NUM:[prefix, "</td> <td class="] 
        }
        sub1 = course_dict[which][0]
        sub2 = course_dict[which][1]
        
        if which in [C.ENROL_PRECENT, C.ENROL_NUM, C.LEC_NUM]:
            
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
