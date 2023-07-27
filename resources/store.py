from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError
from db import db
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):  # Get store by ID
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):  # Delete store by ID
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted."}


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):  # Get all stores
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):  # Create Store
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the store.")
        return store, 201