from flask import Blueprint,jsonify,request
import json
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, Api, reqparse
from sqlalchemy import func
from appcore.models import db
from appcore.models.seller import Seller,Customer


seller_bp = Blueprint('seller', __name__)
api = Api(seller_bp)

class SellerHandler(Resource):
    def get(self):
        items = db.session.query(
             Customer.seller_id, \
             Seller.name.label('seller_name'), \
             func.count(Customer.id).label('total_cst'), \
             func.sum(Customer.money).label('total_money')) \
            .outerjoin(Seller, Customer.seller_id == Seller.id).group_by(Customer.seller_id).all()
        result = []

        for item in items:
            temp = {}
            temp["seller_id"] = str(item.seller_id)
            temp["seller_name"] = item.seller_name
            temp["cst_count"] = item.total_cst
            temp["total_money"] = str(item.total_money)
            result.append(temp)

        items = db.session.query(
            func.count(Customer.id).label('number'), \
            Customer.status.label('status'),  \
            Customer.seller_id) \
           .outerjoin(Seller, Customer.seller_id == Seller.id).group_by(Customer.seller_id,Customer.status).all()   

        for item in items:
            for res in result:
                if(res["seller_id"] == str(item.seller_id)):                                   
                    res['status'+str(item.status)] = item.number
                    
        return jsonify({"data":result})


api.add_resource(SellerHandler, '/seller/')