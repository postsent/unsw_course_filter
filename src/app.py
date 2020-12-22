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
degree = ""
term = "T1"
under_post = "undergrad"
perc_num = "num"
courses_done = ""
year = "2021"

@app.route("/")
def table():
    global headings
    global data
    global courses_done
    global under_post
    global perc_num
    global degree
    global term
    global year
    
    return render_template("table.html", headings=headings, data=data, term=term, courses_done=courses_done, under_post=under_post, perc_num=perc_num, year=year)
    
@app.route('/', methods=['POST'])
def my_form_post():

    global headings
    global data
    global degree
    global under_post
    global perc_num
    global courses_done
    global term
    global year

    try:
        prev = degree
        degree = request.form['degree'] if request.form['degree'] else degree # handle no input and initial assignment of none
    except:
        pass
    try:
        term = request.form.get("termDropdown") if request.form.get("termDropdown") else term
    except:
        pass
    try:
        year = request.form.get("yearDropdown") if request.form.get("yearDropdown") else year
    except:
        pass
    try:
        under_post = request.form.get("levelDropdown") if request.form.get("levelDropdown") else under_post
    except:
        pass
    try:
        perc_num = request.form.get("percDropdown") if request.form.get("percDropdown") else perc_num
    except:
        pass
    try:
        courses_done = request.form.get('courses_done') if request.form.get("courses_done") or request.form.get("courses_done")=="" else courses_done
    except:
        pass
    
    if degree:
        c = Class_scrapter(degree, term, True, (True if "under" in under_post else False), perc_num, True, courses_done, "", year)
        data_list = c.get_list()
        headings= data_list[0]
        data = data_list[1:]
    
    return render_template('table.html', under_post=under_post, headings=headings, data=data, degree=degree, term=term, perc_num=perc_num, courses_done=courses_done, year=year)    


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
    degree = ""
    under_post = "under"
    perc_num = "num"
    courses_done = ""

atexit.register(exit_handler)

if __name__=="__main__":
    app.run(debug=1)