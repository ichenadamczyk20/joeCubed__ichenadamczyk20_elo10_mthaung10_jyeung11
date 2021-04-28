import os
from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.exceptions import HTTPException
import dbmanager as db

#API STUFF START
import http.client
import json
import urllib.parse
import requests
import random
#API STUFF END

print("v")
app = Flask(__name__)
app.secret_key = os.urandom(10)

#forward thinking
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

#root route loads home page
@app.route("/", methods=["GET", "POST"])
def root():
    #checks to see if the user is already logged in
    loggedIn = "false"
    if "username" in session:
        loggedIn = "true"

    return render_template("home.html", loggedIn = loggedIn)


#login route loads login page
@app.route("/login", methods=["GET", "POST"])
def login():

    #error msgs are for when login attempt fails and returns you to the login page, and this code displays that error
    if "error_msg" in session:
        error_msg = session.pop("error_msg")
        return render_template("login.html", error_msg=error_msg)

    #this may not be necessary since a successful login attempt will just direct you to the home page
    if "success_msg" in session:
        success_msg = session.pop("success_msg")
        return render_template("login.html", success_msg=success_msg)

    return render_template("login.html")


#login submit route handles the form submission from pressing the login button on the login page
@app.route("/login-submit", methods=["POST"])
def authenticate():
    #obtain the inputted user and pass
    userInput = request.form['username']
    passInput = request.form['password']

    #check info against login database
    loginInfo = db.checkLogin(userInput, passInput)

    #if the check passes, adds account to the session and redirects you to home
    if loginInfo[0]:
        session["userid"] = loginInfo[2]
        session["username"] = userInput
        session["password"] = passInput
        return redirect("/")

    #if the check fails, returns the type of error message explaining what failed
    session["error_msg"] = loginInfo[1]
    return redirect("/login")


#register route returns the register page
@app.route("/register", methods=["GET", "POST"])
def register():
    if "error_msg" in session:
        error_msg = session.pop("error_msg")
        return render_template("register.html", error_msg=error_msg)
    if "success_msg" in session:
        success_msg = session.pop("success_msg")
        return render_template("register.html", success_msg=success_msg)
    return render_template("register.html")


#handles form submission for register
@app.route("/register-submit", methods=["POST"])
def registrate():
    userInput = request.form['username']
    passInput = request.form['password']
    passConfInput = request.form['passwordConf']

    # pls check if username and password and passwordConf are valid
    if not userInput.isalnum():
        session["error_msg"] = "Username must be alphanumeric"
        return redirect("/register")
    if not passInput == passConfInput:
        session["error_msg"] = "Passwords don't match"
        return redirect("/register")
    if db.getUserInfo(userInput) != None:
        session["error_msg"] = "Username already exists"
        return redirect("/register")

    # register the user
    db.registerUser(userInput, passInput)

    session["success_msg"] = "Success!"
    return redirect("/login")


#logout route logs the user out
@app.route("/logout", methods=["GET", "POST"])
def logout():

    #handles deleting session info
    if "username" in session:
        username = session.pop("username")
        session.pop("password")
        session.pop("userid")
        session["success_msg"] = "Logged you out! See you again, " + username
        return redirect("/")
    else:
        session["error_msg"] = "You weren't logged in"

    return redirect("/")

#list category route loads relevant info from the db

#apis = {
#    "dog": callThisFunction,
#    "fruit": callThisFunction
#}
@app.route("/list/<category>", methods=["GET", "POST"])
def list(category):

    #fetch the ids of all the entries belonging to the category
    ids = db.getAllItemsOf(category)

    #create a mini db of all the information of all the entries belonging to the category
    titles, pictures, descriptions, flairs, listids, itemids = [], [], [], [], [], []
    for i in ids:
        itemInfo = db.getItemInfo(i)
        titles.append(itemInfo[0])
        pictures.append(itemInfo[1])
        descriptions.append(itemInfo[2])
        flairs.append(itemInfo[3])
        listids.append(itemInfo[4])
        itemids.append(itemInfo[5])
    
    itemidsoffavoritedids = []
    if "username" in session:
        favoritedids = db.getAllFavoritedItemsOf(session['userid'])
        if favoritedids != None: #this only happens if the user has no favorited things
            for i in favoritedids:
                itemidsoffavoritedids.append(db.getFavoritedInfo(i)[2])


    #pass the mini db to the list page
    return render_template("generic_list.html", titles=titles, pictures=pictures, \
        descriptions=descriptions, flairs=flairs, listids=listids, itemids=itemids, category=category, \
        favorited=itemidsoffavoritedids, loggedIn="username" in session)


