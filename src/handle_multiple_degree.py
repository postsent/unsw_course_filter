from class_scraper import Class_scrapter, C

class Degrees_sorting():
    def __init__(self, degree=[], term="T1", is_frontend=True, is_undergrad=True, sort_algo=C.ENROL_NUM, is_table=True, courses_done="", url_rank="", year="2021"):
        self.result = []
        total_enrol = 0
        total_enrol_size = 0
        total_lec = 0
        totla_lec_size = 0
        n_on_campus = 0
        courses_done = []
        course_on_campus = []
        for d in degree:
            c = Class_scrapter(d, term, True, is_undergrad, sort_algo, True, courses_done, "", year)
            data_list = c.get_list() 
            courses_done += c.courses_done
            course_on_campus += c.course_on_campus
            
            self.result += data_list
            if not data_list:
                continue
            tmp = c.convert_format(data_list, c.course_on_campus, c.courses_done)
            _total_enrol, _total_enrol_size, _total_lec, _totla_lec_size, _n_on_campus = tmp[1:]
            total_enrol += _total_enrol
            total_enrol_size += _total_enrol_size
            total_lec += _total_lec
            totla_lec_size += _totla_lec_size
            n_on_campus += _n_on_campus
            

        if not self.result:
            self.result.append(("count", f"course code", "enrol_precentage", "enrol_number", "course_name", "has_on_campus"))
            self.result.append(("invalid url or error occur during search", "", "", "", "", ""))
        
        self.result = Class_scrapter().sort_based_percent(sort_algo, self.result, course_on_campus)
        
        self.result = Class_scrapter().convert_format(self.result, course_on_campus, courses_done)[0]
        self.result.insert(0, ("Count", f"Course code ({term})", "Enrol precentage", "Enrol number", "Lec/Web/Prj/Thesis", "Course name", "On campus"))
        self.result.append(("Total", "", "", f"{total_enrol} / {total_enrol_size}", f"{total_lec} / {totla_lec_size}", "", str(n_on_campus) + "  (in total)"))

    def get_list(self):
        return self.result