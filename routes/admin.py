from flask import Blueprint, request, jsonify
from models import db, Admin

admin_bp = Blueprint("admin_bp", __name__)

# REGISTER
@admin_bp.route("/admin/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    if Admin.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400

    new_admin = Admin(username=username)
    new_admin.set_password(password)

    db.session.add(new_admin)
    db.session.commit()

    return jsonify({"message": "Admin registered successfully"}), 201


# LOGIN
@admin_bp.route("/admin/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    admin = Admin.query.filter_by(username=username).first()

    if admin and admin.check_password(password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401