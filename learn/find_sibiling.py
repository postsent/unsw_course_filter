from bs4 import BeautifulSoup

soup = BeautifulSoup('<html><p>line 1</p><div><a>line 2</a></div></html>', features="lxml")
print(soup.find('p').nextSibling.name)
