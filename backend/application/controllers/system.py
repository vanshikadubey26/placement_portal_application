from flask import Blueprint, jsonify

system_bp = Blueprint('system', __name__)

@system_bp.route('/api/system/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200