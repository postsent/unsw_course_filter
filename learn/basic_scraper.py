from bs4 import BeautifulSoup
import requests
url_verge = "https://www.theverge.com/tech"
#url = "http://ethans_fake_twitter_site.surge.sh/"
response = requests.get(url_verge, timeout=5)
content = BeautifulSoup(response.content, "html.parser")
#print(content) # print out all html for the wepage
tweet = content.findAll('h3', attrs={"class":"c-entry-box-base__headline"}) # here class == c-entry...
for i, t in enumerate(tweet):
    print(t.text)
    print()
    if (i == 3): break
#print(tweet)