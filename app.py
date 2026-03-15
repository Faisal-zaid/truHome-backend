from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from models import db
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager

import cloudinary
import cloudinary.uploader

#import routes
from routes.admin import admin_bp
#from routes.bathrobes import bathrobes_bp
#from routes.pajamas import pajamas_bp
#from routes.rompers import rompers_bp
#from routes.nightdress import nightdress_bp
from routes.purchase import purchase_bp
from routes.mpesa_callback import mpesa_bp
from routes.categories import categories_bp
from routes.products import products_bp

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

app = Flask(__name__, static_folder="static")

CORS(app, origins=["https://tru-home-apparels.vercel.app"], supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "https://tru-home-apparels.vercel.app")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS")
    return response

#CORS(
 #   app,
  #  resources={r"/*": {"origins": "*"}},
  #  allow_headers=["Content-Type", "Authorization"],
  #  methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"]
#)
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
#app.register_blueprint(pajamas_bp)
#app.register_blueprint(nightdress_bp)
#app.register_blueprint(rompers_bp)
#app.register_blueprint(bathrobes_bp)
app.register_blueprint(purchase_bp)
app.register_blueprint(mpesa_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(products_bp)


# ⭐ CREATE DATABASE TABLES
#with app.app_context():
   # db.create_all()


if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)



#ignore this 
#DATABASE_URL=postgresql://truhome_user:Fa0711498001@localhost/truhome