from flask import Blueprint, jsonify
from app.models.menu_item import MenuItem
import logging

# Create a logger for this module
logger = logging.getLogger(__name__)

menu_bp = Blueprint('menu_bp', __name__)

@menu_bp.route('/api/menu', methods=['GET'])
def view_restaurant_menu():
    """API endpoint to display restaurant menu items"""
    try:
        logger.info("Attempting to fetch menu items")
        # Get available menu items only
        menu_items = MenuItem.query.filter_by(is_available=True).all()
        
        # Group menu items by category
        menu_by_category = {}
        for item in menu_items:
            category = item.category
            if category not in menu_by_category:
                menu_by_category[category] = []
            menu_by_category[category].append(item.to_dict())
        
        logger.info(f"Successfully retrieved {len(menu_items)} menu items")
        return jsonify({
            'success': True,
            'menu': menu_by_category,
            'item_count': len(menu_items)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching menu items: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
