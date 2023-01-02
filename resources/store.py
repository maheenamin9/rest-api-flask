from flask import request
from flask_smorest import Blueprint, abort
import uuid
from flask.views import MethodView
from schemas import StoreSchema
from models import StoreModel
from db import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

blp = Blueprint("Stores", "stores", description="operations on store")

# stores = [
#     {
#         "name": "Maheen store",
#         "items": [
#             {
#                 "name": "pencils",
#                 "price": 20
#             }
#         ]
#     }
# ]

# ---------- store endpoints ----------
@blp.route('/store')
class StoreList(MethodView):
    # create store
    @blp.arguments(StoreSchema) # blueprint.arguments decorator
    @blp.response(201, StoreSchema)
    def post(self, storeData):
        # creating store model
        newStore = StoreModel(**storeData)
        try:
            db.session.add(newStore)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "Store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message = "An error occured during store insertion.")
        return newStore
        # if "name" not in storeData:
        #     abort(400, message="Bad request: name is required field.")
        # for store in stores.values():
        #     if storeData['name'] == store['name']:
        #         abort(400, message="Bad request: store already exists.")
        # storeId = uuid.uuid4().hex
        # newStore = {**storeData , "id": storeId}
        # stores[storeId] = newStore
        # return newStore, 201

        # requestData = request.get_json()
        # newStore = {"name": requestData["name"], "items": []}
        # stores.append(newStore)
        # return newStore, 201

    # get all stores
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

        # return stores.values()

        # return { "stores": stores }

@blp.route('/store/<int:storeId>')
class Store(MethodView):
    # get specific store
    @blp.response(200, StoreSchema)    
    def get(self, storeId):
        store = StoreModel.query.get_or_404(storeId)
        return store
        # try:
        #     return stores[storeId]
        # except KeyError:
        #     abort(404, message = "store not found.")

        # for store in stores:
        #     if store['name'] == storeName:
        #         return {"store": store}
        # return {"message": "store not found"}, 404

    # delete store
    def delete(self, storeId):
        store = StoreModel.query.get_or_404(storeId)
        db.session.delete(store)
        db.session.commit()
        return { "message": "store deleted" }
        # try:
        #     del stores[storeId]
        #     return { "message": "store deleted" }
        # except KeyError:
        #     abort(404, message = "store not found.")
