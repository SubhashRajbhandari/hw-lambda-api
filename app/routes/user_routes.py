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
        
        logger.info(f"Successfully retrieved {len(user)} users with role: {user_role}")
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