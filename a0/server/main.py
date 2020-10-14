from flask import Flask, render_template, url_for, request, session, redirect, Response
# from flask_reverse_proxy_fix.middleware import ReverseProxyPrefixFix

from pymongo import MongoClient
from urllib.parse import urljoin
import bcrypt
import requests

app = Flask(__name__)  # ,  static_url_path="/STATIC_FOLDER")
# app.config['REVERSE_PROXY_PATH'] = '/streamlit'
# ReverseProxyPrefixFix(app)

MONGO_USER = "root"
MONGO_PASSWORD = "password"
mongo = MongoClient('localhost:27017',
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


@app.route('/streamlit', methods=['GET'])
def streamlit():
    print('streamlit')

    if not verify_access(session):
        return redirect(url_for('index'))

    if request.method == 'GET':
        resp = requests.get(f'http://localhost:8501')
        excluded_headers = ['content-encoding',
                            'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items(
        ) if name.lower() not in excluded_headers]
        # resp.content = resp.content.replace('/static/','/cassiano/')
        print("------------", type(resp.content))
        content = resp.content.decode('utf-8')

        content = content.replace('/static/', '/streamlit/static/')
        content = content.replace('/healthz/', '/streamlit/healthz/')
        content = content.replace(
            'ws://localhost:5000/streamlit/stream', 'ws://localhost:8501/streamlit/stream')

        # ws://localhost:5000/streamlit/stream
        print(content)

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

# @app.route('/<path:path>', methods=['GET', 'POST', 'DELETE'])
# def proxy2(path):
#     SITE_NAME = 'http://localhost:8501/streamlit'
#     if request.method == 'GET':
#         URL = urljoin(SITE_NAME, path)
#         print(URL)
#         resp = requests.get(URL)

#         excluded_headers = ['content-encoding',
#                             'content-length', 'transfer-encoding', 'connection']
#         headers = [(name, value) for (name, value) in resp.raw.headers.items(
#         ) if name.lower() not in excluded_headers]
#         response = Response(resp.content, resp.status_code, headers)
#         return response
#     elif request.method == 'POST':
#         resp = requests.post(f'{SITE_NAME}{path}', json=request.get_json())
#         excluded_headers = ['content-encoding',
#                             'content-length', 'transfer-encoding', 'connection']
#         headers = [(name, value) for (name, value) in resp.raw.headers.items(
#         ) if name.lower() not in excluded_headers]
#         response = Response(resp.content, resp.status_code, headers)
#         return response
#     elif request.method == 'DELETE':
#         resp = requests.delete(f'{SITE_NAME}{path}').content
#         response = Response(resp.content, resp.status_code, headers)
#         return response


# @app.route('/static', methods=['GET', 'POST'])
# def staticFiles():
#     print('static')
#     if request.method == 'GET':
#         resp = requests.get(f'http://localhost:8501/streamlit/static')

#         excluded_headers = ['content-encoding',
#                             'content-length', 'transfer-encoding', 'connection']
#         headers = [(name, value) for (name, value) in resp.raw.headers.items(
#         ) if name.lower() not in excluded_headers]
#         resp.content = resp.content.replace('/static', '/streamlit/static')
#         response = Response(resp.content, resp.status_code, headers)
#     return response


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True, host="0.0.0.0")
