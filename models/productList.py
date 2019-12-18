from sql_alchemy import banco


class ProductList(banco.Model):
    __tablename__ = 'productList'
    list_id = banco.Column(banco.Integer, primary_key=True)
    client_id = banco.Column(banco.Integer, banco.ForeignKey('clients.client_id'))
    def __init__ (self):
        self.productList = []
    
    def insertList(self):
        banco.session.add(self)
        banco.session.commit()