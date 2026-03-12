from flask import Blueprint, request, jsonify
from models import db, Nightdress
from flask_jwt_extended import jwt_required

nightdress_bp = Blueprint("nightdress_bp", __name__)

# GET ALL
@nightdress_bp.route("/nightdress", methods=["GET"])
def get_nightdress():
    items = Nightdress.query.all()
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
@nightdress_bp.route("/nightdress", methods=["POST"])
@jwt_required()
def add_nightdress():
    data = request.get_json()
    new_item = Nightdress(
        name=data["name"],
        price=data["price"],
        description=data["description"],
        image=data.get("image", ""),
        quantity=data.get("quantity", 0)
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Nightdress added"}), 201

# PATCH
@nightdress_bp.route("/nightdress/<int:id>", methods=["PATCH"])
@jwt_required()
def update_nightdress(id):
    item = Nightdress.query.get_or_404(id)
    data = request.get_json()
    item.name = data.get("name", item.name)
    item.price = data.get("price", item.price)
    item.description = data.get("description", item.description)
    item.image = data.get("image", item.image)
    item.quantity = data.get("quantity", item.quantity)
    db.session.commit()
    return jsonify({"message": "Nightdress updated"}), 200

# DELETE
@nightdress_bp.route("/nightdress/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_nightdress(id):
    item = Nightdress.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Nightdress deleted"}), 200