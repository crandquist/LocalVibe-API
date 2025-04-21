from flask import Blueprint, request, jsonify
from app.models.datastore_client import client
from app.utils.errors import error_response
from google.cloud import datastore

businesses_bp = Blueprint('businesses', __name__)

# Create a new business
@businesses_bp.route('/businesses', methods=['POST'])
def create_business():
    data = request.get_json()
    
    required_fields = [
        'owner_id', 
        'name', 
        'street_address',
        'city', 
        'state',
        'zip_code'
        ]
    
    # Check for missing fields
    if not data or not all(field in data for field in required_fields):
        return error_response(
            "The request body is missing at least one of the required attributes",
            400
            )
        
    # Create new business entity in Datastore
    key = client.key('Businesses')
    new_business = datastore.Entity(key=key)
    new_business.update({
        'owner_id': data['owner_id'],
        'name': data['name'],
        'street_address': data['street_address'],
        'city': data['city'],
        'state': data['state'],
        'zip_code': data['zip_code']
    })
    
    # Save entity to Datastore
    client.put(new_business)
    
    # Add generated ID to the response
    new_business['id'] = new_business.key.id
    
    return jsonify(new_business), 201

# Get a business by ID
@businesses_bp.route('/businesses/<int:business_id>', methods=['GET'])
def get_business(business_id):
    print(f"Fetching business with ID: {business_id}")  # Add this line clearly
    key = client.key('Businesses', business_id)
    business = client.get(key)

    if not business:
        print("No business found.")  # Helpful debug line
        return error_response(
            "No business with this business_id exists",
            404
        )

    business['id'] = business_id
    return jsonify(business), 200

# List all businesses
@businesses_bp.route('/businesses', methods=['GET'])
def list_businesses():
    # Create a Datastore query for 'Businesses' kind
    query = client.query(kind='Businesses')
    results = list(query.fetch())
    
    # Attach the ID from the key to each business result
    businesses = []
    for business in results:
        business_data = {
            'id': business.key.id,
            'owner_id': business['owner_id'],
            'name': business['name'],
            'street_address': business['street_address'],
            'city': business['city'],
            'state': business['state'],
            'zip_code': business['zip_code']
        }
        businesses.append(business_data)
        
    return jsonify(businesses), 200

# Edit a Business by ID
@businesses_bp.route('/businesses/<int:business_id>', methods=['PUT'])
def edit_business(business_id):
    data = request.get_json()

    required_fields = ["owner_id", "name", "street_address", "city", "state", "zip_code"]

    # Check for missing fields
    if not data or not all(field in data for field in required_fields):
        return error_response(
            "The request body is missing at least one of the required attributes",
            400
        )

    # Fetch the existing business
    key = client.key('Businesses', business_id)
    business = client.get(key)

    if not business:
        return error_response(
            "No business with this business_id exists",
            404
        )

    # Update the business with new values
    business.update({
        "owner_id": data["owner_id"],
        "name": data["name"],
        "street_address": data["street_address"],
        "city": data["city"],
        "state": data["state"],
        "zip_code": data["zip_code"]
    })

    client.put(business)

    # Add the id to the response
    business["id"] = business_id

    return jsonify(business), 200

# Delete a Business by ID (and its associated reviews)
@businesses_bp.route('/businesses/<int:business_id>', methods=['DELETE'])
def delete_business(business_id):
    # Fetch the business entity
    key = client.key('Businesses', business_id)
    business = client.get(key)

    # If the business does not exist
    if not business:
        return error_response(
            "No business with this business_id exists",
            404
        )

    # First, delete all associated reviews
    query = client.query(kind='Reviews')
    query.add_filter('business_id', '=', business_id)
    reviews = list(query.fetch())

    for review in reviews:
        client.delete(review.key)

    # Now delete the business
    client.delete(key)

    return ('', 204)

# List all Businesses for an Owner
@businesses_bp.route('/owners/<int:owner_id>/businesses', methods=['GET'])
def list_businesses_for_owner(owner_id):
    # Query businesses by owner_id
    query = client.query(kind='Businesses')
    query.add_filter('owner_id', '=', owner_id)
    results = list(query.fetch())

    businesses = []
    for business in results:
        business_data = {
            "id": business.key.id,
            "owner_id": business["owner_id"],
            "name": business["name"],
            "street_address": business["street_address"],
            "city": business["city"],
            "state": business["state"],
            "zip_code": business["zip_code"]
        }
        businesses.append(business_data)

    return jsonify(businesses), 200
