import sqlite3
from datetime import datetime

from flask import Flask, g

app = Flask(__name__)

DATABASE = "/sqlitedata/database.sqlite3"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/")
def hello_world():
    get_db().execute("insert into hits values (1)")
    get_db().commit()

    cur = get_db().execute("select sum(x) as sum from hits")
    result = cur.fetchall()
    cur.close()
    return f"hello again from disco! total hits: {result[0][0]}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
