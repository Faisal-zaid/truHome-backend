from flask import Blueprint, request, jsonify
from models import db, Product, Category
from services.mpesa import stk_push

purchase_bp = Blueprint("purchase_bp", __name__)

@purchase_bp.route("/purchase/<category_name>/<int:id>", methods=["POST"])
def purchase_item(category_name, id):
    data = request.get_json()
    phone = data.get("phone")

    if not phone:
        return jsonify({"message": "Phone number is required"}), 400

    # Find the category first
    category = Category.query.filter_by(name=category_name).first()
    if not category:
        return jsonify({"message": "Invalid category"}), 400

    # Find the product in that category
    item = Product.query.filter_by(id=id, category_id=category.id).first()
    if not item:
        return jsonify({"message": "Product not found"}), 404

    if item.quantity <= 0:
        return jsonify({"message": "Out of stock"}), 400

    try:
        # Trigger M-Pesa payment
        response = stk_push(phone, item.price)

        # Subtract quantity after successful payment
        item.quantity -= 1
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "Payment failed", "error": str(e)}), 500

    return jsonify({
        "message": "M-Pesa prompt sent",
        "mpesa_response": response
    }), 200