import os
import re
from flask import Blueprint, request, jsonify
from models import db, Admin
#from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_access_token, jwt_required

admin_bp = Blueprint("admin_bp", __name__)

PASSKEY = os.getenv("ADMIN_PASSKEY")


# PASSWORD VALIDATION
def valid_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{6,}$"
    return re.match(pattern, password)


# ADMIN REGISTER
@admin_bp.route("/admin/register", methods=["POST"])
def register():

    data = request.get_json()

    first = data.get("firstName")
    last = data.get("lastName")
    email = data.get("email")
    password = data.get("password")
    confirm = data.get("confirmPassword")

    if password != confirm:
        return jsonify({"message": "Passwords do not match"}), 400

    if not valid_password(password):
        return jsonify({"message": "Weak password"}), 400

    if Admin.query.filter(Admin.email.ilike(email)).first():
        return jsonify({"message": "Email already exists"}), 400

    admin = Admin(
        first_name=first,
        last_name=last,
        email=email
    )

    admin.set_password(password)

    db.session.add(admin)
    db.session.commit()

    return jsonify({"message": "Admin registered. Waiting approval"}), 201


# LOGIN
@admin_bp.route("/admin/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    passkey = data.get("passkey")

    admin = Admin.query.filter_by(email=email).first()

    if not admin:
        return jsonify({"message": "Admin not found"}), 404

    if not admin.check_password(password):
        return jsonify({"message": "Wrong password"}), 401

    if passkey != PASSKEY:
        return jsonify({"message": "Invalid passkey"}), 403

    if not admin.is_approved:
        return jsonify({"message": "Admin not approved yet"}), 403

    token = create_access_token(identity=admin.email)

    return jsonify({
        "token": token,
        "admin": admin.email
    }), 200


# LIST PENDING ADMINS
@admin_bp.route("/admin/pending", methods=["GET"])
@jwt_required()
def pending_admins():

    admins = Admin.query.filter_by(is_approved=False).all()

    return jsonify([
        {
            "id": a.id,
            "name": f"{a.first_name} {a.last_name}",
            "email": a.email
        }
        for a in admins
    ])


# APPROVE ADMIN
@admin_bp.route("/admin/approve/<int:id>", methods=["PATCH"])
@jwt_required()
def approve_admin(id):

    admin = Admin.query.get(id)

    if not admin:
        return jsonify({"message": "Admin not found"}), 404

    admin.is_approved = True

    db.session.commit()

    return jsonify({"message": "Admin approved"})