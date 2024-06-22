from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db
from routes import auth
from config import Config
import argparse
from pyngrok import ngrok, conf
import os
import sys
def create_app():
    # conf.get_default().auth_token = "2hjx1FsNHqaSsPeEdjvGH4fuPhT_5nvEUth2Zrk3Uon7RFycf"
    # os.environ["FLASK_ENV"] = "development"
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)
    CORS(app, resources={r"/api/*": {"origins": ["*"]}})  # Enable CORS for all routes

    app.register_blueprint(auth, url_prefix='/api')

    # public_url = ngrok.connect(7860).public_url
    # print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}/\"".format(public_url, 7860))
    
    # app.config["BASE_URL"] = public_url


    @app.route('/')
    def serve_index():
        return send_from_directory('static', 'index.html')

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':    
    app = create_app()
    
    with open('test.txt', 'w') as f:
        print(os.getpid(), file=f)
    app.run(debug=True, port=int(sys.argv[1]))
