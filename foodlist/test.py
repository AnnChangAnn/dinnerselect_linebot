
import os

from bs4 import BeautifulSoup
from selenium import webdriver

import random
import re
import urllib
import json


q_string = {'q': "蘋果" }
    
url = f"https://www.google.com/search?tbm=isch&tbs=isz:m&{urllib.parse.urlencode(q_string)}/"
print(url)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

soup = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=headers)),'html.parser')

ActualImages=[]
for a in soup.find_all("img", class_="rg_i Q4LuWd tx8vtf", limit=1):
    print(a.get('data-iurl'))
    ActualImages.append(a.get('data-iurl'))
    print(ActualImages)

#        return ActualImages
       


       
