from flask import jsonify
from .. import app


@app.route('/',  methods=['GET'])
def index():
    return jsonify({'message': 'Initial Route'})
