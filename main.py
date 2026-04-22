import os
import secrets
import sqlite3

import flask
from flask import Flask, g


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ["FLASK_SECRET"]

    DATABASE = "main.db"

    def get_db():
        db = getattr(g, "_database", None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
            db.row_factory = sqlite3.Row
        return db

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, "_database", None)
        if db is not None:
            db.close()

    @app.route("/")
    def index():
        return flask.render_template("index.html")

    return app
