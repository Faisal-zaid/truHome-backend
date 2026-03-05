from flask import Blueprint, jsonify
from models import db, Pajamas, Nightdress, Rompers, Bathrobes

purchase_bp = Blueprint("purchase_bp", __name__)

@purchase_bp.route("/purchase/<category>/<int:id>", methods=["POST"])
def purchase_item(category, id):
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
    if item.quantity > 0:
        item.quantity -= 1
        db.session.commit()
        return jsonify({"message": "Purchased successfully"}), 200
    else:
        return jsonify({"message": "Out of stock"}), 400