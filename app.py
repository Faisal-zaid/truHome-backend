from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from models import db

#import routes
from routes.admin import admin_bp
from routes.bathrobes import bathrobes_bp
from routes.pajamas import pajamas_bp
from routes.rompers import rompers_bp
from routes.nightdress import nightdress_bp

app=Flask(__name__)

#database config

app.config["SQL_DATABASE_URI"]="sqllite:///TruHome.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

#initialize extensions
db.init_app(app)
Migrate(app,db)
CORS(app)

#register blueprints
app.register_blueprints(admin_bp)
app.register_blueprints(pajamas_bp)
app.register_blueprints(nightdress_bp)
app.register_blueprints(rompers_bp)
app.register_blueprints(bathrobes_bp)

if __name__=="__main__":
    app.run(debug=True)
