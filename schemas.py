from marshmallow import Schema, fields, validate



class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name= fields.Str(required=True)
    price= fields.Float(required=True)
    

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name= fields.Str(required=True)    

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    

class ItemUpdateSchema(Schema):
    name= fields.Str()
    price= fields.Float()
    store_id= fields.Int()


class ItemSchema(PlainItemSchema):
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    store_id= fields.Int(required=True, load_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class TagSchema(PlainTagSchema):
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    store_id = fields.Int(load_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    email = fields.Email(required=True, validate=validate.Length(max=120))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))