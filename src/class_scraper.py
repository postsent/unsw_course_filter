"""
given the order of course listed is in ascending order
places add assumption for booting the speed
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
"""
heroku free tier - limits,up to 256 threads/process
https://devcenter.heroku.com/articles/limits
"""

from bs4 import BeautifulSoup
import requests
import re
from enum import Enum
import cchardet # https://thehftguy.com/2020/07/28/making-beautifulsoup-parsing-10-times-faster/#comments
import lxml
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
    
    def __init__(self, degree="COMP", term="T1", is_frontend=True, 
                is_undergrad=True, sort_algo=C.ENROL_NUM, is_table=True, courses_done="", url_rank="", year="2021", requests_session=None):
        
        try: # handle invalid url
            self.degree = degree.upper()
            if term == "U1" and year <= "2018":
                term = "X1"
            response = requests_session.get(self.generate_class_url(self.degree, term, year), timeout=5)
            if url_rank:
                response = requests_session.get(url_rank, timeout=5) # rank not implement 
        except Exception as e:
            print(e)
            self.output_list = []
            return
        self.current_year = "2021"
        self.year = year # 
        #  text may faster than content - https://stackoverflow.com/questions/25539330/speeding-up-beautifulsoup, https://www.crummy.com/software/BeautifulSoup/bs4/doc/
        self.content = BeautifulSoup(response.text, "lxml") # 
        self.output_list = []
        self.perc_condition = ["class=\""+ i + "\">" for i in ["cufull", "cu80", "cu50", "cu00"]]# see explain above
        self.level = "(Course Enrolment, UGRD)" if is_undergrad else "(Course Enrolment, PGRD)"
        self.opposite_level = "UGRD" if not is_undergrad else "PGRD"
        self.term = term
        self.postpone = ["Canc", "Stop", "Tent"]
        self.tweet = self.content.findAll(["tr"]) #self.findall_condition
        self.is_table = is_table
        self.course_on_campus = []

        self.collect_data()
        #self.output_list = self.sort_based_percent(sort_algo, self.output_list)
        #self.convert_format()
        #self.print_output()
        if not is_frontend:
            self.output_to_gui()

    # add condition on findall - https://stackoverflow.com/questions/36659904/python-beautiful-soup-or-condition-in-soup-find-all
    def findall_condition(self, tag):
        #print(tag.attrs)
        
        # if (tag.has_attr('name') and tag.name == "a"):
        #     print(tag.text)
        #     return True
        if tag.name == "tr": 
            # and \
            # any(i in t for i in ["LEC", "WEB", "THE", "PRJ", "TLB", "LAB", "SEM", "TUT"]):   
            return True
        
        return False

    def collect_data(self):

        info_bag = self.get_empty_bag()
        lec_record = "0/0"
        lec_bag = []
        
        for t in self.tweet:

            texts = t.text            
            # if "COMP6080" in t:
            #     print(texts)  
            lec_tmp = self.generate_lec_record(texts, lec_record, lec_bag)
            lec_record = lec_tmp if lec_tmp else lec_record
            
            if self.degree in texts[:10]: # meet course code, assumption - COMP9021  Principles of Programming
                
                info_bag[C.LEC_NUM] = lec_record 
                lec_record = "0/0" # reset when meet new course code
                lec_bag = []
                try:
                    #print(t)
                    if (info_bag[C.ENROL_NUM] and info_bag[C.ENROL_PRECENT]) : # before shift to new course code, append bag
                        
                        self.output_list.append(info_bag)
                        info_bag = self.get_empty_bag()

                    elif self.year <= "2018" and info_bag[C.COURSE_CODE] and len(info_bag[C.COURSE_CODE]) >= 8:
                        info_bag[C.ENROL_NUM] = "0/0"
                        info_bag[C.ENROL_PRECENT] = "0/0" # by default, no enrollent, too long ago
                        self.output_list.append(info_bag)
                        info_bag = self.get_empty_bag()

                    info_bag[C.COURSE_CODE] = self.get_data_between(texts, C.COURSE_CODE)                    
                    info_bag[C.COURSE_NAME] = self.get_data_between(texts, C.COURSE_NAME)
                    # info_bag[C.COURSE_CODE] = self.get_str_between(t, C.COURSE_CODE)[:-2]
                    # info_bag[C.COURSE_NAME] = self.get_str_between(t, C.COURSE_NAME)
                    
                except Exception as e:
                    pass
                    #print(e)
            
            if "CRS" == texts[1:4]and self.level in texts: # any(i in t for i in self.perc_condition)
                #print(texts.split()[2])
                info_bag[C.ENROL_PRECENT] = self.get_data_between(texts, C.ENROL_PRECENT)
                
                if not info_bag[C.ENROL_NUM]:
                    info_bag[C.ENROL_NUM] = self.get_data_between(texts, C.ENROL_NUM)#get_data_between(texts, C.ENROL_NUM)
                else:
                    new_enrol = self.get_data_between(texts, C.ENROL_NUM)#get_data_between(texts, C.ENROL_NUM)
                    info_bag[C.ENROL_NUM] = Class_scrapter.str_sum(new_enrol, info_bag[C.ENROL_NUM]) # sum of all coruse enrolment num
                
                if "CR02" in texts: # if two courses available, then first ususally is online version                    
                    info_bag[C.COURSE_NAME] += " - CR1/CR2" # a few courses in 2021 term2 has offering both online and offline
                    
            if not self.opposite_level in texts:  # refresh when meets new course code regardless within the right leve
                self.generate_on_campus_course(texts, info_bag[C.COURSE_CODE])

        if self.output_list and info_bag[C.COURSE_CODE] and info_bag != self.output_list[-1]: # fix the last item that may not be appended
            info_bag[C.LEC_NUM] = lec_record 
            if self.year <= "2018":
                if len(info_bag[C.COURSE_CODE]) >= 8:
                    info_bag[C.ENROL_NUM] = "0/0"
                    info_bag[C.ENROL_PRECENT] = "0/0" # by default, no enrollent, too long ago
                    self.output_list.append(info_bag)
                    return
            if (info_bag[C.ENROL_NUM] and info_bag[C.ENROL_PRECENT]):
                self.output_list.append(info_bag)
    @staticmethod
    def str_sum(a, b):
        
        c_enrol = int(a[:a.index("/")]) 
        c_total = int(a[a.index("/") + 1:]) 
        prev_enrol = int(b[:b.index("/")]) 
        prev_total = int(b[b.index("/") + 1:]) 
        enrol = c_enrol  + prev_enrol
        total = prev_total + c_total
        return str(enrol) + "/" + str(total)
        
    def is_duplicate_lec(self, lec_bag, cur_name, cur_enrol_stats):
        """if there is a web that is the sum of lec, then ignore the web, if there is one web same number as lec, ignore web

        Args:
            lec_bag (list): contains records e.g {"LEC":"1/1"}
            t (str): source page part
            cur_name (str): LEC/WEB
            cur_enrol_stats (str): e.g "1/1", number in this WEB / LEC

        Returns:
            Bool: if duplicate lec
        """
        
        if ("LEC" in list(*zip(*lec_bag)) and cur_name == "WEB") or ("WEB" in list(*zip(*lec_bag)) and cur_name == "LEC"):
            lec_sum = "0/0"
            for lec in lec_bag:
                for k, v in lec.items():
                    if k == "LEC":
                        c_enrol = int(v[:v.index("/")]) 
                        c_total = int(v[v.index("/") + 1:]) 
                        prev_enrol = int(lec_sum[:lec_sum.index("/")]) 
                        prev_total = int(lec_sum[lec_sum.index("/") + 1:]) 
                        lec_sum = str(prev_enrol + c_enrol) + "/" + str(c_total + prev_total)
                    
                    if k == "LEC" and cur_name == "WEB" and v == cur_enrol_stats:
                        return  True # ignore the result
                    if k == "WEB" and cur_name == "LEC" and v == cur_enrol_stats:
                        return  True
            if cur_name == "WEB" and lec_sum == cur_enrol_stats:
                return True
        return False
        
    def generate_lec_record(self, t, lec_record, lec_bag):
        """
        assume below list is disjoint condition, sum up all lec number regradless under or post grad
        OTH and Lec is disjoint, but OTH not consider yet #TODO
        """
        
        if not any(i in t[1:4] for i in ["LEC", "WEB", "THE", "PRJ"]) or any(i in t for i in self.postpone): #  
            return

        try:
            prev_enrol = int(lec_record[:lec_record.index("/")]) 
            prev_total = int(lec_record[lec_record.index("/") + 1:]) 

            cur = self.get_data_between(t, C.LEC_NUM)
            cur_enrol = int(cur[:cur.index("/")]) 
            cur_total = int(cur[cur.index("/") + 1:]) 
            res = str(prev_enrol + cur_enrol) + "/" + str(cur_total + prev_total)
            
            cur_name = {"LEC" in t:"LEC", "WEB" in t:"WEB"}.get(True, None) # lec/web
            
            if self.is_duplicate_lec(lec_bag, cur_name, cur):
                return
            if cur_name and not {cur_name:cur} in lec_bag:
                lec_bag.append({cur_name:cur})
            
            return res
        except Exception as e:
            # if "LEC" in tmp and "6080" in t:
            #     print(cur)
            #     print("22222222222222222222222222222222222222")
            # print(e)
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
    @staticmethod
    def sort_based_percent(which=C.ENROL_PRECENT, output_list=[], course_on_campus=[]):
        """
        sort in ascending order based on percent / num / lec num
        sort list of dictionaries - https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
        """
        if not output_list:
            return
        if which == C.ON_CAMPUS:
            return Class_scrapter.sort_based_on_campus(output_list, course_on_campus)
            
        sort_dict = {
            C.ENROL_PRECENT:lambda k: int(k[C.ENROL_PRECENT].replace("%", "")),
            C.ENROL_NUM:lambda k: int(k[C.ENROL_NUM][:k[C.ENROL_NUM].index("/")]),
            C.LEC_NUM:lambda k: int(k[C.LEC_NUM][:k[C.LEC_NUM].index("/")])
        }
        res = sorted(output_list, key=sort_dict[which], reverse=True) 
  
        return res
    @staticmethod
    def sort_based_on_campus(output_list, course_on_campus):
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
    @staticmethod
    def convert_format(output_list, course_on_campus, courses_done, levels=[]):
        """
        return  table like format in tuple
        """
        if not output_list:
            return
        res = []
        total_enrol = 0
        total_enrol_size = 0
        total_lec = 0
        total_lec_size = 0
        
        for n, i in enumerate(output_list):

            total_enrol_size += int(i[C.ENROL_NUM][i[C.ENROL_NUM].index("/") + 1:])
            total_enrol += int(i[C.ENROL_NUM][:i[C.ENROL_NUM].index("/")])
            total_lec_size += int(i[C.LEC_NUM][i[C.LEC_NUM].index("/") + 1:])
            total_lec += int(i[C.LEC_NUM][:i[C.LEC_NUM].index("/")])
            is_on_campus = "True" if i[C.COURSE_CODE] in course_on_campus else ""
           
            if not any(i[C.COURSE_CODE][4] == str(l) for l in levels): # ignore certain levels , e.g level 1 course
                res.append((str(n + 1), "", "", "", "", "", ""))
                continue

            if any(c in i[C.COURSE_CODE] for c in courses_done) and courses_done != [""]: # ignore course done
                res.append((str(n + 1), "", "", "", "", "", "")) # TODO clean up
                continue
            
            res.append((str(n + 1), i[C.COURSE_CODE], i[C.ENROL_PRECENT], i[C.ENROL_NUM], i[C.LEC_NUM], i[C.COURSE_NAME], is_on_campus))
            # except Exception as e:
            #     #print("convert_format function")
            #     # print(e)
            #     pass
                
            
        return res, total_enrol, total_enrol_size, total_lec, total_lec_size, len(course_on_campus)

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
    def find_idxs(self, s, ch):
        return [i for i, ltr in enumerate(s) if ltr == ch]

    def substr_digit(self, s, forward=True):
        sub = ""
        if forward:
            
            for l in s[::-1]:
                if not l.isdigit(): break
                sub += l
            sub = sub[::-1]
        else:
            for l in s:
                if not l.isdigit(): break
                sub += l
        return sub

    def get_substr_by_letter(self, s, ch):
        ch_list = self.find_idxs(s, ch)
        res = ""
        for idx in ch_list:
            forward_str = self.substr_digit(s[:idx], True)
            backward_str = self.substr_digit(s[idx + 1:], False)
            if forward_str and backward_str:
                res = (forward_str + "/" + backward_str)
        return res
        

    def get_data_between(self, s, which):
        
        if which == C.COURSE_NAME:
            idx = s.index("\n")
            s = s[idx + 1:]
            
        elif which == C.COURSE_CODE:
            idx = s.index("\n")
            s = s[:idx]
        elif which == C.ENROL_PRECENT:
            s = s.split()[2]
            if ">" in s: # e.g. >100%  
                s = s.replace(">", "")
            if s == "N/A":
                s = "-1%"
        elif which == C.ENROL_NUM or C.LEC_NUM:
            # e.g. "CRSCR01 2094Open32/91 35%" -> "2094Open32/91" -> "*19/23nepO4902" -> ""19/23"
            # LECA10164RelOpen57/100 57%   Mon 18-20# (w1-5,7,9-10, Online); Thu 18-20# (w1-5,7-10, Online) Comb/w  COMP6080-UGRD
            
            s = self.get_substr_by_letter(s, "/")
            if s == "N/A":
                s = "0/0"
        
        
        return s

    def get_str_between(self, s, which):
        
        prefix = [i + "</td><td>" for i in ["Open", "Open\*", "Stop", "Full", "Closed", "Full\*"]]
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
        if "&gt;" in result: # e.g. >100%  
            result = result.replace("&gt;", "")[1:]
        return result

if __name__=="__main__":
    main()
