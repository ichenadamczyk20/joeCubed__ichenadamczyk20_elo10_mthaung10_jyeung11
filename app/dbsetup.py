import sqlite3

DB_FILE = "./app/db.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()

def createTables():

    command = "DROP TABLE IF EXISTS users;"

    command += "DROP TABLE IF EXISTS favorited;"

    command += "DROP TABLE IF EXISTS listn;"
    
    command += "CREATE TABLE users(username TEXT, password TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);"

    command += "CREATE TABLE favorited(userid INTEGER, listid INTEGER, id INTEGER PRIMARY KEY AUTOINCREMENT);"

    command += "CREATE TABLE listn(title TEXT, picture TEXT, descriptions TEXT, flairs TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);"

    c.executescript(command)
    db.commit()

if __name__ == "__main__":
    createTables()