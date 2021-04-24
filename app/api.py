#!/usr/bin/env python3
import http.client
import json
import urllib.parse
import requests

def getRandomDog():
    return ""

def getWikipediaImg(name):
    #wikipedia
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    SEARCHPAGE = name

    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": SEARCHPAGE
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    print(DATA['query']['search'][0])
    url = "https://en.wikipedia.org/w/api.php?action=parse&pageid=" + str(DATA['query']['search'][0]['pageid']) + "&prop=text&format=json"
    conn = http.client.HTTPSConnection("wikipedia.org")
    conn.request('GET', url)
    response = conn.getresponse()
    src = response.read().decode().split('img')[1].split('src=\\"')[1].split('\\"')[0]
    return src

if __name__ == "__main__":
    #https://dog.ceo/dog-api/
    
    conn = http.client.HTTPSConnection("dog.ceo")
    quest = input('Would you like to see a dog of the Hound breed? ')
    #question = urllib.parse.quote(quest)
    if (quest.lower() == "yes"):
        conn.request('GET', '/api/breed/hound/images')
        response = conn.getresponse()
        dict = json.loads(response.read())
        print (dict['message'][1])
    else:
        print ("Okay then. :(")

    print()

    quest = input('What breed of dog would you like to see? ').lower()
    conn.request('GET', '/api/breed/' + quest + '/images/random')
    response = conn.getresponse()
    dict = json.loads(response.read())
    print (dict['message'])

    print ()

    #https://www.fruityvice.com/
    conn = http.client.HTTPSConnection("fruityvice.com")
    quest = input('Would you like to see a fruit? ')
    keys = ["genus", "name", "id", "family", "order", "nutritions"]
    if (quest.lower() == "yes"):
        quest2 = input('What fruit would you like info on? (please type a singular fruit) ')
        conn.request('GET', '/api/fruit/' + quest2.lower())
        response = conn.getresponse()
        dict = json.loads(response.read().decode('utf-8'))
        for x in keys:
            if (x != "id" and x != "nutritions"):
                print (x + ": " + dict[x])
            if (x == "nutritions"):
                print ()
                print ("nutritions:")
                for x in dict["nutritions"]:
                    print (x + ": " + str(dict["nutritions"][x]))
    else:
        print ("That's unfortunate. ;v;")

    print()

