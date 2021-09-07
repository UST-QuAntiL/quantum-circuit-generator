from . import api
from ..services import encoding_service
from flask import request




@api.route('/', methods=['GET', 'POST'])
def index():
    return '<h1>Quantum Circuit Generator is Running!!!</h1>'

@api.route('/encoding/<name>', methods=['POST'])
def encoding(name):
    # TODO splitting in service - check if name exists/functional , check if request is not empty
    if(name == 'basis'):
        response = encoding_service.generate_basis_encoding(request.json)
        return response.to_json()
    elif(name == 'angle'):
        return '<h4>angle encoding rocks!!!</h4>'
    else:
        return 'Encoding does not exist'
