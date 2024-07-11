import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///philhealth.db")

@app.route("/")
@login_required
def home():
    return render_template("dashboard.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash("Missing username", "error")
            return redirect("/register")
        elif not password:
            flash("Missing password", "error")
            return redirect("/register")
        elif not confirmation:
            flash("Confirm your password", "error")
            return redirect("/register")
        elif confirmation != password:
            flash("Passwords do not match", "error")
            return redirect("/register")

        hashed_password = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashed_password)
        except:
            flash("Username already exists", "error")
            return redirect("/register")

        flash("Registered successfully! Please log in.", "success")
        return redirect("/login")

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            flash("Must provide username", "error")
            return redirect("/login")
        elif not password:
            flash("Must provide password", "error")
            return redirect("/login")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Invalid username or password", "error")
            return redirect("/login")

        session["user_id"] = rows[0]["id"]
        flash("Logged in successfully!", "success")
        return redirect("/")

    return render_template("index.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect("/login")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run(debug=True)
