from flask import Flask, jsonify
from flask_restful import Resource, Api
from resources.client import Clients, Client, ClientRegister, ClientLogin, ClientLogout, addProduct
from flask_jwt_extended import JWTManager #gerenciar autenticacao
from blacklist import BLACKLIST


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db' #pode ser outro banco (mongo, postgres etc) | postgresql+psycopg2://
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'Há um beijo, um segredo pairando no ar' #garante criptografia, apenas a aplicação tem a chave
app.config['JWT_BLACKLIST_ENABLED'] = True

api = Api(app) #gerencia o funcionamento da API
jwt = JWTManager(app)

@app.before_first_request #verifica se existe banco e executa o create all se não existir
def create_db():
    banco.create_all()

@jwt.token_in_blacklist_loader #determina que funcao verifique se o token esta na blacklist
def check_blacklist (token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader #acesso revogado
def revoked_token():
    return jsonify({'message': 'You have been logged out'}), 401 #dicionario aqui em app não é reconhecido diretamente, por isso o uso do jsonify

api.add_resource(Clients, '/clients')
api.add_resource(Client, '/client/<string:email>')
api.add_resource(ClientRegister, '/signup')
api.add_resource(ClientLogin, '/login')
api.add_resource(ClientLogout, '/logout')
api.add_resource(addProduct, '/addProduct/<string:email>')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app) #só executa se for chamado aqui
    app.run(debug=True)