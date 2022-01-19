from flask import Flask, request, make_response, jsonify
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory
from passlib.hash import sha256_crypt
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
     taskID INTEGER PRIMARY KEY AUTOINCREMENT, 
     userID TEXT REFERENCES User, 
     title TEXT, 
     description TEXT,
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
    # Checks if the user gave all necessary information
    if not ("username" in request.json and "password" in request.json):
        return "Did not enter all necessary information", 400

    username = request.json["username"]
    password = request.json["password"]

    try:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            rows = cur.execute(
                "SELECT password FROM User WHERE username = (?)", (username,)
            ).fetchall()
        if len(rows) == 0:
            return "Username not found", 404
        else:
            if sha256_crypt.verify(password, rows[0][0]):

                return (
                    "Successfully logged in",
                    200,
                )  # Maybe return user's first and/or last name
            else:
                return "Password not found", 404
    except:
        return "Error with login", 500


@app.route("/signup", methods=["POST"])
def signup():

    # Checks if the user gave all necessary information
    if not (
        "firstname" in request.json
        and "lastname" in request.json
        and "username" in request.json
        and "password" in request.json
    ):
        return "Did not enter all necessary information", 400

    firstname = request.json["firstname"]
    lastname = request.json["lastname"]
    username = request.json["username"]
    password = request.json["password"]

    # Checks if the info is valid
    if not (check_valid_credentials(username)):
        return (
            "The username is not of the right format. Usernames must be at least 8 characters long and only contain alphanumeric characters",
            400,
        )

    if not (check_valid_credentials(password)):
        return (
            "The pasword is not of the right format. Passwords must be at least 8 characters long and only contain alphanumeric characters",
            400,
        )

    if not (check_valid_name(firstname)):
        return (
            "The firstname is not of the right format. Firstnames must only contain alphabetical characters",
            400,
        )

    if not (check_valid_name(lastname)):
        return (
            "The lastname is not of the right format. Lastnames must only contain alphabetical characters",
            400,
        )

    # Stores the info in the db
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
        return "Error with inserting user", 500


@app.route("/logout", methods=["GET"])
def logout():
    return "Logout Successful", 200


@app.route("/api/addTask", methods=["POST"])
def addTask():

    # Checks if the user gave all necessary information
    if not (
        "username" in request.json
        and "title" in request.json
        and "description" in request.json
        and "priority" in request.json
    ):
        return "Did not enter all necessary information", 400

    title = request.json["title"]
    description = request.json["description"]
    username = request.json["username"]
    priority = request.json["priority"]
    cur_day = datetime.datetime.now()

    # Check if the priority is one of H (High), M (Medium), L (Low)
    if priority != "H" or priority != "M" or priority != "L":
        return "The priority is invalid", 404

    try:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(
                """
                INSERT INTO Task 
                (userID, title, description, createdAt, priority) 
                values 
                (?,?,?,?,?,?)
                """,
                (username, title, description, cur_day, priority),
            )
            con.commit()
        return "Task successfully added", 200
    except sqlite3.IntegrityError as err:
        return "That username doesn't exists.", 404
    except:
        return "Error with adding task", 500


@app.route("/api/editTask", methods=["PATCH"])
def editTask():

    # Checks if the user gave all necessary information
    if not (
        "taskID" in request.json
        and "title" in request.json
        and "description" in request.json
        and "priority" in request.json
    ):
        return "Did not enter all necessary information", 400

    title = request.json["title"]
    description = request.json["description"]
    taskID = request.json["taskID"]
    priority = request.json["priority"]

    try:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(
                """
                UPDATE Task 
                SET 
                title = (?),
                description = (?),
                priority = (?)
                WHERE taskID = (?)
                """,
                (title, description, priority, taskID),
            )
            con.commit()
        return "Task successfully updated", 200
    except:
        return "Error with updating task", 500


@app.route("/api/deleteTask", methods=["DELETE"])
def deleteTask():
    """
    Deletes a task from the database
    """

    # Checks if the user gave all necessary information
    taskID = request.args.get("taskID")
    if not taskID:
        return "Did not enter a taskID", 400

    try:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(
                """
                DELETE FROM Task WHERE taskID = (?)
                """,
                (taskID,),
            )
        return "Task successfully deleted", 200
    except:
        return "Error with deleting task", 500


@app.route("/api/getTask", methods=["GET"])
def getTask():

    # Checks if the user gave all necessary information
    pageNumber = request.args.get("pageNumber")
    userID = request.args.get("user")
    filterTag = (
        request.args.get("filter").upper()
        if request.args.get("filter").upper() != None
        else "%"
    )

    if not pageNumber:
        return "Did not give a page number", 400

    if not userID:
        return "Did not give a userID", 400

    pageNumber = int(pageNumber)

    if pageNumber < 1:
        return "Invalid page number", 400

    try:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            rows = cur.execute(
                """
                SELECT title, description, priority, taskID 
                FROM Task 
                WHERE userID = (?) and priority like filterTag
                ORDER BY createdAt
                LIMIT (?)
                OFFSET (?)
                """,
                (userID, filterTag, pageNumber * 6, (pageNumber - 1) * 6),
            ).fetchall()
        return jsonify(rows), 200
    except:
        return "Error with getting task", 500


@app.route("/")
def home():
    return "Hello World"


def check_valid_name(name):
    return name.isalpha()


def check_valid_credentials(credential):
    return len(credential) >= 8 and credential.isalnum() and not credential.isnumeric()


if __name__ == "__main__":
    app.secret_key = b"secretkey"
    app.run(debug=True)

