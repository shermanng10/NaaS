from flask import Flask, jsonify
import logging
from logging.handlers import RotatingFileHandler
import werkzeug

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)

handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))

app.logger.addHandler(handler)


@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_bad_request(e):
    app.logger.error(e)
    return jsonify({'message': 'Oops, nothing to see here'})

from .db.database import initdb, close_db_connection  # noqa: F401

from .compliments import views  # noqa: F401
