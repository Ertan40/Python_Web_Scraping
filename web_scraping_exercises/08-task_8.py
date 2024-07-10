# Task: 8. Write a Python program to extract and display all the image links
# from en.wikipedia.org/wiki/Peter_Jeffrey_(RAAF_officer).


from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen('https://en.wikipedia.org/wiki/Peter_Jeffrey_(RAAF_officer)')
soup = BeautifulSoup(html, "html.parser")
image_links = soup.find_all("img", {'src': re.compile('.jpg')})
# print(image_links)
for image in image_links:
    print(image['src'])