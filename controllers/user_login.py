from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from config.database import get_db

user_bp = Blueprint('user_bp', __name__)


