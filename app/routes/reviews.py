from flask import Blueprint, request, jsonify
from app.models.datastore_client import client
from app.utils.errors import error_response

reviews_bp = Blueprint('reviews', __name__)

# Create a Review
@reviews_bp.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()

    required_fields = ["user_id", "business_id", "stars"]

    # Check for missing fields
    if not data or not all(field in data for field in required_fields):
        return error_response(
            "The request body is missing at least one of the required attributes",
            400
        )

    user_id = data["user_id"]
    business_id = data["business_id"]

    # Check if the business exists
    business_key = client.key('Businesses', business_id)
    business = client.get(business_key)
    if not business:
        return error_response(
            "No business with this business_id exists",
            404
        )

    # Check if user already reviewed this business
    query = client.query(kind='Reviews')
    query.add_filter('user_id', '=', user_id)
    query.add_filter('business_id', '=', business_id)
    existing_reviews = list(query.fetch())

    if existing_reviews:
        return error_response(
            "You have already submitted a review for this business. You can update your previous review, or delete it and submit a new review",
            409
        )

    # Create new review entity
    key = client.key('Reviews')
    new_review = client.entity(key=key)
    new_review.update({
        "user_id": user_id,
        "business_id": business_id,
        "stars": data["stars"],
        "review_text": data.get("review_text", "")
    })

    client.put(new_review)

    new_review["id"] = new_review.key.id

    return jsonify(new_review), 201

# Get a Review by ID
@reviews_bp.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    key = client.key('Reviews', review_id)
    review = client.get(key)

    if not review:
        return error_response(
            "No review with this review_id exists",
            404
        )

    review["id"] = review_id

    return jsonify(review), 200

# Edit a Review by ID
@reviews_bp.route('/reviews/<int:review_id>', methods=['PUT'])
def edit_review(review_id):
    data = request.get_json()

    # Check if stars is missing
    if not data or "stars" not in data:
        return error_response(
            "The request body is missing at least one of the required attributes",
            400
        )

    key = client.key('Reviews', review_id)
    review = client.get(key)

    # If the review does not exist
    if not review:
        return error_response(
            "No review with this review_id exists",
            404
        )

    # Update fields
    review["stars"] = data["stars"]

    # Only update review_text if it's provided
    if "review_text" in data:
        review["review_text"] = data["review_text"]

    client.put(review)

    review["id"] = review_id

    return jsonify(review), 200

# Delete a Review by ID
@reviews_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    key = client.key('Reviews', review_id)
    review = client.get(key)

    # If the review does not exist
    if not review:
        return error_response(
            "No review with this review_id exists",
            404
        )

    client.delete(key)

    return ('', 204)

# List all Reviews for a User
@reviews_bp.route('/users/<int:user_id>/reviews', methods=['GET'])
def list_reviews_for_user(user_id):
    # Query reviews by user_id
    query = client.query(kind='Reviews')
    query.add_filter('user_id', '=', user_id)
    results = list(query.fetch())

    reviews = []
    for review in results:
        review_data = {
            "id": review.key.id,
            "user_id": review["user_id"],
            "business_id": review["business_id"],
            "stars": review["stars"],
            "review_text": review.get("review_text", "")
        }
        reviews.append(review_data)

    return jsonify(reviews), 200
