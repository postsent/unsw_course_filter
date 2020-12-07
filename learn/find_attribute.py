from bs4 import BeautifulSoup
"""https://stackoverflow.com/questions/11205386/python-beautifulsoup-get-an-attribute-value-based-on-the-name-attribute
"""
s = '<div class="question" id="get attrs" name="python" x="something">Hello World</div>'
soup = BeautifulSoup(s, features="lxml")

attributes_dictionary = soup.find('div').attrs
print (attributes_dictionary)
# prints: {'id': 'get attrs', 'x': 'something', 'class': ['question'], 'name': 'python'}

print (attributes_dictionary['class'][0])
# prints: question

print (soup.find('div').get_text())
# prints: Hello World