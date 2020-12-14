"""
ctrol + shift + l to convert "term 1" to "term1"
"""
from bs4 import BeautifulSoup
import requests
from class_scraper import Class_scrapter

def generate_format_dict():
    degree_dict = {}

    with open("degrees", "r") as f:
        lines = f.readlines()
        for l in lines:
            d = l.strip().split(" ")
            degree_dict[d[0]] = d[1:]
    return degree_dict

year = "2020"

#"https://nss.cse.unsw.edu.au/sitar/classes2020/ACCT_T1.html"

url_prefix = "https://nss.cse.unsw.edu.au/sitar/classes"
degree_dict = generate_format_dict()

for degree, terms in degree_dict.items():
    for t in terms:
        
        url = f"{url_prefix}{year}/{degree}_{t}.html"
        
        c = Class_scrapter(degree, t, True, True, "lec", None, None, url)
        ls = c.get_list()
        for l in ls[:20]: # get top 20 based on lec number
            print(l[1], l[4], l[5])
        print()
    break

