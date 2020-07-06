#using archMod.mat and printing archMod.classid

#import necessary packages

import requests as r
import bs4
import numpy as np
import re

#the following code webscrapes the url stored in the var "url"

url = "http://127.0.0.1:2211/?data.classid;"
request = r.get(url)
xml_stuff = request.text


soup = bs4.BeautifulSoup(xml_stuff,features="lxml")
classes = []
clean_classes = []

for result in soup.findAll("tr"):
	classes.append(result.text)

for i in range(len(classes)):
	classes[i] = [x for x in classes[i].split('\n')]
for i in range(len(classes)):
	if(classes[i] != ['','','']):
		clean_classes.append(classes[i])

for myclass in clean_classes:
	del myclass[0],myclass[-1]

print(clean_classes)
