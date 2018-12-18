from flask import jsonify, json
from flask import Blueprint
import datetime

from sqlalchemy import and_

from app.db import db
from .models import User
from .models import Items, Variant
from .models import ItemEdited, VariantEdited
from .models import VariantProperties
bp = Blueprint('views', __name__, url_prefix='/api')


@bp.route('/useractivity/<path:user_id>/<path:time_range>')
@bp.route('/useractivity/<path:time_range>', defaults={'user_id': None})
def hello_world(user_id, time_range):

    now = datetime.datetime.now()
    then = now - datetime.timedelta(hours=int(time_range))
    response, a = {}, 0
    all_user_activities_item = db.session.query(ItemEdited).filter(and_(ItemEdited.edited_timestamp >= then))
    all_user_activities_variant = db.session.query(VariantEdited).filter(
        and_(VariantEdited.edited_timestamp >= then))
    all_user_activities_variant_prop = db.session.query(VariantProperties).filter(
        and_(VariantProperties.timestamp >= then))
    user_activities_on_items = db.session.query(ItemEdited).filter(and_(ItemEdited.user_id==user_id,
                                                                        ItemEdited.edited_timestamp>=then))
    user_activities_on_variants = db.session.query(VariantEdited).filter(and_(VariantEdited.user_id==user_id,
                                                                              VariantEdited.edited_timestamp>=then))
    user_activities_on_variant_prop = db.session.query(VariantProperties).filter(
        and_(VariantProperties.user_id == user_id, VariantProperties.timestamp >= then))
    if user_id:
        ls = user_activities_on_items
        ls1 = user_activities_on_variants
        ls2 = user_activities_on_variant_prop
    else:
        ls = all_user_activities_item
        ls1 = all_user_activities_variant
        ls2 = all_user_activities_variant_prop
    for activity in ls:
        item_attr_dict = {}
        item_attr_dict['name'] = activity.name
        item_attr_dict['brand'] = activity.brand
        item_attr_dict['category'] = activity.category
        if activity.new_item_created:
            response[a] = "{0} created new item {1}".format(activity.user.first_name, activity.items.name)
            a += 1
        else:
            edited_attributes = ""
            for key, value in item_attr_dict.items():
                if value:
                    edited_attributes = edited_attributes + key + ","
                    # ls + "{0} edited {1} of item '{2}' \n".format(user.user.first_name, key, user.items.name)
            edited_attributes = edited_attributes[:-1]
            response[a] = "{0} edited {1} of item {2} on {3}".format(activity.user.first_name,
                                                                     edited_attributes, activity.items.name,
                                                                     activity.edited_timestamp)
            a += 1
    for var_activity in ls1:
        var_attr_dict = {}
        var_attr_dict['var_name'] = var_activity.var_name
        var_attr_dict['cp'] = var_activity.cp
        var_attr_dict['sp'] = var_activity.sp
        var_attr_dict['quantity'] = var_activity.quantity
        if var_activity.new_variant_created:
            response[a] = "{0} Created new variant {1} on {2}".format(var_activity.user.first_name,
                                                                      var_activity.variant.var_name,
                                                                      var_activity.edited_timestamp)
            a += 1
        elif var_activity.variant_deleted:
            response[a] = "{0} Deleted a variant {1} on {2}".format(var_activity.user.first_name,
                                                                var_activity.variant.var_name,
                                                                var_activity.edited_timestamp)
            a += 1
        else:
            edited_var_attributes = ""
            for key, value in var_attr_dict.items():
                if value:
                    edited_var_attributes = edited_var_attributes + key + ","
                    # ls + "{0} edited {1} of item '{2}' \n".format(user.user.first_name, key, user.items.name)
            edited_var_attributes = edited_var_attributes[:-1]
            response[a] = "{0} edited {1} of variant {2} on {3}".format(var_activity.user.first_name, edited_var_attributes,
                                                                     var_activity.variant.var_name,
                                                                     var_activity.edited_timestamp)
            a += 1
    for prop_activity in ls2:

        response[a] = "{0} {1} new variant property {2} for variant {3} on {4}".format(prop_activity.user.first_name,
                                                                                       prop_activity.status,
                                                                                       prop_activity.prop_name,
                                                                                       prop_activity.variant.var_name,
                                                                                       prop_activity.timestamp)
        a += 1
    return jsonify(response)
