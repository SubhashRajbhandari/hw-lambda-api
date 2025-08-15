from flask import Blueprint, jsonify, request
import logging
from app.models.user import User
from app.models.menu import Menu
from app.models.restaurant import Restaurant
import uuid

# Create a logger for this module
logger = logging.getLogger(__name__)

user_bp = Blueprint('user_bp', __name__)


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

        # If user_type is Restaurant, also create a Restaurant entry and a Menu entry
        restaurant_obj = None
        menu_obj = None
        if user_type == 'Restaurant':
            from app.models.restaurant import Restaurant
            from app.models.menu import Menu
            import uuid as uuidlib
            restaurant_obj = Restaurant(
                owner_user_id=new_user.user_id if hasattr(
                    new_user, 'user_id') else new_user.id,
                name=name,
                address=data.get('address', ''),
                latitude=data.get('latitude', 0.0),
                longitude=data.get('longitude', 0.0),
                phone_number=phone_number or '',
                email=email,
                description=data.get('description'),
                logo_url=data.get('logo_url'),
                opening_hours=data.get('opening_hours', {})
            )
            restaurant_obj.save()
            # Create menu for the restaurant
            menu_uuid = str(uuidlib.uuid4())
            menu_obj = Menu(
                menu_id=menu_uuid,
                restaurant_id=restaurant_obj.restaurant_id,
                name=restaurant_obj.name,
                description=f"{restaurant_obj.name} menu"
            )
            menu_obj.save()

        logger.info(f"User {name} added successfully with type: {user_type}")
        response = {
            'success': True,
            'message': f'User {name} added successfully',
            'user': new_user.to_dict()
        }
        if restaurant_obj:
            response['restaurant'] = restaurant_obj.to_dict()
        if menu_obj:
            response['menu'] = menu_obj.to_dict()
        return jsonify(response), 201
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
                'user_type': user.user_type,  # Return user_type as well
                'user_id': user.user_id
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


@user_bp.route('/api/getAllUsers', methods=['GET'])
def get_all_users():
    """API endpoint to retrieve all users"""
    try:
        users = User.query.all()
        if not users:
            logger.info("No users found")
            return jsonify({
                'success': True,
                'users': [],
                'count': 0
            }), 200

        logger.info(f"Retrieved {len(users)} users")
        return jsonify({
            'success': True,
            'users': [user.to_dict() for user in users],
            'count': len(users)
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving all users: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@user_bp.route('/api/addRestaurant', methods=['POST'])
def add_restaurant():
    """API endpoint to add a new restaurant"""
    try:
        data = request.get_json()
        # Required fields for Restaurant (adjust as per your Restaurant model)
        required_fields = [
            'name', 'address', 'latitude', 'longitude',
            'phone_number', 'opening_hours'
        ]
        if not data or not all(field in data for field in required_fields):
            logger.warning(
                "Request missing required fields in payload for restaurant")
            return jsonify({
                'success': False,
                'error': 'name, address, latitude, longitude, phone_number, and opening_hours are required in the request body'
            }), 400
        # Create user first
        from app.models.user import User
        user_uuid = str(uuid.uuid4())
        new_user = User(
            user_id=user_uuid,
            user_type='Restaurant',
            email=data.get('email', ''),
            name=data['name'],
            phone_number=data.get('phone_number', '')
        )
        new_user.save()

        # Now create restaurant
        from app.models.menu import Menu
        import uuid as uuidlib
        new_restaurant = Restaurant(
            owner_user_id=user_uuid,
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
        # Create menu for the restaurant
        menu_uuid = str(uuidlib.uuid4())
        new_menu = Menu(
            menu_id=menu_uuid,
            restaurant_id=new_restaurant.restaurant_id,
            name=new_restaurant.name,
            description=f"{new_restaurant.name} menu"
        )
        new_menu.save()

        logger.info(f"Restaurant {data['name']} and user created successfully")
        return jsonify({
            'success': True,
            'message': f"Restaurant {data['name']} and user added successfully",
            'restaurant': new_restaurant.to_dict(),
            'user': new_user.to_dict(),
            'menu': new_menu.to_dict()
        }), 201
    except Exception as e:
        logger.error(f"Error adding restaurant: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@user_bp.route('/api/addMenu-items', methods=['POST'])
def add_menu_items():
    """API endpoint to add items to the menu"""
    try:
        data = request.get_json()

        # Retrieve email from session cookie
        user_id = data.get('user_id')
       
        # Find restaurant by user_id
        restaurant = Restaurant.query.filter_by(
            owner_user_id= user_id).first()
        if not restaurant:
            logger.warning(f"No restaurant found for user_id: {user_id}")
            return jsonify({
                'success': False,
                'error': f"No restaurant found for user_id: {user_id}"
            }), 404

        # Find menu by restaurant_id
        menu = Menu.query.filter_by(
            restaurant_id=restaurant.restaurant_id).first()
        if not menu:
            logger.warning(
                f"No menu found for restaurant_id: {restaurant.restaurant_id}")
            return jsonify({
                'success': False,
                'error': f"No menu found for restaurant_id: {restaurant.restaurant_id}"
            }), 404

        menu_id = menu.menu_id

        # Validate required fields for MenuItem
        required_fields = ['name', 'description', 'price',
                           'category', 'image_url', 'is_available']
        if not data or not all(field in data for field in required_fields):
            logger.warning(
                "Request missing required fields in payload for menu item")
            return jsonify({
                'success': False,
                'error': 'name, description, price, category, image_url, and is_available are required'
            }), 400

        # Extract fields from the request payload
        name = data['name']
        description = data['description']
        price = data['price']
        category = data['category']
        image_url = data['image_url']
        is_available = data['is_available']

        # Create a new MenuItem
        from app.models.menu_item import MenuItem
        new_menu_item = MenuItem(
            menu_id=menu_id,
            name=name,
            description=description,
            price=price,
            category=category,
            image_url=image_url,
            is_available=is_available
        )
        new_menu_item.save()

        logger.info(f"Menu item {name} added successfully to menu {menu_id}")
        return jsonify({
            'success': True,
            'message': f'Menu item {name} added successfully',
            'menu_item': new_menu_item.to_dict()
        }), 201
    except Exception as e:
        logger.error(f"Error adding menu item: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
