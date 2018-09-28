import datetime
from flask import request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import jsonify, json
from sqlalchemy import and_

from Lib.tokenize import String


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config.from_pyfile('dev_config.py', silent=True)
    from Scripts.activityfeed.app.models import db
    db.init_app(app)
    migrate = Migrate(app, db)
    from Scripts.activityfeed.app.models import User, ItemEdited, Items, Variant, VariantEdited


    # @app.route('/')
    @app.route('/api/useractivity/<path:user_id>/<path:time_range>')
    @app.route('/api/useractivity/<path:time_range>', defaults={'user_id': None})
    def hello_world(user_id, time_range):

        now = datetime.datetime.now()
        then = now - datetime.timedelta(hours=int(time_range))
        dicto, a = {}, 0
        all_user_activities_item = db.session.query(ItemEdited).filter(and_(ItemEdited.edited_timestamp >= then))
        all_user_activities_variant = db.session.query(VariantEdited).filter(
            and_(VariantEdited.edited_timestamp >= then))
        user_activities_on_items = db.session.query(ItemEdited).filter(and_(ItemEdited.user_id==user_id, ItemEdited.edited_timestamp>=then))
        user_activities_on_variants = db.session.query(VariantEdited).filter(and_(VariantEdited.user_id==user_id, VariantEdited.edited_timestamp>=then))
        if user_id:
            ls = user_activities_on_items
            ls1 = user_activities_on_variants
        else:
            ls = all_user_activities_item
            ls1 = all_user_activities_variant

        for activity in ls:
            item_attr_dict = {}
            item_attr_dict['name'] = activity.name
            item_attr_dict['brand'] = activity.brand
            item_attr_dict['category'] = activity.category
            if activity.new_item_created:
                dicto[a] = "{0} created new item {1}".format(activity.user.first_name, activity.items.name)
                a+=1
            else:
                edited_attributes = ""
                for key, value in item_attr_dict.items():
                    if value:
                        edited_attributes = edited_attributes + key + ","
                        # ls + "{0} edited {1} of item '{2}' \n".format(user.user.first_name, key, user.items.name)
                edited_attributes = edited_attributes[:-1]
                dicto[a] = "{0} edited {1} of item {2} on {3}".format(activity.user.first_name, edited_attributes, activity.items.name, activity.edited_timestamp)
                a+=1
        for var_activity in ls1:
            var_attr_dict = {}
            var_attr_dict['var_name'] = var_activity.var_name
            var_attr_dict['cp'] = var_activity.cp
            var_attr_dict['sp'] = var_activity.sp
            var_attr_dict['quantity'] = var_activity.quantity
            if var_activity.new_variant_created:
                dicto[a] = "{0} Created new variant {1} on ".format(var_activity.user.first_name, var_activity.variant.var_name, var_activity.edited_timestamp)
                a+=1
            elif var_activity.variant_deleted:
                dicto[a] = "{0} Deleted a variant {1} on ".format(var_activity.user.first_name,
                                                                    var_activity.variant.var_name,
                                                                    var_activity.edited_timestamp)
                a+=1
            else:
                edited_var_attributes = ""
                for key, value in var_attr_dict.items():
                    if value:
                        edited_var_attributes = edited_var_attributes + key + ","
                        # ls + "{0} edited {1} of item '{2}' \n".format(user.user.first_name, key, user.items.name)
                edited_var_attributes = edited_var_attributes[:-1]
                dicto[a] = "{0} edited {1} of variant {2} on {3}".format(var_activity.user.first_name, edited_var_attributes,
                                                                         var_activity.variant.var_name,
                                                                         var_activity.edited_timestamp)
                a += 1
        return jsonify(dicto)

    return app

# return "Time range {}".format(time_range)
# itemedited = ItemEdited(user_id=4, item_id=3, name=True, brand=True, category=True)
# variantedited1 = VariantEdited(user_id=1, variant_id=2, var_name=True, sp=True, quantity=False)
# variantedited2 = VariantEdited(user_id=1, variant_id=1, var_name=True, cp=False, quantity=True)
# variantedited3 = VariantEdited(user_id=5, variant_id=2, var_name=True, sp=True, quantity=False)
# variantedited4 = VariantEdited(user_id=2, variant_id=1, var_name=True, cp=False, quantity=True)
# # db.session.add(itemedited)
# db.session.add(variantedited1)
# db.session.add(variantedited2)
# db.session.add(variantedited3)
# db.session.add(variantedited4)
