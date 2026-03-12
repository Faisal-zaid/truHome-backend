from flask import Blueprint, request, jsonify
from models import db, Bathrobes
from flask_jwt_extended import jwt_required

bathrobes_bp = Blueprint("bathrobes_bp", __name__)

# GET ALL
@bathrobes_bp.route("/bathrobes", methods=["GET"])
def get_bathrobes():
    items = Bathrobes.query.all()
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
@bathrobes_bp.route("/bathrobes", methods=["POST"])
@jwt_required()
def add_bathrobes():
    data = request.get_json()
    new_item = Bathrobes(
        name=data["name"],
        price=data["price"],
        description=data["description"],
        image=data.get("image", ""),
        quantity=data.get("quantity", 0)
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Bathrobes added"}), 201

# PATCH
@bathrobes_bp.route("/bathrobes/<int:id>", methods=["PATCH"])
@jwt_required()
def update_bathrobes(id):
    item = Bathrobes.query.get_or_404(id)
    data = request.get_json()
    item.name = data.get("name", item.name)
    item.price = data.get("price", item.price)
    item.description = data.get("description", item.description)
    item.image = data.get("image", item.image)
    item.quantity = data.get("quantity", item.quantity)
    db.session.commit()
    return jsonify({"message": "Bathrobes updated"}), 200

# DELETE
@bathrobes_bp.route("/bathrobes/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_bathrobes(id):
    item = Bathrobes.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Bathrobes deleted"}), 200