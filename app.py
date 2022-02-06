from flask import Flask, request, make_response, jsonify
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory
from passlib.hash import sha256_crypt
import sqlite3
import datetime
import json


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
     userID TEXT, 
     title TEXT, 
     description TEXT,
     createdAt DATE, 
     priority TEXT,
     FOREIGN KEY(userID) REFERENCES User (username) ON DELETE CASCADE
    )
    """
)
conn.close()


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    return response

@app.route("/login", methods=["POST", "OPTIONS"])
def login():

    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    
    # Checks if the user gave all necessary information
    if not ("username" in request.json and "password" in request.json):
        return _corsify_actual_response(jsonify("Did not enter all necessary information")), 400

    username = request.json["username"]
    password = request.json["password"]

    try:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            rows = cur.execute(
                "SELECT password FROM User WHERE username = (?)", (username,)
            ).fetchall()
        if len(rows) == 0:
            return _corsify_actual_response(jsonify("Username not found")), 404
        else:
            if sha256_crypt.verify(password, rows[0][0]):

                return (
                    _corsify_actual_response(jsonify("Successfully logged in")),
                    200,
                )  # Maybe return user's first and/or last name
            else:
                return _corsify_actual_response(jsonify("Password not found")), 404
    except:
        return _corsify_actual_response(jsonify("Error with login")), 500


@app.route("/signup", methods=["POST", "OPTIONS"])
def signup():

    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
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
            _corsify_actual_response(jsonify("The username is not of the right format. Usernames must be at least 8 characters long and only contain alphanumeric characters")),
            400,
        )

    if not (check_valid_credentials(password)):
        return (
            _corsify_actual_response(jsonify("The pasword is not of the right format. Passwords must be at least 8 characters long and only contain alphanumeric characters")),
            400,
        )

    if not (check_valid_name(firstname)):
        return (
            _corsify_actual_response(jsonify("The firstname is not of the right format. Firstnames must only contain alphabetical characters")),
            400,
        )

    if not (check_valid_name(lastname)):
        return (
            _corsify_actual_response(jsonify("The lastname is not of the right format. Lastnames must only contain alphabetical characters")),
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
        return _corsify_actual_response(jsonify("User successfully added")), 200
    except sqlite3.IntegrityError as err:
        return _corsify_actual_response(jsonify("That username already exists. Please choose a new one.")), 400
    except:
        return _corsify_actual_response(jsonify("Error with inserting user")), 500


@app.route("/logout", methods=["GET"])
def logout():
    return "Logout Successful", 200


@app.route("/api/addTask", methods=["POST", "OPTIONS"])
def addTask():

    if request.method == "OPTIONS":
        return _build_cors_preflight_response()

    # Checks if the user gave all necessary information
    if not (
        "username" in request.json
        and "title" in request.json
        and "description" in request.json
        and "priority" in request.json
    ):
        return _corsify_actual_response(jsonify("Did not enter all necessary information")), 400

    title = request.json["title"]
    description = request.json["description"]
    username = request.json["username"]
    priority = request.json["priority"]
    cur_day = datetime.datetime.now()

    # Check if the priority is one of H (High), M (Medium), L (Low)
    if priority != "H" and priority != "M" and priority != "L":
        return _corsify_actual_response(jsonify("The priority is invalid")), 404

    try:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            rows = cur.execute(
                "SELECT username FROM User WHERE username = (?)", (username,)
            ).fetchall()
            if len(rows) == 0:
                return "That username doesn't exists.", 404
            else:
                cur.execute(
                    """
                    INSERT INTO Task 
                    (userID, title, description, createdAt, priority) 
                    values 
                    (?,?,?,?,?)
                    """,
                    (username, title, description, cur_day, priority),
                )
                con.commit()
            return _corsify_actual_response(jsonify("Task successfully added")), 200
    except:
        return _corsify_actual_response(jsonify("Error with adding task")), 500


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
            rows = cur.execute(
                "SELECT taskID FROM Task WHERE taskID = (?)", (taskID,)
            ).fetchall()
            if len(rows) == 0:
                return "That taskID doesn't exists.", 404
            else:
                cur.execute(
                    """
                    DELETE FROM Task WHERE taskID = (?)
                    """,
                    (taskID,),
                )
            return "Task successfully deleted", 200
    except:
        return "Error with deleting task", 500


def row_to_dict(cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
    data = {}
    for idx, col in enumerate(cursor.description):
        data[col[0]] = row[idx]
    return data


@app.route("/api/getTask", methods=["GET", "OPTIONS"])
def getTask():

    if request.method == "OPTIONS":
        return _build_cors_preflight_response()

    # Checks if the user gave all necessary information
    pageNumber = request.args.get("pageNumber")
    userID = request.args.get("username")
    filterTag = (
        request.args.get("filter").upper()
        if request.args.get("filter") != None
        else "%"
    )

    if not pageNumber:
        return _corsify_actual_response(jsonify("Did not give a page number")), 400

    if not userID:
        return _corsify_actual_response(jsonify("Did not give a userID")), 400

    if not pageNumber.isdigit() or int(pageNumber) < 1:
        return _corsify_actual_response(jsonify("Invalid page number")), 400

    pageNumber = int(pageNumber)
    try:
        with sqlite3.connect("database.db") as con:
            con.row_factory = row_to_dict
            rows = con.execute(
                """
                SELECT title, description, priority, taskID 
                FROM Task 
                WHERE userID = (?) and priority like (?)
                ORDER BY createdAt
                LIMIT (?)
                OFFSET (?)
                """,
                (userID, filterTag, pageNumber * 6, (pageNumber - 1) * 6),
            ).fetchall()
        return _corsify_actual_response(jsonify(rows)), 200
    except:
        return _corsify_actual_response(jsonify("Error with getting task")), 500


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

