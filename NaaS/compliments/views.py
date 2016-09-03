from flask import jsonify, abort, request
from .. import app

from .models import Compliment


def build_compliment(compliment):
    return {'id': compliment['id'], 'text': compliment['text']} if compliment else abort(404)


@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Hi, this is an API that you can use to get a nice compliment.'})


@app.route('/compliments', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = "Compliment added but is waiting for review!"
        compliment = Compliment(request.form['text'])
        try:
            compliment.save()
        except Exception as e:
            message = str(e)
        return jsonify({"message": message})
    else:
        compliments = Compliment.get_all()
        json = [build_compliment(compliment) for compliment in compliments]
        return jsonify(json)


@app.route('/compliments/<int:compliment_id>', methods=['GET'])
def show(compliment_id):
    compliment = Compliment.get_by_id(compliment_id)
    return jsonify(build_compliment(compliment))


@app.route('/compliments/random', methods=['GET'])
def random():
    compliment = Compliment.get_random()
    return jsonify(build_compliment(compliment))
