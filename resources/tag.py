from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models import StoreModel, TagModel, ItemModel
from schemas import TagSchema, TagAndItemSchema


blp = Blueprint("Tags", __name__, description="Operations on tags")


@blp.route("/store/<int:store_id>/tag")  # Gets all tags
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))  # Formats output data according to TagSchema
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return TagModel.query.filter_by(store_id=store_id).all()
        # Alternatively: return store.tags.all()
    

    @blp.arguments(TagSchema)       # Creates a new tag
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter_by(name=tag_data["name"]).first():
            abort(400, message="A tag with that name already exists in this store.")
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A tag with that name already exists in this store.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the tag.")

        return tag
    

@blp.route("/item/<int:item_id>/tag/<int:tag_id>")  # Links or unlinks a tag to/from an item
class LinkTagsToItem(MethodView):
    @blp.response(200, TagAndItemSchema)
    def post(self, item_id, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        item = ItemModel.query.get_or_404(item_id)

        if item.store.id != tag.store.id:
            abort(400, message="Make sure item and tag belong to the same store before linking.")

        try:
            item.tags.append(tag)
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred linking the tag to the item.")

        return {"message": "Item is linked to the ", "tag": tag, "item": item}
    

    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        item = ItemModel.query.get_or_404(item_id)

        if item.store.id != tag.store.id:
            abort(400, message="Make sure item and tag belong to the same store before linking.")

        try:
            item.tags.remove(tag)
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred unlinking the tag from the item.")

        return {"message":"Item removed from the ", "tag": tag, "item": item}
    
@blp.route("/tag/<int:tag_id>")  # Gets a specific tag
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    @blp.response(202,
                    description="Deletes a tag if no item is tagged with it.",
                    example={"message": "Tag deleted."})
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.",
        example={"message": "Tag is assigned to one or more items and cannot be deleted."},
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(400, message="Tag is assigned to one or more items and cannot be deleted.")