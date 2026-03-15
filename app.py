from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from models import db
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager

#import routes
from routes.admin import admin_bp
from routes.bathrobes import bathrobes_bp
from routes.pajamas import pajamas_bp
from routes.rompers import rompers_bp
from routes.nightdress import nightdress_bp
from routes.purchase import purchase_bp
from routes.mpesa_callback import mpesa_bp

load_dotenv()

app = Flask(__name__, static_folder="static")

CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True,
    expose_headers=["Authorization"],
    allow_headers=["Content-Type", "Authorization"]
)
#CORS(app, origins=["http://localhost:5173"])

#database config
database_url = os.getenv("DATABASE_URL")

if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)

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
