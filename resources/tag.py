from flask_smorest import Blueprint, abort
from flask.views import MethodView
from schemas import TagSchema, ItemTagSchema
from db import db
from models import StoreModel, TagModel, ItemModel
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Tags", "tags", description='Operations on tag')

# ---------- tag endpoints ----------
@blp.route('/store/<int:storeId>/tag')
class TagsInStore(MethodView):
    # get all tags in specific store
    @blp.response(200, TagSchema(many=True))
    def get(self, storeId):
        # first get the target store
        store = StoreModel.query.get_or_404(storeId)
        return store.tags.all()
    
    # create tag in specific store
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tagData, storeId):
        tag = TagModel(**tagData, storeId=storeId)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message = str(e))
        return tag


@blp.route('/tag/<int:tagId>')
class Tag(MethodView):
    # get specific tag
    @blp.response(200, TagSchema)
    def get(self, tagId):
        tag = TagModel.query.get_or_404(tagId)
        return tag

    # delete specific tag
    @blp.response(202, 
        description="Deletes a tag if no item is tagged with it."
    )
    @blp.alt_response(404,
        description="Tag not found."
    )
    @blp.alt_response(400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted."
    )
    def delete(self, tagId):
        tag = TagModel.query.get_or_404(tagId)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return { 'message': 'tag deleted' }
        abort(400, message = "Could not delete tag. Make sure tag is not associated with any items, then try again.")

@blp.route('/item/<int:itemId>/tag/<int:tagId>')
class LinkTagstoItem(MethodView):
    # link tag to item
    @blp.response(201, TagSchema)
    def post(self, itemId, tagId):
        # first find the tag and item
        item = ItemModel.query.get_or_404(itemId)
        tag = TagModel.query.get_or_404(tagId)
        # make sure item and tag have same store id
        if item.store.id != tag.store.id:
            abort(400, message = "Make sure item and tag belong to the same store before linking.")
        
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "An error occured during tag insertion.")
        return tag


    # Unlink tag to item
    @blp.response(200, ItemTagSchema)
    def delete(self, itemId, tagId):
        # first find the tag and item
        item = ItemModel.query.get_or_404(itemId)
        tag = TagModel.query.get_or_404(tagId)
        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "An error occured during tag deletion.")
        return { "message": "tag removed successfully" }