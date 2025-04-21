from flask import jsonify

def error_response(message, status_code):
    """Return a JSON error response."""
    response = jsonify({"Error": message})
    response.status_code = status_code
    return response