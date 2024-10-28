from flask import Blueprint
from flask_restful import Api
from .resources import IndicatorResource


# Define your blueprint
main = Blueprint('main', __name__)
api = Api(main)

#  Register the new resource with a route
api.add_resource(IndicatorResource, '/indicator/<string:indicator_name>')

@main.route('/')
def home():
    return 'Hello, World From AfCFTA'
