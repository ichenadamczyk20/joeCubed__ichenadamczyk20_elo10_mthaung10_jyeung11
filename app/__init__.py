import os
from flask import Flask, redirect, render_template, request, session, url_for
import dbmanager as db

#API STUFF START
import http.client
import json
import urllib.parse
import requests
#API STUFF END

app = Flask(__name__)
app.secret_key = os.urandom(10)
salt = b"We might copy a lot of things from p0 and p1, but not our salt string! Because we are safe and secure and huadsgp9aysrb86t42wbttas"

#root route loads home page
@app.route("/", methods=["GET", "POST"])
def root():

    #checks to see if the user is already logged in
    loggedIn = False
    if "username" in session:
        loggedIn = True

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

#THIS FUNCTION NEEDS TO BE COMMENTED BY IAN LATER
#THIS FUNCTION NEEDS TO BE COMMENTED BY IAN LATER
#THIS FUNCTION NEEDS TO BE COMMENTED BY IAN LATER
@app.route("/loginYT", methods=["GET", "POST"])
def loginYT():
    if "error_msg" in session:
        error_msg = session.pop("error_msg")
        return render_template("tester.html", error_msg=error_msg)
    if "success_msg" in session:
        success_msg = session.pop("success_msg")
        return render_template("tester.html", success_msg=success_msg)
    return render_template("tester.html")

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
        session["success_msg"] = "Logged you out! See you again,", username
        return render_template("login.html")
    else:
        session["error_msg"] = "You weren't logged in"

    return redirect("/login")

#list category route loads relevant info from the db
@app.route("/list/<category>", methods=["GET"])
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

    #pass the mini db to the list page
    return render_template("generic_list.html", titles=titles, pictures=pictures, descriptions=descriptions, \
            flairs=flairs, listids=listids, itemids=itemids)

@app.route("/dog", methods=["GET", "POST"])
def dogsite():
    return render_template("dog.html")

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

    return render_template("randomDog.html", images = list, message = message)
    
@app.route("/randomBreed", methods=["GET", "POST"])
def getRandomBreed():
    number = int(request.form["numDogs"]) #requested number of images
    list = [None] * number#initialize list

    for x in range(0,number):#get an image <number> amount of times
        conn = http.client.HTTPSConnection("dog.ceo")
        dogBreed = request.form['breed']
        conn.request('GET', '/api/breed/' + dogBreed + '/images/random')
        response = conn.getresponse()
        dict = json.loads(response.read())
        list[x]=dict['message']#get image source

    if (number == 1):
        message = "Here is your random dog image"
    else:
        message = "Here are your " + str(number) + " random dog images"

    return render_template("randomDog.html", images = list, message = message, breedQuery = " of the " + dogBreed + " breed!")
#API STUFF END

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
    #app.run()