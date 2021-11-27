from flask import Flask, request, make_response, jsonify
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory
from passlib.hash import sha256_crypt
import json
import sqlite3


app = Flask(__name__, static_folder="frontend/build", static_url_path="")

conn = sqlite3.connect("database.db")

# Creates the User table
conn.execute(
    "CREATE TABLE IF NOT EXISTS User (username TEXT PRIMARY KEY, password TEXT, firstName TEXT, lastName TEXT)"
)


# Creates the Task table
conn.execute(
    "CREATE TABLE IF NOT EXISTS Task (taskID INT PRIMARY KEY AUTOINCREMENT, userID TEXT REFERENCES User, title TEXT, description TEXT, completed BOOLEAN, createdAt DATE, deleted BOOLEAN, priority TEXT)"
)
conn.close()


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/api/login", methods=["POST"])
def login():
    """
    Input:
        - Username (Text)
        - Password (Text)
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
                return "Success", 200
            else:
                return "Invalid Password", 400
    except:
        "Error with login", 500


@app.route("/api/signup", methods=["POST"])
def signup():
    """
    Input:
        - Username (Text)
        - Password (Text)
        - FirstName (Text)
        - LastName (Text)
    Takes the 4 inputs listed above and checks if they're valid.
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


@app.route("/")
def home():
    return "Hello World"


if __name__ == "__main__":
    app.secret_key = b"secretkey"
    app.run(debug=True)

