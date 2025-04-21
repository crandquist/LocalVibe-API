from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Import Blueprints
    from .routes.businesses import businesses_bp
    from .routes.reviews import reviews_bp
    
    # Register Blueprints
    app.register_blueprint(businesses_bp)
    app.register_blueprint(reviews_bp)
    
    return app