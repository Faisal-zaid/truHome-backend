from flask import Blueprint, request, jsonify
from models import db, Pajamas, Nightdress, Rompers, Bathrobes
from services.mpesa import stk_push

purchase_bp = Blueprint("purchase_bp", __name__)

@purchase_bp.route("/purchase/<category>/<int:id>", methods=["POST"])
def purchase_item(category, id):

    data = request.get_json()
    phone = data.get("phone")

    model_map = {
        "pajamas": Pajamas,
        "nightdress": Nightdress,
        "rompers": Rompers,
        "bathrobes": Bathrobes,
    }

    Model = model_map.get(category)

    if not Model:
        return jsonify({"message": "Invalid category"}), 400

    item = Model.query.get_or_404(id)

    if item.quantity <= 0:
        return jsonify({"message": "Out of stock"}), 400

    # Trigger M-Pesa payment
    response = stk_push(phone, item.price)

    return jsonify({
        "message": "M-Pesa prompt sent",
        "mpesa_response": response
    }), 200