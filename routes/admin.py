from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from extensions import db
from utils.password import hash_password

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.route("/petugas", methods=["POST"])
@jwt_required()
def add_petugas():
    current = get_jwt_identity()

    if current["role"] != "admin":
        return jsonify({"msg": "Akses ditolak"}), 403

    data = request.json

    user = User(
        username=data["username"],
        password=hash_password(data["password"]),
        role="petugas"
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "Petugas berhasil ditambahkan"})

@bp.route("/users", methods=["GET"])
@jwt_required()
def get_all_users():
    current = get_jwt_identity()

    # hanya admin yang boleh akses
    if current["role"] != "admin":
        return jsonify({"msg": "Akses ditolak"}), 403

    users = User.query.all()

    result = []
    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "role": user.role
        })

    return jsonify({
        "msg": "Berhasil mengambil data user",
        "data": result
    }), 200
