import uuid
from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import TEXT, TIMESTAMP


class User(db.Model):
    """User model for restaurant customers"""
    __tablename__ = 'users'
    __table_args__ = {'schema': 'hataimaWaiter'}

    user_id = db.Column(db.String(36), primary_key=True,
                        default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False)
    user_type = db.Column(
        db.Enum('SuperAdmin', 'Restaurant', 'RegularUser'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    created_at = db.Column(TIMESTAMP(timezone=True),
                           nullable=False, default=datetime.utcnow)
    updated_at = db.Column(TIMESTAMP(timezone=True), nullable=False,
                           default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.name}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

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
