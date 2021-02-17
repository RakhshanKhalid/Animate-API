from urllib.request import urlopen,Request
from bs4 import BeautifulSoup as bs
import re 
import json

#website url
base_url = "https://123animes.mobi/filter?country%5B%5D=j&status%5B%5D=ongoing&keyword="
url_="https://123animes.mobi"
url = base_url

#Requesting the html source code
url_link = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
url_page = urlopen(url_link).read()
url_html = bs(url_page, 'html.parser')

containers = url_html.find_all('div',class_='film-list')

#looping through containers to extract more detailed info
for items in containers[:1]:
    animes_url_name = items.find_all('a',class_ = "name") #extracting name/title of all Anime in the current page
    anime_image = items.find_all('img')
    anime_lang = items.find_all(True, {"class":["sub", "dub"]})

#anime url and name
array_length = len(animes_url_name)
anime_data=[0]*array_length

#store collected data in list
data=[]
for x in range(array_length):
    item={}
    item['title'] = animes_url_name[x].get('data-jtitle')
    item['url'] = url_+animes_url_name[x].get('href')
    item['lang'] = anime_lang[x].get_text()
    item['image'] = anime_image[x].get('src')
    data.append(item)
    
#convertind list to json
with open("textbooks.json", "w") as writeJSON:
    json.dump(data, writeJSON, ensure_ascii=False)

