from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import TEXT, TIMESTAMP

import uuid
from app import db
from datetime import datetime


class MenuItem(db.Model):
    __tablename__ = 'menu_item'

    menu_item_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    menu_id = db.Column(db.String(36), db.ForeignKey(
        'menu.menu_id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.Text)
    is_available = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'menu_item_id': self.menu_item_id,
            'menu_id': self.menu_id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price) if self.price is not None else None,
            'category': self.category,
            'image_url': self.image_url,
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
