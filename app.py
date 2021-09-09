import os
from os.path import join, dirname

import sqlite3

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, url_for, request, flash, session
from flask import redirect, abort, g

from FDataBase import FDataBase


app = Flask(__name__)


def get_from_env(key):
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)
    return os.environ.get(key)


app.config["SECRET_KEY"] = get_from_env("SECRET_KEY")
app.config["DATABASE"] = get_from_env("DATABASE")
app.config["DEBUG"] = get_from_env("DEBUG")

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


# def create_db():
#     db = connect_db()
#     with app.open_resource('sq_db.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()
#     db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


def dbase():
    db = get_db()
    dbase = FDataBase(db)
    return dbase


@app.context_processor
def main_menu():
    return dict(
        dbase=dbase(),
        menu=dbase().getmenu(),
        path=request.url
    )


def send_message(chat_id, text):
    method = "sendMessage"
    token = get_from_env("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    print(requests.post(url, json=data).text)


@app.route("/telegram", methods=["POST"])
def process():
    print(request.json)
    chat_id = request.json["message"]["chat"]["id"]
    text = "а я знаю, шо ты додик )"
    send_message(chat_id, text)
    return {"ok": True}


@app.route("/check", methods=["POST", "GET"])
def checking_post():
    print(request.json)
    return {"ok": True}


@app.route("/")
def index():  # put application's code here
    print(url_for("index"))
    print('Secret key is: ', app.config['SECRET_KEY'])
    print(main_menu()['menu'])
    article_list = dbase().showPostList()
    return render_template("index.html", article_list=article_list)


@app.route("/hey")
def hey():
    print(url_for("hey"))
    return render_template("hey.html", title="hey")


@app.route("/login", methods=["POST", "GET"])
def login():
    print(url_for("login"))
    print(request)
    print(request.form)

    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))

    if request.method == "POST" and request.form["email"] and len(request.form["password"]) > 2:

        if request.form['email'] == '1@w.t' and request.form['password'] == '123':
            session['userLogged'] = request.form['email']
            return redirect(url_for('profile', username=session['userLogged']))
        flash("Login success", category="success")

    elif request.method == 'POST':
        flash("You must to fill all the fields correctly", category="error")
    return render_template("login.html", title="LogIn")


@app.route("/profile/<username>")
def profile(username):
    # return f"User {username} profile"
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return render_template("profile.html", title="Profile", username=session['userLogged'])


@app.route("/logout")
def logout():
    return f"You are logged out {session.pop('userLogged', None)} profile"


@app.route("/add_post", methods=["POST", "GET"])
def addPost():
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase().addPost(request.form['name'], request.form['post'])
            if not res:
                flash('Add article error', category='error')
            else:
                flash('Add article successful', category='success')
        else:
            flash('Add article error', category='error')

    return render_template('add_post.html', title='Add article')


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", title="Page not found", error=error), 404


@app.errorhandler(401)
def error_page(error):
    return render_template('error.html', title="Error 401", error=error), 401


if __name__ == '__main__':
    app.run()
