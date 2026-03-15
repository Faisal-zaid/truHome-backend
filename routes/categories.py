from flask import Blueprint, request, jsonify
from models import db, Category
from flask_jwt_extended import jwt_required
from flask_cors import CORS

categories_bp = Blueprint("categories_bp", __name__)




@categories_bp.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()

    return jsonify([
        {"id": c.id, "name": c.name}
        for c in categories
    ])


@categories_bp.route("/categories", methods=["POST"])
@jwt_required()
def create_category():

    data = request.get_json()

    category = Category(name=data["name"])

    db.session.add(category)
    db.session.commit()

    return jsonify({"message": "Category created"})