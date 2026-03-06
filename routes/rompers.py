from flask import Blueprint, request, jsonify
from models import db, Rompers
import os
from werkzeug.utils import secure_filename

rompers_bp = Blueprint("rompers_bp", __name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "../uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@rompers_bp.route("/rompers", methods=["GET"])
def get_rompers():
    items = Rompers.query.all()
    return jsonify([{
        "id": i.id,
        "name": i.name,
        "price": i.price,
        "description": i.description,
        "image": i.image,
        "quantity": i.quantity
    } for i in items]), 200

@rompers_bp.route("/rompers", methods=["POST"])
def add_rompers():
    name = request.form["name"]
    price = request.form["price"]
    description = request.form["description"]
    quantity = request.form.get("quantity", 1)

    file = request.files.get("image")
    image_url = ""
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        image_url = f"/uploads/{filename}"

    new_item = Rompers(name=name, price=price, description=description, quantity=quantity, image=image_url)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Rompers added"}), 201

@rompers_bp.route("/rompers/<int:id>", methods=["PATCH"])
def update_rompers(id):
    item = Rompers.query.get_or_404(id)
    item.name = request.form.get("name", item.name)
    item.price = request.form.get("price", item.price)
    item.description = request.form.get("description", item.description)
    item.quantity = request.form.get("quantity", item.quantity)

    file = request.files.get("image")
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        item.image = f"/uploads/{filename}"

    db.session.commit()
    return jsonify({"message": "Rompers updated"}), 200

@rompers_bp.route("/rompers/<int:id>", methods=["DELETE"])
def delete_rompers(id):
    item = Rompers.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Rompers deleted"}), 200