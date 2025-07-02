from app import db
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID, JSONB


class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    __table_args__ = {'schema': 'hataimaWaiter'}

    restaurant_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_user_id = db.Column(db.String(255), db.ForeignKey(
        'hataimaWaiter.users.user_id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(320), nullable=True)
    description = db.Column(db.Text, nullable=True)
    logo_url = db.Column(db.Text, nullable=True)
    opening_hours = db.Column(JSONB, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime(
        timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'restaurant_id': self.restaurant_id,
            'owner_user_id': self.owner_user_id,
            'name': self.name,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'phone_number': self.phone_number,
            'email': self.email,
            'description': self.description,
            'logo_url': self.logo_url,
            'opening_hours': self.opening_hours,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
