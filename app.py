from flask import Flask, render_template, url_for, request, flash
import requests
from dotenv import load_dotenv
import os
from os.path import join, dirname
import json
import telebot

app = Flask(__name__)


def get_from_env(key):
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)
    return os.environ.get(key)


app.config["SECRET_KEY"] = get_from_env("SECRET_KEY")


@app.context_processor
def main_menu():
    return dict(
        menu=[{"name": "Index", "url": "/"},
              {"name": "Hey", "url": "/hey"},
              {"name": "Login", "url": "/login"}],
        path=request.url
    )


def send_message(chat_id, text):
    method = "sendMessage"
    token = get_from_env("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    # requests.post(url, json.dumps(data))
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
    return render_template("index.html")


@app.route("/hey")
def hey():
    print(url_for("hey"))
    return render_template("hey.html", title="hey")


@app.route("/login", methods=["POST", "GET"])
def login():
    print(url_for("login"))

    if request.method == "POST":
        print(request.form)
        print(request)
        if request.form["email"] and len(request.form["password"]) > 2:
            flash("Login success", category="success")
        else:
            flash("You must to fill all the fields correctly", category="error")
    return render_template("login.html", title="LogIn")


if __name__ == '__main__':
    app.run()
