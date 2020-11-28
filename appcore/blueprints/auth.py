from flask import Blueprint,jsonify,request
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, Api
from sqlalchemy import exc
from typing import Dict
import os

from appcore.models import db
from appcore.models.user import User
from appcore.schemas import *
from appcore.common_method import *
from appcore.errors import *
auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)


class UserHandler(Resource):

    def post(self):
        data = request.get_json(force=True)
        if not validateJson(data, InputUserSchema):
            raise BadRequestError("Paramter Error")
        user = User()
        user.email = data["email"]
        user.password = data["password"]
        db.session.add(user)
        db.session.flush()
        
        try:
            db.session.commit()
        except exc.SQLAlchemyError as e:           
            db.session.rollback()
            raise BadRequestError(str(e))
       
        return {"status":"success"}

    @jwt_required()
    def get(self):
        return output_schema_dic["users"](current_identity)
    

api.add_resource(UserHandler, '/user/')
