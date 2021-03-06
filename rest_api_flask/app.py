import os

from flask import Flask
from flask_restful import Api

from rest_api_flask.resources.item import Item, ItemList

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
api = Api(app)

api.add_resource(Item, '/item/<string:name>')

if __name__ == '__main__':
    from rest_api_flask.db import db

    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request  #run below method only before first request
        def create_tables():
            db.create_all()

    app.run(port=5000)
