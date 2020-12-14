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
for i, t in enumerate(tweet):
    s = t.text
    l = s.split(" ")
    print(regexp_find(s))
