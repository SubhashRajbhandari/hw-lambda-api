from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import TEXT, TIMESTAMP

class MenuItem(db.Model):
    """Model for restaurant menu items"""
    __tablename__ = 'menu_items'
    __table_args__ = {'schema': 'hataimaWaiter'}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(TEXT, nullable=False)
    description = db.Column(TEXT, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(TEXT, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = db.Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<MenuItem {self.name}>'
    
    def to_dict(self):
        """Convert model to dictionary for API response"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'category': self.category,
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<MenuItem {self.name}>'
    
    def to_dict(self):
        """Convert model to dictionary for API response"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'category': self.category,
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
