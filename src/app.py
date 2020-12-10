"""
https://www.youtube.com/watch?v=mCy52I4exTU&ab_channel=teclado
"""
from flask import Flask, render_template, request
import os
from class_scraper import Class_scrapter

app = Flask(__name__)

headings = []
data = []

@app.route("/")
def table():
    global headings
    global data

    return render_template("table.html", headings=headings, data=data)
    
@app.route('/', methods=['POST'])
def my_form_post():
    global headings
    global data
    
    try:
        url = request.form['text']
        c = Class_scrapter(url)
        data_list = c.get_list()
        headings= data_list[0]
        data = data_list[1:]
    except:
        pass
    
    return render_template("table.html", headings=headings, data=data)

@app.route("/submitted", methods=['POST'])
def hello():
   myvariable = request.form.get("teamDropdown")
   print(myvariable)
   return myvariable

# p = os.path.abspath("table.html")
# print(p)
if __name__=="__main__":
    app.run(debug=1)