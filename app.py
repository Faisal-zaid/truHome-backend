from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from models import db
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager
from extensions import mail



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

# ── absolute path so SQLite can always find / create the file ──
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)

app = Flask(__name__, static_folder="static")

CORS(
    app,
    origins=["https://tru-home-apparels.vercel.app"],  # your frontend URL
    supports_credentials=True,
    methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)

mail.init_app(app)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587

app.config["MAIL_USE_TLS"] = True

app.config["MAIL_USERNAME"] = os.getenv("EMAIL_USER")

app.config["MAIL_PASSWORD"] = os.getenv("EMAIL_PASSWORD")

mail.init_app(app)

# ── database config ──
# PostgreSQL (production) — uncomment and set DATABASE_URL in .env to switch
# database_url = os.getenv("DATABASE_URL")
# if database_url and database_url.startswith("postgres://"):
#     database_url = database_url.replace("postgres://", "postgresql://", 1)
# app.config["SQLALCHEMY_DATABASE_URI"] = database_url

# SQLite (local dev)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(INSTANCE_DIR, 'TruHome.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)

# ── initialize extensions ──
db.init_app(app)
Migrate(app, db)

# ── register blueprints ──
app.register_blueprint(admin_bp)
#app.register_blueprint(pajamas_bp)
#app.register_blueprint(nightdress_bp)
#app.register_blueprint(rompers_bp)
#app.register_blueprint(bathrobes_bp)
app.register_blueprint(purchase_bp)
app.register_blueprint(mpesa_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(products_bp)

# ── create database tables ──
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


# ── PostgreSQL connection string (for production / .env) ──
# DATABASE_URL=postgresql://truhome_user:Fa0711498001@localhost/truhome