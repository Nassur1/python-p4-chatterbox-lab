from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)

# ----------------- ROUTES -----------------

# GET all messages
@app.route("/messages", methods=["GET"])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([{
        "id": msg.id,
        "body": msg.body,
        "username": msg.username,
        "created_at": msg.created_at,
        "updated_at": msg.updated_at
    } for msg in messages])

# GET a single message by ID
@app.route("/messages/<int:id>", methods=["GET"])
def get_message(id):
    msg = Message.query.get_or_404(id)
    return jsonify({
        "id": msg.id,
        "body": msg.body,
        "username": msg.username,
        "created_at": msg.created_at,
        "updated_at": msg.updated_at
    })

# POST a new message
@app.route("/messages", methods=["POST"])
def create_message():
    data = request.get_json()
    new_msg = Message(body=data["body"], username=data["username"])
    db.session.add(new_msg)
    db.session.commit()
    return jsonify({
        "id": new_msg.id,
        "body": new_msg.body,
        "username": new_msg.username,
        "created_at": new_msg.created_at,
        "updated_at": new_msg.updated_at
    })

# PATCH update a message
@app.route("/messages/<int:id>", methods=["PATCH"])
def update_message(id):
    data = request.get_json()
    msg = Message.query.get_or_404(id)
    msg.body = data.get("body", msg.body)
    db.session.commit()
    return jsonify({
        "id": msg.id,
        "body": msg.body,
        "username": msg.username,
        "created_at": msg.created_at,
        "updated_at": msg.updated_at
    })

# DELETE a message
@app.route("/messages/<int:id>", methods=["DELETE"])
def delete_message(id):
    msg = Message.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    return jsonify({"message": f"Message {id} deleted"})

# ----------------- RUN -----------------
if __name__ == "__main__":
    app.run(port=5555, debug=True)

