from class_scraper import Class_scrapter, C
import requests
from threading import Thread, Lock 
import sys

class Degrees_sorting():
    
    def __init__(self, degree=[], term="T1", is_frontend=True, is_undergrad=True, sort_algo=C.LEC_NUM, 
                    is_table=True, courses_done="", url_rank="", year="2021", levels={}, is_degree_changed=True, data_list=[]):
        levels = self.convert_levels_2_list(levels)
        self.courses_done = []
        if courses_done: # convert str to list
            self.courses_done = courses_done.split(",")
            self.courses_done = [i.strip() for i in self.courses_done]

        if not is_degree_changed and data_list: # reuse data when no change in input
            self.result = self.sort_by_for_degree_unchanged(sort_algo, data_list, levels, self.courses_done)
            return

        self.get_faculty_data()
        degree = self.add_faculty(degree)
        #degree = degree[:10] # cap at max 10
        self.result = []
        self.total_enrol = 0
        self.total_enrol_size = 0
        self.total_lec = 0
        self.total_lec_size = 0
        self.n_on_campus = 0
        
        self.requests_session = requests.Session() # with this, 3x faster!!!
        
        
        self.course_on_campus = []
        self.threads = []
        self.lock = Lock() # https://www.bogotobogo.com/python/Multithread/python_multithreading_Synchronization_Lock_Objects_Acquire_Release.php

        if term == "All_Term":
            all_terms = ["U1", "T1", "T2", "T3"] if year > "2018" else ["X1", "S1", "S2"]
            res_tmp = []
            for t in all_terms:
                prev_total_enrol = self.total_enrol
                prev_total_enrol_size = self.total_enrol_size
                prev_total_lec = self.total_lec
                prev_total_lec_size = self.total_lec_size
                prev_n_on_campus = self.n_on_campus
                prev_result = self.result
                self.result = []
                self.search_by_degrees(degree, t, is_undergrad, sort_algo, self.courses_done, year)

                self.total_enrol = self.total_enrol + prev_total_enrol
                self.total_enrol_size = self.total_enrol_size + prev_total_enrol_size
                self.total_lec = self.total_lec + prev_total_lec
                self.total_lec_size = self.total_lec_size + prev_total_lec_size
                self.n_on_campus = self.n_on_campus + prev_n_on_campus
                # for i in self.result:
                #     if i and i not in prev_result:
                #         self.result.append(i)
                res_tmp += self.result
            self.result = res_tmp.copy()
            self.result = self.sort_by_key(self.result)
            
        else:
            self.search_by_degrees(degree, term, is_undergrad, sort_algo, self.courses_done, year)
        
        #print("courses on campus are: ", course_on_campus)
        if not self.result:
            self.result.append(("count", f"course code", "enrol_precentage", "enrol_number", "course_name", "has_on_campus"))
            self.result.append(("No result or error during search, check if term is right", "", "", "", "", ""))
            return

        self.result = self.filter_postgrad_semester(self.result, year, is_undergrad)
        self.result = Class_scrapter.sort_based_percent(sort_algo, self.result, self.course_on_campus)
        
        self.result = Class_scrapter.convert_format(self.result, self.course_on_campus, \
                                                self.courses_done, levels)[0]
        
        self.result = self.result[:200] # at most 100 result
        self.result.insert(0, ("Count", f"Course code ({term})", "Enrol precentage", "Enrol number", \
                                "Lec/Web/Prj/Thesis", "Course name", "On campus"))
        self.result.append(("Total", "", "", f"{self.total_enrol} / {self.total_enrol_size}", \
                            f"{self.total_lec} / {self.total_lec_size}", "", str(self.n_on_campus) + "  (in total)"))
    
    def sort_by_for_degree_unchanged(self, which, data_list, levels, courses_done):
        # sort the already formatted data based on column
        if not data_list:
            return
        heading = data_list[0]
        summary = data_list[-1]
        data_list = data_list[1:-1]   
        
        sort_dict = {
            C.ON_CAMPUS: lambda k:k[6], 
            C.ENROL_PRECENT:lambda k: int(k[2].replace("%", "")),
            C.ENROL_NUM:lambda k: int(k[3][:k[3].index("/")]),
            C.LEC_NUM:lambda k: int(k[4][:k[4].index("/")])
        }
        res = sorted(data_list, key=sort_dict[which], reverse=True) 
        final_res = []
        for n, r in enumerate(res):
            if not any(r[1][4] == str(l) for l in levels): # ignore certain levels , e.g level 1 course
                final_res.append((str(n + 1), "", "", "", "", "", ""))
                continue

            if courses_done != [""] and any(c in r[1] for c in courses_done): # ignore course done
                final_res.append((str(n + 1), "", "", "", "", "", "")) # TODO clean up
                continue
            tmp = list(r)
            tmp[0] = n + 1
            tmp = tuple(tmp)
            final_res.append(tmp)

        final_res.insert(0, heading)
        final_res.append(summary)
        return final_res

    def sort_by_key(self, l):
        # if cur == prev , add sum, else , append
        if not l:
            return []
        tmp = sorted(l, key=lambda k: k[C.COURSE_CODE]) 
        res = []
        res.append(tmp[0])
        for t in tmp[1:]:
            if t[C.COURSE_CODE]  == res[-1][C.COURSE_CODE]:
                res[-1][C.ENROL_NUM] = Class_scrapter.str_sum(res[-1][C.ENROL_NUM], t[C.ENROL_NUM])
                res[-1][C.LEC_NUM] = Class_scrapter.str_sum(res[-1][C.LEC_NUM], t[C.LEC_NUM])
                continue
            res.append(t)
        return res

    def filter_postgrad_semester(self, l, year, is_undergrad):
        if not year <= "2018":
            return l
        
        # if cur == prev , add sum, else , append
        if not l:
            return []
        tmp = sorted(l, key=lambda k: k[C.COURSE_NAME]) 
        res = []
        res.append(tmp[0])
        for t in tmp[1:]:
            if t[C.COURSE_NAME] == res[-1][C.COURSE_NAME]: 
                if is_undergrad:
                    if t[C.COURSE_CODE] < res[-1][C.COURSE_CODE]: # e.g. comp9201 > comp3201 so postgrad
                        res.pop()
                        res.append(t)
                else:
                    if t[C.COURSE_CODE] > res[-1][C.COURSE_CODE]: 
                        res.pop()
                        res.append(t)
                continue
            res.append(t)
        return res

    # for each degree, get sum of total lec size etc and course resul
    def search_by_degrees(self, degree, term, is_undergrad, sort_algo, courses_done, year):
        self.threads = []
        for d in degree:
            # t = Thread(target=self.run_scrapter, args=(d, term, is_undergrad, sort_algo, courses_done, year))
            # t.daemon = True
            # self.threads.append(t)
            self.run_scrapter(d, term, is_undergrad, sort_algo, courses_done, year)
        # for t in self.threads:
        #     t.start()
        # for t in self.threads:
        #     t.join()
    def run_scrapter(self, d, term, is_undergrad, sort_algo, courses_done, year):
        
        c = Class_scrapter(d, term, True, is_undergrad, sort_algo, True, courses_done, "", year, self.requests_session)
        data_list = c.get_list() 
        if not data_list:
            return
        self.course_on_campus += c.course_on_campus
        self.lock.acquire()
        self.result += data_list
        self.lock.release()
        tmp = c.convert_format(data_list, c.course_on_campus, [])
        _total_enrol, _total_enrol_size, _total_lec, _total_lec_size, _n_on_campus = tmp[1:]
        self.total_enrol += _total_enrol
        self.total_enrol_size += _total_enrol_size
        self.total_lec += _total_lec
        self.total_lec_size += _total_lec_size
        self.n_on_campus += _n_on_campus
        #sys.exit(1) # stop thread after use - https://stackoverflow.com/questions/4541190/how-to-close-a-thread-from-within

    def get_list(self):
        return self.result

    def convert_levels_2_list(self, levels):
        res = []
        for k, v in levels.items():
            if v:
                res.append(k)
        return res

    def add_faculty(self, degree):

        faculty_dict = {
            "E": self.engineering,
            "EV": self.environment,
            "A": self.arts,
            "S": self.science,
            "M": self.medicine,
            "L": self.law,
            "B": self.business,
            "ALL":self.engineering + self.environment + self.arts + self.science +  self.medicine + self.law + self.business
        }
        tmp = degree.copy()
        for d in degree:
            res = faculty_dict.get(d, None)
            if res:
                tmp += res
        tmp = list (set(tmp) - set([*faculty_dict]))
        return tmp # remove duplicate
        
            
    def get_faculty_data(self):

        self.engineering = ["ACIV" ,"AERO" ,"AVEN" ,"BINF" ,"BIOM" ,"CEIC" ,"CHEN" ,"COMP" ,"CVEN" ,"ELEC" ,"ENGG" ,
        "FOOD" ,"FUEL" ,"GENE" ,"GENS" ,"GENZ" ,"GSOE" , "INDC" ,"MANF" ,"MATS" ,"MECH" ,"MINE" ,"MMAN" ,"MNNG" ,
        "MTRN" ,"NANO" ,"NAVL" ,"PHTN" ,"POLY" ,"PTRL" ,"SAFE" ,"SENG" ,"SOLA" ,"TELE" ,"TEXT" ,"WOOL" ,"ZEIT" ,"ZINT"]

        self.arts = ["ARTS", "ASIA", "AUST", "COFA", "COMD", "DANC", "EDST", "ENGL", "EURO", "EXPA", "FILM", "GEND", 
        "GENT", "GLST", "HUMS", "IRSH", "ITAL", "JWST", "MDCM", "MDIA", "MEFT", "MUSC", "SAHT", "SART", 
        "SDES", "SLST", "SOMA", "SPRC", "THST", "WOMS"]

        self.environment = ["ARCH", "BENV", "BLDG", "GEOH", "GSBE", "IDES", "INTA", "LAND", "MUPS", "PLAN", "SUSD", "UDES"]

        self.science = ["AENG", "AGOC", "AHIS", "ANAM", "APHY", "APOL", "ATSI", "BABS", "BIOC", "BIOC", "BIOD", 
        "BSSM", "CHEM", "CRIM", "HESC", "HIST", "HPSC", "HPST", "INOV", "INST", "LIFE", 
        "MATH", "MICM", "MICR", "NEUR", "OPTM", "PATM", "PECO", "PHAR", "PHPH", "PHSL", "PHYS", 
        "POLS", "PROR", "PSYC", "SCIF", "SCIF", "SCOM", "SCTS", "SESC", "SLSP", "SOCA", "SOCF", 
        "SOCW", "SOMS", "SRAP", "VISN", "ZHSS", "ZHSS", "ZPEM"]

        self.medicine = ["SURG", "MEDM", "MFAC", "PDCS", "MEED", "RUHE", "GENM", "MDSG", 
        "PHCM", "NEUR", "PDCS", "CMED", "MDCN", "HEAL"]

        self.law = ["HPSC", "LEGT", "GENC", "GENC", "TABL", "LAWS", "JURD", "GENL", 
        "LEGT", "JURD", "ATAX"]

        self.business = ["ACCT", "AECM", "COMM", "ECON", "FINS", "GBAT", "GENC", "GSOE", "IBUS", "IROB", "LEGT", 
        "MFIN", "MGMT", "MNGT", "REGZ", "STRE", "TABL", "XACC", "XBUS", "XFIN", "XINT", "XMKM", "XPRO", 
        "ZBUS", "ZGEN", "ZINT"]


