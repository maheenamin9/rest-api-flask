from db import db

class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    storeId = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    # one(store) to many(tags) relationship
    store = db.relationship('StoreModel', back_populates='tags')
    # many(items) to many(tags) relationship
    items = db.relationship('ItemModel', back_populates='tags', secondary='itemtag')