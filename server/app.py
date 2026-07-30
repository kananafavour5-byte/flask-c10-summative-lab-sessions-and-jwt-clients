from flask import Flask, request, jsonify, session
from flask_migrate import Migrate
from flask_session import Session

from config import Config
from models import db, bcrypt, User, Task


app = Flask(__name__)
app.config.from_object(Config)

# Session configuration
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False

Session(app)

db.init_app(app)
bcrypt.init_app(app)

migrate = Migrate(app, db)


@app.route("/")
def index():
    return {"message": "Task Manager API is running"}

@app.post("/signup")
def signup():
    data = request.get_json()

    if not data:
        return jsonify({
            "errors": ["No input data provided."]
        }), 400

    username = data.get("username")
    password = data.get("password")
    password_confirmation = data.get("password_confirmation")


    if password != password_confirmation:
        return jsonify({
            "errors": ["Passwords do not match."]
        }), 400

    if User.query.filter_by(username=username).first():
        return jsonify({
            "errors": ["Username already exists."]
        }), 400

    try:
        user = User(username=username)
        user.password = password

        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id

        return jsonify(user.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "errors": [str(e)]
        }), 400

@app.post("/login")
def login():
    data = request.get_json()

    if not data:
        return jsonify({
            "errors": ["No input data provided."]
        }), 400

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and user.authenticate(password):
        session["user_id"] = user.id
        return jsonify(user.to_dict()), 200

    return jsonify({
        "errors": ["Invalid username or password."]
    }), 401

@app.get("/check_session")
def check_session():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "errors": ["Unauthorized."]
        }), 401

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "errors": ["Unauthorized."]
        }), 401

    return jsonify(user.to_dict()), 200

@app.delete("/logout")
def logout():
    session.pop("user_id", None)
    return "", 204


if __name__ == "__main__":
    app.run(port=5555, debug=True)