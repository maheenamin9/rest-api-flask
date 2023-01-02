from flask_smorest import Blueprint, abort
from flask.views import MethodView
from schemas import ItemSchema, ItemUpdateSchema
from db import db
from models import ItemModel
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint("Items", "items", description="operations on item")

# ---------- item endpoints ----------
@blp.route('/item')
class ItemList(MethodView):
    # create item in specific store
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    @jwt_required()
    def post(self, itemData):
        newItem = ItemModel(**itemData)
        try:
            db.session.add(newItem)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "An error occured during item insertion.")
        return newItem, 201

        # # duplicate validation
        # for item in items.values():
        #     if (
        #         itemData['name'] == item["name"] and
        #         itemData['storeId'] == item["storeId"]
        #     ):
        #         abort(400, message="item already exits")

        # if itemData["storeId"] not in stores:
        #     abort(404, message = "store not found.")
        # itemId = uuid.uuid4().hex
        # newItem = { **itemData, "id": itemId }
        # items[itemId] = newItem
        # return newItem, 201

        # requestData = request.get_json()
        # for store in stores:
        #     if store['name'] == storeName:
        #         newItem = { "name": requestData["name"], "price": requestData["price"] }
        #         store["items"].append(newItem)
        #         return newItem, 201
        # return {"message": "store not found"}, 404

    # get all items
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

        # return items.values()

@blp.route('/item/<int:itemId>')
class Item(MethodView):
    # get specific item
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, itemId):
        item = ItemModel.query.get_or_404(itemId)
        return item
        # try:
        #     return items[itemId]
        # except KeyError:
        #     abort(404, message = "item not found.")

    # delete item
    @jwt_required(fresh=True)  # need fresh token to delete item
    def delete(self, itemId):
        # jwt claims
        jwt = get_jwt()
        if not jwt.get('isAdmin'):
            abort(401, message="Admin privilage required")
        item = ItemModel.query.get_or_404(itemId)
        db.session.delete(item)
        db.session.commit()
        return { "message": "item deleted" }

        # try:
        #     del items[itemId]
        #     return { "message": "item deleted" }
        # except KeyError:
        #     abort(404, message = "item not found.")

    # update item
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemUpdateSchema)
    @jwt_required()
    def put(self, itemData, itemId):  # update existing or add new item
        item = ItemModel.query.get(itemId)
        if item:
            item.name = itemData['name']
            item.price = itemData['price']
        else:
            item = ItemModel(id=itemId, **itemData)
            print(item)

        db.session.add(item)
        db.session.commit()
        return item

        # itemData = request.get_json()
        # try:
        #     item = items[itemId]
        #     item |= itemData
        #     return item
        # except KeyError:
        #     abort(404, message = "item not found.")
