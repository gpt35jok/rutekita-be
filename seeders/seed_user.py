import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app import app
from extensions import db
from models.user import User
from utils.password import hash_password

def run_seed():
    with app.app_context():
        # cek admin
        admin_exist = User.query.filter_by(username="admin").first()
        if not admin_exist:
            admin = User(
                username="admin",
                email="admin@mail.com",
                password=hash_password("admin123"),
                role="admin"
            )
            db.session.add(admin)
            print("Admin dibuat")

        # cek petugas
        petugas_exist = User.query.filter_by(username="petugas").first()
        if not petugas_exist:
            petugas = User(
                username="petugas",
                email="petugas@mail.com",
                password=hash_password("petugas123"),
                role="petugas"
            )
            db.session.add(petugas)
            print("Petugas dibuat")

        db.session.commit()
        print("Seeder selesai!")

if __name__ == "__main__":
    run_seed()
