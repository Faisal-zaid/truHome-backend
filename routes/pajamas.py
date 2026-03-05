from flask import Blueprint, request, jsonify
from models import db, Pajamas

pajamas_bp=Blueprint("pajamas_bp", __name__)

#GET ALL
@pajamas_bp.route("/pajamas", methods=["GET"])
def get_pajamas():
    items=Pajamas.query.all()
    result=[]

    for item in items:
        result.append({
            "id":item.id,
            "name":item.name,
            "price":item.price,
            "description":item.description,
            "image":item.image
        })

    return jsonify(result), 200

# POST
@pajamas_bp.route("/pajamas", methods=["POST"])
def add_pajamas():
    data = request.get_json()

    new_item = Pajamas(
        name=data["name"],
        price=data["price"],
        description=data["description"],
        image=data["image"]
    )

    db.session.add(new_item)
    db.session.commit()

    return jsonify({"message": "Pajama added"}), 201


# PATCH
@pajamas_bp.route("/pajamas/<int:id>", methods=["PATCH"])
def update_pajamas(id):
    item = Pajamas.query.get_or_404(id)
    data = request.get_json()

    item.name = data.get("name", item.name)
    item.price = data.get("price", item.price)
    item.description = data.get("description", item.description)
    item.image = data.get("image", item.image)

    db.session.commit()

    return jsonify({"message": "Pajama updated"}), 200


# DELETE
@pajamas_bp.route("/pajamas/<int:id>", methods=["DELETE"])
def delete_pajamas(id):
    item = Pajamas.query.get_or_404(id)

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Pajama deleted"}), 200    