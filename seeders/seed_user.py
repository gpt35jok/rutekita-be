from app import app
from extensions import db
from models.user import User
from werkzeug.security import generate_password_hash

def run_seed():
    with app.app_context():
        # cek admin
        admin_exist = User.query.filter_by(username="admin").first()
        if not admin_exist:
            admin = User(
                username="admin",
                password=generate_password_hash("admin123"),
                role="admin"
            )
            db.session.add(admin)
            print("Admin dibuat")

        # cek petugas
        petugas_exist = User.query.filter_by(username="petugas").first()
        if not petugas_exist:
            petugas = User(
                username="petugas",
                password=generate_password_hash("petugas123"),
                role="petugas"
            )
            db.session.add(petugas)
            print("Petugas dibuat")

        db.session.commit()
        print("Seeder selesai!")

if __name__ == "__main__":
    run_seed()
