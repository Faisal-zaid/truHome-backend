from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db=SQLAlchemy()

#ADMIN
class Admin(db.Model):
    __tablename__="admins"

    id=db.Column(db.Integer, primary_key=True)
    userName=db.Column(db.Text, unique=True, nullable =False)
    password=db.Column(db.Text, unique=True, nullable=False)

      # Set password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Check password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#products
class Pajamas(db.Model):
    __tablename__="pajamas"   

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)
    image = db.Column(db.String(500), nullable=False)


class Nightdress(db.Model):
    __tablename__ = "nightdress"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)
    image = db.Column(db.String(500), nullable=False)


class Rompers(db.Model):
    __tablename__ = "rompers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)
    image = db.Column(db.String(500), nullable=False)


class Bathrobes(db.Model):
    __tablename__ = "bathrobes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)
    image = db.Column(db.String(500), nullable=False) 