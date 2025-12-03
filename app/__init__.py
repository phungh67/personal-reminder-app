from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Configuration usually goes here (e.g., app.config.from_object(Config))

    # Register Blueprints
    from app.main.routes import main
    app.register_blueprint(main)

    return app