#profile route loads the profile page
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if not "username" in session:
        session["error_msg"] = "You must be logged in to have a profile page!"
        return redirect("/")
    favorites = db.getAllFavoritedItemsOf(session["userid"]) #get the user's favorited items in the form of ids in favorites table
    titles, pictures, descriptions, flairs, listids, itemids = [], [], [], [], [], []
    if favorites != None:
        items = [] #convert the fave ids to their respective item ids in the lists table
        for i in favorites:
            items.append(db.getItemIDByFaveID(i))
        for i in items: #populate the jinja parameters necessary to load the html
            info = db.getItemInfo(i)
            titles.append(info[0])
            pictures.append(info[1])
            descriptions.append(info[2])
            flairs.append(info[3])
            listids.append(info[4])
            itemids.append(info[5])
    return render_template("profile.html", titles=titles, pictures=pictures, descriptions=descriptions, \
            flairs=flairs, listids=listids, itemids=itemids)

#1. javascript sends a request to /favorite and waits for what is returned
#2. flask favorites/unfavorites and returns "unfavorited" or "favorited"
#3. javascript takes the returned "unfavorited" or "favorited"
@app.route("/favorite", methods=["POST"])
def favorite():
    itemID = int(request.form["itemID"])
    print(itemID)
    userID = session["userid"]
    print(userID)
    faveID = db.getFaveID(userID, itemID)
    print(faveID)
    if faveID != None:
        print("unfavoriting")
        db.deleteFavoritedItem(faveID)
        return "unfavorited"
    else: #if favorited is False or None
        print("favoriting")
        db.addFavoritedItem(session["userid"], request.form["listID"], itemID)
        return "favorited"
    db.showFavorited()

#API STUFF START
#https://dog.ceo/dog-api/
@app.route("/randomDog", methods=["GET", "POST"])
def getRandomDog():
    number = int(request.form["numDogs"]) #requested number of images
    list = [None] * number#initialize list
    
    for x in range (0,number):#get an image <number> amount of times
        conn = http.client.HTTPSConnection("dog.ceo")
        conn.request('GET', '/api/breeds/image/random')
        response = conn.getresponse()
        dict = json.loads(response.read())
        list[x]=dict['message']#get image source

    if (number == 1):
        message = "Here is your random dog image!"
    else:
        message = "Here are your " + str(number) + " random dog images!"

    return render_template("random.html", images = list, message = message)


@app.route("/randomBreed", methods=["GET", "POST"])
def getRandomBreed():
    number = int(request.form["numDogs"]) #requested number of images
    list = [None] * number#initialize list
    errorMsg = False

    conn = http.client.HTTPSConnection("dog.ceo")
    dogBreed = request.form['breed']
    for x in range(0,number):#get an image <number> amount of times
        conn.request('GET', '/api/breed/' + dogBreed + '/images/random')
        response = conn.getresponse()
        dict = json.loads(response.read())
        list[x]=dict['message']#get image source
        if list[x][0] != "h":
           errorMsg = True
           break

    if (number == 1):
        message = "Here is your random dog image"
    else:
        message = "Here are your " + str(number) + " random dog images"

    return render_template("random.html", images = list, message = message, breedQuery1 = " of the ", dogBreed=dogBreed.capitalize(), breedQuery2=" breed!", errorMsg=errorMsg)

