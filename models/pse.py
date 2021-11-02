from sql_alchemy import banco



class PseModel(banco.Model):
    __tablename__= 'listapse'

    pse_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80))
    data = banco.Column(banco.PickleType())
    pse = banco.Column(banco.String(2))
    duracao = banco.Column(banco.String(3))


    def __init__ (self, pse_id, nome, data, pse, duracao):
        self.pse_id = pse_id
        self.nome =  nome
        self.data = data
        self.pse = pse
        self.duracao = duracao
    def json(self):
        return {
            'pse_id': self.pse_id,
            'nome' : self.nome,
            'data': self.data,
            'pse': self.pse,
            'duracao': self.duracao

        }
    @classmethod
    def find_pse(cls, pse_id):
        pse = cls.query.filter_by(pse_id=pse_id).first()
        if pse:
            return pse
        return None

    def save_pse(self):
        banco.session.add(self)
        banco.session.commit()

    def update_pse(self, nome, data, pse, duracao):
        self.nome =  nome
        self.data = data
        self.pse = pse
        self.duracao = duracao

    def delete_pse(self):
        banco.session.delete(self)
        banco.session.commit()
