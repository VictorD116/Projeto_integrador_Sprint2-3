from flask_restful import Resource, reqparse
from models.pse import PseModel
from flask_jwt_extended import jwt_required

class ListaPSE(Resource):
    def get(self):
        return {'listapse': [pse.json() for pse in PseModel.query.all()]} #SELECT * FROM listpse

class Pse(Resource):
    atributos= reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank")
    atributos.add_argument('data')
    atributos.add_argument('pse')
    atributos.add_argument('duracao')


    def get(self, pse_id):
        pse = PseModel.find_pse(pse_id)
        if pse:
            return pse.json()
        return {'message': 'PSE not found'}, 404 #not found

    @jwt_required()
    def post(self, pse_id):
        if PseModel.find_pse(pse_id):
            return {"message": "PSE id '{}' already existis.".format(pse_id)}, 400 #Bad Request
        dados = Pse.atributos.parse_args()
        pse= PseModel(pse_id, **dados)
        try:
            pse.save_pse()
        except:
            return {'message': 'An internal erro ocurred trying to save PSE.'}, 500 #Internal Server ERROR
        return pse.json()

    @jwt_required()
    def put(self, pse_id):
        dados = Pse.atributos.parse_args()

        pse_encontrado = PseModel.find_pse(pse_id)
        if pse_encontrado:
            pse_encontrado.update_pse(**dados)
            pse_encontrado.save_pse()
            return pse_encontrado.json(), 200 #OK
        pse= PseModel(pse_id, **dados)
        try:
            pse.save_pse()
        except:
            return {'message': 'An internal erro ocurred trying to save PSE.'}, 500 #Internal Server ERROR
        return pse.json(), 201 #created

    @jwt_required()
    def delete(self, pse_id):
        pse = PseModel.find_pse(pse_id)
        if pse:
            try:
                pse.delete_pse()
            except:
                return {'message': 'An error ocurred trying to delete PSE'}, 500
            return {'massage': 'Pse deleted'}
        return {'massage': 'Pse not found.'}, 404
