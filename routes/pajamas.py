import os
from flask import Blueprint, request, jsonify, current_app
from models import db, Pajamas
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS



pajamas_bp = Blueprint("pajamas_bp", __name__)

# GET ALL
@pajamas_bp.route("/pajamas", methods=["GET"])
def get_pajamas():
    items = Pajamas.query.all()
    result = []

    for item in items:
        result.append({
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "description": item.description,
            "image": item.image,
            "quantity": item.quantity  # added
        })

    return jsonify(result), 200

# POST
@pajamas_bp.route("/pajamas", methods=["POST"])
@jwt_required()
def add_pajamas():
    data = request.get_json()

    new_item = Pajamas(
        name=data["name"],
        price=data["price"],
        description=data["description"],
        image=data["image"],
        quantity=data.get("quantity", 0)  # added
    )

    db.session.add(new_item)
    db.session.commit()

    return jsonify({"message": "Pajama added"}), 201

@pajamas_bp.route("/pajamas/upload", methods=["POST"])
@jwt_required()
def upload_pajama_image():
    if "image" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(current_app.root_path, "static", "images")
        os.makedirs(upload_folder, exist_ok=True)
        save_path = os.path.join(upload_folder, filename)
        file.save(save_path)

        image_url = f"{request.host_url}static/images/{filename}"
        return jsonify({"image_path": image_url}), 201
    return jsonify({"message": "Invalid file type"}), 400

# PATCH
@pajamas_bp.route("/pajamas/<int:id>", methods=["PATCH"])
@jwt_required()
def update_pajamas(id):
    item = Pajamas.query.get_or_404(id)
    data = request.get_json()

    item.name = data.get("name", item.name)
    item.price = data.get("price", item.price)
    item.description = data.get("description", item.description)
    item.image = data.get("image", item.image)
    item.quantity = data.get("quantity", item.quantity)  # added

    db.session.commit()

    return jsonify({"message": "Pajama updated"}), 200

# DELETE
@pajamas_bp.route("/pajamas/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_pajamas(id):
    item = Pajamas.query.get_or_404(id)

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Pajama deleted"}), 200