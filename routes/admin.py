from flask import Blueprint, request,jsonify
from models import db,Admin

admin_bp=Blueprint("admin_bp,__naame__")

@admin_bp.route("/admin/login",methods=["POST"])
def login():
    data=request.get_json()

    username=data.get("username")
    password=data.get("password")

    admin=Admin.query.filterby(username=username, password=password).first()

    if admin:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
    
