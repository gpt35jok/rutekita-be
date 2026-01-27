from flask import Flask
from extensions import db, jwt
from routes import auth, admin, routing

app = Flask(__name__)
app.config.from_object("config.Config")

db.init_app(app)
jwt.init_app(app)

app.register_blueprint(auth.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(routing.bp)

if __name__ == "__main__":
    app.run(debug=True)
