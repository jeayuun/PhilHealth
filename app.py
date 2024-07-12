import os
import sqlite3
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
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

def get_db_connection():
    conn = sqlite3.connect('philhealth.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == 'admin' and password == 'password':
            session["user_id"] = 1
            flash("Logged in successfully!", "success")
            return redirect("/")
        else:
            flash("Invalid username or password", "error")
            return redirect("/login")

    return render_template("index.html")

@app.route("/")
@login_required
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dependents")
    dependents_data = cursor.fetchall()
    cursor.execute("SELECT * FROM member")
    member_data = cursor.fetchall()
    cursor.execute("SELECT * FROM membertype")
    membertype_data = cursor.fetchall()
    conn.close()

    return render_template("dashboard.html", dependents=dependents_data, members=member_data, membertypes=membertype_data)

@app.route("/get_table_data/<table_name>")
@login_required
def get_table_data(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns_info = cursor.fetchall()
    column_names = [info[1] for info in columns_info]

    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    conn.close()

    results = []
    for row in data:
        results.append(dict(zip(column_names, row)))

    return jsonify({
        "columns": column_names,
        "data": results
    })

@app.route("/get_table_schema/<table_name>")
@login_required
def get_table_schema(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns_info = cursor.fetchall()
    conn.close()

    columns = [{'name': info[1], 'type': info[2]} for info in columns_info]
    return jsonify(columns)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        table_name = request.form.get("table_name")
        columns = request.form.getlist("columns[]")
        values = request.form.getlist("values[]")
        placeholders = ", ".join(["?"] * len(values))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})", values)
        conn.commit()
        conn.close()

        flash("Record added successfully!", "success")
        return redirect("/")

    return render_template("add.html")

@app.route("/add_record", methods=["POST"])
@login_required
def add_record():
    data = request.form
    table_name = data.get('table')
    # Extract column names and values from the form
    columns = data.keys()
    values = [data.get(col) for col in columns]

    conn = get_db_connection()
    cursor = conn.cursor()

    # Construct SQL query
    columns_str = ", ".join(columns)
    placeholders = ", ".join(["?"] * len(values))  # SQLite uses '?' for placeholders
    query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

    cursor.execute(query, values)
    conn.commit()
    conn.close()

    flash(f"Record added to {table_name} successfully!", "success")
    return redirect("/add")


@app.route("/mysql")
@login_required
def mysql():
    return render_template("mysql.html")

@app.route("/about")
@login_required
def about():
    return render_template("about.html")

@app.route('/update')
@login_required
def edit_record():
    return render_template('update.html')

def errorhandler(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run(debug=True)
