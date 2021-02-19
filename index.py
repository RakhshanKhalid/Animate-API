from urllib.request import urlopen,Request
from bs4 import BeautifulSoup as bs
import re 
import json
import flask
from flask import jsonify

#flask
app = flask.Flask(__name__)
app.config["DEBUG"] = True

#website url
base_url = "https://123animes.mobi"





def getData(url): 
    #Requesting the html source code
    url_link = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    url_page = urlopen(url_link).read()
    url_html = bs(url_page, 'html.parser')

    containers = url_html.find_all('div',class_='film-list')

    #looping through containers to extract more detailed info
    for items in containers[:1]:
        animes_url_name = items.find_all('a',class_ = "name") #extracting name/title and URL of all Anime in the current page
        anime_image = items.find_all('img') #extracting IMAGE all Anime in the current page
        anime_lang = items.find_all(True, {"class":["sub", "dub"]}) #extracting LANGUAGE of all Anime in the current page

    #anime url and name
    array_length = len(animes_url_name)

    #store collected data in list
    data=[]
    for x in range(array_length):
        item={}
        item['title'] = animes_url_name[x].get('data-jtitle')
        item['url'] = base_url+animes_url_name[x].get('href')
        item['lang'] = anime_lang[x].get_text()
        item['image'] = anime_image[x].get('src')
        data.append(item)
    
    return data




@app.route('/home', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/api/v1/airing', methods=['GET'])
def airin_anime():
    url_ = base_url + "/filter?status[]=ongoing&keyword="
    data_ = getData(url_)
    return jsonify(data_)

@app.route('/api/v1/upcoming', methods=['GET'])
def upcoming_anime():
    url_ = base_url + "/filter?status[]=upcoming&keyword="
    data_ = getData(url_)
    return jsonify(data_)

@app.route('/api/v1/finished', methods=['GET'])
def finished_anime():
    url_ = base_url + "/filter?status[]=completed&keyword="
    data_ = getData(url_)
    return jsonify(data_)

@app.route('/api/v1/search/', methods=['GET'])
def search_anime():
    url_ = base_url + "/filter?keyword=shingeki-no-kyojin"
    data_ = getData(url_)
    return jsonify(data_)

app.run()