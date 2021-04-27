import sqlite3
import hashlib

DB_FILE = "./app/db.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False)
db.text_factory = str
c = db.cursor()
salt = b"We might copy a lot of things from p0 and p1, but not our salt string! Because we are safe and secure and huadsgp9aysrb86t42wbttas"
def saltString(string, salt):
    return hashlib.pbkdf2_hmac('sha256', string.encode('utf-8'), salt, 100000)

#================================================================================
# USER RELATED METHODS
#================================================================================

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

#================================================================================
# AUTHENTICATION RELATED METHODS
#================================================================================

# returns a tuple in the following format: (login_successful, issue, user_id)
# login_successful will be either True (correct info) or False
# issue will be None if login_successful is True. Otherwise will be "user not found" or
# "incorrect username or password"
# user_id will be returned if login_successful. None if not login_successful
def checkLogin(username: str, password: str) -> tuple:
    info = getUserInfo(username)
    if info == None:
        return (False, "User not found", None)
    elif (info[0] == username) and (info[1] == saltString(password, salt)):
        return (True, None, info[2])
    return (False, "Incorrect username or password", None)


# registers a new user by adding their info to the db
# returns the unique user_id so that it can be added to the session in app.py
def registerUser(username: str, password: str):
    command = 'INSERT INTO users VALUES (?, ?, NULL);'
    c.execute(command, [username, saltString(password, salt)])
    db.commit()

#================================================================================
# LIST RELATED METHODS
#================================================================================

#retrieves all the info of an item from one of the lists given its unique entry id.
#returns a tuple in the form of (title, picture, descriptions, flairs, listid, entryid)
#returns none if the id query doesn't exist in the database
def getItemInfo(itemid: int) -> tuple:
    command = 'SELECT title, picture, descriptions, flairs, listid, id FROM lists WHERE id=?;'
    info = ()
    for row in c.execute(command, [itemid]):
        info += (row[0], row[1], row[2], row[3], row[4], row[5])
    if info == ():
        return None
    return info

#retrieves all the info of an item from one of the lists given its picture url.
#returns a tuple in the form of (title, picture, descriptions, flairs, listid, entryid)
#returns none if the id query doesn't exist in the database
def getItemInfoByPicture(picture: str) -> tuple:
    command = 'SELECT title, picture, descriptions, flairs, listid, id FROM lists WHERE picture=?;'
    info = ()
    for row in c.execute(command, [picture]):
        info += (row[0], row[1], row[2], row[3], row[4], row[5])
    if info == ():
        return None
    return info

#insert row into lists table
def addItem(title: str, picture: str, descriptions: str, flairs: str, listid: str):
	command = 'INSERT INTO lists VALUES (?, ?, ?, ?, ?, NULL);'
	c.execute(command, [title, picture, descriptions, flairs, listid])
	db.commit()


#retrieve all the items belonging to a given list
#returns a tuple of all the ids of the items
#returns none if the listid doesn't belong to any items
def getAllItemsOf(listid: str) -> tuple:
    command = 'SELECT id FROM lists WHERE listid=?;'
    entries = ()
    for row in c.execute(command, [listid]):       
        entries += (row[0],)
    if entries == ():
        return None
    return entries

#================================================================================
# FAVORITED RELATED METHODS
#================================================================================

#retrieves all the info of a favorited item from a given user id.
#returns a tuple in the form of (userid, listid, itemid)
#returns none if the id query doesn't exist in the database
def getFavoritedInfo(faveid: int) -> tuple:
    command = 'SELECT userid, listid, itemid, id FROM favorited WHERE id=?;'
    info = ()
    for row in c.execute(command, [faveid]):
        info += (row[0], row[1], row[2], row[3])
    if info == ():
        return None
    return info


#retrieve all the favorited items belonging to a given user by their ids
#returns a tuple of all the ids of the items
#returns none if the userid doesn't belong to any items
def getAllFavoritedItemsOf(userid: int) -> tuple:
    command = 'SELECT id FROM favorited WHERE userid=?;'
    entries = ()
    for row in c.execute(command, [userid]):
        entries += row[0]
    if entries == ():
        return None
    return entries


#inserts a new row into the favorited table
def addFavoritedItem(userid: int, listid: str, itemid: int):
    command = 'INSERT INTO favorited VALUES (?, ?, ?, NULL);'
    c.execute(command, [userid, listid, itemid])
    db.commit()


#deletes a row out of the favorited table
def deleteFavoritedItem(faveid: int):
    command = 'DELETE FROM favorited WHERE id=?;'
    c.execute(command, [faveid])
    db.commit()

#================================================================================
# TEST METHODS
#================================================================================

#prints the entire table
def showUsers():
    print("users:")
    command = 'SELECT * FROM users'
    for row in c.execute(command):
        print(row)

#prints the entire table
def showLists():
    print("lists:")
    command = 'SELECT * FROM lists'
    for row in c.execute(command):
        print(row)

#prints the entire table
def showFavorited():
    print("favorited:")
    command = 'SELECT * FROM favorited'
    for row in c.execute(command):
        print(row)

def close():
    db.close()