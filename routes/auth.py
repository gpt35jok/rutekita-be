from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from utils.password import verify_password

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(username=data["username"]).first()
    if not user or not verify_password(data["password"], user.password):
        return jsonify({"msg": "Login gagal"}), 401

    token = create_access_token(
        identity={"id": user.id, "role": user.role}
    )

    return jsonify(access_token=token)
