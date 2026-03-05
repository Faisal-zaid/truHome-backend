from flask import Blueprint, request, jsonify
from models import db, Rompers

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
            "image": item.image
        })

    return jsonify(result), 200


# POST
@rompers_bp.route("/rompers", methods=["POST"])
def add_rompers():
    data = request.get_json()

    new_item = Rompers(
        name=data["name"],
        price=data["price"],
        description=data["description"],
        image=data["image"]
    )

    db.session.add(new_item)
    db.session.commit()

    return jsonify({"message": "Romper added"}), 201


# PATCH
@rompers_bp.route("/rompers/<int:id>", methods=["PATCH"])
def update_rompers(id):
    item = Rompers.query.get_or_404(id)
    data = request.get_json()

    item.name = data.get("name", item.name)
    item.price = data.get("price", item.price)
    item.description = data.get("description", item.description)
    item.image = data.get("image", item.image)

    db.session.commit()

    return jsonify({"message": "Romper updated"}), 200


# DELETE
@rompers_bp.route("/rompers/<int:id>", methods=["DELETE"])
def delete_rompers(id):
    item = Rompers.query.get_or_404(id)

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Romper deleted"}), 200