from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from models import db
from dotenv import load_dotenv
import os

#import routes
from routes.admin import admin_bp
from routes.bathrobes import bathrobes_bp
from routes.pajamas import pajamas_bp
from routes.rompers import rompers_bp
from routes.nightdress import nightdress_bp
from routes.purchase import purchase_bp
from routes.mpesa_callback import mpesa_bp

load_dotenv()

app=Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

#database config

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///TruHome.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

#initialize extensions
db.init_app(app)
Migrate(app,db)


#register blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(pajamas_bp)
app.register_blueprint(nightdress_bp)
app.register_blueprint(rompers_bp)
app.register_blueprint(bathrobes_bp)
app.register_blueprint(purchase_bp)
app.register_blueprint(mpesa_bp)


# ⭐ CREATE DATABASE TABLES
with app.app_context():
    db.create_all()


if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)
