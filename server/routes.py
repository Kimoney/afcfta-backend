from flask import Blueprint


# Define your blueprint
main = Blueprint('main', __name__)


@main.route('/')
def home():
    return 'Hello, World From AfCFTA'