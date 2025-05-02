from flask import Blueprint, request, jsonify
from bson import ObjectId
from config.database import get_db
from werkzeug.security import check_password_hash
from models.users import UserSchema  # Your schema file
import bcrypt

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/api/register', methods=['POST'])
def register_user():
    db = get_db()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    try:
        user_data = request.get_json()
        user = UserSchema(**user_data)
    except Exception as e:
        return jsonify({"error": f"Invalid data: {e}"}), 400

    # Check if user with the same staff_id already exists
    if db.users.find_one({"staff_id": user.staff_id}):
        return jsonify({"error": "User with this staff ID already exists"}), 409

    try:
        user_dict = user.dict()
        # No hashing — save raw password as-is (⚠️ not safe for production)
        result = db.users.insert_one(user_dict)

        return jsonify({
            "message": "User registered successfully",
            "user_id": str(result.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({"error": f"Failed to register user: {e}"}), 500


@user_bp.route('/api/login', methods=['POST'])
def login_user():
    db = get_db()

    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    try:
        login_data = request.get_json()
        staff_id = login_data['staff_id']
        password = login_data['password']
    except KeyError:
        return jsonify({"error": "Missing staff_id or password"}), 400

    try:
        user_data = db.users.find_one({"staff_id": staff_id})
        if user_data:
            stored_password = user_data['password']  # plain text password stored

            if stored_password == password:
                return jsonify({"message": "Login successful"}), 200
            else:
                return jsonify({"error": "Invalid password"}), 401
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": f"Error during login: {e}"}), 500
