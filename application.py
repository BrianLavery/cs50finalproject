from cs50 import SQL
from flask import Flask, render_template
from flask_session import Session
from tempfile import mkdtemp

from helper import numbers

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
## db = SQL("sqlite:///database.db")

# Make sure API key is set
### TO DO ###


@app.route("/")
##@login_required
def indexs():
    data = numbers(25)
    return render_template("index.html", data=data)