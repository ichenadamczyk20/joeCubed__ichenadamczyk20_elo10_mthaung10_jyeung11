import sqlite3
import dbmanager
#API STUFF START
import http.client
import json
import urllib.parse
import requests
#API STUFF END

for x in range (0,5):#get an image <number> amount of times
    conn = http.client.HTTPSConnection("dog.ceo")
    conn.request('GET', '/api/breeds/image/random')
    response = conn.getresponse()
    dict = json.loads(response.read())
    picture=dict['message']#get image source

    
    "https://images.dog.ceo/breeds/collie-border/n02106166_4450.jpg"
    
    title = picture[30:]
    index = title.rindex("/")
    title = title[:index]
    title = title.replace("-", " ")

    # print(title)
    # print(picture)
    
    if dbmanager.getItemInfoByPicture(picture) == None:
        dbmanager.addItem(title, picture, "description", "flair", "dogs")

dbmanager.showLists()
