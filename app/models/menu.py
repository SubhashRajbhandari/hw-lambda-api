import uuid
from app import db
from datetime import datetime


class Menu(db.Model):
    __tablename__ = 'menu'

    menu_id = db.Column(db.String(36), primary_key=True,
                        default=lambda: str(uuid.uuid4()))
    restaurant_id = db.Column(db.String(36), db.ForeignKey(
        'restaurant.restaurant_id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'menu_id': self.menu_id,
            'restaurant_id': self.restaurant_id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
