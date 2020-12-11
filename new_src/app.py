"""
https://www.youtube.com/watch?v=mCy52I4exTU&ab_channel=teclado
"""
from flask import Flask, render_template, request
import os
from class_scraper import Class_scrapter
import atexit



app = Flask(__name__)

headings = []
data = []
url = ""
under_post = "undergrad"
perc_num = "number"
courses_done = ""

@app.route("/")
def table():
    global headings
    global data

    return render_template("table.html", headings=headings, data=data)
    
@app.route('/', methods=['POST'])
def my_form_post():

    global headings
    global data
    global url
    global under_post
    global perc_num
    global courses_done
    
    try:
        prev = url
        url = request.form['text'] if request.form['text'] else url # handle no input and initial assignment of none
        if url != prev:
            courses_done = "" # reload
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
    
    if url:
        c = Class_scrapter(url, True, (True if "under" in under_post else False), (True if "perc" in perc_num else False), True, courses_done)
        data_list = c.get_list()
        headings= data_list[0]
        data = data_list[1:]
    
    return render_template('table.html', under_post=under_post, headings=headings, data=data, url=url, perc_num=perc_num, courses_done=courses_done)    


# https://stackoverflow.com/questions/3850261/doing-something-before-program-exit
def exit_handler():
    global headings
    global data
    global url
    global under_post
    global perc_num
    global courses_done

    headings = []
    data = []
    url = ""
    under_post = "under"
    perc_num = "num"
    courses_done = ""

atexit.register(exit_handler)

if __name__=="__main__":
    app.run(debug=1)