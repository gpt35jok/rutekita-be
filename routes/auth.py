from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from utils.password import verify_password, hash_password
from extensions import db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(email=data["email"]).first()
    print(user)
    print(verify_password(data["password"], user.password))
    if not user or not verify_password(data["password"], user.password):
        return jsonify({"msg": "Login gagal"}), 401

    token = create_access_token(
        identity={"id": user.id, "role": user.role}
    )

    return jsonify({
        "access_token": token, 
        "user": {
            "id": user.id,
            "name": user.username, # atau user.name sesuai kolom DB kamu
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "status": "active" # tambahkan field yang dibutuhkan React User type
        }
    })

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    # validasi input dasar
    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({
            "msg": "username, email, dan password wajib diisi"
        }), 400

    # cek username
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({
            "msg": "username sudah digunakan"
        }), 401

    # cek email
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({
            "msg": "email sudah digunakan"
        }), 401

    # buat user baru
    user = User(
        username=data["username"],
        email=data["email"],
        password=hash_password(data["password"]),
        role=data.get("role", "petugas")  # default role user
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "user": {
            "id": user.id,
            "name": user.username,
            "username": user.username,
            "role": user.role,
            "status": "active"
        }
    }), 201