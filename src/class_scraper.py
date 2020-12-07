"""
given the order of course listed is in ascending order
"""

"""
Notes:
cu00 - less than half
cufull - full
cu50 - over half
"""
from bs4 import BeautifulSoup
import requests
import re
from enum import Enum

class C(str, Enum):
    COURSE_NAME = "name"
    COURSE_CODE = "code"
    ENROL_PRECENT = "prec"
    ENROL_NUM = "num"

def main():
    Class_scrapter()

class Class_scrapter:

    def __init__(self):
        
        url_search = "http://classutil.unsw.edu.au/COMP_T1.html"

        response = requests.get(url_search, timeout=5)
        self.content = BeautifulSoup(response.content, "html.parser")
        self.output_list = []
        self.perc_condition = ["class=\"cufull\">", "class=\"cu50\">", "class=\"cu00\">"] # see explain above

        tweet = self.content.findAll(["a", "tr"])
        prev = None
        is_first = True
        is_one_record = True # get only the first percent record which is about enrolment, others are class %
        info_bag = self.get_empty_bag()
        
        for i, t in enumerate(tweet):
            
            t = str(t)
            if not is_first:
                t = t[26:] #  get rid of duplicate of previous #TODO: be improved

            if ("href=\"#COMP" not in t and "name=\"COMP" in t) or any(i in t for i in self.perc_condition):
                
                try:
                    #print(t)
                    info_bag[C.COURSE_CODE] = self.get_str_between(t, C.COURSE_CODE)[:-2]
                    info_bag[C.COURSE_NAME] = self.get_str_between(t, C.COURSE_NAME)
                    
                    is_first = False
                    is_one_record = True
                except:
                    pass
                if any(i in t for i in self.perc_condition) and is_one_record:
                    
                    info_bag[C.ENROL_PRECENT] = self.get_str_between(t, C.ENROL_PRECENT)
                    info_bag[C.ENROL_NUM] = self.get_str_between(t, C.ENROL_NUM)
                    is_one_record = False
                    
                    self.output_list.append(info_bag)
                    info_bag = self.get_empty_bag()

        self.print_output()
    
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
                    perc = int(i[C.ENROL_NUM][:i[C.ENROL_NUM].index("/")])

                if perc > maxv:
                    maxv = perc
                    p = i
            res.append(p)
            self.output_list.remove(p)
        self.output_list = res

    def sort_based_number(self):
        pass

    def print_output(self):
        self.sort_based_percent(C.ENROL_NUM)
        print("\nBelow is the list in descending order of popularity in courses enrolled:\n")
        for i in self.output_list:
            print(i[C.COURSE_CODE], i[C.ENROL_PRECENT], i[C.ENROL_NUM], i[C.COURSE_NAME])

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
            C.ENROL_NUM:[["Open\*</td><td>", "Full</td><td>", "Open</td><td>"], "</td> <td class="] 
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


"""
below not used
"""


"""
https://stackoverflow.com/questions/32898916/find-all-tags-of-certain-class-only-after-tag-with-certain-text
"""
def get_precentage_after_course(self, course_code:str):
    # if "COMP" in t.text:
        #     print(t)
        #     if prev and int(t.text[4:8]) < int(prev[4:8]): # get only course number e.g comp1511 -> 1511, if wrong order, then assume noisy data
        #         break
        #     print(i, t.text)
        #     self.get_precentage_after_course(t.text)
        #     prev = t.text
    start = self.content.find("a", text=course_code).parent
    #print(start)
    for tr in start.find_next_siblings("tr"):
        # exit if reached C
        print(tr)
        break
        # if tr.find("td", text="C"):
        #     break

        # # get all tds with a desired class
        # tds = tr.find_all("td", class_="y")
        # for td in tds:
        #     print(td.get_text())
