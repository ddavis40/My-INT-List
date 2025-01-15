import os
import requests
from dotenv import load_dotenv
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure db with cs50 library
db = SQL("sqlite:///data.db")

# after request
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log in a user """

    # Forget any user_id
    session.clear()

    # render html
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    #query data base for our users listed players
    ints = db.execute("SELECT summ_name, summ_tag, notes, puuid FROM int_list WHERE user_id = ?", session["user_id"])
    #if method is GET show index with a list of current listed players
    if request.method == "GET":
        return render_template("index.html", ints=ints)
    #else update notes for list member
    else:
        notes = request.form.get("notes")
        puuid = request.form.get("puuid")
        db.execute("UPDATE int_list SET notes = ? WHERE user_id = ? AND puuid = ?", notes, session["user_id"], puuid)
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # get info from form
        username = request.form.get("username")
        password = request.form.get("password")
        password1 = request.form.get("confirmation")
        # get info on usernames from database
        currentUsernames = db.execute("SELECT username FROM users")
        # check if input is valid -
        # check if any field is left blank
        if not username:
            return apology("must provide username")
        if not password:
            return apology("must provide password")
        # check if password and confirmation dont match return an apology
        if password != password1:
            return apology("passwords must match")
        # check if the username is already taken
        for user in currentUsernames:
            if username == user["username"]:
                return apology("Username taken")
        # hash plaintext password
        hash = generate_password_hash(password)
        # add input to the database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        # Log user in
        # Remember which user has logged in
        rows = db.execute("SELECT id FROM users WHERE username = ?", username)
        if rows:
            session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    #render add.html
    if request.method == "GET":
        return render_template("add.html")
    #query api and add to db
    else:
        # referenced chat gpt for better understanding of using api keys safely and accurately, .env files, and .json files
        load_dotenv()
        # my api key I used is only valid for 24hrs and is only a dev key and not a permanent one, it is still associated with my account with the api supplier but will expire after 24hrs and need to be replaced.
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            return ValueError("API_KEY not found in environment variables. Ensure it's set in your .env file.")
        gameName = request.form.get("name")
        tagLine = request.form.get("tag")

        URL = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": f"{API_KEY}"
        }
        t = "add"
        response = requests.get(URL, headers=headers)
        if not response:
            return apology("No response / invalid name")
        data = response.json()
        inlist = db.execute("SELECT * FROM int_list WHERE user_id = ? AND puuid = ?", session["user_id"], data["puuid"])
        #if not on list add them
        if not inlist:
            db.execute("INSERT INTO int_list (user_id, summ_name, summ_tag, puuid) VALUES (?, ?, ?, ?)", session["user_id"], data["gameName"], data["tagLine"], data["puuid"])
            db.execute("INSERT INTO history (user_id, summ_name, summ_tag, bool) VALUES (?, ?, ?, ?)", session["user_id"], data["gameName"], data["tagLine"], t)
            return redirect("/")
        else:
            return apology("already in list")


@app.route("/history")
@login_required
def history():
    #query db
    ints = db.execute("SELECT summ_name, summ_tag, bool, timestamp FROM history WHERE user_id = ?", session["user_id"])
    #render history with list data
    return render_template("history.html", ints=ints)

@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    #display current list with options to remove each member
    ints = db.execute("SELECT summ_name, summ_tag, puuid FROM int_list WHERE user_id = ?", session["user_id"])
    if request.method == "GET":
        return render_template("remove.html", ints=ints)
    #remove selected member from db
    else:
        puuid = request.form.get("puuid")
        f = "drop"
        data = db.execute("SELECT summ_name, summ_tag FROM int_list WHERE user_id = ? AND puuid = ?", session["user_id"], puuid)
        db.execute("INSERT INTO history (user_id, summ_name, summ_tag, bool) VALUES (?, ?, ?, ?)", session["user_id"], data[0]["summ_name"], data[0]["summ_tag"], f)

        db.execute("DELETE FROM int_list WHERE user_id = ? AND puuid = ?", session["user_id"], puuid)
        return redirect("/remove")

@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Change password"""
    if request.method == "GET":
        # display change password form
        return render_template("change.html")
    else:
        # get info from form
        password = request.form.get("password")
        password1 = request.form.get("confirmation")
        # check if input is valid -
        # check if any field is left blank
        if not password:
            return apology("must provide password")
        if not password1:
            return apology("must provide second password")
        # check if password and confirmation dont match return an apology
        if password != password1:
            return apology("passwords must match")
        # hash plaintext password
        hash = generate_password_hash(password)
        # update input to the database
        db.execute("UPDATE users SET hash = ? WHERE id =?", hash, session["user_id"])
        # Redirect user to home page
        return redirect("/")

@app.route("/check", methods=["GET", "POST"])
@login_required
def check():
    #render check html
    if request.method == "GET":
        return render_template("check.html")
    #query api for current game participants based on your inputed ign
    else:
        load_dotenv()
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("API_KEY not found in environment variables. Ensure it's set in your .env file.")

        gameName = request.form.get("name")
        tagLine = request.form.get("tag")
        URL = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": f"{API_KEY}"
        }
        response = requests.get(URL, headers=headers)
        data = response.json()
        id = data.get("puuid")
        #error check if name DNE
        if not id:
            return apology("Name does not exist / is misspelled")

        URL1 = f"https://na1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{id}"
        gamedata = requests.get(URL1, headers=headers)
        data = gamedata.json()
        #error check if player is not in game
        #used chat gpt to better understand how to avoid value errors using .get()
        participants = data.get("participants")
        if not participants:
            return apology("No data recieved / player is not in game")

        intlist = db.execute("SELECT puuid, summ_name FROM int_list WHERE user_id = ?", session["user_id"])
        #check for member in list, display them if found
        summ_names = []
        for int_entry in intlist:
            for participant in participants:
                if int_entry["puuid"] == participant["puuid"]:
                    summ_names.append(int_entry["summ_name"])

        if not summ_names:
            #display no int
            return render_template("check_no.html")
        else:
            #display int
            return render_template("check_int.html", summ_names=summ_names)


