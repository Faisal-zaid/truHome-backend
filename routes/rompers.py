from flask import Blueprint, request, jsonify
from models import db, Rompers
from flask_jwt_extended import jwt_required

rompers_bp = Blueprint("rompers_bp", __name__)

# GET ALL
@rompers_bp.route("/rompers", methods=["GET"])
def get_rompers():
    items = Rompers.query.all()
    result = []
    for item in items:
        result.append({
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "description": item.description,
            "image": item.image,
            "quantity": item.quantity
        })
    return jsonify(result), 200

# POST
@rompers_bp.route("/rompers", methods=["POST"])
@jwt_required()
def add_rompers():
    data = request.get_json()
    new_item = Rompers(
        name=data["name"],
        price=data["price"],
        description=data["description"],
        image=data.get("image", ""),
        quantity=data.get("quantity", 0)
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Rompers added"}), 201

# PATCH
@rompers_bp.route("/rompers/<int:id>", methods=["PATCH"])
@jwt_required()
def update_rompers(id):
    item = Rompers.query.get_or_404(id)
    data = request.get_json()
    item.name = data.get("name", item.name)
    item.price = data.get("price", item.price)
    item.description = data.get("description", item.description)
    item.image = data.get("image", item.image)
    item.quantity = data.get("quantity", item.quantity)
    db.session.commit()
    return jsonify({"message": "Rompers updated"}), 200

# DELETE
@rompers_bp.route("/rompers/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_rompers(id):
    item = Rompers.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Rompers deleted"}), 200