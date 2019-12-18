from flask_restful import Resource, reqparse
from models.client import ClientModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

args = reqparse.RequestParser()
args.add_argument('name', type=str, required=True, help="This field cannot be left blank")
args.add_argument('email', type=str, required=True, help="This field cannot be left blank")

class Clients(Resource):
    def get(self):
        return {'clients': [client.json() for client in ClientModel.query.all()]}

class Client (Resource):
    # /user/{userid}
    def get (self, user_id):
        client = ClientModel.find_client(user_id)
        if client:
            return client.json()
        return {'message' : 'client not found'}, 404 #status code do http para dizer que não achou

    @jwt_required
    def delete(self, client_id):
        client = ClientModel.find_client(client_id)
        if client:
            try:
                client.deleteClient()
            except:
                return {'message': 'Internal error trying to delete client.'}, 500 #status code para internal server error
            return {'message': 'Client deleted'}

        return {'message': 'Client not found.'}, 404
    
    def put(self, client_id):
        data = args.parse_args()
        client = ClientModel.find_by_email(data['email'])
    
        if client:
            client.updateClient(data['name'])
            try:
                client.insertClient()
            except:
                return {'message': 'Internal error trying to update client'}, 500
            return client.json(), 200
        client = ClientModel(client_id, **data)
        try:
            client.insertClient()
        except:
            return {'message': 'Internal error trying to update client'}, 500
        return client.json(), 200

class ClientRegister(Resource):
    #/signup
    def post(self):
        data = args.parse_args()

        if ClientModel.find_by_email(data['email']): #quando usuario é criado, ele ainda não sabe seu user_id
            return {'message': "Email {} already been used.".format(data['email'])}, 400
        
        client = ClientModel(**data)
        client.insertClient()
        return {'message': 'Client created successfully'}, 201

class ClientLogin(Resource):
    @classmethod
    def post (cls):
        data = args.parse_args()
        
        client = ClientModel.find_by_email(data['email'])
        if client:
            accessToken = create_access_token(identity=client.client_id)
            return {'accessToken': accessToken}, 200
        return {'message': 'Username or password incorrect'}, 401

class ClientLogout(Resource):
    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti'] #jwt token identifier
        BLACKLIST.add(jwt_id) #arquivo de tokens usados
        return {'message': 'Logged out.'}, 200
