from datetime import datetime
from appcore.models import db

class Seller(db.Model):
    __tablename__ = 'seller'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=True)
   


class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=True)
    seller_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    money = db.Column(db.Numeric, nullable=False)
