from db import db

# secondary table to be used in many to many relationship
class ItemTagModel(db.Model):
    __tablename__ = 'itemtag'

    id = db.Column(db.Integer, primary_key=True)
    itemId = db.Column(db.Integer, db.ForeignKey('items.id'))
    tagId = db.Column(db.Integer, db.ForeignKey('tags.id'))