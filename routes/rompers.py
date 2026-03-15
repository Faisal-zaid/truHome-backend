import os
from flask import Blueprint, request, jsonify, current_app
from models import db, Rompers
from flask_jwt_extended import jwt_required
import cloudinary

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

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

# UPLOAD IMAGE
@rompers_bp.route("/rompers/upload", methods=["POST"])
@jwt_required()
def upload_romper_image():
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