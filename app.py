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
    primary_key_column = next((col[1] for col in columns_info if col[5] == 1), 'id')

    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    conn.close()

    results = []
    for row in data:
        results.append(dict(zip(column_names, row)))

    return jsonify({
        "columns": column_names,
        "data": results,
        'primary_key': primary_key_column
    })

@app.route('/get_record/<table_name>/<record_id>', methods=['GET'])
def get_record(table_name, record_id):
    if table_name not in ['member', 'dependents', 'membertype']:
        return jsonify({'success': False, 'message': 'Invalid table name'})

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cur.fetchall()]

    # Determine the primary key column for the table
    pk_column = 'dependent_id' if table_name == 'dependents' else 'PhilHealth_ID'

    sql = f"SELECT * FROM {table_name} WHERE {pk_column} = ?"
    cur.execute(sql, (record_id,))
    record = cur.fetchone()
    conn.close()

    if record:
        record_dict = dict(zip(columns, record))
        return jsonify(record_dict)
    else:
        return jsonify({'success': False, 'message': 'Record not found'})

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
    return render_template("add.html")

@app.route('/add_record', methods=['POST'])
def add_record():
    data = request.json
    table_name = data.pop('table')

    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?' for _ in data.keys()])
    values = tuple(data.values())

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
    conn.commit()

    # Fetch the newly added record to return
    cursor.execute(f"SELECT * FROM {table_name} WHERE rowid = last_insert_rowid()")
    new_record = cursor.fetchone()
    column_names = [description[0] for description in cursor.description]  # Get column names
    new_record_dict = dict(zip(column_names, new_record))
    conn.close()

    return jsonify(new_record_dict)

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

@app.route('/update_record/<table_name>/<pk_value>', methods=['POST'])
def update_record(table_name, pk_value):
    if table_name not in ['member', 'dependents', 'membertype']:
        return jsonify({'success': False, 'message': 'Invalid table name'})

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cur.fetchall()]

    update_data = request.get_json()

    set_clause = ', '.join([f"{col} = ?" for col in update_data.keys()])
    sql = f"UPDATE {table_name} SET {set_clause} WHERE {'dependent_id' if table_name == 'dependents' else 'PhilHealth_ID'} = ?"

    cur.execute(sql, (*update_data.values(), pk_value))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Record updated successfully'})

@app.route('/delete_record/<table_name>/<pk_value>', methods=['DELETE'])
def delete_record(table_name, pk_value):
    if table_name not in ['member', 'dependents', 'membertype']:
        return jsonify({'success': False, 'message': 'Invalid table name'})

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Determine the primary key column for the table
        pk_column = 'dependent_id' if table_name == 'dependents' else 'PhilHealth_ID'

        # Construct the SQL DELETE statement
        sql = f"DELETE FROM {table_name} WHERE {pk_column} = ?"

        # Execute the SQL statement
        cur.execute(sql, (pk_value,))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Record deleted successfully'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

def errorhandler(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run(debug=True)
