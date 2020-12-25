from class_scraper import Class_scrapter, C

class Degrees_sorting():
    
    def __init__(self, degree=[], term="T1", is_frontend=True, is_undergrad=True, sort_algo=C.LEC_NUM, 
                    is_table=True, courses_done="", url_rank="", year="2021", levels={}):
        
        self.get_faculty_data()
        self.add_faculty(degree)

        self.result = []
        total_enrol = 0
        total_enrol_size = 0
        total_lec = 0
        totla_lec_size = 0
        n_on_campus = 0
        self.courses_done = []
        if courses_done:
            self.courses_done = courses_done.split(",")
            self.courses_done = [i.strip() for i in self.courses_done]
        course_on_campus = []

        for d in degree:
            c = Class_scrapter(d, term, True, is_undergrad, sort_algo, True, courses_done, "", year)
            data_list = c.get_list() 
            course_on_campus += c.course_on_campus
            
            self.result += data_list
            if not data_list:
                continue
            tmp = c.convert_format(data_list, c.course_on_campus, [])
            _total_enrol, _total_enrol_size, _total_lec, _totla_lec_size, _n_on_campus = tmp[1:]
            total_enrol += _total_enrol
            total_enrol_size += _total_enrol_size
            total_lec += _total_lec
            totla_lec_size += _totla_lec_size
            n_on_campus += _n_on_campus
            
        #print("courses on campus are: ", course_on_campus)
        if not self.result:
            self.result.append(("count", f"course code", "enrol_precentage", "enrol_number", "course_name", "has_on_campus"))
            self.result.append(("No result or error during search, check if term is right", "", "", "", "", ""))
            return
        
        self.result = Class_scrapter().sort_based_percent(sort_algo, self.result, course_on_campus)
        
        self.result = Class_scrapter().convert_format(self.result, course_on_campus, self.courses_done, self.convert_levels_2_list(levels))[0]
        self.result.insert(0, ("Count", f"Course code ({term})", "Enrol precentage", "Enrol number", "Lec/Web/Prj/Thesis", "Course name", "On campus"))
        self.result.append(("Total", "", "", f"{total_enrol} / {total_enrol_size}", f"{total_lec} / {totla_lec_size}", "", str(n_on_campus) + "  (in total)"))
        self.result = self.result[:100] # at most 100 result

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
            "B": self.business
        }
        for d in degree:
            tmp = d.upper()
            res = faculty_dict.get(tmp, None)
            if res:
                degree += res
                degree.remove(d)
            
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
        "LEGT", "LAWS", "JURD", "ATAX", "LAWS"]

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
