from flask import Flask, render_template
import os
from class_scraper import Class_scrapter

app = Flask(__name__)
headings= ("Name" "Role", "Salary")
c = Class_scrapter()
data_list = c.get_list()
data = (
    ("a", "b", "c"),
    ("a", "b", "c"),
    ("a", "b", "c")
)

@app.route("/")
def table():
    p = os.path.abspath("table.html")
    return render_template("table.html", headings=headings, data=data)

# p = os.path.abspath("table.html")
# print(p)
if __name__=="__main__":
    app.run(debug=1)