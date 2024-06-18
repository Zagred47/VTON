from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db
from routes import auth
from config import Config
import argparse

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)
    CORS(app, resources={r"/api/*": {"origins": ["*"]}})  # Enable CORS for all routes

    app.register_blueprint(auth, url_prefix='/api')

    @app.route('/')
    def serve_index():
        return send_from_directory('static', 'index.html')

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':    
    app = create_app()
    app.run(debug=True)
