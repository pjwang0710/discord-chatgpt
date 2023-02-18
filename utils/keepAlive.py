from flask import Flask
from threading import Thread
from os import environ

app = Flask('')


@app.route('/')
def home():
    return "Hello. I am alive!"


def run():
    app.run(host='0.0.0.0', port=environ.get('PORT'))


def keep_alive():
    t = Thread(target=run)
    t.start()
