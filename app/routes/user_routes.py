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