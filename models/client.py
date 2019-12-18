from sql_alchemy import banco

class ClientModel(banco.Model):
    __tablename__ = 'clients'
    client_id = banco.Column(banco.Integer, primary_key=True)
    name = banco.Column(banco.String(40))
    email = banco.Column(banco.String(40))

    def __init__(self, client_id, name, email): #não passa o id e o sistema vai incrementando ao ver vazio
        self.name = name
        self.email = email
    
    def json(self):
        return {
            'client': self.client_id,
            'login': self.name,
            'email': self.email
        }

    @classmethod
    def find_client(cls, client_id): #cls é a mesma coisa de escrever HotelModel poe ex
        client = cls.query.filter_by(client_id=client_id).first() #faz uma consulta usando um método de banco.Model
        #SELECT * FROM hotels WHERE hotel_id=$hotel_id LIMIT 1
        if client:
            return client
        return None
    
    @classmethod
    def find_by_email(cls, email): #cls é a mesma coisa de escrever HotelModel poe ex
        user = cls.query.filter_by(email=email).first() #faz uma consulta usando um método de banco.Model
        #SELECT * FROM hotels WHERE hotel_id=$hotel_id LIMIT 1
        if user:
            return user
        return None


    def insertClient(self):
        banco.session.add(self)
        banco.session.commit()

    def updateClient(self, name):
        self.name = name

    def deleteClient(self):
        banco.session.delete(self)
        banco.session.commit()