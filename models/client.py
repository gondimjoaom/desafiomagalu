from sql_alchemy import banco
import copy

class ClientModel(banco.Model):
    __tablename__ = 'clients'
    #client_id = banco.Column(banco.Integer, primary_key=True)
    name = banco.Column(banco.String(40))
    email = banco.Column(banco.String(40), primary_key=True)
    productList = banco.Column(banco.JSON)

    def __init__(self, productList, name, email): #não passa o id e o sistema vai incrementando ao ver vazio
        self.name = name
        self.email = email
        self.productList = productList

    def json(self):
        return {
            'login': self.name,
            'email': self.email,
            'productList': self.productList
        }
    
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
    
    def updateProductList(self, price, image, brand, id, title, reviewScore):
        newProductList = copy.deepcopy(self.productList)
        newProductList[id] = {
            "price": price,
            "image": image,
            "brand": brand,
            "title": title,
            "reviewScore": reviewScore 
        }
        self.productList = copy.deepcopy(newProductList)
        #print(self.productList)

    def deleteClient(self):
        banco.session.delete(self)
        banco.session.commit()