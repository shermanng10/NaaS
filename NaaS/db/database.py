import psycopg2
import flask

from .. import app


def request_has_connection():
    return hasattr(flask.g, 'dbconn')


def get_connection():
    try:
        if not request_has_connection():
            flask.g.dbconn = psycopg2.connect(app.config.get('DB_STRING'))
        return flask.g.dbconn
    except Exception as e:
        app.logger.error(e)


def init_db():
    conn = get_connection()
    with app.open_resource('db/schema.sql', mode='r') as f:
        conn.cursor().execute(f.read())
    conn.commit()


@app.teardown_appcontext
def close_db_connection(error):
    if request_has_connection():
        conn = get_connection()
        conn.close()


@app.cli.command()
def initdb():
    init_db()
    print('Initialized the database.')
