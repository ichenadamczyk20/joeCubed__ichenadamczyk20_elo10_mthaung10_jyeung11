import os
from flask import Flask, redirect, render_template, request, session, url_for
import dbmanager as db

app = Flask(__name__)
app.secret_key = os.urandom(10)
salt = b"We might copy a lot of things from p0 and p1, but not our salt string! Because we are safe and secure and huadsgp9aysrb86t42wbttas"

@app.route("/", methods=["GET", "POST"])
def root():
    return "<hi>Hello!</hi>"

@app.route("/login", methods=["GET", "POST"])
def login():
    if "error_msg" in session:
        error_msg = session.pop("error_msg")
        return render_template("login.html", error_msg = error_msg)
    if "success_msg" in session:
        success_msg = session.pop("success_msg")
        return render_template("login.html", success_msg = success_msg)
    return render_template("login.html")

@app.route("/login-submit", methods=["POST"])
def authenticate():
    userInput = request.form['username']
    passInput = request.form['password']

    loginInfo = db.checkLogin(userInput, passInput)

    if loginInfo[0]:
        session["userid"] = loginInfo[2] 
        session["username"] = userInput
        session["password"] = passInput
        return render_template("home.html")

    session["error_msg"] = loginInfo[1]
    return redirect("/login")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if "error_msg" in session:
        error_msg = session.pop("error_msg")
        return render_template("register.html", error_msg = error_msg)
    if "success_msg" in session:
        success_msg = session.pop("success_msg")
        return render_template("register.html", success_msg = success_msg)
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

@app.route("/logout", methods=["GET", "POST"])
def logout():
    if "username" in session:
        username = session.pop("username")
        session.pop("password")
        session.pop("userId")
        session["success_msg"] = "Logged you out! See you again,", username
    else:
        session["error_msg"] = "You weren't logged in"
    
    return redirect("/login")
    
    

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
    #app.run()