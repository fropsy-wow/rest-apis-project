from db import db


class TagModel(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    store = db.relationship('StoreModel', back_populates='tags')
    items = db.relationship('ItemModel', secondary='items_tags', back_populates='tags')


    def __repr__(self):
        return f"<Tag {self.name}>"