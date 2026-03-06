from flask import Blueprint, request, jsonify
from models import db, Nightdress
import os
from werkzeug.utils import secure_filename

nightdress_bp = Blueprint("nightdress_bp", __name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "../uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@nightdress_bp.route("/nightdress", methods=["GET"])
def get_nightdress():
    items = Nightdress.query.all()
    return jsonify([{
        "id": i.id,
        "name": i.name,
        "price": i.price,
        "description": i.description,
        "image": i.image,
        "quantity": i.quantity
    } for i in items]), 200

@nightdress_bp.route("/nightdress", methods=["POST"])
def add_nightdress():
    name = request.form["name"]
    price = request.form["price"]
    description = request.form["description"]
    quantity = request.form.get("quantity", 1)

    file = request.files.get("image")
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        image_url = f"/uploads/{filename}"
    else:
        image_url = ""

    new_item = Nightdress(name=name, price=price, description=description, quantity=quantity, image=image_url)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Nightdress added"}), 201

@nightdress_bp.route("/nightdress/<int:id>", methods=["PATCH"])
def update_nightdress(id):
    item = Nightdress.query.get_or_404(id)
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
    return jsonify({"message": "Nightdress updated"}), 200

@nightdress_bp.route("/nightdress/<int:id>", methods=["DELETE"])
def delete_nightdress(id):
    item = Nightdress.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Nightdress deleted"}), 200