from flask import Blueprint, jsonify, request
import logging
from app.models.user import User

# Create a logger for this module
logger = logging.getLogger(__name__)

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/api/users', methods=['GET'])
def get_all_users():
    """API endpoint to retrieve all users"""
    try:
        logger.info("Attempting to fetch all users")
        users = User.query.all()
        logger.info(f"Successfully retrieved {len(users)} users")
        return jsonify({
            'success': True,
            'users': [user.to_dict() for user in users],
            'count': len(users)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@user_bp.route('/api/test', methods=['GET'])
def test_endpoint():
    return jsonify({
        'success': True,
        'message': 'Hey this is a test endpoint'
    }), 200


@user_bp.route('/api/addUser', methods=['POST'])
def add_user():
    """API endpoint to add a new user"""
    try:
        logger.info("Received request to add a new user")
        data = request.get_json()
        logger.info("Request payload: %s", data)
        # Required fields
        required_fields = ['email', 'user_type', 'name']
        if not data or not all(field in data for field in required_fields):
            logger.warning("Request missing required fields in payload")
            return jsonify({
                'success': False,
                'error': 'email, user_type, and name are required in the request body'
            }), 400

        email = data['email']
        user_type = data['user_type']
        name = data['name']
        phone_number = data.get('phone_number')

        logger.info(
            f"Attempting to add user: {email}, {user_type}, {name}, {phone_number}")

        new_user = User(
            email=email,
            user_type=user_type,
            name=name,
            phone_number=phone_number
        )
        new_user.save()

        logger.info(f"User {name} added successfully with type: {user_type}")
        return jsonify({
            'success': True,
            'message': f'User {name} added successfully',
            'user': new_user.to_dict()
        }), 201
    except Exception as e:
        logger.error(f"Error adding user: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@user_bp.route('/api/users/details', methods=['POST'])
def get_user_details():
    """API endpoint to retrieve a specific user by user_id"""
    try:
        data = request.get_json()

        if not data or 'user_role' not in data:
            logger.warning("Request missing user_id in payload")
            return jsonify({
                'success': False,
                'error': 'user_role is required in the request body'
            }), 400

        user_role = data['user_role']
        logger.info(f"Attempting to fetch user with ID: {user_role}")

        user = User.query.filter_by(user_type=user_role).all()

        if not user:
            logger.warning(f"User with ID {user_role} not found")
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404

        logger.info(
            f"Successfully retrieved {len(user)} users with role: {user_role}")
        return jsonify({
            'success': True,
            'users': [u.to_dict() for u in user],
            'count': len(user)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching user details: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@user_bp.route('/api/users/update', methods=['POST'])
def update_user():
    """API endpoint to update a user's details"""
    try:
        data = request.get_json()

        if not data or 'user_id' not in data:
            logger.warning("Request missing user_id in payload")
            return jsonify({
                'success': False,
                'error': 'user_id is required in the request body'
            }), 400

        user_id = data['user_id']
        user = User.query.get(user_id)

        if not user:
            logger.warning(f"User with ID {user_id} not found")
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404

        # Update fields if provided
        if 'email' in data:
            user.email = data['email']
        if 'name' in data:
            user.name = data['name']
        if 'phone_number' in data:
            user.phone_number = data['phone_number']
        if 'user_type' in data:
            user.user_type = data['user_type']

        user.save()
        logger.info(f"User {user_id} updated successfully")

        return jsonify({
            'success': True,
            'message': f'User {user_id} updated successfully',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@user_bp.route('/api/isEmailRegistered', methods=['GET'])
def is_email_registered():
    """API endpoint to check if an email is already registered"""
    try:
        email = request.args.get('email')
        if not email:
            logger.warning("Email parameter is missing")
            return jsonify({
                'success': False,
                'error': 'Email parameter is required'
            }), 400

        user = User.query.filter_by(email=email).first()
        if user:
            logger.info(f"Email {email} is already registered")
            return jsonify({
                'success': True,
                'is_registered': True,
                'user_type': user.user_type  # Return user_type as well
            }), 200
        else:
            logger.info(f"Email {email} is not registered")
            return jsonify({
                'success': False,
                'is_registered': False
            }), 404
    except Exception as e:
        logger.error(f"Error checking email registration: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@user_bp.route('/api/restaurants', methods=['POST'])
def add_restaurant():
    """API endpoint to add a new restaurant"""
    try:
        data = request.get_json()
        # Required fields for Restaurant (adjust as per your Restaurant model)
        required_fields = [
            'owner_user_id', 'name', 'address', 'latitude', 'longitude',
            'phone_number', 'opening_hours'
        ]
        if not data or not all(field in data for field in required_fields):
            logger.warning(
                "Request missing required fields in payload for restaurant")
            return jsonify({
                'success': False,
                'error': 'owner_user_id, name, address, latitude, longitude, phone_number, and opening_hours are required in the request body'
            }), 400

        from app.models.restaurant import Restaurant
        new_restaurant = Restaurant(
            owner_user_id=data['owner_user_id'],
            name=data['name'],
            address=data['address'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            phone_number=data['phone_number'],
            opening_hours=data['opening_hours'],
            email=data.get('email'),
            description=data.get('description'),
            logo_url=data.get('logo_url')
        )
        new_restaurant.save()

        logger.info(f"Restaurant {data['name']} added successfully")
        return jsonify({
            'success': True,
            'message': f"Restaurant {data['name']} added successfully",
            'restaurant': new_restaurant.to_dict()
        }), 201
    except Exception as e:
        logger.error(f"Error adding restaurant: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
