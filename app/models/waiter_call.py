from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import TEXT, TIMESTAMP

class WaiterCall(db.Model):
    """Model for tracking waiter calls from customers"""
    __tablename__ = 'waiter_calls'
    __table_args__ = {'schema': 'hataimaWaiter'}
    
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(TEXT, nullable=False)
    status = db.Column(TEXT, default='pending')  # pending, completed, cancelled
    created_at = db.Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    completed_at = db.Column(TIMESTAMP(timezone=True), nullable=True)
    
    def __repr__(self):
        return f'<WaiterCall table:{self.table_number} status:{self.status}>'
    
    def to_dict(self):
        """Convert model to dictionary for API response"""
        return {
            'id': self.id,
            'table_number': self.table_number,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
