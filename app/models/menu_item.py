from app import db
from datetime import datetime
import uuid

class MenuItem(db.Model):
    """Model for restaurant menu items"""
    __tablename__ = 'menu_items'
    __table_args__ = {'schema': 'hataimaWaiter'}
    
    menu_item_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    menu_id = db.Column(db.String(36), db.ForeignKey('hataimaWaiter.menu.menu_id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.Text, nullable=True)
    is_available = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        """Convert model to dictionary for API response"""
        return {
            'menu_item_id': self.menu_item_id,
            'menu_id': self.menu_id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'category': self.category,
            'image_url': self.image_url,
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
