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

def current_user():
    user_id = session.get("user_id")

    if not user_id:
        return None

    return db.session.get(User, user_id)

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
    user = current_user()

    if not user:
        return jsonify({
            "errors": ["Unauthorized."]
        }), 401

    return jsonify(user.to_dict()), 200

@app.delete("/logout")
def logout():
    session.pop("user_id", None)
    return "", 204

@app.get("/tasks")
def get_tasks():
    user = current_user()

    if not user:
        return jsonify({
            "errors": ["Unauthorized."]
        }), 401

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    pagination = Task.query.filter_by(user_id=user.id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "tasks": [task.to_dict() for task in pagination.items],
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages
    }), 200

@app.post("/tasks")
def create_task():
    user = current_user()

    if not user:
        return jsonify({
            "errors": ["Unauthorized."]
        }), 401

    data = request.get_json()

    if not data:
        return jsonify({
            "errors": ["No input data provided."]
        }), 400

    try:
        task = Task(
            title=data.get("title"),
            description=data.get("description"),
            due_date=data.get("due_date"),
            completed=data.get("completed", False),
            user_id=user.id
        )

        db.session.add(task)
        db.session.commit()

        return jsonify(task.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "errors": [str(e)]
        }), 400

@app.patch("/tasks/<int:id>")
def update_task(id):
    user = current_user()

    if not user:
        return jsonify({
            "errors": ["Unauthorized."]
        }), 401

    task = Task.query.filter_by(id=id, user_id=user.id).first()

    if not task:
        return jsonify({
            "errors": ["Task not found."]
        }), 404

    data = request.get_json()

    try:
        if "title" in data:
            task.title = data["title"]

        if "description" in data:
            task.description = data["description"]

        if "due_date" in data:
            task.due_date = data["due_date"]

        if "completed" in data:
            task.completed = data["completed"]

        db.session.commit()

        return jsonify(task.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "errors": [str(e)]
        }), 400
    
@app.delete("/tasks/<int:id>")
def delete_task(id):
    user = current_user()

    if not user:
        return jsonify({
            "errors": ["Unauthorized."]
        }), 401

    task = Task.query.filter_by(id=id, user_id=user.id).first()

    if not task:
        return jsonify({
            "errors": ["Task not found."]
        }), 404

    db.session.delete(task)
    db.session.commit()

    return "", 204



if __name__ == "__main__":
    app.run(port=5555, debug=True)
