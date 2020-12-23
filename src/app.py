"""
https://www.youtube.com/watch?v=mCy52I4exTU&ab_channel=teclado

perc, num, are fixed constant connected between front and back end

"""
from flask import Flask, render_template, request
import os
from class_scraper import Class_scrapter
import atexit

app = Flask(__name__)

headings = []
data = []
degree = []
term = "T1"
under_post = "undergrad"
perc_num = "num"
courses_done = ""
year = "2021"

def get_database():
    global headings
    global data
    global courses_done
    global under_post
    global perc_num
    global degree
    global term
    global year

    return headings, data, courses_done, under_post, perc_num, degree, term, year

def set_database(_headings, _data, _courses_done, _under_post, _perc_num, _degree, _term, _year):
    global headings
    global data
    global courses_done
    global under_post
    global perc_num
    global degree
    global term
    global year
    headings, data, courses_done, under_post, perc_num, degree, term, year = _headings, _data, _courses_done, _under_post, _perc_num, _degree, _term, _year

@app.route("/")
def table():
    headings, data, courses_done, under_post, perc_num, degree, term, year = get_database()
    
    return render_template("table.html", headings=headings, data=data, term=term, courses_done=courses_done, under_post=under_post, perc_num=perc_num, year=year)

@app.route('/handle_close', methods=['GET']) 
def handle_close():
    headings, data, courses_done, under_post, perc_num, degree, term, year = get_database()

    c = request.args.get('close') # handle no input and initial assignment of none
    print(c)
    print(degree)
    try:
        degree.remove(c)
    except:
        pass
    set_database(headings, data, courses_done, under_post, perc_num, degree, term, year)
    return render_template("table.html", headings=headings, data=data, term=term, courses_done=courses_done, under_post=under_post, perc_num=perc_num, year=year, degree=degree)

@app.route('/handle_degree', methods=['GET']) 
def handle_degree():
    headings, data, courses_done, under_post, perc_num, degree, term, year = get_database()

    d = request.args.get('degree') # handle no input and initial assignment of none
    if d and not d in degree:
        degree.append(d)
        
    set_database(headings, data, courses_done, under_post, perc_num, degree, term, year)
    
    return render_template("table.html", headings=headings, data=data, term=term, courses_done=courses_done, under_post=under_post, perc_num=perc_num, year=year, degree=degree)

@app.route('/handle_search', methods=['POST'])
def handle_search():

    headings, data, courses_done, under_post, perc_num, degree, term, year = get_database()
    term= request.form.get("termDropdown") if request.form.get("termDropdown") else term
    year= request.form.get("yearDropdown") if request.form.get("yearDropdown") else year
    under_post= request.form.get("levelDropdown") if request.form.get("levelDropdown") else under_post
    perc_num= request.form.get("percDropdown") if request.form.get("percDropdown") else perc_num
    courses_done= request.form.get('courses_done') if request.form.get("courses_done") or request.form.get("courses_done") == "" else courses_done

    if degree:
        c = Class_scrapter(degree, term, True, (True if "under" in under_post else False), perc_num, True, courses_done, "", year)
        data_list = c.get_list()
        headings= data_list[0]
        data = data_list[1:]
    set_database(headings, data, courses_done, under_post, perc_num, degree, term, year)
    return render_template('table.html', under_post=under_post, headings=headings, data=data, term=term, perc_num=perc_num, courses_done=courses_done, year=year)    


# https://stackoverflow.com/questions/3850261/doing-something-before-program-exit
def exit_handler():
    global headings
    global data
    global degree
    global under_post
    global perc_num
    global courses_done

    headings = []
    data = []
    degree = []
    under_post = "under"
    perc_num = "num"
    courses_done = ""

atexit.register(exit_handler)

if __name__=="__main__":
    app.run(debug=1)