import requests
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
user="postgres",
password="12344321sdaF",
host="localhost",
port="5432")
cursor = conn.cursor()

@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    errors = list()
    if username == "":
        errors.append("Name required")
    if password == "":
        errors.append("Password required")
    if len(errors) > 0:
        return render_template('login.html', errors=errors)

    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
    records = list(cursor.fetchall())
    print(records)
    if len(records) == 0:
        errors.append("No such user in database")
    if len(errors) > 0:
        return render_template('login.html', errors=errors)

    return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])