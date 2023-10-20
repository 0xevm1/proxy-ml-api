from flask import jsonify

def not_found_error(e):
    return jsonify({"error": "Not Found"}), 404

def internal_server_error(e):
    return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

def bad_request_error(e):
    return jsonify({"error": "Bad Request", "message": str(e)}), 400
