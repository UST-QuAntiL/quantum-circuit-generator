from . import api
from ..services import encoding_service
from flask import request, jsonify




@api.route('/', methods=['GET', 'POST'])
def index():
    return '<h1>Quantum Circuit Generator is Running!!!</h1>'

@api.route('/encoding/<name>', methods=['POST'])
def encoding(name):
    if(name == 'basis'):
        input = request.json
        print(input)
        response = encoding_service.generate_basis_encoding(input)
        return response.to_json()
    elif(name == 'angle'):
        return '<h4>angle encoding rocks!!!</h4>'
    else:
        return 'Encoding does not exist'
