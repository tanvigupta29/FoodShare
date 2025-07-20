import random
from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify, request
from datetime import datetime
from sqlalchemy.orm import joinedload
from app import db
from app.models import FoodPost, Claim, DeliveryPartner  # ✅ FIXED: typo in your import

recipient_bp = Blueprint("recipient", __name__, template_folder="../templates")


# --------------------- Recipient Dashboard ---------------------
@recipient_bp.route("/dashboard")
def recipient_dashboard():
    if "user_id" not in session or session.get("user_role") != "recipient":
        flash("Please log in as a recipient to access the dashboard.", "warning")
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    # Load claimed items with related food and delivery info
    claimed_items = (
        Claim.query
        .filter_by(recipient_id=user_id)
        .options(
            joinedload(Claim.food_item),
            joinedload(Claim.delivery_partner)
        )
        .order_by(Claim.claimed_at.desc())
        .all()
    )

    # Get all available food posts (not expired or claimed)
    available_food = (
        FoodPost.query
        .filter(
            FoodPost.is_claimed == False,
            FoodPost.expiration_date >= datetime.utcnow()
        )
        .order_by(FoodPost.created_at.desc())
        .all()
    )

    # Serialize food posts for map rendering
    serialized_food_items = [
        {
            "id": item.id,
            "name": item.name,
            "quantity": item.quantity,
            "location_name": item.location_name,
            "expiration_date": item.expiration_date.strftime('%Y-%m-%d'),
            "description": item.description,
            "created_at": item.created_at.strftime('%Y-%m-%d %H:%M'),
            "latitude": item.latitude,
            "longitude": item.longitude
        }
        for item in available_food if item.latitude is not None and item.longitude is not None
    ]

    return render_template(
        "recipient_dashboard.html",
        claimed_items=claimed_items,
        food_items=available_food,
        serialized_food_items=serialized_food_items
    )


# --------------------- Claim Food Route ---------------------
@recipient_bp.route("/claim/<int:food_id>", methods=["POST"])
def claim_food(food_id):
    if "user_id" not in session or session.get("user_role") != "recipient":
        return jsonify({"success": False, "message": "Login as a recipient to claim food."}), 401

    user_id = session["user_id"]
    food_item = FoodPost.query.get(food_id)

    if not food_item:
        return jsonify({"success": False, "message": "Food item not found."}), 404

    if food_item.is_claimed:
        return jsonify({"success": False, "message": "This item has already been claimed."}), 400

    if food_item.donor_id == user_id:
        return jsonify({"success": False, "message": "You cannot claim your own food post."}), 403

    data = request.get_json()
    wants_delivery = data.get("wants_delivery", False)

    # Mark item as claimed
    food_item.is_claimed = True

    # Create new claim
    claim = Claim(
        food_id=food_id,
        recipient_id=user_id,
        claimed_at=datetime.utcnow(),
        status="pending"
    )

    delivery_partner_info = None

    if wants_delivery:
        partners = DeliveryPartner.query.all()
        if partners:
            selected_partner = random.choice(partners)
            claim.delivery_partner = selected_partner
            delivery_partner_info = {
                "name": selected_partner.name,
                "phone": selected_partner.phone,
                "email": selected_partner.email
            }

    db.session.add(claim)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Food item successfully claimed!",
        "delivery_partner": delivery_partner_info
    })
