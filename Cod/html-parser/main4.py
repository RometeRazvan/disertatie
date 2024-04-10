import requests
import json
from bs4 import BeautifulSoup
import html_to_json

# username = 'vgtgayan'
# base_url = 'https://www.kaggle.com/'
# url = base_url+str(username)

# r = requests.get(url)
# print(r.status_code)

# html_string = r.text
#read from sample.html
with open("sample.html", "r") as file:
    html_string = file.read()

output_json = html_to_json.convert(html_string)
with open("horoscope_data.json", "w") as file:
    json.dump(output_json, file)

# print(output_json)

lst = []

def iterate_json(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == '_value' and value[0] == ':' :  # Do whatever operation you want here
                print(value)
                lst.append(value)
            iterate_json(value)
    elif isinstance(obj, list):
        for item in obj:
            iterate_json(item)
    # else:
    #     print(obj)  # Base case, when it's neither a dict nor a list

iterate_json(output_json)
print(lst)