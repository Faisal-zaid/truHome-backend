from flask import Blueprint, request, jsonify
from models import db, Nightdress

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
            "image": item.image
        })

    return jsonify(result), 200


# POST
@nightdress_bp.route("/nightdress", methods=["POST"])
def add_nightdress():
    data = request.get_json()

    new_item = Nightdress(
        name=data["name"],
        price=data["price"],
        description=data["description"],
        image=data["image"]
    )

    db.session.add(new_item)
    db.session.commit()

    return jsonify({"message": "Nightdress added"}), 201


# PATCH
@nightdress_bp.route("/nightdress/<int:id>", methods=["PATCH"])
def update_nightdress(id):
    item = Nightdress.query.get_or_404(id)
    data = request.get_json()

    item.name = data.get("name", item.name)
    item.price = data.get("price", item.price)
    item.description = data.get("description", item.description)
    item.image = data.get("image", item.image)

    db.session.commit()

    return jsonify({"message": "Nightdress updated"}), 200


# DELETE
@nightdress_bp.route("/nightdress/<int:id>", methods=["DELETE"])
def delete_nightdress(id):
    item = Nightdress.query.get_or_404(id)

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Nightdress deleted"}), 200