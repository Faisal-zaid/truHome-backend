from flask import Blueprint, request

mpesa_bp = Blueprint("mpesa_bp", __name__)

@mpesa_bp.route("/mpesa/callback", methods=["POST"])
def mpesa_callback():
    data = request.json
    print(data)

    # here you confirm payment success
    # then reduce stock

    return {"ResultCode": 0, "ResultDesc": "Accepted"}