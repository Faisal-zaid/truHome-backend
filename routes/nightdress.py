import os
from flask import Blueprint, request, jsonify, current_app
from models import db, Nightdress
from flask_jwt_extended import jwt_required
import cloudinary

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

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

# UPLOAD IMAGE
@nightdress_bp.route("/nightdress/upload", methods=["POST"])
@jwt_required()
def upload_nightdress_image():
    if "image" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        result = cloudinary.uploader.upload(file)
        image_url = result.get("secure_url")
        return jsonify({"image_path": image_url}), 201

    return jsonify({"message": "Invalid file type"}), 400

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