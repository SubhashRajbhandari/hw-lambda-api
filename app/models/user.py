from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import TEXT, TIMESTAMP

class User(db.Model):
    """User model for restaurant customers"""
    __tablename__ = 'users'
    __table_args__ = {'schema': 'hataimaWaiter'}
    
    user_id = db.Column(TEXT, primary_key=True)
    email = db.Column(TEXT, unique=True, nullable=False)
    user_type = db.Column(db.Enum('SuperAdmin', 'Restaurant', 'RegularUser'), nullable=False)
    name = db.Column(TEXT, nullable=False)
    phone_number = db.Column(TEXT, nullable=True)
    created_at = db.Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = db.Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.name}>'
    
    def to_dict(self):
        """Convert model to dictionary for API response"""
        return {
            'user_id': self.user_id,
            'email': self.email,
            'user_type': self.user_type,
            'name': self.name,
            'phone_number': self.phone_number,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
