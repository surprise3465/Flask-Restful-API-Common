import json

from flask import Blueprint,jsonify,request,abort
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, Api, reqparse
from sqlalchemy import (func, exc, distinct, inspect, desc)

from appcore.models import db
from appcore.schemas import *
from appcore.common_method import *
from appcore.errors import *

common_resource_bp = Blueprint('common_resource', __name__)
api = Api(common_resource_bp)

            
class ResourceHandler(Resource):
    
    @jwt_required()
    def post(self,table_name):
        data = request.get_json(force=True)

        if not validateJson(data, input_schema_dic[table_name]):
            raise BadRequestError("Paramter Error")

        try:
            TableClass = get_class_by_tablename(table_name)
            if TableClass == None: raise Exception("Table not found: %s" % table_name)

            obj = TableClass(**data)
            if "user_id" in TableClass.__table__.columns.keys():
                obj.user_id = current_identity.id

            db.session.add(obj)
            db.session.commit()
           
            return jsonify({
                "status": "success",
                "id": obj.id,
                })
        except Exception as e:
            db.session.rollback()
            raise BadRequestError(str(e))

    
    @jwt_required()
    def get(self,table_name):
        try:
            TableClass = get_class_by_tablename(table_name)
            if TableClass == None: raise Exception("Table not found: %s" % table_name)

            query = db.session.query(TableClass) 

            if "user_id" in TableClass.__table__.columns.keys():
                query = query.filter_by(user_id = current_identity.id)

            objects = query.all()

            return jsonify({"data":[output_schema_dic[table_name](item) for item in objects]})

        except Exception as e:
            raise BadRequestError(str(e))


class ResourceEditHandler(Resource):

    @jwt_required()
    def delete(self, table_name, id):

        try:
            TableClass = get_class_by_tablename(table_name)
            if TableClass == None: 
                raise Exception("Table not found: %s" % table_name)
            
            query = db.session.query(TableClass) 

            obj = query.filter_by(**{"id":id}).first()

            if "is_deleted" in TableClass.__table__.columns.keys():
                setattr(obj,"is_deleted",1)
            else:    
                db.session.delete(obj)

            db.session.commit()

            status = {'status': 'success'}
            return jsonify(status)

        except Exception as e:
            db.session.rollback()
            raise BadRequestError(str(e))


    @jwt_required()
    def get(self, table_name, id):

        try:
            TableClass = get_class_by_tablename(table_name)
            if TableClass == None: raise Exception("Table not found: %s" % table_name)

            query = db.session.query(TableClass) 

            obj = query.filter_by(**{"id":id}).first_or_404()

            data = output_schema_dic[table_name](obj)

            return jsonify(data)

        except Exception as e:
            raise BadRequestError(str(e))


    @jwt_required()
    def patch(self, table_name, id):

        data = request.get_json(force=True)

        if not validateJson(data, input_schema_dic[table_name]):
            raise BadRequestError("Paramter Error")

        try:
            TableClass = get_class_by_tablename(table_name)
            if TableClass == None: raise Exception("Table not found: %s" % table_name)

            obj = db.session.query(TableClass).filter_by(**{"id":id}).first()

            if obj == None: raise Exception("No data found.")
            for key in data.keys():
                setattr(obj, key, data[key])
            db.session.commit()

            return jsonify({
                "status": "success",
                "id": obj.id,
                })

        except Exception as e:
            db.session.rollback()
            raise BadRequestError(str(e))


class ResourceFetchHandler(Resource):

    @jwt_required()
    def post(self,table_name):

        try:          
            TableClass = get_class_by_tablename(table_name)
            if TableClass == None: 
                raise Exception("Table not found: %s" % table_name)

            data = request.get_json(force=True)
          
            query = db.session.query(TableClass) 

            if "user_id" in TableClass.__table__.columns.keys():
                query = query.filter_by(user_id = current_identity.id)
            
            if "is_deleted" in TableClass.__table__.columns.keys():
                query = query.filter_by(is_deleted=False)

            if 'where' in data:
                query = query.filter_by(**data['where'])

            if 'orderby' in data:
                for cname in data['orderby'].split(','):
                    reverse = False
                    if cname.endswith(' desc'):
                        reverse = True
                        cname = cname[:-5]
                    elif cname.endswith(' asc'):
                        cname = cname[:-4]
                    print("cname: ", cname)
                    column = getattr(TableClass, cname)
                    if reverse: 
                        column = desc(column)
                    query = query.order_by(column)

            if "inlist" in data:
                for key,val in  data["inlist"].items():  
                    query = query.filter(getattr(TableClass, key).in_(val))

            if "like" in data:
                for key,val in  data["like"].items():  
                    query = query.filter(getattr(TableClass, key).like("%" + val + "%"))

            if "compare" in data:
                filters = get_filter_by_args(TableClass, data["compare"])
                query = query.filter(*filters)

            if 'limit' in data:
                query = query.limit(data['limit'])

            if 'offset' in data:
                query = query.offset(data['offset'])

            objects = query.all()

            return jsonify({"data":[output_schema_dic[table_name](item) for item in objects]})

        except Exception as e:
            raise BadRequestError(str(e))


api.add_resource(ResourceHandler, '/resource/<table_name>/')

api.add_resource(ResourceEditHandler, '/resource/<table_name>/<int:id>/')

api.add_resource(ResourceFetchHandler, '/resource/<table_name>/fetch/')