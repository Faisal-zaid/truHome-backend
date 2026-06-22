from flask import Blueprint, request, jsonify
from models import db, Product, Category
from services.mpesa import stk_push

purchase_bp = Blueprint("purchase_bp", __name__)

@purchase_bp.route("/purchase/<category_name>/<int:id>", methods=["POST"])
def purchase_item(category_name, id):
    data = request.get_json()
    phone = data.get("phone")
    email = data.get("email")

    if not phone or not email:
        return jsonify({"message":"Phone and email required"}),400
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

@purchase_bp.route("/purchase/cart", methods=["POST"])
def purchase_cart():

    data = request.get_json()
    phone = data.get("phone")
    items = data.get("items")

    if not phone or not items:
        return jsonify({"message": "Missing data"}), 400

    total = 0

    for cart_item in items:
        product = Product.query.get(cart_item["id"])

        if not product or product.quantity < cart_item["quantity"]:
            return jsonify({"message": f"{product.name} out of stock"}), 400

        total += product.price * cart_item["quantity"]

    try:
        response = stk_push(phone, total)

        # reduce stock
        for cart_item in items:
            product = Product.query.get(cart_item["id"])
            product.quantity -= cart_item["quantity"]

        db.session.commit()

    except Exception as e:
        return jsonify({"message": "Payment failed"}), 500

    return jsonify({"message": "Payment sent", "total": total}), 200