import sqlite3

DB_FILE = "./app/db.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()

# returns the username and password for a given user_id in a tuple (username,
# password)
# consider case when 2 users have the same username and password. Technically
# would work because they have different ids. Should we make username unique as well?
def getUserId(username: str) -> int:
    command = 'SELECT id FROM users WHERE username=?;'
    info = 0
    for row in c.execute(command, [username]):
        info = row[0]

    return info


# returns a username for any given user_id
def getUsername(user_id: int) -> str:
    command = 'SELECT username FROM users WHERE id=?;'
    user = ""
    for row in c.execute(command, [user_id]):
        user = row[0]
    return user


# returns (username, password, user_id) for a given username. Returns None
# if argument username is not present in the database
def getUserInfo(username: str):
    command = 'SELECT username, password, id FROM users WHERE username=?;'
    info = ()
    for row in c.execute(command, [username]):
        info += (row[0], row[1], row[2])

    if info == ():
        return None
    return info

# returns a tuple in the following format: (login_successful, issue, user_id)
# login_successful will be either True (correct info) or False
# issue will be None if login_successful is True. Otherwise will be "user not found" or
# "incorrect username or password"
# user_id will be returned if login_successful. None if not login_successful
def checkLogin(username: str, password: str) -> tuple:
    info = getUserInfo(username)
    if info == None:
        return (False, "User not found", None)
    elif (info[0] == username) and (info[1] == password):
        return (True, None, info[2])
    return (False, "Incorrect username or password", None)


# registers a new user by adding their info to the db
# returns the unique user_id so that it can be added to the session in app.py
def registerUser(username: str, password: str):
    command = 'INSERT INTO users VALUES (?, ?, NULL);'
    c.execute(command, [username, password])
    db.commit()

def close():
    db.close()