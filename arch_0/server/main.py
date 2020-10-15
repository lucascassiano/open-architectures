from flask import Flask, render_template, url_for, request, session, redirect, Response
from pymongo import MongoClient
from urllib.parse import urljoin
import bcrypt
import requests
import os

DOCKER = os.getenv('DOCKER')

app = Flask(__name__)

MONGO_USER = "root"
MONGO_PASSWORD = "password"
MONGO_URL = "localhost:27017"

if DOCKER:
    MONGO_URL = "mongo:27017"

mongo = MongoClient(host=MONGO_URL,
                    username='root',
                    password='password')

APP_SECRET = "mainSecret"


@app.route('/')
def index():
    if not session or not session['username']:
        return render_template('index.html')

    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return render_template('index.html')


def verify_access(session):
    if 'secret' in session and session['secret'] == APP_SECRET:
        return True
    return False


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})
    print("login_user", login_user)

    if login_user:
        if bcrypt.checkpw(request.form['pass'].encode('utf-8'), login_user['password']):
            session['username'] = request.form['username']
            session['secret'] = APP_SECRET
            return redirect(url_for('index'))

    return 'Invalid username/password combination'


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(
                request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert(
                {'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('register.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session['username'] = ''
    session['secret'] = ''
    return 'logout'


@app.route('/app', methods=['POST', 'GET'])
def dataApp():
    if not verify_access(session):
        return redirect(url_for('index'))

    return 'data app'


SITE_NAME = "http://localhost:8501/"
if DOCKER:
    SITE_NAME = "http://streamlit-app:8501/"


@app.route('/streamlit', methods=['GET'])
def streamlit():
    print('streamlit')

    if not verify_access(session):
        return redirect(url_for('index'))

    if request.method == 'GET':
        resp = requests.get(SITE_NAME)
        excluded_headers = ['content-encoding',
                            'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items(
        ) if name.lower() not in excluded_headers]

        content = resp.content.decode('utf-8')

        content = content.replace('/static/', '/streamlit/static/')
        content = content.replace('/healthz/', '/streamlit/healthz/')

        response = Response(content.encode('utf-8'), resp.status_code, headers)
        return response


@app.route('/streamlit/<path:path>', methods=['GET'])
def proxy(path):
    print("inside proxy")
    print(path)
    URL = f'{SITE_NAME}{path}'
    print(URL)
    if request.method == 'GET':
        resp = requests.get(URL)
        excluded_headers = ['content-encoding',
                            'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items(
        ) if name.lower() not in excluded_headers]

        response = Response(resp.content, resp.status_code, headers)
        return response


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True, host="0.0.0.0")
