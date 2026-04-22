import datetime
import os
import sqlite3

import flask
from flask import Flask, g, request

from potyk_stats_back.activity import ActivityRepo, ActivityEntry
from potyk_stats_back.dt_utils import parse_dt


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

    @app.route("/", methods=["GET", "POST"])
    def index():
        cursor = get_db().cursor()
        repo = ActivityRepo(cursor)

        if request.method == "POST":
            form = request.form
            activity: str = form["activity"]
            created_str = form.get("created")
            comment: str | None = form.get("comment")
            secret: str = form["secret"]

            if secret != os.environ["FLASK_SECRET"]:
                raise flask.abort(403)

            created = parse_dt(created_str) if created_str else datetime.datetime.now()

            entry = ActivityEntry(activity, created, comment)
            repo.insert_activity(entry)

        options = [
            [{"value": activity, "text": activity}]
            for activity in repo.list_activity_values()
        ]
        activities = repo.list_activities()

        return flask.render_template(
            "index.html",
            options=options,
            activities=activities,
        )

    return app
