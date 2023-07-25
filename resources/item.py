import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdataSchema
from db import items

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item")
class Item(MethodView):
    @blp.arguments(ItemSchema)
    def post(self, item_data):  # Create Item
        for item in items.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message="Item already exists.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201

    def get(self):  # Get all items
        return {"items": list(items.values())}


@blp.route("/item/<string:item_id>")
class ItemList(MethodView):
    def get(self, item_id):  # Get item by item_ID
        try:
            return items[item_id], 200
        except KeyError:
            abort(404, message="Item not found")

    def delete(self, item_id):  # Delete item by item_ID
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found")


@blp.arguments(ItemUpdataSchema)
def put(self, item_id, item_data):  # Update item by item_ID
    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        abort(404, message="Item not found")
