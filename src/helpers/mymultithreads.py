from multiprocessing.dummy import Pool as ThreadPool
import requests
import itertools

def get_request(requests_session, urls):
    try:
        return requests_session.get(urls, timeout=3)
    except:
        return
def get_request_multi(urls):
    try:
        return requests.get(urls, timeout=3)
    except:
        return
# https://stackoverflow.com/questions/2846653/how-can-i-use-threading-in-python
def parse_url_with_parallel(urls):
    requests_session= requests.Session()
    
    # Make the Pool of workers
    pool = ThreadPool(len(urls)) # this seems to be more optimised

    # Open the URLs in their own threads
    # and return the results
    results = pool.starmap(get_request, zip(itertools.repeat(requests_session), urls)) # starmap - https://stackoverflow.com/questions/5442910/how-to-use-multiprocessing-pool-map-with-multiple-arguments

    # Close the pool and wait for the work to finish
    pool.close()
    pool.join()

    return results
    
def generate_class_url(course_code:str, term:str, year:str):
        
    if year != "2021":
        
        return "https://nss.cse.unsw.edu.au/sitar/classes" + f"{year}" + f"/{course_code}_{term}.html"
    return "http://classutil.unsw.edu.au/" + course_code + "_" + term + ".html"

def get_faculty_data():

    engineering = ["ACIV" ,"AERO" ,"AVEN" ,"BINF" ,"BIOM" ,"CEIC" ,"CHEN" ,"COMP" ,"CVEN" ,"ELEC" ,"ENGG" ,
    "FOOD" ,"FUEL" ,"GENE" ,"GENS" ,"GENZ" ,"GSOE" , "INDC" ,"MANF" ,"MATS" ,"MECH" ,"MINE" ,"MMAN" ,"MNNG" ,
    "MTRN" ,"NANO" ,"NAVL" ,"PHTN" ,"POLY" ,"PTRL" ,"SAFE" ,"SENG" ,"SOLA" ,"TELE" ,"TEXT" ,"WOOL" ,"ZEIT" ,"ZINT"]

    arts = ["ARTS", "ASIA", "AUST", "COFA", "COMD", "DANC", "EDST", "ENGL", "EURO", "EXPA", "FILM", "GEND", 
    "GENT", "GLST", "HUMS", "IRSH", "ITAL", "JWST", "MDCM", "MDIA", "MEFT", "MUSC", "SAHT", "SART", 
    "SDES", "SLST", "SOMA", "SPRC", "THST", "WOMS"]

    environment = ["ARCH", "BENV", "BLDG", "GEOH", "GSBE", "IDES", "INTA", "LAND", "MUPS", "PLAN", "SUSD", "UDES"]

    science = ["AENG", "AGOC", "AHIS", "ANAM", "APHY", "APOL", "ATSI", "BABS", "BIOC", "BIOC", "BIOD", 
    "BSSM", "CHEM", "CRIM", "HESC", "HIST", "HPSC", "HPST", "INOV", "INST", "LIFE", 
    "MATH", "MICM", "MICR", "NEUR", "OPTM", "PATM", "PECO", "PHAR", "PHPH", "PHSL", "PHYS", 
    "POLS", "PROR", "PSYC", "SCIF", "SCIF", "SCOM", "SCTS", "SESC", "SLSP", "SOCA", "SOCF", 
    "SOCW", "SOMS", "SRAP", "VISN", "ZHSS", "ZHSS", "ZPEM"]

    medicine = ["SURG", "MEDM", "MFAC", "PDCS", "MEED", "RUHE", "GENM", "MDSG", 
    "PHCM", "NEUR", "PDCS", "CMED", "MDCN", "HEAL"]

    law = ["HPSC", "LEGT", "GENC", "GENC", "TABL", "LAWS", "JURD", "GENL", 
    "LEGT", "JURD", "ATAX"]

    business = ["ACCT", "AECM", "COMM", "ECON", "FINS", "GBAT", "GENC", "GSOE", "IBUS", "IROB", "LEGT", 
    "MFIN", "MGMT", "MNGT", "REGZ", "STRE", "TABL", "XACC", "XBUS", "XFIN", "XINT", "XMKM", "XPRO", 
    "ZBUS", "ZGEN", "ZINT"]
    res = engineering + environment + arts + science +  medicine + law + business
    return list(set(res))
def get_urls():
    res = []
    with open("url_lists.txt", "r")  as f:
        lines = f.readlines()
        for n, l in enumerate(lines):
            
            try:
                s = "http://"
                s += l.split()[1].rstrip()
                if any(i in s for i in ["google", "blogspot"]):
                    continue
                res.append(s)
            except:
                pass
    return res
# urls = [
#     'http://www.python.org',
#     'http://www.python.org/about/',
#     'http://www.onlamp.com/pub/a/python/2003/04/17/metaclasses.html',
#     'http://www.python.org/doc/',
#     'http://www.python.org/download/',
#     'http://www.python.org/getit/',
#     'http://www.python.org/community/',
#     'https://wiki.python.org/moin/',
# ]

urls = []
urls = get_urls()
#print(urls[:20])
# data = get_faculty_data()
# print(len(data))
# year = "2020"
# for term in ["U1", "T1", "T2", "T3"]:
#     for code in data:
#         urls.append( generate_class_url(code, term, year))
# print(len(urls))
# import sys
# sys.exit(1)
import time
start_time = time.time()
# res = parse_url_with_parallel(urls)
###
if __name__ == "__main__":
    
    from multiprocessing import Pool
    import itertools
    p = Pool(processes=4)
    #requests_session = requests.Session()
    try:
        res = p.map(get_request_multi, urls)
    except Exception as e:
        print(e)
        import sys
        sys.exit(1)
    ###


    l = [i for i in res if i]
    print (len(l))
    #print(res)
    print("--- %s seconds ---" % (time.time() - start_time))

