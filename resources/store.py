import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import StoreModel
from db import db

from schemas import StoreSchema

blp = Blueprint("Stores", __name__, description="Operations on stores")

@jwt_required()
@blp.route("/store") #Gets all stores
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True)) #Formats output data according to StoreSchema
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store


@jwt_required()
@blp.route("/store/<int:store_id>") #Gets, deletes a specific store by ID
class Store(MethodView):
    @blp.response(200, StoreSchema) #Formats output data according to StoreSchema
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store


    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted."}

