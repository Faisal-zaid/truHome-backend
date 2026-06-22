from flask import Blueprint, request
from models import db, Product, PendingPurchase
from services.email_service import send_purchase_email

mpesa_bp = Blueprint("mpesa_bp", __name__)

@mpesa_bp.route("/mpesa/callback", methods=["POST"])
def mpesa_callback():

    data = request.json
    print(data)

    body = data["Body"]["stkCallback"]

    result_code = body["ResultCode"]

    checkout_id = body["CheckoutRequestID"]

    purchase = PendingPurchase.query.filter_by(
        checkout_request_id=checkout_id
    ).first()

    if purchase and result_code == 0:

        purchase.is_paid = True

        product = Product.query.get(
            purchase.product_id
        )

        product.quantity -= purchase.quantity

        db.session.commit()

        send_purchase_email(
            purchase.email,
            product
        )

    return {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }