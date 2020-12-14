from class_scraper import Class_scrapter
degree = "COMP"
term = "T1"
under_post = "under"
perc_num = "lec"
courses_done = ""
Class_scrapter(degree, term, True, (True if "under" in under_post else False), perc_num, True, courses_done)
