#using archMod.mat and printing archMod.class

#import necessary packages

import requests as r
import bs4
import numpy as np
import re

#the following code webscrapes the url stored in the var "url"

url = "http://127.0.0.1:2211/?data.class;"
request = r.get(url)
xml_stuff = request.text


soup = bs4.BeautifulSoup(xml_stuff,features="lxml")
classes = []

for result in soup.findAll("td"):
	classes.append(result.text)

for i in range(len(classes)):
	classes[i] = [x for x in classes[i].split('\n') if x != '']

print(classes)

