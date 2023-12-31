from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdataSchema

blp = Blueprint("items", __name__, description="Operations on items")


@jwt_required()
@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, item_data):  # Create Item
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return item, 201

    # @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):  # Get all items
        return ItemModel.query.all()


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):  # Get item by item_ID
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):  # Delete item by item_ID
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    @blp.arguments(ItemUpdataSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):  # Update item by item_ID
        item = ItemModel.query.get(item_id)

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
            item.image = item_data["image"]
            item.description = item_data["description"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item
