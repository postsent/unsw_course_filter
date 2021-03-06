"""
https://www.youtube.com/watch?v=mCy52I4exTU&ab_channel=teclado

flask session - https://stackoverflow.com/questions/32815451/are-global-variables-thread-safe-in-flask-how-do-i-share-data-between-requests

perc, num, are fixed constant connected between front and back end


"""
from flask import Flask, render_template, request, session
from flask_session import Session
import os
from class_scraper import Class_scrapter
from handle_multiple_degree import Degrees_sorting # main 
import atexit

app = Flask(__name__)
# Check Configuration section for more details
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)  
Session(app) 
# The limits of what you can store in a cookie are relatively low and depend on the browser, but typically is 4kb.
# https://stackoverflow.com/questions/43435217/how-to-set-sessions-limit-in-flask

def init_database():
    session["headings"] = []
    session["data"] = []
    session["degree"] = []
    session["term"] = "T1"
    session["under_post"] = "undergrad"
    session["perc_num"] = "lec"
    session["courses_done"] = ""
    session["year"] = "2021"
    session["levels"] = {0:True, 1:True,2:True,3:True, 4:True, 5:True, 6:True, 7:True, 8:True, 9:True} # course level
    session["data_list"] = []
    session["is_search_changed"] = True # TODO - is_search_changed - degree, year, term, under_post changes, send new request, degree is in separate submit form
    
    # 0 - GENM0709  

def get_database():

    return session["headings"], session["data"], session["courses_done"], session["under_post"], \
            session["perc_num"], session["degree"], session["term"], session["year"], session["levels"]

def set_database(_headings, _data, _courses_done, _under_post, _perc_num, _degree, _term, _year, _levels):
    session["headings"] = _headings
    session["data"] = _data
    session["degree"] = _degree
    session["term"] = _term
    session["under_post"] = _under_post
    session["perc_num"] = _perc_num
    session["courses_done"] = _courses_done
    session["year"] = _year
    session["levels"] = _levels

@app.route("/") # default page
def table():
    init_database()
    headings, data, courses_done, under_post, perc_num, degree, term, year, levels = get_database()
    
    return render_template("table.html", headings=headings, data=data, term=term, courses_done=courses_done, \
                            under_post=under_post, perc_num=perc_num, year=year, levels=levels)

@app.route('/handle_search', methods=['POST']) # main
def handle_search():

    headings, data, courses_done, under_post, perc_num, degree, term, year, levels = get_database()
    old_data = {}
    old_data["term"], old_data["year"], old_data["under_post"] = term, year, under_post
    
    term= request.form.get("termDropdown") if request.form.get("termDropdown") else term
    year= request.form.get("yearDropdown") if request.form.get("yearDropdown") else year
    under_post= request.form.get("levelDropdown") if request.form.get("levelDropdown") else under_post
    perc_num= request.form.get("percDropdown") if request.form.get("percDropdown") else perc_num
    courses_done = request.form.get('courses_done') if request.form.get("courses_done") or request.form.get("courses_done") == "" else courses_done
    prev_level = levels
    levels = {}
    for i in [*prev_level]:
        l = True if request.form.get(f"level{i}") or request.form.get(f"level{i}") == "" else False
        levels[i] = l
    # change if need to send new request
    if not (old_data["term"] == term and old_data["year"] == year and old_data["under_post"] == under_post):    
        session["is_search_changed"] = True

    if degree:
        c = Degrees_sorting(degree, term, True, (True if "under" in under_post else False), 
                            perc_num, True, courses_done, "", year, levels, session["is_search_changed"], session["data_list"])
        data_list = c.get_list()
        headings= data_list[0]
        data = data_list[1:]
        if session["is_search_changed"]:
            session["data_list"] = data_list # only when data input change
        session["is_search_changed"] = False # refresh

    set_database(headings, data, courses_done, under_post, perc_num, degree, term, year, levels)
    return render_template('table.html', under_post=under_post, headings=headings, data=data, term=term, \
                            perc_num=perc_num, courses_done=courses_done, year=year, degree=degree, levels=levels) 

@app.route('/handle_close', methods=['GET']) 
def handle_close(): # close the degree button
    headings, data, courses_done, under_post, perc_num, degree, term, year, levels = get_database()

    c = request.args.get('close') # handle no input and initial assignment of none

    try:
        degree.remove(c)
        session["is_search_changed"] = True
    except:
        pass
    set_database(headings, data, courses_done, under_post, perc_num, degree, term, year, levels)
    return render_template("table.html", headings=headings, data=data, term=term, courses_done=courses_done, \
                            under_post=under_post, perc_num=perc_num, year=year, degree=degree, levels=levels)

@app.route('/handle_clear', methods=['GET']) 
def handle_clear(): # close the degree button
    headings, data, courses_done, under_post, perc_num, degree, term, year, levels = get_database()
    degree = []
    set_database(headings, data, courses_done, under_post, perc_num, degree, term, year, levels)
    return render_template("table.html", headings=headings, data=data, term=term, courses_done=courses_done, \
                            under_post=under_post, perc_num=perc_num, year=year, degree=degree, levels=levels)

@app.route('/handle_degree', methods=['GET']) # handle multiple degree input, add to list
def handle_degree():
    headings, data, courses_done, under_post, perc_num, degree, term, year, levels = get_database()

    d = request.args.get('degree').upper() # handle no input and initial assignment of none
    if d and not d in degree:
        degree.append(d)
        session["is_search_changed"] = True
    
    set_database(headings, data, courses_done, under_post, perc_num, degree, term, year, levels)
    
    return render_template("table.html", headings=headings, data=data, term=term, courses_done=courses_done, \
                            under_post=under_post, perc_num=perc_num, year=year, degree=degree, levels=levels)

# https://stackoverflow.com/questions/3850261/doing-something-before-program-exit
# def exit_handler():
#     global headings
#     global data
#     global degree
#     global under_post
#     global perc_num
#     global courses_done

#     headings = []
#     data = []
#     degree = []
#     under_post = "under"
#     perc_num = "num"
#     courses_done = ""

# atexit.register(exit_handler)

if __name__=="__main__":
    # import cProfile
    # import pstats
    # import io
    # pr = cProfile.Profile()
    # pr.enable()
    import time
    start_time = time.time()
    app.run(debug=1)
    print("--- %s seconds ---" % (time.time() - start_time))

    # pr.disable()
    # s = io.StringIO()
    # ps = pstats.Stats(pr, stream=s).sort_stats("cumtime")
    # ps.print_stats()
    # with open("time.txt", "w+") as f:
    #     f.write(s.getvalue())
