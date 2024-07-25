# Task: Write a Python program to display the contains of different attributes like status_code, headers, url,
# history, encoding, reason, cookies, elapsed, request and content of a specified resource.

import requests

url = 'https://python.org'

response = requests.get(url)

print(f"Status code: {response.status_code}")
# for i, j in response.headers.items():
#     print(f"{i} and {j}")
print(f"Headers: {response.headers}")
print(f"Encoding: {response.encoding}")
print(f"Reason: {response.reason}")
print("Cookies: ", response.cookies)
print("Elapsed: ", response.elapsed)
print("Request: ", response.request)
print("Content: ", response._content)