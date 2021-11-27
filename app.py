from flask import Flask, request, make_response, jsonify, session
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory
from passlib.hash import sha256_crypt
import json
import sqlite3
import datetime


app = Flask(__name__, static_folder="frontend/build", static_url_path="")

conn = sqlite3.connect("database.db")

# Creates the User table
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS User 
    (
        username TEXT PRIMARY KEY, 
        password TEXT, 
        firstName TEXT, 
        lastName TEXT
    )
    """
)


# Creates the Task table
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS Task 
    (
     taskID INT PRIMARY KEY AUTOINCREMENT, 
     userID TEXT REFERENCES User, 
     title TEXT, description TEXT, 
     completed BOOLEAN, 
     createdAt DATE, 
     priority TEXT
    )
    """
)
conn.close()


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/login", methods=["POST"])
def login():
    """
    Checks if the username and password are valid, and if they are, let the user in.
    """
    try:
        username = request.json["username"]
        password = request.json["password"]
    except:
        return "Did not enter all necessary information", 400

    try:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT password FROM User WHERE username = (?)", (username,))
            rows = cur.fetchall()
        if len(rows) == 0:
            return "Invalid username", 400
        else:
            if sha256_crypt.verify(password, rows[0]):
                session["userID"] = username
                return "Success", 200
            else:
                return "Invalid Password", 400
    except:
        "Error with login", 500


@app.route("/signup", methods=["POST"])
def signup():
    """
    Checks if the username, password, firstname and lastname are valid.
    If they are, we store it in the database.
    """
    try:
        firstname = request.json["firstname"]
        lastname = request.json["lastname"]
        username = request.json["username"]
        password = request.json["password"]
    except:
        return "Did not enter all necessary information", 400

    if (
        check_valid_credentials(username)
        and check_valid_credentials(password)
        and check_valid_name(firstname)
        and check_valid_name(lastname)
    ):
        try:
            new_password = sha256_crypt.hash(password)
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO User values (?,?,?,?)",
                    (username, new_password, firstname, lastname),
                )
                con.commit()
            return "User successfully added", 200
        except sqlite3.IntegrityError as err:
            return "That username already exists. Please choose a new one.", 400
        except:
            "Error with inserting user", 500
    else:
        return "Entered invalid information", 400


@app.route("/logout")
def logout():
    """
    Logs out the user and removes their session id
    """
    session.pop("userID", None)
    return "Logout Successful", 200


@app.route("/api/addTask")
def addTask():
    if "userID" not in session:
        return "Unauthorized Access", 403
    else:
        try:
            username = request.json["username"]
            title = request.json["title"]
            description = request.json["description"]
            priority = request.json["priority"]
            cur_day = datetime.datetime.now()

            # Checks if the user is in the db.

        except:
            return "Did not enter all necessary information", 400


@app.route("/")
def home():
    return "Hello World"


def check_valid_name(name):
    """
    Checks if the name is all alphabetical characters
    """
    return name.isalpha()


def check_valid_credentials(credential):
    """
    Checks if the credential (username and password) is all alphanumeric characters and is at least 8 characters long
    """
    return len(credential) >= 8 and credential.isalnum()


if __name__ == "__main__":
    app.secret_key = b"secretkey"
    app.run(debug=True)

