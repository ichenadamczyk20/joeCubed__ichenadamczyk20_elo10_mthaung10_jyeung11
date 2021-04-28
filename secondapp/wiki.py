import requests, http

queries = ["apple"]
#rstrip removes last character if comma
#split creates a list by slicing at commas
imageSrcs = [None] * len(queries)
i = 0
for query in queries:
    S = requests.Session()

    URL = "https://commons.wikimedia.org/w/api.php"

    SEARCHPAGE = query

    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": SEARCHPAGE
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    print(DATA)

    print(DATA['query']['search'][0])
    url = "https://commons.wikimedia.org/w/api.php?action=parse&pageid=" + str(DATA['query']['search'][0]['pageid']) + "&prop=text&format=json"
    conn = http.client.HTTPSConnection("wikimedia.org")
    conn.request('GET', url)
    response = conn.getresponse().read().decode("ISO-8859-1")
    print(response)
    # src = response.read().decode().split('img')[1].split('src=\\"')[1].split('\\"')[0]
    # imageSrcs[i] = src
    # i += 1