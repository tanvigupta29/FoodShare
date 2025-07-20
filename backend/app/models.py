from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    food_posts = db.relationship("FoodPost", backref="donor", lazy=True)
    claims = db.relationship("Claim", backref="recipient", lazy=True)
    notifications = db.relationship("Notification", backref="user", lazy=True)


class FoodPost(db.Model):
    __tablename__ = "food_posts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.String(50))
    location_name = db.Column(db.String(200), nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    donor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_claimed = db.Column(db.Boolean, default=False)
    is_expired = db.Column(db.Boolean, default=False)

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    claims = db.relationship("Claim", backref="food_item", lazy=True)


class DeliveryPartner(db.Model):
    __tablename__ = "delivery_partners"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    deliveries = db.relationship("Claim", back_populates="delivery_partner", lazy=True)


class Claim(db.Model):
    __tablename__ = "claims"
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey("food_posts.id"), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    claimed_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="pending")
    delivery_partner_id = db.Column(db.Integer, db.ForeignKey("delivery_partners.id"))

    delivery_partner = db.relationship("DeliveryPartner", back_populates="deliveries")


class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
