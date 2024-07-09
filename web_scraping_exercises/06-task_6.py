# Task: 6. Write a Python program to extract h1 tag from example.com.

from lxml import html
import requests


response = requests.get('http://example.com/')
doc = html.fromstring(response.text)
# h1_element = doc.cssselect('h1')[0].text_content()   ## only getting the title text
h1_element = doc.cssselect('h1')[0]
title_with_tags = html.tostring(h1_element, encoding='unicode')
print(title_with_tags)





