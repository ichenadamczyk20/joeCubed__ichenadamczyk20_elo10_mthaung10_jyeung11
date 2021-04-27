import sqlite3
import dbmanager
#API STUFF START
import http.client
import json
import urllib.parse
import requests
#API STUFF END

# for x in range (0,5):#get an image <number> amount of times
#     conn = http.client.HTTPSConnection("dog.ceo")
#     conn.request('GET', '/api/breeds/image/random')
#     response = conn.getresponse()
#     dict = json.loads(response.read())
#     picture=dict['message']#get image source

    
#     "https://images.dog.ceo/breeds/collie-border/n02106166_4450.jpg"
    
#     title = picture[30:]
#     index = title.rindex("/")
#     title = title[:index]
#     title = title.replace("-", " ")

#     # print(title)
#     # print(picture)
    
#     if dbmanager.getItemInfoByPicture(picture) == None:
#         dbmanager.addItem(title, picture, "description", "flair", "dogs")

# dbmanager.showLists()

food = ["adzuki", "almond", "amla", "arbi", "aubergine", "avocado", "bael fruit", "banana", "betelnut", "bora berry", "bora jujube", "breadfruit", "cacao", "calamondin", "carambola", "cashew", "cashew apple", "cassava", "chickpea", "chili pepper", "clove", "coconut", "coriander", "curry leaf", "custard apple", "date palm", "dill", "doringu", "dragon fruit", "dudhi", "durian", "fennel", "fenugreek", "fig", "ginger", "gisuri", "guar", "guava", "gunda", "hazelnut", "jackfruit", "jambolan", "java apple", "kantola", "karela", "kiwi", "langsat", "lentil", "lime", "longan", "loquat", "lychee", "macadamia", "mango", "mangosteen", "manila tamarind", "millet", "mogri", "mooli", "moringa", "mung", "mustard", "naranjilla", "neem", "nutmeg", "okra", "olive", "oregano", "papaya", "passionfruit", "peanut", "pecan", "pepper", "persimmon", "physalis", "pineapple", "pineapple guava", "pistachio", "pomegranate", "pommelo", "prickly pear", "rambutan", "rosemary", "sapodilla", "sesame", "sittu", "star anise", "strawberry guava", "sugar apple", "sugarcane", "tamarillo", "tamarind", "tindora", "tropical almond", "tuar", "tulsi", "turmeric", "urad", "vanilla", "wood apple", "zalacca"]
for x in range (0, 101):
    quest = food[x]
    quest = quest.replace(" ", "%20")
    link = "http://api.tropicalfruitandveg.com/tfvjsonapi.php?tfvitem=" + quest.lower()
    u = urllib.request.urlopen(link)
    response = json.loads(u.read().decode("ISO-8859-1"))
    print (response['results'][0]['tfvname']) #name of fruit/vegetable
    print (response['results'][0]['imageurl'])
    dbmanager.addItem(response['results'][0]['tfvname'], response['results'][0]['imageurl'], "description", "flair", "fruits")

dbmanager.showLists()