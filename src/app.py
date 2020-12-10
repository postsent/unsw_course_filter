"""
https://www.youtube.com/watch?v=mCy52I4exTU&ab_channel=teclado
"""
from flask import Flask, render_template, request
import os
from class_scraper import Class_scrapter

app = Flask(__name__)

c = Class_scrapter()
data_list = c.get_list()
headings= data_list[0]
data = data_list[1:]
@app.route("/")
def table():
    p = os.path.abspath("table.html")
    return render_template("table.html", headings=headings, data=data)

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    print(processed_text)
    return processed_text

# p = os.path.abspath("table.html")
# print(p)
if __name__=="__main__":
    app.run(debug=1)