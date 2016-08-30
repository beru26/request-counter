from flask import Flask, request, jsonify, g
import sqlite3

app = Flask(__name__)


@app.route("/")
@app.route("/request-counter")
def request_counter(method='GET'):
    return 'hello'


DATABASE = 'database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# Query runner
def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    db.commit()
    cur.close()

    return (rv[0] if rv else None) if one else rv


def setup_db():
    query_db("""
    CREATE TABLE IF NOT EXISTS request_counter(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        GET INT,
        POST INT,
        OTHER INT
    )
    """)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    with app.app_context():
        setup_db()
        app.run(debug=True)
