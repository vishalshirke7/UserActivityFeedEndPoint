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
        if user_id:
            now = datetime.datetime.now()
            then = now - datetime.timedelta(hours=int(time_range))
            print(then)
            user_activities = db.session.query(ItemEdited).filter(and_(ItemEdited.user_id==user_id, ItemEdited.edited_timestamp>=then))
            ls = ""
            dicto = {}
            for user in user_activities:
                # item_list = [i for i in user.]
                name = user.user.first_name
                print(name)
                dicto[name] = "edited item {0} at {1}".format(user.items.name, user.edited_timestamp)
                # ls + "{0} edited item {1} at {2}".format(user.user.first_name, user.items.name, user.edited_timestamp)
            return jsonify(dicto)
            # return "User id {}".format(user_id)
        all_activities = db.session.query(ItemEdited).all()
        return "Time range {}".format(time_range)

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
