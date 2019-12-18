from flask_restful import Resource, reqparse
from models.client import ClientModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST
import requests
import json

#args.add_argument('productList', type=dict, required=True, help="This field cannot be left blank")
productList = {}

class Clients(Resource):
    def get(self):
        return {'clients': [client.json() for client in ClientModel.query.all()]}

class addProduct(Resource):
    args = reqparse.RequestParser()
    args.add_argument('price', type=float, required=True, help="This field cannot be left blank")
    args.add_argument('image', type=str, required=True, help="This field cannot be left blank")
    args.add_argument('brand', type=str, required=True, help="This field cannot be left blank")
    args.add_argument('id', type=str, required=True, help="This field cannot be left blank")
    args.add_argument('title', type=str, required=True, help="This field cannot be left blank")
    args.add_argument('reviewScore', type=float)

    def put(self, email):
        client = ClientModel.find_by_email(email)
        productData = addProduct.args.parse_args()
        url = 'http://challenge-api.luizalabs.com/api/product/' + productData.get('id')
        magalu = requests.request('GET', url)
        if magalu.status_code == 200:
            client.updateProductList(**productData)
            try:
                client.insertClient()
            except:
                return {'message': 'Error trying to update list'}, 500
            return client.json(), 200
        return {'message': 'Product does not exist.'}, 400

class Client (Resource):
    args = reqparse.RequestParser()
    args.add_argument('name', type=str)
    args.add_argument('email', type=str, required=True, help="This field cannot be left blank")
    # /user/{userid}
    def get (self, email):
        client = ClientModel.find_by_email(email)
        if client:
            return client.json()
        return {'message' : 'client not found'}, 404 #status code do http para dizer que não achou

    @jwt_required
    def delete(self, email):
        client = ClientModel.find_by_email(email)
        if client:
            try:
                client.deleteClient()
            except:
                return {'message': 'Internal error trying to delete client.'}, 500 #status code para internal server error
            return {'message': 'Client deleted'}

        return {'message': 'Client not found.'}, 404
    
    def put(self, email):
        data = Client.args.parse_args()
        client = ClientModel.find_by_email(email)
    
        if client:
            client.updateClient(data['name'])
            try:
                client.insertClient()
            except:
                return {'message': 'Internal error trying to update client'}, 500
            return client.json(), 200
        client = ClientModel(productList, **data)
        try:
            client.insertClient()
        except:
            return {'message': 'Internal error trying to update client'}, 500
        return client.json(), 200

class ClientRegister(Resource):
    #/signup
    args = reqparse.RequestParser()
    args.add_argument('name', type=str)
    args.add_argument('email', type=str, required=True, help="This field cannot be left blank")
    def post(self):
        
        data = ClientRegister.args.parse_args()

        if ClientModel.find_by_email(data['email']): #quando usuario é criado, ele ainda não sabe seu user_id
            return {'message': "Email {} already been used.".format(data['email'])}, 400
        
        client = ClientModel(productList, **data)
        client.insertClient()
        return {'message': 'Client created successfully'}, 201

class ClientLogin(Resource):
    args = reqparse.RequestParser()
    args.add_argument('name', type=str)
    args.add_argument('email', type=str, required=True, help="This field cannot be left blank")
    @classmethod
    def post (cls):
        data = ClientLogin.args.parse_args()
        
        client = ClientModel.find_by_email(data['email'])
        if client:
            accessToken = create_access_token(identity=client.email)
            return {'accessToken': accessToken}, 200
        return {'message': 'Username or password incorrect'}, 401

class ClientLogout(Resource):
    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti'] #jwt token identifier
        BLACKLIST.add(jwt_id) #arquivo de tokens usados
        return {'message': 'Logged out.'}, 200
