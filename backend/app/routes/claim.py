from flask import Blueprint, request, jsonify, session
from datetime import datetime
from app import db
from app.models import Claim, FoodPost, DeliveryPartner
import random

claim_bp = Blueprint('claim', __name__)

def assign_delivery_partner():
    """Randomly assign an available delivery partner."""
    partners = DeliveryPartner.query.all()
    if not partners:
        return None
    return random.choice(partners)

@claim_bp.route('/<int:food_id>', methods=['POST'])
def claim_food(food_id):
    user_id = session.get('user_id')
    user_role = session.get('user_role')

    if not user_id or user_role != 'recipient':
        return jsonify({'success': False, 'message': 'Only recipients can claim food items.'}), 403

    food_item = FoodPost.query.get(food_id)
    if not food_item:
        return jsonify({'success': False, 'message': 'Food item not found.'}), 404

    if food_item.is_claimed:
        return jsonify({'success': False, 'message': 'This food item has already been claimed.'}), 400

    if food_item.donor_id == user_id:
        return jsonify({'success': False, 'message': 'You cannot claim your own post.'}), 403

    # Parse JSON data (optional delivery request)
    wants_delivery = request.get_json(silent=True, force=False) or {}
    wants_delivery = wants_delivery.get('wants_delivery', False)

    delivery_partner = assign_delivery_partner() if wants_delivery else None

    # Create claim
    claim = Claim(
        food_id=food_item.id,
        recipient_id=user_id,
        claimed_at=datetime.utcnow(),
        status='pending',
        delivery_partner_id=delivery_partner.id if delivery_partner else None
    )

    food_item.is_claimed = True
    db.session.add(claim)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Claim successful.',
        'delivery_partner': {
            'name': delivery_partner.name,
            'phone': delivery_partner.phone,
            'email': delivery_partner.email
        } if delivery_partner else None
    })
