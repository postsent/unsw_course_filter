"""
see degrees as example
extract info from classutil for 2020 ranking of classes
"""

from bs4 import BeautifulSoup
import requests
import re

# https://stackoverflow.com/questions/18297791/consecutive-uppercase-letters-regex
def regexp_find(s):
    res = re.findall("(?<![A-Z])[A-Z]{4}(?![A-Z])", s)
    
    return res[0] if res else ""
    
url = "https://nss.cse.unsw.edu.au/sitar/classes2020/index.html"

response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")

tweet = content.findAll(["tr"])
degrees_list = []
for i, t in enumerate(tweet):
    s = t.text
    normalised = s.replace("\n", " ")
    l = s.split(" ")
    s = regexp_find(s)
    
    if s and s != "UNSW":
        s = s.strip()
        n = normalised.index(s)
        res_str = normalised[:n].strip()
        degrees_list.append(s + " " + res_str)

with open("degrees", "w",  encoding='utf-8') as f: # https://stackoverflow.com/questions/3218014/unicodeencodeerror-gbk-codec-cant-encode-character-illegal-multibyte-sequen
    for d in degrees_list:
        f.write(d)
        f.write("\n")