@app.route("/loadMoreDogs", methods=["GET", "POST"])
def loadMoreDogs():
    for x in range (0,10):#get an image <number> amount of times
        conn = http.client.HTTPSConnection("dog.ceo")
        conn.request('GET', '/api/breeds/image/random')
        response = conn.getresponse()
        dict = json.loads(response.read())
        picture=dict['message']#get image source

        
        #"https://images.dog.ceo/breeds/collie-border/n02106166_4450.jpg"
        
        title = picture[30:]
        index = title.rindex("/")
        title = title[:index]
        title = title.replace("-", " ")

    # print(title)
    # print(picture)
    
        if db.getItemInfoByPicture(picture) == None:
            db.addItem(title, picture, "description", "flair", "dogs")
    return redirect("/list/dogs")
#====================================================================================



@app.route("/wikiImages", methods=["GET", "POST"])
def wikiImages():
    queries = request.form['queries'].rstrip(",").split(',') 
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
        thingsa = random.choice(DATA['query']['search'])
        url = "https://commons.wikimedia.org/w/api.php?action=parse&pageid=" + str(thingsa['pageid']) + "&prop=text&format=json"
        conn = http.client.HTTPSConnection("wikimedia.org")
        conn.request('GET', url)
        response = conn.getresponse().read().decode("ISO-8859-1")
        #src = "https://commons.wikimedia.org" + response.split('<img')[0].split('<a')[-1].split('href=\\"')[1].split('\\" ')[0]
        src = []
        for j in response.split('<img')[1:]:
            try:
                width = int(j.split('width=\\"')[1].split('\\"')[0])
                height = int(j.split('height=\\"')[1].split('\\"')[0])
                if width > 67 and height > 67 and src != 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Noimage.svg/173px-Noimage.svg.png':
                    src += ["https://" + j.split('>')[0].split('https://')[-1].split(' ')[0]]
            except:
                pass
        if (src == []):
            return "http://s3.amazonaws.com/pix.iemoji.com/images/emoji/apple/ios-12/256/pensive-face.png!!!try again"
        src = random.choice(src)
        if src.endswith('\\"'):
            src = src[:-2]
        imageSrcs[i] = src
        i += 1
        return imageSrcs[0] + "!!!" + thingsa['title']

@app.route("/randomTropical", methods=["GET", "POST"])
def randomTropical():
    food = ["adzuki", "almond", "amla", "arbi", "aubergine", "avocado", "bael fruit", "banana", "betelnut", "bora berry", "bora jujube", "breadfruit", "cacao", "calamondin", "carambola", "cashew", "cashew apple", "cassava", "chickpea", "chili pepper", "clove", "coconut", "coriander", "curry leaf", "custard apple", "date palm", "dill", "doringu", "dragon fruit", "dudhi", "durian", "fennel", "fenugreek", "fig", "ginger", "gisuri", "guar", "guava", "gunda", "hazelnut", "jackfruit", "jambolan", "java apple", "kantola", "karela", "kiwi", "langsat", "lentil", "lime", "longan", "loquat", "lychee", "macadamia", "mango", "mangosteen", "manila tamarind", "millet", "mogri", "mooli", "moringa", "mung", "mustard", "naranjilla", "neem", "nutmeg", "okra", "olive", "oregano", "papaya", "passionfruit", "peanut", "pecan", "pepper", "persimmon", "physalis", "pineapple", "pineapple guava", "pistachio", "pomegranate", "pommelo", "prickly pear", "rambutan", "rosemary", "sapodilla", "sesame", "sittu", "star anise", "strawberry guava", "sugar apple", "sugarcane", "tamarillo", "tamarind", "tindora", "tropical almond", "tuar", "tulsi", "turmeric", "urad", "vanilla", "wood apple", "zalacca"]
    number = int(request.form["numTropical"]) #requested number of images
    list = [None] * number #initialize list
    for x in range(0, number):
        integer = random.randint(0, 100)
        quest = food[integer].replace(" ", "%20")
        link = "http://api.tropicalfruitandveg.com/tfvjsonapi.php?tfvitem=" + quest.lower()
        u = urllib.request.urlopen(link)
        response = json.loads(u.read().decode("ISO-8859-1"))
        list[x] = response['results'][0]['imageurl']

    if (number == 1):
        message = "Here is your random tropical fruit/vegetable image!"
    else:
        message = "Here are your " + str(number) + " random tropical fruit/vegetable images!"
    return render_template("random.html", images = list, message = message, errorMsg = False)

#API STUFF END


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
    #app.run()