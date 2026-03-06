from flask import Blueprint, request, jsonify
from models import db, Bathrobes
import os
from werkzeug.utils import secure_filename

bathrobes_bp = Blueprint("bathrobes_bp", __name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "../uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@bathrobes_bp.route("/bathrobes", methods=["GET"])
def get_bathrobes():
    items = Bathrobes.query.all()
    return jsonify([{
        "id": i.id,
        "name": i.name,
        "price": i.price,
        "description": i.description,
        "image": i.image,
        "quantity": i.quantity
    } for i in items]), 200

@bathrobes_bp.route("/bathrobes", methods=["POST"])
def add_bathrobes():
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

    new_item = Bathrobes(name=name, price=price, description=description, quantity=quantity, image=image_url)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Bathrobes added"}), 201

@bathrobes_bp.route("/bathrobes/<int:id>", methods=["PATCH"])
def update_bathrobes(id):
    item = Bathrobes.query.get_or_404(id)
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
    return jsonify({"message": "Bathrobes updated"}), 200

@bathrobes_bp.route("/bathrobes/<int:id>", methods=["DELETE"])
def delete_bathrobes(id):
    item = Bathrobes.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Bathrobes deleted"}), 200