from flask import Flask

def create_app():
    app = Flask(__name__)

    # Register blueprints or routes
    with app.app_context():
        from .routes import main  # Import your routes
        app.register_blueprint(main)

    return app