# below is the sql for getting the faculty 

#         CREATE OR REPLACE VIEW tmp
#  AS
#  SELECT distinct(substring(s.code, 0, 5)) AS a,
#     o.*
#    FROM subjects s
#      JOIN orgunits o ON o.id = s.offeredby
#   WHERE o.name ilike'%science%' and o.name not ilike'%arts%' and o.name not ilike'%engineer%' 
#   and o.name not ilike'%fins%';
  
#   CREATE OR REPLACE VIEW myarts
#  AS
#  SELECT distinct(substring(s.code, 0, 5)) AS a

#    FROM subjects s
#      JOIN orgunits o ON o.id = s.offeredby
#   WHERE o.name ilike'%art%';
  
#     CREATE OR REPLACE VIEW myeng
#  AS
 
#  SELECT distinct(substring(s.code, 0, 5)) AS a
    
#    FROM subjects s
#      JOIN orgunits o ON o.id = s.offeredby
#   WHERE o.name ilike'%eng%';
#       CREATE OR REPLACE VIEW mybus
#  AS
 
#  SELECT distinct(substring(s.code, 0, 5)) AS a
    
#    FROM subjects s
#      JOIN orgunits o ON o.id = s.offeredby
#   WHERE o.name ilike'%bus%';
  
#  select distinct a, name from tmp 
#  where a not in (select * from myarts union select * from myeng)
#  order by a 
#  
