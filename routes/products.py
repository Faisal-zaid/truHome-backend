from flask import Blueprint, request, jsonify
from models import db, Product, Category
from flask_jwt_extended import jwt_required
import cloudinary

products_bp = Blueprint("products_bp", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# GET PRODUCTS BY CATEGORY
@products_bp.route("/products/<category>", methods=["GET"])
def get_products(category):

    cat = Category.query.filter_by(name=category).first()

    if not cat:
        return jsonify([])

    products = Product.query.filter_by(category_id=cat.id).all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description,
            "image": p.image,
            "quantity": p.quantity
        }
        for p in products
    ])


# ADD PRODUCT
@products_bp.route("/products/<category>", methods=["POST"])
@jwt_required()
def add_product(category):

    cat = Category.query.filter_by(name=category).first()

    if not cat:
        return jsonify({"message": "Category not found"}), 404

    data = request.get_json()

    product = Product(
        name=data["name"],
        price=data["price"],
        description=data["description"],
        quantity=data.get("quantity", 0),
        image=data.get("image", ""),
        category_id=cat.id
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Product added"}), 201


# UPDATE PRODUCT
@products_bp.route("/products/<int:id>", methods=["PATCH"])
@jwt_required()
def update_product(id):

    product = Product.query.get_or_404(id)

    data = request.get_json()

    product.name = data.get("name", product.name)
    product.price = data.get("price", product.price)
    product.description = data.get("description", product.description)
    product.image = data.get("image", product.image)
    product.quantity = data.get("quantity", product.quantity)

    db.session.commit()

    return jsonify({"message": "Product updated"}), 200


# DELETE PRODUCT
@products_bp.route("/products/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_product(id):

    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted"}), 200


# IMAGE UPLOAD
@products_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload():

    if "image" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):

        result = cloudinary.uploader.upload(file)

        image_url = result.get("secure_url")

        return jsonify({
            "image_path": image_url
        }), 201

    return jsonify({"message": "Invalid file type"}), 400