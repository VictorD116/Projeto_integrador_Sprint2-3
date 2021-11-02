from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import safe_str_cmp

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank ")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank ")

class User(Resource):
    # /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404 #not found

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return {'massage': 'User deleted'}
        return {'massage': 'User not found.'}, 404

class UserRegister(Resource):
    # /cadastro
    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"messege":"The login '{}' already existis.".format(dados['login'])}

        user = UserModel(**dados)
        user.save_user()
        return {'message:' 'User created sucessfully'}, 201 #created

class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'access_token': token_de_acesso}, 200
        return {'massage': 'The username or password is incorrect.'}, 401 #Unauthorized
