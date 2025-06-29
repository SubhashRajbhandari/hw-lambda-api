from flask import Blueprint, jsonify, request
from app.models.waiter_call import WaiterCall
from app import db
from datetime import datetime
import logging

# Create a logger for this module
logger = logging.getLogger(__name__)

waiter_bp = Blueprint('waiter_bp', __name__)

@waiter_bp.route('/api/waiter/call', methods=['POST'])
def call_waiter():
    """API endpoint to notify waitstaff for assistance"""
    try:
        logger.info("Processing waiter call request")
        data = request.get_json()
        
        if not data or 'table_number' not in data:
            logger.warning("Missing table_number in waiter call request")
            return jsonify({
                'success': False,
                'error': 'Table number is required'
            }), 400
        
        # Create a new waiter call
        waiter_call = WaiterCall(
            table_number=data['table_number'],
            status='pending'
        )
        
        db.session.add(waiter_call)
        db.session.commit()
        
        logger.info(f"Waiter called successfully for table {data['table_number']}")
        return jsonify({
            'success': True,
            'message': f'Waiter has been called for table {data["table_number"]}',
            'waiter_call': waiter_call.to_dict()
        }), 201
    except Exception as e:
        logger.error(f"Error processing waiter call: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
