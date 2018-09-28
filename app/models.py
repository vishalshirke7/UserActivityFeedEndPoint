from Scripts.activityfeed.app.db import db
import datetime


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    variant_edited = db.relationship('VariantEdited', backref="user")
    item_edited = db.relationship('ItemEdited', backref="user")
    var_prop = db.relationship('VariantProperties', backref="user")
    # items_edited = db.relationship('Items')

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '<User: {}>'.format(self.first_name)


class Items(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    brand = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    # edited_timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.now,)
    item_edited = db.relationship('ItemEdited', backref="items")
    variants = db.relationship('Variant', backref="items")
    # variant_edited = db.relationship('VariantEdited', backref="items")

    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, brand, category):
        self.name = name
        self.brand = brand
        self.category = category


class Variant(db.Model):

    __tablename__ = 'variant'

    id = db.Column(db.Integer, primary_key=True)
    var_name = db.Column(db.String(120), nullable=False)
    sp = db.Column(db.Integer, nullable=False)
    cp = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    variant_edited = db.relationship('VariantEdited', backref="variant")
    variant_prop = db.relationship('VariantProperties', backref="variant")


class ItemEdited(db.Model):

    __tablename__ = 'itemedited'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    new_item_created = db.Column(db.Boolean, default=False)
    item_edited = db.Column(db.Boolean, default=False)
    edited_timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.now)
    name = db.Column(db.Boolean, default=False)
    brand = db.Column(db.Boolean, default=False)
    category = db.Column(db.Boolean, default=False)


class VariantEdited(db.Model):

    __tablename__ = 'variantedited'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    variant_id = db.Column(db.Integer, db.ForeignKey('variant.id'))
    new_variant_created = db.Column(db.Boolean, default=False)
    variant_deleted = db.Column(db.Boolean, default=False)
    variant_edited = db.Column(db.Boolean, default=False)
    edited_timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.now)
    var_name = db.Column(db.Boolean, default=False)
    sp = db.Column(db.Boolean, default=False)
    cp = db.Column(db.Boolean, default=False)
    quantity = db.Column(db.Boolean, default=False)


class VariantProperties(db.Model):

    __tablename__ = 'variantproperties'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    variant_id = db.Column(db.Integer, db.ForeignKey('variant.id'))
    prop_name = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.now)
